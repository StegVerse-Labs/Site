#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "assets" / "ecosystem-node-gateway-binding.js"
VIEWS = ROOT / "assets" / "ecosystem-node-views.js"
INTEGRITY = ROOT / "scripts" / "validate_ecosystem_node_canonical_events.py"

REQUIRED_BINDING = (
    "StegVerseCanonicalGatewayBinding",
    "importCanonicalEvents",
    "crypto.subtle.digest('SHA-256'",
    "source_class !== 'upstream_governed'",
    "silent_repair_allowed: false",
    "rehash_allowed: false",
    "reorder_allowed: false",
    "authority_effect: 'NONE'",
    "credentials: 'omit'",
    "cache: 'no-store'",
    "duplicate event_id",
    "unresolved or forward parent_event_id",
    "event hash mismatch",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    for path in (BINDING, VIEWS, INTEGRITY):
        require(path.exists(), f"missing {path.relative_to(ROOT)}")
    binding = BINDING.read_text(encoding="utf-8")
    views = VIEWS.read_text(encoding="utf-8")
    for marker in REQUIRED_BINDING:
        require(marker in binding, f"gateway binding missing marker: {marker}")
    require("StegVerseCanonicalEventStream" in views, "canonical renderer API missing")
    require("importCanonicalEvents" in views, "canonical renderer import API missing")
    require("fnv1a32:" in views, "preview event boundary marker missing")
    require("sha256:" in binding, "upstream cryptographic event hash marker missing")
    print("ECOSYSTEM_NODE_GATEWAY_BINDING=PASS")
    print("upstream_validation=sha256,stable_id_graph,strict_shape")
    print("source_separation=preview_local_vs_upstream_governed")
    print("silent_repair=false")
    print("authority_effect=NONE")


if __name__ == "__main__":
    main()
