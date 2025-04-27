import psycopg2
from psycopg2 import pool

# Configura la conexión a PostgreSQL
db_config = {
    'host': '172.17.0.2',  
    'user': 'turnonauta',
    'password': 'pirineus',
    'database': 'turnonauta',
    'port': 5432
}

# Pool de conexiones
db_pool = pool.SimpleConnectionPool(1, 30, **db_config)

def get_db_connection():
    conn = db_pool.getconn()
    try:
        # Reset sequences when a connection is established
        cursor = conn.cursor()
        reset_commands = [
            "SELECT setval('emparallaments_id_emperallent_seq', COALESCE((SELECT MAX(id_emperallent) FROM public.emparallaments), 0) + 1, false);"
            "SELECT setval('estadistiques_id_estats_seq', COALESCE((SELECT MAX(id_estats) FROM public.estadistiques), 0) + 1, false);"
            "SELECT setval('format_id_format_seq', COALESCE((SELECT MAX(id_format) FROM public.format), 0) + 1, false);"
            "SELECT setval('puntuacio_id_puntuacio_seq', COALESCE((SELECT MAX(id_puntuacio) FROM public.puntuacio), 0) + 1, false);"
            "SELECT setval('rang_id_rang_seq', COALESCE((SELECT MAX(id_rang) FROM public.rang), 0) + 1, false);"
            "SELECT setval('resultat_id_resultat_seq', COALESCE((SELECT MAX(id_resultat) FROM public.resultat), 0) + 1, false);"
            "SELECT setval('rol_id_rol_seq', COALESCE((SELECT MAX(id_rol) FROM public.rol), 0) + 1, false);"
            "SELECT setval('ronda_id_ronda_seq', COALESCE((SELECT MAX(id_ronda) FROM public.ronda), 0) + 1, false);"
            "SELECT setval('subscripcio_id_subscripcio_seq', COALESCE((SELECT MAX(id_subscripcio) FROM public.subscripcio), 0) + 1, false);"
            "SELECT setval('torneig_id_torneig_seq', COALESCE((SELECT MAX(id_torneig) FROM public.torneig), 0) + 1, false);"
            "SELECT setval('usuaris_id_usuaris_seq', COALESCE((SELECT MAX(id_usuaris) FROM public.usuaris), 0) + 1, false);"
        ]
        for command in reset_commands:
            cursor.execute(command)
        conn.commit()
    except Exception as e:
        print(f"Error resetting sequences: {e}")
        conn.rollback()
    finally:
        cursor.close()
    return conn

def release_db_connection(conn):
    db_pool.putconn(conn)

    #psql -h 172.17.0.2 -U turnonauta -d turnonauta -f ./insertsTurnonauta.psql