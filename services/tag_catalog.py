from typing import List

from database.db import fetch_all


def get_all_tag_names(conn) -> List[str]:
    """Return all tag names defined in the tags table."""
    rows = fetch_all(conn, "SELECT name FROM tags ORDER BY name")
    return [row["name"] for row in rows]

