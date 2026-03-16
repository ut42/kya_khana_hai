import logging
from typing import List, Tuple

from database.db import fetch_all


logger = logging.getLogger(__name__)


def search_dishes_by_tags(
    conn,
    include_tags: List[str],
    exclude_tags: List[str],
) -> Tuple[List[dict], List[dict]]:
    """
    Search dishes using include and exclude tag lists.

    - Include tags: contribute to a score based on how many tags a dish matches.
    - Exclude tags: any dish with one of these tags is filtered out.
    """
    if not include_tags:
        # Browse view: show all dishes, optionally excluding some tags.
        params: List[str] = []
        exclude_clause = ""
        if exclude_tags:
            placeholders_ex = ",".join(["?"] * len(exclude_tags))
            exclude_clause = f"""
            WHERE d.dish_id NOT IN (
                SELECT dt2.dish_id
                FROM dish_tags dt2
                JOIN tags t2 ON t2.tag_id = dt2.tag_id
                WHERE t2.name IN ({placeholders_ex})
            )
            """
            params.extend(exclude_tags)

        rows = fetch_all(
            conn,
            f"""
            SELECT d.dish_id,
                   d.name,
                   d.description,
                   GROUP_CONCAT(t.name, ',') AS all_tags
            FROM dishes d
            LEFT JOIN dish_tags dt ON d.dish_id = dt.dish_id
            LEFT JOIN tags t ON t.tag_id = dt.tag_id
            {exclude_clause}
            GROUP BY d.dish_id, d.name, d.description
            ORDER BY d.name
            """,
            params,
        )
        dishes = [_row_to_dish(row, score=0) for row in rows]
        logger.info(
            "Browse search: exclude=%s -> %d dishes",
            exclude_tags,
            len(dishes),
        )
        return dishes, []

    placeholders_in = ",".join(["?"] * len(include_tags))
    params_in: List[str] = list(include_tags)

    exclude_clause_scored = ""
    if exclude_tags:
        placeholders_ex = ",".join(["?"] * len(exclude_tags))
        exclude_clause_scored = f"""
        AND d.dish_id NOT IN (
            SELECT dt2.dish_id
            FROM dish_tags dt2
            JOIN tags t2 ON t2.tag_id = dt2.tag_id
            WHERE t2.name IN ({placeholders_ex})
        )
        """
        params_in.extend(exclude_tags)

    rows = fetch_all(
        conn,
        f"""
        SELECT
            d.dish_id,
            d.name,
            d.description,
            COUNT(*) AS score,
            GROUP_CONCAT(DISTINCT t_all.name) AS all_tags
        FROM dish_tags dt
        JOIN tags t ON t.tag_id = dt.tag_id
        JOIN dishes d ON d.dish_id = dt.dish_id
        LEFT JOIN dish_tags dt_all ON dt_all.dish_id = d.dish_id
        LEFT JOIN tags t_all ON t_all.tag_id = dt_all.tag_id
        WHERE t.name IN ({placeholders_in})
        {exclude_clause_scored}
        GROUP BY d.dish_id, d.name, d.description
        ORDER BY score DESC, d.name ASC
        """,
        params_in,
    )

    scored = [_row_to_dish(row, score=row["score"]) for row in rows]

    if not scored:
        logger.info(
            "Search: include=%s exclude=%s -> 0 matches",
            include_tags,
            exclude_tags,
        )
        return [], []

    max_score = scored[0]["score"]
    top_matches = [d for d in scored if d["score"] == max_score]
    other_options = [d for d in scored if d["score"] != max_score]

    logger.info(
        "Search: include=%s exclude=%s -> %d matches (top=%d, other=%d)",
        include_tags,
        exclude_tags,
        len(scored),
        len(top_matches),
        len(other_options),
    )

    return top_matches, other_options


def _row_to_dish(row, score: int) -> dict:
    """Convert a row to a simple serializable dish dictionary."""
    tags = []
    if row["all_tags"]:
        tags = [t.strip() for t in str(row["all_tags"]).split(",") if t.strip()]
    return {
        "dish_id": row["dish_id"],
        "name": row["name"],
        "description": row["description"],
        "tags": sorted(set(tags)),
        "score": int(score),
    }

