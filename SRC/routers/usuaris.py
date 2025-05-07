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
def update_user_password_in_db(user_id: int, new_password: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE usuaris SET contrasenya = %s WHERE id_usuaris = %s RETURNING *;",
            (new_password, user_id)
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
        cursor.execute("SELECT id_usuaris, username FROM usuaris WHERE id_usuaris = %s", (id_usuaris,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Retrieve user statistics
        cursor.execute("""
            SELECT u.username, e.partides_jugades, e.partides_guanyades, e.tornejos_jugats, e.tornejos_guanyats
            FROM usuaris u
            JOIN estadistiques e ON u.id_usuaris = e.id_usuari
            WHERE u.id_usuaris = %s
        """, (id_usuaris,))
        stats = cursor.fetchone()

        if not stats:
            raise HTTPException(status_code=404, detail="User or statistics not found")

        return UserStatistics(
            id=id_usuaris,
            username=stats['username'],
            rounds_played=stats['partides_jugades'],
            rounds_won=stats['partides_guanyades'],
            tournaments_played=stats['tornejos_jugats'],
            tournaments_won=stats['tornejos_guanyats']
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