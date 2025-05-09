from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from ..models import UserStatistics, NewUser

def get_usuaris():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM Usuaris;")
        usuaris = cursor.fetchall()
        return usuaris
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)
def update_user_password_in_db(mail: str, new_password: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Update the password using the email (mail)
        cursor.execute(
            "UPDATE usuaris SET contrasenya = %s WHERE email = %s RETURNING *;",
            (new_password, mail)
        )
        updated_user = cursor.fetchone()
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def get_usuari_id(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Pass `user_id` as a tuple by adding a comma after it
        cursor.execute("SELECT * FROM usuaris WHERE id_usuaris = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def verify_user_credentials(username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT id_usuaris FROM usuaris WHERE username = %s AND contrasenya = %s", (username, password))
        user = cursor.fetchone()
        if user:
            return user['id_usuaris']
        else:
            return -1
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def verify_user_statistics(id_usuaris: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Retrieve user information
        cursor.execute("SELECT username FROM usuaris WHERE id_usuaris = %s", (id_usuaris,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        username = user['username']

        # Count how many times the user appears in puntuacio
        cursor.execute("SELECT COUNT(*) FROM puntuacio WHERE id_usuari = %s", (id_usuaris,))
        count_puntuacions = cursor.fetchone()['count']

        # Count how many times the user has the highest points in tournaments
        cursor.execute("""
            SELECT COUNT(*) 
            FROM puntuacio p
            WHERE p.id_usuari = %s AND p.punts = (
                SELECT MAX(p2.punts) 
                FROM puntuacio p2 
                WHERE p2.id_torneig = p.id_torneig
            )
        """, (id_usuaris,))
        count_highest_points = cursor.fetchone()['count']

        # Sum of partides guanyades and perdudes
        cursor.execute("""
            SELECT SUM(victories) AS total_wins, 
                SUM(derrotes) AS total_losses
            FROM public.puntuacio
            WHERE id_usuari = %s
        """, (id_usuaris,))
        stats = cursor.fetchone()
        total_wins = stats['total_wins'] or 0
        total_losses = stats['total_losses'] or 0

        # Return the UserStatistics object
        return UserStatistics(
            id=id_usuaris,
            username=username,
            rounds_played=total_wins + total_losses,
            rounds_won=total_wins,
            tournaments_played=count_puntuacions,
            tournaments_won=count_highest_points
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def add_usuari(user: NewUser):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Insert the new user into the database
        cursor.execute("""
            INSERT INTO usuaris (rol, username, telefono, email, contrasenya, rang, data_de_registre)
            VALUES (1,%s, %s, %s, %s, 1, NOW())
            RETURNING *;
        """, (user.username, user.phone, user.email, user.password))
        new_user = cursor.fetchone()
        cursor.execute("""
            INSERT INTO estadistiques (id_usuari, partides_jugades, partides_guanyades, tornejos_jugats, tornejos_guanyats)
            VALUES (%s, 0, 0, 0, 0);
        """, (new_user['id_usuaris'],))
        cursor.execute("""
            INSERT INTO public.subscripcio (id_usuari, data_inici, data_final, tipus, estat)
            VALUES (%s, NOW(), NOW() + INTERVAL '1 year', 'Basic', 'Active');
        """, (new_user['id_usuaris'],))
        conn.commit()
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def check_username(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM usuaris WHERE username = %s);", (username,))
        result = cursor.fetchone()
        return result[0]  
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)
        
def check_email_exists(mail: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if the email exists in the database
        cursor.execute("SELECT EXISTS(SELECT 1 FROM usuaris WHERE email = %s);", (mail,))
        result = cursor.fetchone()
        return result[0]  # Return True if the email exists, otherwise False
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def update_username(user_id: int ,new_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE usuaris SET username = %s WHERE id_usuaris = %s RETURNING *;",
            (new_name, user_id)
        )
        updated_user = cursor.fetchone()
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        conn.commit()
        return get_usuari_id(user_id)  
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def delete_user_id(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM estadistiques WHERE id_usuari = %s;", (user_id,))
        cursor.execute("DELETE FROM public.subscripcio WHERE id_usuari = %s;", (user_id,))
        cursor.execute("DELETE FROM usuaris WHERE id_usuaris = %s RETURNING id_usuaris;", (user_id,))
        deleted_user = cursor.fetchone()
        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)