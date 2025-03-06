import psycopg2
from psycopg2 import pool

# Configura la conexión a PostgreSQL
db_config = {
    'host': '127.0.0.1',  
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