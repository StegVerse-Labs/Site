"""
Universal data ingestion runner for StegVerse Sports.

- Reads ingestion/universal_config.json
- For each enabled sport:
  - Iterates sources in priority order
  - Uses the first source that succeeds to produce canonical data
  - Writes JSON output to the configured file (relative to repo root)
"""

import json
import os
import sys
import traceback
from typing import Dict, Any, List

from pathlib import Path

from sources import fetch_from_source


ROOT = Path(__file__).resolve().parents[1]  # site/ root
CONFIG_PATH = ROOT / "ingestion" / "universal_config.json"


def log(msg: str):
    print(msg, file=sys.stdout)


def load_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json_relpath(rel_path: str, data: Dict[str, Any]):
    out_path = ROOT / rel_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=False)
    log(f"Wrote: {out_path}")


def run_for_sport(sport_key: str, sport_cfg: Dict[str, Any]) -> bool:
    if not sport_cfg.get("enabled", False):
        log(f"[{sport_key}] Skipped (disabled).")
        return False

    output_file = sport_cfg.get("output_file")
    sources = sport_cfg.get("sources", [])
    if not output_file or not sources:
        log(f"[{sport_key}] Missing output_file or sources.")
        return False

    # Sort by priority (lowest number = highest priority)
    sources_sorted = sorted(
        [s for s in sources if s.get("enabled", True)],
        key=lambda s: s.get("priority", 999)
    )

    last_error = None
    for src in sources_sorted:
        src_id = src.get("id")
        src_type = src.get("type")
        cfg = src.get("config", {})
        log(f"[{sport_key}] Trying source {src_id} (type={src_type})...")
        try:
            data = fetch_from_source(src_type, cfg)
            write_json_relpath(output_file, data)
            log(f"[{sport_key}] SUCCESS via source {src_id}.")
            return True
        except Exception as e:
            last_error = e
            log(f"[{sport_key}] Source {src_id} failed: {e}")
            traceback.print_exc()

    log(f"[{sport_key}] All sources failed. Last error: {last_error}")
    return False


def main() -> int:
    if not CONFIG_PATH.exists():
        log(f"Config not found: {CONFIG_PATH}")
        return 1

    cfg = load_config()
    sports = cfg.get("sports", {})

    overall_ok = True
    for key, sport_cfg in sports.items():
        ok = run_for_sport(key, sport_cfg)
        overall_ok = overall_ok and ok

    if overall_ok:
        log("✅ Universal ingestion finished successfully.")
        return 0
    else:
        log("⚠️ Universal ingestion finished with some failures.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
