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
    conn2 = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor2 = conn2.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            INSERT INTO public.ronda (id_torneig, estat)
            VALUES (%s, %s)
            RETURNING id_ronda, id_torneig, estat;
        """
        cursor.execute(query, (info_ronda.id_torneig, "Started"))
        new_ronda = cursor.fetchone()  # Fetch the inserted row as a dictionary
        conn.commit()
        print(f"Ronda added with ID: {new_ronda['id_ronda']}")
        query = """
            INSERT INTO public.emparallaments (id_ronda , id_usuari1, resultat_usuari_1, id_usuari2, resultat_usuari_2, id_usuari_guanyador, id_usuari_perdedor)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor2.execute(query, (new_ronda["id_ronda"], info_ronda.id_player1, 0, info_ronda.id_player2, 0, None, None))
        new_emparallament = cursor2.fetchone()  # Fetch the inserted row as a dictionary
        conn2.commit()
        print(f"Emparallament added with ID: {new_emparallament['id_emperallent']}")
        cursor.close()
        conn.close()
        cursor2.close()
        conn2.close()
    
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