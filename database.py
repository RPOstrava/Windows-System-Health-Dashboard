import sqlite3
from datetime import datetime
from config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Vytvoří tabulku historie, pokud neexistuje."""
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_usage REAL NOT NULL,
                ram_usage REAL NOT NULL,
                disk_usage REAL NOT NULL
            )
        ''')
        conn.commit()

def log_metrics(metrics):
    """Zapíše aktuální stav do databáze."""
    with get_db_connection() as conn:
        conn.execute(
            'INSERT INTO history (timestamp, cpu_usage, ram_usage, disk_usage) VALUES (?, ?, ?, ?)',
            (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), metrics['cpu_usage'], metrics['ram_usage'], metrics['disk_usage'])
        )
        conn.commit()

def get_history(limit=20):
    """Načte poslední záznamy historie."""
    with get_db_connection() as conn:
        cursor = conn.execute('SELECT * FROM history ORDER BY id DESC LIMIT ?', (limit,))
        return cursor.fetchall()
