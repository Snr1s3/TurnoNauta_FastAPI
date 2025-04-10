from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from ..models import Torneig
from typing import List

def get_tournament_id(torneig_id: int) -> Torneig:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM Torneig WHERE id_torneig = %s;", (torneig_id,))
        torneig = cursor.fetchone()
        if not torneig:
            raise HTTPException(status_code=404, detail="Tournament not found")
        return Torneig(**torneig)  # Convert the result to a Torneig object
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def get_tournaments_played(user_id: int) -> List[Torneig]:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            SELECT t.* 
            FROM Torneig t
            JOIN Puntuacio p ON t.id_torneig = p.id_torneig
            WHERE p.id_usuari = %s
        """, (user_id,))
        tournaments = cursor.fetchall()
        return [Torneig(**tournament) for tournament in tournaments]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def get_active_tournaments_from_db():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM Torneig WHERE data_final IS NULL OR data_final > CURRENT_DATE;")
        tournaments = cursor.fetchall()
        return [Torneig(**tournament) for tournament in tournaments]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def get_active_tournament_by_id(torneig_id: int) -> int:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            "SELECT id_torneig FROM Torneig WHERE id_torneig = %s AND (data_final IS NULL OR data_final > CURRENT_DATE);",
            (torneig_id,)
        )
        tournament = cursor.fetchone()
        if not tournament:
            return -1
        return tournament["id_torneig"] 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)