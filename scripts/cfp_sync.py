#!/usr/bin/env python
"""
CFP data sync script for StegVerse-Labs/Site.

- Reads CFP_API_URL from env (set in GitHub Actions secrets)
- Calls that endpoint (served by SCW-API)
- Expects a payload with a "files" dict, whose keys are filenames and
  whose values are JSON-serialisable objects
- Writes each file into the repo's ./data directory
"""

import os
import sys
import json
import datetime as dt
from pathlib import Path

import requests


def main() -> int:
    api_url = os.getenv("CFP_API_URL", "").strip()
    if not api_url:
        print("ERROR: CFP_API_URL not set in environment", file=sys.stderr)
        return 1

    print(f"[cfp_sync] Fetching data from {api_url} ...")
    try:
        resp = requests.get(api_url, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f"ERROR: request failed: {e}", file=sys.stderr)
        return 1

    try:
        payload = resp.json()
    except Exception as e:
        print(f"ERROR: could not decode JSON: {e}", file=sys.stderr)
        return 1

    # Expected shape:
    # {
    #   "season": 2025,
    #   "last_release": "...",
    #   "files": {
    #       "cfp-2025.json": {...},
    #       "cfp-data.json": {...},
    #       "cfp-teams.json": {...},
    #       "cfp-tickets.json": {...}
    #   }
    # }
    files = payload.get("files")
    if not isinstance(files, dict):
        print("ERROR: payload missing 'files' dict", file=sys.stderr)
        return 1

    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / "data"
    data_dir.mkdir(exist_ok=True)

    for filename, content in files.items():
        target = data_dir / filename
        try:
            with target.open("w", encoding="utf-8") as f:
                json.dump(content, f, indent=2)
            print(f"[cfp_sync] Wrote {target.relative_to(repo_root)}")
        except Exception as e:
            print(f"ERROR: could not write {target}: {e}", file=sys.stderr)
            return 1

    # Small meta file so the UI can show last-sync info if desired
    meta = {
        "season": payload.get("season"),
        "last_release": payload.get("last_release"),
        "source": api_url,
        "last_sync_utc": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    meta_path = data_dir / "cfp-sync-meta.json"
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"[cfp_sync] Wrote {meta_path.relative_to(repo_root)}")

    print("[cfp_sync] Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
