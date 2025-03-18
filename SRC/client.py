import psycopg2
from psycopg2 import pool

# Configura la conexión a PostgreSQL
db_config = {
    'host': '172.17.0.2',  
    'user': 'postgres',
    'password': 'pirineus',
    'database': 'turnonauta',
    'port': 5432
}

# Pool de conexiones
db_pool = pool.SimpleConnectionPool(1, 5, **db_config)

def get_db_connection():
    return db_pool.getconn()

def release_db_connection(conn):
    db_pool.putconn(conn)

    #psql -h 172.17.0.2 -U turnonauta -d turnonauta -f ./insertsTurnonauta.psql