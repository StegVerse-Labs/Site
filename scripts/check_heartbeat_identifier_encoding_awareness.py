#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "heartbeat-identifier-encoding-awareness.json"


def main() -> int:
    failures = []
    if not STATE.is_file():
        print("HEARTBEAT_IDENTIFIER_AWARENESS_FAIL:missing state")
        return 1
    state = json.loads(STATE.read_text(encoding="utf-8"))
    expected = {
        "encoding": "FIXED_WIDTH_BASE36",
        "prefix": "HB-",
        "width": 8,
        "alphabet": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "display_format": "HB-XXXXXXXX",
        "anchor_epoch": 32,
        "anchor_heartbeat_id": "HB-0000000W",
        "integer_epoch_remains_canonical": True,
        "reversible": True,
        "historical_decimal_labels_remain_valid": True,
        "period_ms": 10,
        "reference_rate_hz": 100,
        "progression_dependency": "OSCILLATOR_ONLY",
        "identifier_encoding_changes_progression": False,
        "authority_effect": "NONE",
        "credential_authority": "TV/TVC",
        "github_runtime_authority": "NONE",
    }
    for key, value in expected.items():
        if state.get(key) != value:
            failures.append(f"{key} must equal {value!r}")
    if failures:
        for failure in failures:
            print("HEARTBEAT_IDENTIFIER_AWARENESS_FAIL:" + failure)
        return 1
    print("HEARTBEAT_IDENTIFIER_AWARENESS_PASS:HB-XXXXXXXX:BASE36:WIDTH8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
