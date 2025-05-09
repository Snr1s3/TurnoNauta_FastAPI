from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from ..models import Torneig, NewTorneig
from typing import List


def get_torneig() -> List[Torneig]:
    """
    Fetch all tournaments from the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM Torneig;")
        tournaments = cursor.fetchall()
        return [Torneig(**tournament) for tournament in tournaments]  # Convert each result to a Torneig object
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

        
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

def get_active_tournament_by_id(torneig_id: int) -> Torneig:
    """
    Fetch an active tournament by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            """
            SELECT * FROM Torneig
            WHERE id_torneig = %s AND (data_final IS NULL OR data_final > CURRENT_DATE);
            """,
            (torneig_id,)
        )
        tournament = cursor.fetchone()
        if not tournament:
            raise HTTPException(status_code=404, detail="Active tournament not found")
        return Torneig(**tournament)  # Convert the result to a Torneig object
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def add_tournament_to_db(tournament: NewTorneig) -> Torneig:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            """
            INSERT INTO Torneig (nom, joc, usuari_organitzador, competitiu, virtual, format, premi, num_jugadors, data_d_inici, data_final)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
            """,
            (
                tournament.nom,
                tournament.joc,
                tournament.usuari_organitzador,
                tournament.competitiu,
                tournament.virtual,
                tournament.format,
                tournament.premi,
                tournament.num_jugadors,
                tournament.data_d_inici,
                tournament.data_final,
            )
        )
        new_tournament = cursor.fetchone()
        conn.commit()
        return Torneig(**new_tournament)  # Convert the result to a Torneig object
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def get_ended_tournaments_from_db() -> List[Torneig]:
    """
    Fetch all tournaments that have ended.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            """
            SELECT * FROM Torneig
            WHERE data_final IS NOT NULL AND data_final <= CURRENT_DATE;
            """
        )
        tournaments = cursor.fetchall()
        return [Torneig(**tournament) for tournament in tournaments]  # Convert each result to a Torneig object
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def get_ended_tournament_by_id(torneig_id: int) -> Torneig:
    """
    Fetch a specific tournament by ID that has ended.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            """
            SELECT * FROM Torneig
            WHERE id_torneig = %s AND data_final IS NOT NULL AND data_final <= CURRENT_DATE;
            """,
            (torneig_id,)
        )
        tournament = cursor.fetchone()
        if not tournament:
            raise HTTPException(status_code=404, detail="Ended tournament not found")
        return Torneig(**tournament)  # Convert the result to a Torneig object
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)