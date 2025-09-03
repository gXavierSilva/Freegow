import psycopg2
from flask import current_app
from models import create_all_tables

def get_db_connection():
    conn = psycopg2.connect(
        host=current_app.config['DB_HOST'],
        database=current_app.config['DB_NAME'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASSWORD'],
        port=current_app.config['DB_PORT']
    )
    return conn

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        create_all_tables(cur)
    except:
        print("Tabela já criada.")
    conn.commit()
    cur.close()
    conn.close()