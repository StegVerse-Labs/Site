"""
Central helper for CFP/NCAAF source config.

Usage (from any script in Site/scripts):

    from cfp_source_config import get_sources, get_primary_source_url

    src = get_primary_source_url("cfp_rankings", year=2025, week=13)
    print(src)  # => 'https://collegefootballplayoff.com/rankings.aspx?year=2025'
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "cfp_sources.json"


def _load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


_CONFIG_CACHE: Optional[Dict[str, Any]] = None


def get_config() -> Dict[str, Any]:
    global _CONFIG_CACHE
    if _CONFIG_CACHE is None:
        _CONFIG_CACHE = _load_config()
    return _CONFIG_CACHE


def get_sources(section: str) -> List[Dict[str, Any]]:
    """
    Return all enabled sources for a given section, sorted by priority.
    section: 'cfp_rankings', 'ap_poll', 'coaches_poll', 'standings', etc.
    """
    cfg = get_config()
    block = cfg.get(section, {})
    sources = [s for s in block.get("sources", []) if s.get("enabled", True)]
    return sorted(sources, key=lambda s: s.get("priority", 999))


def _apply_env_in_headers(headers: Dict[str, str]) -> Dict[str, str]:
    out = {}
    for k, v in headers.items():
        # Replace {ENV_VAR} placeholders with actual env values if present.
        if "{" in v and "}" in v:
            for part in v.split("{"):
                if "}" in part:
                    env_name, tail = part.split("}", 1)
                    if env_name:
                        env_val = os.getenv(env_name, "")
                        v = v.replace("{" + env_name + "}", env_val)
        out[k] = v
    return out


def build_source_url(source: Dict[str, Any], **params: Any) -> str:
    """Fill the url_template of a source with given params (year, week, etc)."""
    url_tmpl = source["url_template"]
    return url_tmpl.format(**params)


def get_primary_source(section: str) -> Optional[Dict[str, Any]]:
    """Get the first enabled source (lowest priority number) for a section."""
    srcs = get_sources(section)
    return srcs[0] if srcs else None


def get_primary_source_url(section: str, **params: Any) -> Optional[str]:
    """
    Convenience: return primary source URL for section, or None if missing.

    Example:
        url = get_primary_source_url('cfp_rankings', year=2025, week=13)
    """
    src = get_primary_source(section)
    if not src:
        return None
    return build_source_url(src, **params)


def get_primary_source_with_headers(section: str, **params: Any) -> Optional[Dict[str, Any]]:
    """
    For APIs that need headers (e.g., CFBD with API key).
    Returns a dict with 'url' and 'headers' keys.
    """
    src = get_primary_source(section)
    if not src:
        return None

    url = build_source_url(src, **params)
    headers = _apply_env_in_headers(src.get("headers", {}))
    return {"url": url, "headers": headers}
