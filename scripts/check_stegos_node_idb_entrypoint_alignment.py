#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPAT = "/assets/stegos-node-idb-schema-compat.js?v=20260911-v3"

WRAPPER_CONTRACTS = {
    "assets/stegverse-node-continuity.js": "/assets/stegverse-node-continuity-impl.js?v=20260911-v3",
    "stegos-node/stegos-node.js": "/stegos-node/stegos-node-impl.js?v=20260911-v3",
    "stegos-bootstrap/stegos-bootstrap.js": "/stegos-bootstrap/stegos-bootstrap-impl.js?v=20260911-v3",
    "stegos-bootstrap/sv001-native-resident-activation.js": "/stegos-bootstrap/sv001-native-resident-activation-impl.js?v=20260911-v3",
}

NATIVE_CANONICAL_OPENERS = {
    "stegos-node/services.js": ("var DB_VERSION = 3;", "intr_outbox"),
}

HELPER_OPENERS = {
    "stegos-node/device-kv-intr-sync.js",
    "stegos-node/hil-intr-sync.js",
}


def die(message):
    print("STEGOS_NODE_IDB_ENTRYPOINT_ALIGNMENT_FAIL")
    print(message)
    raise SystemExit(1)


def validate_wrapper(path, impl):
    text = (ROOT / path).read_text(encoding="utf-8")
    required = [
        'root.document.readyState!=="loading"',
        "STEGOS_NODE_SCHEMA_BOOTSTRAP_REQUIRES_PARSER_LOAD",
        COMPAT,
        impl,
        "document.write",
    ]
    missing = [marker for marker in required if marker not in text]
    if missing:
        die(f"{path}: malformed canonical compatibility bootstrap: {missing}")
    impl_path = impl.split("?", 1)[0].lstrip("/")
    if not (ROOT / impl_path).is_file():
        die(f"{path}: preserved implementation target missing: {impl_path}")


def validate_native(path, markers):
    text = (ROOT / path).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    if missing:
        die(f"{path}: native canonical opener missing markers: {missing}")


for path, impl in WRAPPER_CONTRACTS.items():
    validate_wrapper(path, impl)
for path, markers in NATIVE_CANONICAL_OPENERS.items():
    validate_native(path, markers)

safe_first = set(WRAPPER_CONTRACTS) | set(NATIVE_CANONICAL_OPENERS)
all_openers = safe_first | HELPER_OPENERS
failures = []
checked = 0

for html_path in sorted(ROOT.rglob("*.html")):
    rel = html_path.relative_to(ROOT).as_posix()
    text = html_path.read_text(encoding="utf-8")
    found = []
    for opener in all_openers:
        basename = Path(opener).name
        pos = text.find(basename)
        if pos >= 0:
            found.append((pos, opener))
    if not found:
        continue
    checked += 1
    found.sort()
    first = found[0][1]
    if first not in safe_first:
        failures.append(f"{rel}: first shared Node DB opener is not migration-safe: {first}")

if failures:
    die("\n".join(failures))
if checked < 1:
    die("no runtime entrypoints discovered")

print(
    f"STEGOS_NODE_IDB_ENTRYPOINT_ALIGNMENT_PASS entrypoints={checked} "
    "canonical bootstrap/native opener precedes all shared Node DB helper opens"
)
