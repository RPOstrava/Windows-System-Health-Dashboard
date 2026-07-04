import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "health.db"

# Zajistí existenci složky pro databázi
DB_DIR.mkdir(exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-keep-it-secret")
    DATABASE = str(DB_PATH)
    MONITOR_INTERVAL = 60  # sekundy mezi zápisy do historie
