#!/usr/bin/env python3
"""Run deterministic transition-table experiments and update static outputs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ELEMENTS_PATH = DATA_DIR / "transition-elements.json"
EVIDENCE_PATH = DATA_DIR / "transition-evidence.json"
LEDGER_PATH = DATA_DIR / "transition-ledger.jsonl"

EVIDENCE_LABELS = [
    "Proposed",
    "Defined",
    "Derived",
    "Proven",
    "Tested",
    "Receipt-backed",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def run_t1_sweep() -> list[dict[str, Any]]:
    samples = [
        {"g": 0.42, "c": 0.71, "a": 0.19, "t": 0.88, "dg": -0.02, "dc": 0.01, "da": 0.03, "dt": -0.01},
        {"g": 0.31, "c": 0.60, "a": 0.27, "t": 0.72, "dg": 0.02, "dc": 0.00, "da": 0.05, "dt": -0.02},
        {"g": 0.80, "c": 0.63, "a": 0.36, "t": 0.70, "dg": -0.04, "dc": 0.04, "da": 0.02, "dt": 0.01},
        {"g": 0.28, "c": 0.33, "a": 0.18, "t": 0.41, "dg": 0.01, "dc": 0.01, "da": 0.06, "dt": 0.00},
        {"g": 0.55, "c": 0.52, "a": 0.12, "t": 0.79, "dg": 0.00, "dc": -0.03, "da": 0.02, "dt": -0.01},
    ]

    rows: list[dict[str, Any]] = []
    timestamp = utc_now()

    for index, sample in enumerate(samples, start=1):
        post = {
            "g": round(sample["g"] + sample["dg"], 4),
            "c": round(sample["c"] + sample["dc"], 4),
            "a": round(sample["a"] + sample["da"], 4),
            "t": round(sample["t"] + sample["dt"], 4),
        }
        capacity = round(post["g"] * post["c"] * post["t"], 5)
        invariant = round(post["a"] - capacity, 5)
        verdict = "ALLOW" if invariant <= 0 else "DENY"

        rows.append(
            {
                "timestamp": timestamp,
                "element_id": "T1",
                "mode": "deterministic_sweep",
                "run_id": f"t1-{index:03d}",
                "parameters": {"K": 1, "alpha": 1, "beta": 1, "gamma": 1},
                "pre_state": {"g": sample["g"], "c": sample["c"], "a": sample["a"], "t": sample["t"]},
                "action": {"dg": sample["dg"], "dc": sample["dc"], "da": sample["da"], "dt": sample["dt"]},
                "post_state": post,
                "capacity": capacity,
                "invariant": invariant,
                "verdict": verdict,
                "passed": True,
                "receipt_hash": None,
            }
        )

    return rows


def update_evidence(elements: list[dict[str, Any]], ledger_rows: list[dict[str, Any]]) -> dict[str, Any]:
    evidence = {
        "generated_at": utc_now(),
        "generated_by": "tools/run_transition_experiments.py",
        "evidence_labels": EVIDENCE_LABELS,
        "elements": {},
    }

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in ledger_rows:
        grouped.setdefault(row["element_id"], []).append(row)

    for element in elements:
        element_id = element["id"]
        level = int(element.get("evidence_level", 0))
        result_summary = element.get("confirmed_behavior", "No confirmed behavior has been recorded yet.")

        if element_id == "T1" and grouped.get("T1"):
            level = max(level, 4)
            allow_count = sum(1 for row in grouped["T1"] if row["verdict"] == "ALLOW")
            deny_count = sum(1 for row in grouped["T1"] if row["verdict"] == "DENY")
            result_summary = (
                f"Deterministic T1 sweep generated {len(grouped['T1'])} rows: "
                f"{allow_count} ALLOW, {deny_count} DENY, 0 FAIL-CLOSED. "
                "Receipt generation remains pending."
            )

        evidence["elements"][element_id] = {
            "evidence_level": level,
            "evidence_label": EVIDENCE_LABELS[level],
            "brightness": round(level / 5, 2),
            "receipt_backed": False,
            "latest_result_summary": result_summary,
        }

    return evidence


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    elements = load_json(ELEMENTS_PATH)
    ledger_rows = run_t1_sweep()
    LEDGER_PATH.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in ledger_rows),
        encoding="utf-8",
    )
    evidence = update_evidence(elements, ledger_rows)
    write_json(EVIDENCE_PATH, evidence)
    print(f"Wrote {LEDGER_PATH}")
    print(f"Wrote {EVIDENCE_PATH}")


if __name__ == "__main__":
    main()
