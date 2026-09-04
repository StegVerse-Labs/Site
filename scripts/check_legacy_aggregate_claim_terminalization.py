#!/usr/bin/env python3
"""Run the legacy aggregate claim terminalization adversarial suite."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "scripts" / "test_legacy_aggregate_claim_terminalization.py"


def main() -> int:
    result = subprocess.run([sys.executable, str(TEST)], cwd=ROOT, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    if result.returncode != 0:
        print("LEGACY_AGGREGATE_CLAIM_TERMINALIZATION_CHECK_FAIL")
        return 1
    print("LEGACY_AGGREGATE_CLAIM_TERMINALIZATION_CHECK_PASS authority_effect=NONE activation_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
