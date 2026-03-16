from datetime import datetime
from typing import Callable, List, Optional

import streamlit as st

from database.db import get_db, fetch_all


def render_meal_builder_panel(on_back: Callable[[], None]) -> None:
    """Render the right-side panel showing the current meal and actions."""
    st.markdown("### Current Meal")

    items: List[dict] = st.session_state.get("current_meal_items", [])

    if not items:
        st.caption("No dishes added yet.")
    else:
        for dish in items:
            row = st.container(border=False)
            with row:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"- **{dish['name']}**")
                with cols[1]:
                    if st.button("Remove", key=f"remove_{dish['dish_id']}", use_container_width=True):
                        _remove_dish_from_meal(dish["dish_id"])

    st.divider()

    cols = st.columns(2)
    with cols[0]:
        if st.button("Finalize Meal", type="primary", use_container_width=True, disabled=not items):
            meal_id = _save_current_meal()
            if meal_id:
                st.success("Meal saved.")
                st.session_state.current_meal_items = []
    with cols[1]:
        if st.button("Back to Home", use_container_width=True):
            on_back()


def _remove_dish_from_meal(dish_id: int) -> None:
    """Remove a dish from the in-memory current meal."""
    items: List[dict] = st.session_state.get("current_meal_items", [])
    st.session_state.current_meal_items = [d for d in items if d["dish_id"] != dish_id]


def _save_current_meal() -> Optional[int]:
    """Persist the current meal and its dishes into the database."""
    items: List[dict] = st.session_state.get("current_meal_items", [])
    if not items:
        return None

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO meals (created_at) VALUES (?)",
        (datetime.utcnow().isoformat(timespec="seconds"),),
    )
    meal_id = cur.lastrowid

    cur.executemany(
        "INSERT INTO meal_items (meal_id, dish_id) VALUES (?, ?)",
        [(meal_id, d["dish_id"]) for d in items],
    )
    conn.commit()
    conn.close()
    return int(meal_id)


def render_meal_history(on_back: Callable[[], None]) -> None:
    """Render a simple view listing past meals and their dishes."""
    st.markdown("### Meal History")

    conn = get_db()
    rows = fetch_all(
        conn,
        """
        SELECT
            m.meal_id,
            m.created_at,
            d.name AS dish_name
        FROM meals m
        LEFT JOIN meal_items mi ON mi.meal_id = m.meal_id
        LEFT JOIN dishes d ON d.dish_id = mi.dish_id
        ORDER BY m.created_at DESC, m.meal_id DESC
        """,
    )

    if not rows:
        st.caption("No meals yet.")
    else:
        current_meal_id = None
        current_container = None
        for row in rows:
            if row["meal_id"] != current_meal_id:
                current_meal_id = row["meal_id"]
                current_container = st.container(border=True)
                with current_container:
                    st.markdown(f"**Meal #{current_meal_id}**")
                    st.caption(row["created_at"])
                    if row["dish_name"]:
                        st.markdown(f"- {row['dish_name']}")
            else:
                if current_container and row["dish_name"]:
                    with current_container:
                        st.markdown(f"- {row['dish_name']}")

    conn.close()

    st.divider()
    if st.button("Back to Home", use_container_width=True):
        on_back()

