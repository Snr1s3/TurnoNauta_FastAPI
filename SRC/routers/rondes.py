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

    #print("Received request body:", info_ronda)
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

def get_pairing_by_player_and_tournament(player_id: int, torneig_id: int):
    """
    Retrieve pairing by player ID (id_usuari1 or id_usuari2) and tournament ID (id_torneig)
    where the round is in the 'Started' state.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            SELECT e.*
            FROM public.emparallaments e
            JOIN public.ronda r ON e.id_ronda = r.id_ronda
            WHERE r.id_torneig = %s
              AND r.estat = 'Started'
              AND (e.id_usuari1 = %s OR e.id_usuari2 = %s);
        """
        cursor.execute(query, (torneig_id, player_id, player_id))
        pairings = cursor.fetchall()  # Fetch all matching rows
        return pairings
    except Exception as e:
        print(f"Error while retrieving pairings: {e}")
        raise HTTPException(status_code=400, detail="Error retrieving pairings")
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
        query = """
            UPDATE public.puntuacio
            SET punts = punts + %s, victories = victories + %s, derrotes = derrotes + %s
            WHERE id_usuari = %s AND id_torneig = %s;
        """

        print(2 * update_ronda_request.resultat_usuari_1 )
        print(update_ronda_request.resultat_usuari_1)
        print(update_ronda_request.resultat_usuari_2)
        print(update_ronda_request.id_usuari_1)
        cursor.execute(query, (
            2 * update_ronda_request.resultat_usuari_1, 
            update_ronda_request.resultat_usuari_1,
            update_ronda_request.resultat_usuari_2, 
            update_ronda_request.id_usuari_1, 
            updated_ronda["id_torneig"]
        ))
        conn.commit()

        # Update the 'puntuacio' table for the loser
        query = """
            UPDATE public.puntuacio
            SET punts = punts + %s, victories = victories + %s, derrotes = derrotes + %s
            WHERE id_usuari = %s AND id_torneig = %s;
        """
        print(2 * update_ronda_request.resultat_usuari_2 )
        print(update_ronda_request.resultat_usuari_2)
        print(update_ronda_request.resultat_usuari_1)
        print(update_ronda_request.id_usuari_2)
        cursor.execute(query, (
            2 * update_ronda_request.resultat_usuari_2, 
            update_ronda_request.resultat_usuari_2,
            update_ronda_request.resultat_usuari_1, 
            update_ronda_request.id_usuari_2, 
            updated_ronda["id_torneig"]
        ))
        print(f"Emparallament updated with ID: {updated_emparallament['id_emperallent']}")
        conn.commit()

        query = """
            UPDATE public.puntuacio AS p
            SET sos = subquery.total_opponent_points
            FROM (
                SELECT player_id, SUM(opponent_points) AS total_opponent_points
                FROM (
                    SELECT e.id_usuari1 AS player_id, p2.punts AS opponent_points
                    FROM public.emparallaments e
                    JOIN public.puntuacio p2 ON e.id_usuari2 = p2.id_usuari AND p2.id_torneig = %s
                    WHERE e.id_ronda IN (
                        SELECT id_ronda FROM public.ronda WHERE id_torneig = %s
                    )
                    UNION ALL
                    SELECT e.id_usuari2 AS player_id, p1.punts AS opponent_points
                    FROM public.emparallaments e
                    JOIN public.puntuacio p1 ON e.id_usuari1 = p1.id_usuari AND p1.id_torneig = %s
                    WHERE e.id_ronda IN (
                        SELECT id_ronda FROM public.ronda WHERE id_torneig = %s
                    )
                ) AS combined
                GROUP BY player_id
            ) AS subquery
            WHERE p.id_usuari = subquery.player_id AND p.id_torneig = %s;
        """
        cursor.execute(query, (
            updated_ronda["id_torneig"], 
            updated_ronda["id_torneig"], 
            updated_ronda["id_torneig"], 
            updated_ronda["id_torneig"], 
            updated_ronda["id_torneig"]
        ))
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

def get_ronda_acabada_id(torneig_id: int):
    """
    Check if there are any started rounds for a given tournament ID.
    Returns the count of started rounds.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    print(f"Checking if there are any started rounds for tournament {torneig_id}")
    try:
        query = """
            SELECT COUNT(*) AS started_count FROM public.ronda
            WHERE id_torneig = %s AND estat = 'Started';
        """
        cursor.execute(query, (torneig_id,))
        result = cursor.fetchone()  # Fetch the result as a dictionary
        count = result["started_count"] if result else 0
        return count
    except Exception as e:
        print(f"Error while checking started rounds: {e}")
        raise HTTPException(status_code=400, detail="Error checking started rounds")
    finally:
        cursor.close()
        release_db_connection(conn)