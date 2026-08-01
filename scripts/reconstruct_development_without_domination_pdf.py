#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
from pathlib import Path

ROOT = Path("papers/development-without-domination")
PARTS = ROOT / ".pdf-parts"
OUTPUT = ROOT / "Development_Without_Domination_Rigel_Randolph_Final.pdf"
EXPECTED = "c2fcb0ce76f5eaba1a6dd4ccdd358fcae29b32b3110767b5f2b5b2ffa347c29d"
EXPECTED_PARTS = [PARTS / f"part-{index:04d}.b64" for index in range(1, 5)]


def main() -> int:
    missing = [str(path) for path in EXPECTED_PARTS if not path.exists()]
    if missing:
        print("PDF_RECONSTRUCTION_PENDING")
        for path in missing:
            print(path)
        return 2

    encoded = "".join(path.read_text(encoding="ascii").strip() for path in EXPECTED_PARTS)
    payload = base64.b64decode(encoded, validate=True)
    observed = hashlib.sha256(payload).hexdigest()
    if observed != EXPECTED:
        print(f"PDF_HASH_MISMATCH observed={observed} expected={EXPECTED}")
        return 3

    OUTPUT.write_bytes(payload)
    print(f"PDF_RECONSTRUCTED path={OUTPUT} sha256={observed} bytes={len(payload)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
