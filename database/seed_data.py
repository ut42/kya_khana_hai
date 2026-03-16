"""
Seed the database from external data files.

Loads tags from data/tags.json and dishes (with tag associations) from data/dishes.json.
"""
import json
from datetime import datetime
from pathlib import Path

from .db import execute, executemany, fetch_one

# Paths relative to project root (parent of database/).
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TAGS_PATH = PROJECT_ROOT / "data" / "tags.json"
DISHES_PATH = PROJECT_ROOT / "data" / "dishes.json"


def dishes_exist(conn) -> bool:
    """Return True if any dishes are already present."""
    row = fetch_one(conn, "SELECT COUNT(*) AS c FROM dishes")
    return bool(row and row["c"] > 0)


def _load_json(path: Path):
    """Load and parse a JSON file."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def seed_if_empty(conn) -> None:
    """Populate the database from data/tags.json and data/dishes.json if empty."""
    if dishes_exist(conn):
        return

    tags_data = _load_json(TAGS_PATH)
    dishes_data = _load_json(DISHES_PATH)

    if not isinstance(tags_data, list):
        raise ValueError("data/tags.json must be a JSON array of {name, description} objects")
    if not isinstance(dishes_data, list):
        raise ValueError("data/dishes.json must be a JSON array of {name, description, tags} objects")

    # Insert tags.
    for item in tags_data:
        name = item.get("name")
        desc = item.get("description") or ""
        if not name:
            continue
        conn.execute(
            "INSERT OR IGNORE INTO tags (name, description) VALUES (?, ?)",
            (name.strip(), desc),
        )
    conn.commit()

    # Build tag name -> tag_id map.
    tag_rows = conn.execute("SELECT tag_id, name FROM tags").fetchall()
    tag_by_name = {row["name"]: row["tag_id"] for row in tag_rows}

    # Insert dishes.
    for item in dishes_data:
        name = item.get("name")
        desc = item.get("description") or ""
        if not name:
            continue
        conn.execute(
            "INSERT INTO dishes (name, description) VALUES (?, ?)",
            (name.strip(), desc),
        )
    conn.commit()

    # Build dish name -> dish_id map (dishes were just inserted in order).
    dish_rows = conn.execute("SELECT dish_id, name FROM dishes").fetchall()
    dish_by_name = {row["name"]: row["dish_id"] for row in dish_rows}

    # Insert dish_tags from each dish's "tags" array.
    dish_tag_pairs = []
    for item in dishes_data:
        name = item.get("name")
        tag_names = item.get("tags") or []
        if not name or not isinstance(tag_names, list):
            continue
        dish_id = dish_by_name.get(name)
        if dish_id is None:
            continue
        for t in tag_names:
            tag_id = tag_by_name.get(t if isinstance(t, str) else str(t))
            if tag_id is not None:
                dish_tag_pairs.append((dish_id, tag_id))

    if dish_tag_pairs:
        executemany(
            conn,
            "INSERT INTO dish_tags (dish_id, tag_id) VALUES (?, ?)",
            dish_tag_pairs,
        )

    # One sample meal for history.
    conn.execute(
        "INSERT INTO meals (created_at) VALUES (?)",
        (datetime.utcnow().isoformat(timespec="seconds"),),
    )
    conn.commit()
    meal_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]

    # Add first two dishes as sample meal items if they exist.
    first_names = [item.get("name") for item in dishes_data[:2] if item.get("name")]
    for dname in first_names:
        did = dish_by_name.get(dname)
        if did is not None:
            conn.execute("INSERT INTO meal_items (meal_id, dish_id) VALUES (?, ?)", (meal_id, did))
    conn.commit()
