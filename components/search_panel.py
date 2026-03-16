import json
from typing import List

import streamlit as st

from database.db import get_db
from services.llm_client import is_llm_debug_enabled
from services.tag_parser import TagParseResult, parse_query_tags
from services.search_engine import search_dishes_by_tags

COMPACT_CSS = """
<style>
  [data-testid="stVerticalBlockBorderWrapper"] { padding: 0.35rem 0.5rem !important; }
  [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown, 
  [data-testid="stVerticalBlockBorderWrapper"] .stCaptionContainer { margin: 0 0 0.1rem 0 !important; }
</style>
"""


def _render_tag_chips(included: List[str], excluded: List[str]) -> None:
    """Display interpreted include and exclude tags as small chips."""
    if not included and not excluded:
        return
    if included:
        st.caption(" ".join(f"`{t}`" for t in included))
    if excluded:
        st.caption("Excl: " + " ".join(f"`~{t}`" for t in excluded))


def _render_llm_debug(result: TagParseResult, query: str) -> None:
    """Show a collapsible panel with LLM prompt/response when debug is enabled."""
    if not is_llm_debug_enabled() or not query.strip():
        return

    with st.expander("LLM tag parsing (debug)", expanded=False):
        engine_label = "LLM" if result.used_llm else "Fallback parser"
        st.caption(f"Engine: {engine_label}")

        if result.prompt:
            st.markdown("**Prompt**")
            st.code(result.prompt, language="json")

        if result.raw_response:
            st.markdown("**Response**")
            st.code(json.dumps(result.raw_response, indent=2), language="json")

        if result.error:
            st.warning(result.error)


def render_search_panel(query: str) -> None:
    """Render the left-side search experience: tags + dish results."""
    st.markdown(COMPACT_CSS, unsafe_allow_html=True)
    conn = get_db()

    result = parse_query_tags(query, conn)
    include_tags = result.include
    exclude_tags = result.exclude

    # Persist tags so the meal builder panel or other components can read them.
    st.session_state.current_tags = {
        "include": include_tags,
        "exclude": exclude_tags,
    }

    _render_llm_debug(result, query)
    _render_tag_chips(include_tags, exclude_tags)

    top_matches, other_options = search_dishes_by_tags(conn, include_tags, exclude_tags)

    st.caption("Browse dishes" if not query else "Results")
    _render_dish_section("Top matches", top_matches)
    _render_dish_section("Other options", other_options)
    conn.close()


def _render_dish_section(title: str, dishes: List[dict]) -> None:
    """Render dish cards in a compact 4-per-row grid."""
    if not dishes:
        return
    st.markdown(f"**{title}**")
    for i in range(0, len(dishes), 4):
        row = dishes[i : i + 4]
        cols = st.columns(4)
        for col, dish in zip(cols, row):
            with col:
                _render_dish_card(dish)


def _render_dish_card(dish: dict) -> None:
    """Compact card: name, short description, Add button."""
    desc = (dish.get("description") or "").strip()
    if len(desc) > 45:
        desc = desc[:42].rsplit(" ", 1)[0] + "…" if " " in desc[:42] else desc[:42] + "…"
    card = st.container(border=True)
    with card:
        st.markdown(f"**{dish['name']}**")
        if desc:
            st.caption(desc)
        if st.button("Add", key=f"add_{dish['dish_id']}", use_container_width=True):
            current = st.session_state.get("current_meal_items", [])
            if dish["dish_id"] not in [d["dish_id"] for d in current]:
                st.session_state.current_meal_items = current + [dish]
