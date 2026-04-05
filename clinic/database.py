from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "rehabtrack.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
SEED_PATH = BASE_DIR / "sql" / "seed.sql"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_database(reset: bool = False) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if reset and DB_PATH.exists():
        DB_PATH.unlink()

    if DB_PATH.exists():
        return

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    seed_sql = SEED_PATH.read_text(encoding="utf-8")

    with get_connection() as conn:
        conn.executescript(schema_sql)
        conn.executescript(seed_sql)
        conn.commit()
