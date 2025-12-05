import sqlite3

DB_NAME = "vehicles.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vin TEXT PRIMARY KEY COLLATE NOCASE,
            manufacturer TEXT NOT NULL,
            description TEXT NOT NULL,
            horsepower INTEGER NOT NULL,
            model TEXT NOT NULL,
            model_year INTEGER NOT NULL,
            purchase_price REAL NOT NULL,
            fuel_type TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()
