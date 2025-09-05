import sqlite3
import os

DB_PATH = "data/myductionary.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Foydalanuvchi jadvali
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            native_language TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Foydalanuvchi jadvali
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            native_language TEXT NOT NULL
        )
    """)

    # Lug'atlar jadvali
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dictionaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            target_language TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
