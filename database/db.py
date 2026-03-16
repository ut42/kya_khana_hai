import sqlite3
from pathlib import Path
from typing import Iterable, List, Tuple, Optional


DB_PATH = Path(__file__).resolve().parent.parent / "kya_khaoge.db"


def get_db() -> sqlite3.Connection:
    """Return a SQLite connection with row factory configured for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Create core tables if they do not already exist."""
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS dishes (
            dish_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS tags (
            tag_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS dish_tags (
            dish_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            FOREIGN KEY (dish_id) REFERENCES dishes (dish_id),
            FOREIGN KEY (tag_id) REFERENCES tags (tag_id)
        );

        CREATE TABLE IF NOT EXISTS meals (
            meal_id INTEGER PRIMARY KEY,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS meal_items (
            meal_id INTEGER NOT NULL,
            dish_id INTEGER NOT NULL,
            FOREIGN KEY (meal_id) REFERENCES meals (meal_id),
            FOREIGN KEY (dish_id) REFERENCES dishes (dish_id)
        );
        """
    )

    conn.commit()


def fetch_all(conn: sqlite3.Connection, query: str, params: Iterable = ()) -> List[sqlite3.Row]:
    """Execute a read-only query and return all rows."""
    cur = conn.cursor()
    cur.execute(query, params)
    return cur.fetchall()


def fetch_one(conn: sqlite3.Connection, query: str, params: Iterable = ()) -> Optional[sqlite3.Row]:
    """Execute a read-only query and return a single row."""
    cur = conn.cursor()
    cur.execute(query, params)
    return cur.fetchone()


def execute(conn: sqlite3.Connection, query: str, params: Iterable = ()) -> None:
    """Execute a write query and commit the transaction."""
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()


def executemany(conn: sqlite3.Connection, query: str, seq_of_params: Iterable[Tuple]) -> None:
    """Execute a parametrized write query for many rows and commit."""
    cur = conn.cursor()
    cur.executemany(query, seq_of_params)
    conn.commit()

