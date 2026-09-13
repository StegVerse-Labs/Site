#!/usr/bin/env python3
"""Validate the reusable resident-rendezvous browser profile deterministically."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "tests" / "resident-rendezvous-gadi-profile.test.cjs"
CLIENT = ROOT / "assets" / "kv-ui" / "resident-rendezvous-client.js"


def main() -> int:
    if not CLIENT.is_file() or not TEST.is_file():
        print("REUSABLE_RESIDENT_RENDEZVOUS_SITE_PROFILE_FAIL: missing client or test")
        return 1
    node = shutil.which("node")
    if not node:
        print("REUSABLE_RESIDENT_RENDEZVOUS_SITE_PROFILE_FAIL: node unavailable")
        return 1
    completed = subprocess.run(
        [node, "--test", str(TEST.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        print("REUSABLE_RESIDENT_RENDEZVOUS_SITE_PROFILE_FAIL")
        print(completed.stdout.rstrip())
        return completed.returncode
    print("REUSABLE_RESIDENT_RENDEZVOUS_SITE_PROFILE_PASS")
    print("USER_VERIFICATION_AUTHORITY=KV/SKAP Vault")
    print("TARGET_NODE_IDENTITY_ROLE=ROUTING_ONLY")
    print("RUNTIME_EVIDENCE_EFFECT=NONE_SOURCE_VALIDATION_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
