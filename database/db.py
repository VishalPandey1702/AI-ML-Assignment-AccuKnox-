import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = os.environ.get('DATABASE_PATH', 'books.db')

def get_db_path():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, DATABASE_PATH)

@contextmanager
def get_connection():
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        if conn:
            conn.close()

def initialize_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publication_year INTEGER,
                isbn TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(title, author)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT NOT NULL,
                score REAL NOT NULL CHECK(score >= 0 AND score <= 100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()

def clear_table(table_name):
    valid_tables = {'books', 'students', 'users'}
    if table_name not in valid_tables:
        raise ValueError(f"Invalid table name")
    
    with get_connection() as conn:
        cursor = conn.execute(f"DELETE FROM {table_name}")
        deleted_count = cursor.rowcount
        conn.commit()
        return deleted_count

def get_table_count(table_name):
    valid_tables = {'books', 'students', 'users'}
    if table_name not in valid_tables:
        raise ValueError(f"Invalid table name")
    
    with get_connection() as conn:
        cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]

if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at: {get_db_path()}")
