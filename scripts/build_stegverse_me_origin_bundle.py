#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "stegverse.personal-origin.public-bundle/v1"
INLINE_MARKER = "/*__STEGVERSE_ME_RESOLVER_INLINE__*/"

SOURCES = {
    "node.html": ROOT / "stegos-node/stegverse-me-resolver.html",
    "services.html": ROOT / "stegos-node/stegverse-me-services-origin.html",
    "stegverse-me-opaque-resolver.js": ROOT / "stegos-node/stegverse-me-opaque-resolver.js",
    "services-state.js": ROOT / "stegos-node/services-state.js",
    "services.js": ROOT / "stegos-node/services.js",
    "kv-readiness-snapshot.json": ROOT / "stegos-node/kv-readiness-snapshot.json",
}


class BundleError(RuntimeError):
    pass


def sha256_uri(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def build_bundle(destination: Path) -> dict:
    destination = destination.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)

    root_source = (ROOT / "stegos-node/stegverse-me-origin-root.html").read_text(encoding="utf-8")
    resolver = SOURCES["stegverse-me-opaque-resolver.js"].read_text(encoding="utf-8")
    if INLINE_MARKER not in root_source:
        raise BundleError("origin root resolver inline marker missing")
    index_bytes = root_source.replace(INLINE_MARKER, resolver).encode("utf-8")
    (destination / "index.html").write_bytes(index_bytes)

    for logical, source in SOURCES.items():
        if not source.is_file() or source.is_symlink():
            raise BundleError(f"public source invalid: {source.relative_to(ROOT)}")
        shutil.copyfile(source, destination / logical)

    files = {}
    for logical in ("index.html", *SOURCES.keys()):
        path = destination / logical
        data = path.read_bytes()
        files[logical] = sha256_uri(data)

    manifest = {
        "schema": SCHEMA,
        "canonical_domain": "stegverse.me",
        "routes": ["/", "/n/{opaque_node}/", "/n/{opaque_node}/services.html"],
        "files": files,
        "private_kv_included": False,
        "raw_node_or_device_identifiers_included": False,
        "server_side_identity_registry_included": False,
        "credential_material_included": False,
        "dns_target_included": False,
        "authenticated_interlock_admission_performed": False,
        "authority_effect": "NONE",
        "activation_effect": False,
    }
    manifest_path = destination / "stegverse-me-origin-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = build_bundle(args.output)
    print("STEGVERSE_ME_ORIGIN_BUNDLE_PASS")
    print(f"FILE_COUNT={len(manifest['files'])}")
    print("PRIVATE_KV_INCLUDED=false")
    print("DNS_TARGET_INCLUDED=false")
    print("AUTHORITY_EFFECT=NONE")
    print("ACTIVATION_EFFECT=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
