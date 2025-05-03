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

    print("Received request body:", info_ronda)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            INSERT INTO public.ronda (id_torneig, estat)
            VALUES (%s, %s)
            RETURNING id_ronda, id_torneig, estat;
        """
        cursor.execute(query, (info_ronda.id_torneig, "Started"))
        new_ronda = cursor.fetchone()  # Fetch the inserted row as a dictionary
        conn.commit()
        print(new_ronda)
        print(f"Ronda added with ID: {new_ronda['id_ronda']}")
        return {
            "id_ronda": new_ronda["id_ronda"],
            "id_torneig": new_ronda["id_torneig"],
            "estat": new_ronda["estat"]
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)