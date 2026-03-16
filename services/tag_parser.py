import json
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .llm_client import call_llm_for_json, is_llm_debug_enabled
from .tag_catalog import get_all_tag_names


logger = logging.getLogger(__name__)


def extract_tags(query: str) -> List[str]:
    """
    Simple rule-based tag extraction used as a fallback when the LLM is unavailable.
    """
    text = (query or "").lower()
    tags: List[str] = []

    keyword_map = {
        "chinese": "indo_chinese",
        "indo chinese": "indo_chinese",
        "starter": "starter",
        "crispy": "crispy",
        "rice": "rice",
        "noodles": "noodles",
        "light": "light",
        "khichdi": "comfort",
        "comfort": "comfort",
        "paneer": "paneer",
        "soup": "soup",
        "alkaline": "alkaline",
        "home": "home_style",
        "dinner": "dinner",
        "lunch": "lunch",
        "breakfast": "breakfast",
    }

    for phrase, tag in keyword_map.items():
        if phrase in text and tag not in tags:
            tags.append(tag)

    if not tags and query.strip():
        tags.append(query.strip().replace(" ", "_"))

    return tags


def _build_llm_prompt(query: str, all_tags: List[str]) -> str:
    """
    Build a rich prompt instructing the LLM to select include/exclude tags.
    """
    available = ", ".join(sorted(all_tags))
    instruction = f"""
You are a tag parser for a meal recommendation engine.

Your job:
- Read the user's food query.
- Decide which tags to INCLUDE and which tags to EXCLUDE from the provided tag list.

Very important rules:
- Only ever return tags that exist in available_tags.
- Query can be in English, Hindi & Hinglish. With slangs as well.
- INCLUDE = what the user wants. EXCLUDE = what the user explicitly does not want.
- Put a tag in \"exclude\" ONLY when the user clearly says they don't want it (e.g. \"without X\", \"no X\", \"not X\", \"avoid X\", \"mild\" when they mean not spicy). Do NOT put a tag in exclude just because a word is ambiguous.
- Positive preference: if the user says they want something, put it in include. Examples:
  - \"teekha\", \"spicy\", \"hot\", \"mirch\" mean the user WANTS spicy -> include \"spicy\".
  - \"light\", \"mild\" (when not negating) -> include \"mild\" or \"light\".
- Map common phrases to tags when appropriate:
  - \"chinese\" or \"indo chinese\" -> \"indo_chinese\"
  - \"north indian\", \"punjabi\", \"desi\" -> \"north_indian\" (if present)
  - \"mughal\", \"mughlai\" -> \"mughlai\" (if present)
- Only put a tag in exclude when the user uses clear negation: \"without\", \"no\", \"not\", \"avoid\", \"except\", \"but not\", or asks for \"mild\" in a way that means not spicy.
- Prefer fewer, precise tags over many noisy ones.

Available tags:
{available}

Output format:
Return a single JSON object with exactly two keys: \"include\" and \"exclude\".
Each must be an array of tag strings. Do not include any text outside this JSON.

Examples (assuming the tags exist):
Query: \"teekha chinese starter\" or \"spicy chinese starter\"
Result: {{\"include\": [\"spicy\", \"indo_chinese\", \"starter\"], \"exclude\": []}}

Query: \"light chinese starter crispy without spicy\"
Result: {{\"include\": [\"light\", \"indo_chinese\", \"starter\", \"crispy\"], \"exclude\": [\"spicy\"]}}

Query: \"north indian mughal without paneer\"
Result: {{\"include\": [\"north_indian\", \"mughlai\"], \"exclude\": [\"paneer\"]}}

Query: \"north indian mughal aur paneer nahi\"
Result: {{\"include\": [\"north_indian\", \"mughlai\"], \"exclude\": [\"paneer\"]}}

Now parse this query and respond only with JSON:
\"{query}\"
"""
    payload = {
        "instruction": instruction,
        "available_tags": all_tags,
        "query": query,
    }
    return json.dumps(payload)


def _normalize_tag(tag: str) -> str:
    """Canonical form for matching: strip and replace spaces with underscores."""
    return str(tag).strip().replace(" ", "_")


def _resolve_to_valid_tags(candidates: List[str], valid: set) -> List[str]:
    """Return only tags that exist in valid, using normalized form for matching."""
    seen = set()
    result = []
    for t in candidates:
        nt = _normalize_tag(t)
        if nt in valid and nt not in seen:
            result.append(nt)
            seen.add(nt)
    return result


def _parse_llm_response(data: Dict) -> Tuple[List[str], List[str]]:
    """Normalize the JSON structure returned by the LLM."""
    include = data.get("include") or []
    exclude = data.get("exclude") or []
    if not isinstance(include, list) or not isinstance(exclude, list):
        raise RuntimeError("Invalid tag structure from LLM")
    return [str(t) for t in include], [str(t) for t in exclude]


@dataclass
class TagParseResult:
    include: List[str]
    exclude: List[str]
    used_llm: bool
    prompt: Optional[str] = None
    raw_response: Optional[Dict] = None
    error: Optional[str] = None


def parse_query_tags(query: str, conn) -> TagParseResult:
    """
    Use an LLM to derive include and exclude tags from a free-text query,
    falling back to the rule-based extractor when needed.
    """
    all_tags = get_all_tag_names(conn)

    if not query.strip():
        return TagParseResult(include=[], exclude=[], used_llm=False)

    debug = is_llm_debug_enabled()

    try:
        prompt = _build_llm_prompt(query, all_tags)
        raw = call_llm_for_json(prompt)
        include, exclude = _parse_llm_response(raw)

        valid = set(all_tags)
        include_clean = _resolve_to_valid_tags(include, valid)
        exclude_clean = _resolve_to_valid_tags(exclude, valid)

        logger.info(
            "Tag parse (LLM): query=%s include=%s exclude=%s",
            query,
            include_clean,
            exclude_clean,
        )

        return TagParseResult(
            include=include_clean,
            exclude=exclude_clean,
            used_llm=True,
            prompt=prompt if debug else None,
            raw_response=raw if debug else None,
            error=None,
        )
    except Exception as exc:
        logger.warning("Tag parse fallback due to error: %s", exc)
        include_only = extract_tags(query)
        logger.info("Tag parse (fallback): query=%s include=%s", query, include_only)
        return TagParseResult(
            include=include_only,
            exclude=[],
            used_llm=False,
            prompt=None,
            raw_response=None,
            error=str(exc) if debug else None,
        )

