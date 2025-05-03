from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor

def get_emparellaments():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = 'SELECT * FROM emparallaments;'  # Use double quotes for case-sensitive table names
        cursor.execute(query)
        emparellaments = cursor.fetchall()
        return emparellaments
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)