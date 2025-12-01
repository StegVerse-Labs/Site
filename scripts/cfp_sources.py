# scripts/cfp_sources.py

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


CONFIG_PATH = Path("data/cfp_sources.json")


class SourceConfigError(RuntimeError):
    pass


def _load_raw_config() -> Dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise SourceConfigError(f"CFP source config not found at {CONFIG_PATH}")
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SourceConfigError(f"Invalid JSON in {CONFIG_PATH}: {e}") from e


def list_sources(kind: Optional[str] = None, season: Optional[int] = None) -> List[Dict[str, Any]]:
    cfg = _load_raw_config()
    sources = cfg.get("sources", [])
    filtered: List[Dict[str, Any]] = []

    for src in sources:
        if not src.get("enabled", True):
            continue
        if kind and src.get("kind") != kind:
            continue
        if season and src.get("season") not in (None, season):
            continue
        filtered.append(src)

    # Higher priority first
    filtered.sort(key=lambda s: s.get("priority", 0), reverse=True)
    return filtered


def pick_best_source(kind: str, season: int = 2025) -> Dict[str, Any]:
    sources = list_sources(kind=kind, season=season)
    if not sources:
        raise SourceConfigError(f"No enabled sources found for kind='{kind}', season={season}")
    return sources[0]
