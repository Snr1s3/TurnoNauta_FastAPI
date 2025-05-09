from typing import List
from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from ..models import PuntuacioName, UserWithPoints, NewPuntuacio

def get_puntuacions():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM Puntuacio;")
        puntuacions = cursor.fetchall()
        return puntuacions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def get_putuacio_by_sos(torneig_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            WITH ordered_puntuacions AS (
                SELECT *
                FROM public.puntuacio
                WHERE id_torneig = %s
                ORDER BY sos ASC
            ),
            conflicts AS (
                SELECT p1.id_usuari AS player1, p2.id_usuari AS player2
                FROM public.emparallaments e
                JOIN public.puntuacio p1 ON e.id_usuari1 = p1.id_usuari AND p1.id_torneig = %s
                JOIN public.puntuacio p2 ON e.id_usuari2 = p2.id_usuari AND p2.id_torneig = %s
            )
            SELECT *
            FROM ordered_puntuacions op
            WHERE EXISTS (
                SELECT 1
                FROM conflicts c
                WHERE (c.player1 = op.id_usuari OR c.player2 = op.id_usuari)
            );
        """
        cursor.execute(query, (torneig_id, torneig_id, torneig_id))
        puntuacions = cursor.fetchall()
        return puntuacions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)


def get_putuacio_by_sosname(torneig_id: int) -> List[PuntuacioName]:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            WITH ordered_puntuacions AS (
                SELECT *
                FROM public.puntuacio
                WHERE id_torneig = %s
                ORDER BY sos ASC
            ),
            conflicts AS (
                SELECT p1.id_usuari AS player1, p2.id_usuari AS player2
                FROM public.emparallaments e
                JOIN public.puntuacio p1 ON e.id_usuari1 = p1.id_usuari AND p1.id_torneig = %s
                JOIN public.puntuacio p2 ON e.id_usuari2 = p2.id_usuari AND p2.id_torneig = %s
            )
            SELECT op.*, u.username AS nom
            FROM ordered_puntuacions op
            JOIN public.usuaris u ON op.id_usuari = u.id_usuaris
            WHERE EXISTS (
                SELECT 1
                FROM conflicts c
                WHERE (c.player1 = op.id_usuari OR c.player2 = op.id_usuari)
            );
        """
        cursor.execute(query, (torneig_id, torneig_id, torneig_id))
        puntuacions = cursor.fetchall()

        # Map the results to the PuntuacioName model
        return [
            PuntuacioName(
                id_torneig=row["id_torneig"],
                id_usuari=row["id_usuari"],
                nom=row["nom"],
                sos=row["sos"],
                victories=row["victories"],
                empat=row["empat"],
                derrotes=row["derrotes"],
                punts=row["punts"]
            )
            for row in puntuacions
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def get_puntuacio_id(torneig_id: int):
    """
    Retrieve all puntuacions for a specific tournament ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            SELECT * FROM public.puntuacio
            WHERE id_torneig = %s
            ORDER BY punts DESC;
        """
        cursor.execute(query, (torneig_id,))
        puntuacions = cursor.fetchall()
        print(f"Retrieved puntuacions: {puntuacions}")
        if not puntuacions:
            raise HTTPException(status_code=404, detail="No puntuacions found for the specified tournament ID")
        return puntuacions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def get_users_points(torneig_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Query to get username and points, ordered by points in descending order
        cursor.execute("""
            SELECT u.username, p.punts
            FROM usuaris u
            JOIN puntuacio p ON u.id_usuaris = p.id_usuari
            WHERE p.id_torneig = %s
            ORDER BY p.punts DESC
        """, (torneig_id,))
        users = cursor.fetchall()
        if not users:
            raise HTTPException(status_code=404, detail="No users found for the specified tournament")
        return [{"username": user[0], "punts": user[1]} for user in users]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def add_puntuacio_to_db(puntuacio: NewPuntuacio):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)  # Use RealDictCursor
    try:
        query = """
        INSERT INTO public.puntuacio (id_torneig, id_usuari, sos, victories, empat, derrotes, punts)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_puntuacio, id_torneig, id_usuari, sos, victories, empat, derrotes, punts;
        """
        cursor.execute(query, (puntuacio.id_torneig, puntuacio.id_usuari, puntuacio.sos, puntuacio.victories, puntuacio.empat, puntuacio.derrotes, puntuacio.punts))
        result = cursor.fetchone()  # Fetch as a dictionary
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def delete_puntuacions_by_tournament(torneig_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete all puntuacions for the specified tournament
        query = "DELETE FROM public.puntuacio WHERE id_torneig = %s;"
        cursor.execute(query, (torneig_id,))
        conn.commit()
        return {"message": f"All puntuacions for tournament ID {torneig_id} have been deleted."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

    
def delete_puntuacions_by_user(user_id: int, tournament_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete all puntuacions for the specified user
        query = "DELETE FROM public.puntuacio WHERE id_usuari = %s and id_torneig = %s;"
        cursor.execute(query, (user_id, tournament_id))
        conn.commit()
        return {"message": f"All puntuacions for user ID {user_id} have been deleted."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)