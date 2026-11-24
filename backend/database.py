import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "cars.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                plate    TEXT NOT NULL UNIQUE,
                region   TEXT NOT NULL,
                car_type TEXT NOT NULL,
                model    TEXT
            )
        """)


if __name__ == "__main__":
    init_db()
    print("Baza tayyor:", DB_PATH)