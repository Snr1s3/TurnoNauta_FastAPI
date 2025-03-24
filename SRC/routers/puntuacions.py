from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from ..models import UserWithPoints

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
def get_users_points(torneig_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
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
        return users
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)