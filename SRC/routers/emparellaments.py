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

def delete_emparellament_torneig_id(torneig_id: int):
    """
    Delete all emparellaments for a specific tournament ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Start a transaction
        query_get_rondas = """
            SELECT id_ronda FROM ronda WHERE id_torneig = %s;
        """
        cursor.execute(query_get_rondas, (torneig_id,))
        rondas = cursor.fetchall()

        # Extract all id_ronda values
        id_rondas = [ronda[0] for ronda in rondas]

        if id_rondas:
            # Delete emparellaments associated with the rondas
            query_delete_emparellaments = """
                DELETE FROM emparallaments WHERE id_ronda = ANY(%s);
            """
            cursor.execute(query_delete_emparellaments, (id_rondas,))

        # Delete the rondas associated with the tournament
        query_delete_rondas = """
            DELETE FROM ronda WHERE id_torneig = %s;
        """
        cursor.execute(query_delete_rondas, (torneig_id,))

        # Commit the transaction
        conn.commit()
        return {"message": "Rondas and associated emparellaments deleted successfully"}
    except Exception as e:
        conn.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)