import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


CONFIG_PATH = Path(__file__).resolve().parent.parent / "llm_config.json"
logger = logging.getLogger(__name__)


@dataclass
class LLMConfig:
    """Configuration describing how to talk to the chosen LLM provider."""

    provider: str
    model: str
    api_key: str
    base_url: Optional[str] = None
    debug: bool = False


def load_config() -> LLMConfig:
    """
    Load LLM settings from llm_config.json in the project root.

    This keeps credentials out of source code. The expected JSON shape is:
    {
      "provider": "openai",
      "model": "gpt-4.1-mini",
      "api_key": "sk-...",
      "base_url": null
    }
    """
    if not CONFIG_PATH.exists():
        raise RuntimeError(f"LLM config not found at {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    cfg = LLMConfig(
        provider=raw.get("provider", "openai"),
        model=raw["model"],
        api_key=raw["api_key"],
        base_url=raw.get("base_url"),
        debug=bool(raw.get("debug", False)),
    )
    logger.info("Loaded LLM config: provider=%s, model=%s, debug=%s", cfg.provider, cfg.model, cfg.debug)
    return cfg


def is_llm_debug_enabled() -> bool:
    """Return True when LLM debug information should be surfaced in the UI."""
    try:
        cfg = load_config()
        return bool(cfg.debug)
    except Exception:
        return False


def call_llm_for_json(prompt: str) -> Dict[str, Any]:
    """
    Call the configured LLM with a prompt expected to return JSON.

    This function is intentionally minimal. It raises on errors so that the
    caller can decide whether to fall back to a rule-based implementation.
    """
    cfg = load_config()
    logger.info("LLM call: provider=%s, model=%s", cfg.provider, cfg.model)

    if cfg.provider == "openai":
        try:
            from openai import OpenAI  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "openai package is not installed. Install it in your environment to enable LLM parsing."
            ) from exc

        client = OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)
        logger.debug("OpenAI prompt=%s", prompt)
        response = client.chat.completions.create(
            model=cfg.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that only replies with valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        content = response.choices[0].message.content or ""
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            logger.exception("OpenAI JSON parse failed")
            raise RuntimeError("LLM response was not valid JSON") from exc

    if cfg.provider == "gemini":
        try:
            import google.generativeai as genai  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "google-generativeai package is not installed. Install it in your environment to enable Gemini parsing."
            ) from exc

        genai.configure(api_key=cfg.api_key)
        model = genai.GenerativeModel(model_name=cfg.model)
        logger.debug("Gemini prompt=%s", prompt)
        response = model.generate_content(
            [prompt],
            generation_config={"temperature": 0},
        )
        content = response.text or ""
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            logger.exception("Gemini JSON parse failed")
            raise RuntimeError("Gemini response was not valid JSON") from exc

    if cfg.provider == "groq":
        try:
            from groq import Groq  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "groq package is not installed. Install it in your environment to enable Groq parsing."
            ) from exc

        client = Groq(api_key=cfg.api_key)
        logger.debug("Groq prompt=%s", prompt)
        response = client.chat.completions.create(
            model=cfg.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that only replies with valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        content = response.choices[0].message.content or ""
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            logger.exception("Groq JSON parse failed")
            raise RuntimeError("Groq response was not valid JSON") from exc

    raise RuntimeError(f"Unsupported LLM provider: {cfg.provider}")

