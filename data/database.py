import psycopg2
from config import Config

def get_connection():
    """Cria e retorna uma conexão com o PostgreSQL."""
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )
    return conn
