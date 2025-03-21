from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from ..models import UserStatistics

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
            SELECT * FROM emparallaments WHERE id_usuari = %s
        """, (id_usuaris))
        stats = cursor.fetchone()

        return UserStatistics(
            id=user['id_usuaris'],
            username=user['username'],
            rounds_played=stats['rounds_played'],
            rounds_won=stats['rounds_won'],
            tournaments_played=stats['tournaments_played'],
            tournaments_won=stats['tournaments_won']
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)