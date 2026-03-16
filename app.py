import logging

import streamlit as st

from database.db import get_db, init_db
from database.seed_data import seed_if_empty
from components.search_panel import render_search_panel
from components.meal_builder import render_meal_builder_panel, render_meal_history


APP_TITLE = "Kya Khaoge"


def ensure_db_ready() -> None:
    """Initialize database schema and seed sample data if needed."""
    conn = get_db()
    init_db(conn)
    seed_if_empty(conn)
    conn.close()


def init_session_state() -> None:
    """Initialize Streamlit session state keys used across screens."""
    if "view" not in st.session_state:
        st.session_state.view = "home"
    if "current_meal_items" not in st.session_state:
        st.session_state.current_meal_items = []
    if "current_tags" not in st.session_state:
        st.session_state.current_tags = []


def go_to(view: str) -> None:
    """Helper to switch between high-level screens."""
    st.session_state.view = view


def render_home_screen() -> None:
    """Simple landing screen with primary navigation actions."""
    st.title(APP_TITLE)
    st.markdown("A minimal personal meal decision engine.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Meal", use_container_width=True):
            go_to("builder")
    with col2:
        if st.button("View Meal History", use_container_width=True):
            go_to("history")


def render_meal_builder_screen() -> None:
    """Main interface with dish search on the left and meal builder on the right."""
    st.markdown("### What do you want to eat?")

    query = st.text_input(
        "Search",
        placeholder="light chinese starter, paneer dinner, healthy breakfast",
        label_visibility="collapsed",
    )

    left, right = st.columns([2, 1], gap="large")

    with left:
        render_search_panel(query)

    with right:
        render_meal_builder_panel(on_back=lambda: go_to("home"))


def render_history_screen() -> None:
    """Display previously created meals and their dishes."""
    render_meal_history(on_back=lambda: go_to("home"))


def main() -> None:
    """Entry point for the Streamlit application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )

    st.set_page_config(page_title=APP_TITLE, layout="wide")
    ensure_db_ready()
    init_session_state()

    view = st.session_state.view

    if view == "home":
        render_home_screen()
    elif view == "builder":
        render_meal_builder_screen()
    elif view == "history":
        render_history_screen()
    else:
        render_home_screen()


if __name__ == "__main__":
    main()

