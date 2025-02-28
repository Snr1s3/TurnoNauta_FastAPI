from fastapi import HTTPException
from client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor

def get_rangs():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM Rang;")
        rangs = cursor.fetchall()
        return rangs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)