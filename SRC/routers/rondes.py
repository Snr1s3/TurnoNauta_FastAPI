from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from ..models import *
from psycopg2.extras import RealDictCursor

def get_rondes():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM Ronda;")
        rondes = cursor.fetchall()
        return rondes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def add_ronda_to_db(info_ronda: NewRonda):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            INSERT INTO public.ronda (id_torneig, estat)
            VALUES (%s, %s)
            RETURNING id_ronda, id_torneig, estat;
        """
        cursor.execute(query, (info_ronda.id_torneig, "Started"))
        new_ronda = cursor.fetchone() 
        conn.commit()
        print(f"Ronda added with ID: {new_ronda[0]}")
        return {
            "id_ronda": new_ronda[0],
            "id_torneig": new_ronda[1],
            "estat": new_ronda[2]
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)