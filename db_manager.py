import psycopg
from psycopg.rows import dict_row

# Note: 'host=db' refers to the service name in your docker-compose.yml
DB_URL = "postgresql://admin:password123@db:5432/my_database"

def get_all_data():
    # 'dict_row' makes the output look like {'id': 1, 'name': 'test'}
    with psycopg.connect(DB_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM my_table;")
            return cur.fetchall()

def add_entry(content):
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO my_table (content) VALUES (%s);", (content,))
            conn.commit()
