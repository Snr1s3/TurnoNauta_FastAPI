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
        print(f"Ronda added with ID: {new_ronda['id_ronda']}")
        query = """
            INSERT INTO public.emparallaments (id_ronda , id_usuari1, resultat_usuari_1, id_usuari2, resultat_usuari_2, id_usuari_guanyador, id_usuari_perdedor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_emperallent, id_ronda, id_usuari1, resultat_usuari_1, id_usuari2, resultat_usuari_2, id_usuari_guanyador, id_usuari_perdedor;
        """
        cursor.execute(query, (new_ronda["id_ronda"], info_ronda.id_player1, 0, info_ronda.id_player2, 0, None, None))
        new_emparallament = cursor.fetchone()  # Fetch the inserted row as a dictionary
        conn.commit()
        print(f"Emparallament added with ID: {new_emparallament['id_emperallent']}")
        cursor.close()
        conn.close()
    
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

def update_ronda_to_db(update_ronda_request: UpdateRondaRequest):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            UPDATE public.ronda
            SET estat = %s
            WHERE id_ronda = %s
            RETURNING id_ronda, id_torneig, estat;
        """
        cursor.execute(query, ("Done", update_ronda_request.id_ronda))
        updated_ronda = cursor.fetchone()  # Fetch the updated row as a dictionary
        conn.commit()
        query = """
            UPDATE public.emparallaments
            SET resultat_usuari_1 = %s, resultat_usuari_2 = %s, id_usuari_guanyador = %s, id_usuari_perdedor = %s
            WHERE id_ronda = %s 
            RETURNING id_emperallent, id_ronda, id_usuari1, resultat_usuari_1, id_usuari2, resultat_usuari_2, id_usuari_guanyador, id_usuari_perdedor;
        """
        cursor.execute(query, (update_ronda_request.resultat_usuari_1, update_ronda_request.resultat_usuari_2, update_ronda_request.id_usuari_guanyador, update_ronda_request.id_usuari_perdedor, update_ronda_request.id_ronda))
        updated_emparallament = cursor.fetchone()  # Fetch the updated row as a dictionary
        conn.commit()
        return {
            "id_ronda": updated_ronda["id_ronda"],
            "id_torneig": updated_ronda["id_torneig"],
            "estat": updated_ronda["estat"]
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)