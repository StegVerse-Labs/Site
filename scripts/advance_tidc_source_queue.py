#!/usr/bin/env python3
"""Advance the internal TIDC source queue without halting on missing evidence."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "data" / "tidc" / "source-work-queue.v0.1.json"
ACTIVE_PATH = ROOT / "data" / "tidc" / "source-work" / "active.json"
RECEIPTS = ROOT / "data" / "tidc" / "source-receipts"


def receipt_path(item: dict[str, Any]) -> Path:
    target = item["completion_target"].split(";")[-1].strip()
    return ROOT / target


def receipt_is_complete(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return data.get("status") in {"COMPLETE", "LIMITATION_RETAINED"}


def make_active(item: dict[str, Any]) -> dict[str, Any]:
    target = receipt_path(item)
    return {
        "schema": "stegverse.site.tidc.active_source_work.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "work_id": item["work_id"],
        "record_ids": item["record_ids"],
        "task": item["task"],
        "exists_at": item["exists_at"],
        "completion_target": item["completion_target"],
        "receipt_path": str(target.relative_to(ROOT)),
        "status": "ACTIVE",
        "allowed_terminal_states": ["COMPLETE", "LIMITATION_RETAINED"],
        "instructions": [
            "Use the strongest available primary sources.",
            "Preserve inaccessible or unresolved evidence explicitly.",
            "Do not recode the first pass to force agreement.",
            "Write the completion receipt at receipt_path.",
            "After the receipt is committed, the coordinator advances automatically to the next READY item."
        ],
        "continuation": "This active task does not block validators, return processing, or unrelated source work preparation."
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ACTIVE_PATH)
    args = parser.parse_args()

    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    items = queue.get("queue", [])
    completed: list[str] = []
    next_item: dict[str, Any] | None = None

    for item in items:
        path = receipt_path(item)
        if receipt_is_complete(path):
            completed.append(item["work_id"])
            continue
        if next_item is None and item.get("status") in {"READY", "ACTIVE"}:
            next_item = item

    args.out.parent.mkdir(parents=True, exist_ok=True)
    if next_item is None:
        state = {
            "schema": "stegverse.site.tidc.active_source_work.v0.1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "QUEUE_EXHAUSTED",
            "completed_work_ids": completed,
            "development_halted": False,
            "continuation": "Source queue exhausted; continue gate evaluation and publication synchronization."
        }
    else:
        state = make_active(next_item)
        state["completed_work_ids"] = completed
        state["remaining_count"] = len(items) - len(completed)
        state["development_halted"] = False

    args.out.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": state["status"],
        "work_id": state.get("work_id"),
        "completed": len(completed),
        "remaining": state.get("remaining_count", 0),
        "development_halted": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
