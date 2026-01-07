import sqlite3
from pathlib import Path
import pandas as pd

DB_FILE = Path("ledger_data.db")

def init_db():
    """Initialize DB with year table if not exists"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ledger_years (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def add_year(year: int):
    """Add year if not exists"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO ledger_years (year) VALUES (?)", (year,))
    conn.commit()
    conn.close()

def get_years():
    """Return list of years in DB"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT year FROM ledger_years ORDER BY year DESC")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]

def delete_year(year: int):
    """Remove year from DB"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM ledger_years WHERE year=?", (year,))
    conn.commit()
    conn.close()
