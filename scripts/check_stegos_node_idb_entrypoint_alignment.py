#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPAT_NAMES = (
    "assets/stegos-node-idb-schema-compat.js",
    "../assets/stegos-node-idb-schema-compat.js",
    "./../assets/stegos-node-idb-schema-compat.js",
)
OPENERS = (
    "stegverse-node-continuity.js",
    "stegos-node.js",
    "device-kv-intr-sync.js",
    "hil-intr-sync.js",
    "stegos-bootstrap.js",
    "sv001-native-resident-activation.js",
    "services.js",
)

failures = []
checked = 0
for path in sorted(ROOT.rglob("*.html")):
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    positions = [(name, text.find(name)) for name in OPENERS if text.find(name) >= 0]
    if not positions:
        continue
    checked += 1
    first_opener = min(pos for _, pos in positions)
    compat_positions = [text.find(name) for name in COMPAT_NAMES if text.find(name) >= 0]
    if not compat_positions:
        failures.append(f"{rel}: missing canonical Node IndexedDB compatibility loader before opener(s) {','.join(name for name, _ in positions)}")
        continue
    first_compat = min(compat_positions)
    if first_compat > first_opener:
        failures.append(f"{rel}: compatibility loader appears after first stegos-node-v1 opener")

if failures:
    print("STEGOS_NODE_IDB_ENTRYPOINT_ALIGNMENT_FAIL")
    for failure in failures:
        print(failure)
    raise SystemExit(1)

if checked < 1:
    raise SystemExit("STEGOS_NODE_IDB_ENTRYPOINT_ALIGNMENT_FAIL: no runtime entrypoints discovered")
print(f"STEGOS_NODE_IDB_ENTRYPOINT_ALIGNMENT_PASS entrypoints={checked}")
