#!/usr/bin/env python3
"""Retain public 8374 discovery as historical, non-authorizing static evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import http.client
import json
from pathlib import Path
import re
import tempfile
import urllib.request

ORIGIN = "https://8374.stegverse.org"
DOCUMENTS = {"offer": ("/offer", "offer.json"),
             "openapi": ("/openapi.json", "openapi.json"),
             "x402": ("/.well-known/x402", "x402.json")}
SCHEMA = "stegverse.8374.discovery-mirror/v1"
WARNING = ("Historical public discovery snapshot, not current terms, endpoint health, "
           "a payment challenge or authorization. Obtain fresh authoritative terms "
           "from the live source before any paid request.")
LIMIT = 2 * 1024 * 1024
ROOT = Path(__file__).resolve().parents[1]
MIRROR = Path("0r10n15-8374/discovery")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def document(name: str, body: bytes) -> dict:
    value = json.loads(body.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{name}: expected a JSON object")
    if name == "offer" and value.get("document") != "OFFER__MACHINE__READABLE__01":
        raise ValueError("offer: unexpected document identity")
    if name == "openapi" and not str(value.get("openapi", "")).startswith("3."):
        raise ValueError("openapi: expected an OpenAPI 3 document")
    if name == "x402":
        resources = value.get("resources")
        if not isinstance(resources, list) or not resources or not all(isinstance(r, str) and r for r in resources):
            raise ValueError("x402: expected nonempty resource URLs")
    return value


def fetch_public(url: str) -> tuple[bytes, str, str]:
    req = urllib.request.Request(url, headers={"Accept": "application/json",
        "User-Agent": "StegVerse-Site-discovery-mirror/1"})
    with urllib.request.urlopen(req, timeout=20) as response:
        if response.status != 200:
            raise ValueError(f"source returned HTTP {response.status}")
        final_url = response.geturl()
        if final_url != url:
            raise ValueError("source redirect refused; review the canonical source URL")
        media_type = response.headers.get_content_type()
        if media_type != "application/json":
            raise ValueError(f"expected application/json, got {media_type}")
        body = response.read(LIMIT + 1)
        if len(body) > LIMIT:
            raise ValueError("source exceeds the 2 MiB discovery-document limit")
        return body, media_type, final_url


def generation_id(rows: list[dict]) -> str:
    identity = [{k: row[k] for k in ("name", "source_url", "bytes", "sha256")} for row in rows]
    return hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate(root: Path) -> dict:
    base = root / MIRROR
    manifest = json.loads((base / "current.json").read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("mirror manifest must be a JSON object")
    if (manifest.get("schema") != SCHEMA or manifest.get("authority_effect") != "NONE"
            or manifest.get("live_payment_authorization") is not False
            or manifest.get("evidence_class") != "HISTORICAL_PUBLIC_DISCOVERY_SNAPSHOT"
            or manifest.get("snapshot_warning") != WARNING):
        raise ValueError("mirror must retain its historical, non-authorizing classification")
    rows = manifest.get("documents")
    if (not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows)
            or [r.get("name") for r in rows] != list(DOCUMENTS)):
        raise ValueError("mirror must contain exactly offer, openapi and x402 in order")
    gen = manifest.get("generation")
    if not isinstance(gen, str) or re.fullmatch(r"[0-9a-f]{64}", gen) is None or generation_id(rows) != gen:
        raise ValueError("generation digest mismatch")
    for row in rows:
        name = row["name"]
        source, filename = DOCUMENTS[name]
        if (row.get("source_url") != ORIGIN + source or row.get("source_final_url") != ORIGIN + source
                or row.get("source_status") != 200 or row.get("source_content_type") != "application/json"
                or row.get("mirror_path") != f"generations/{gen}/{filename}"):
            raise ValueError(f"{name}: source or retained path mismatch")
        stamp = row.get("captured_at")
        if not isinstance(stamp, str) or not stamp.endswith("Z"):
            raise ValueError(f"{name}: missing UTC capture timestamp")
        datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        path = base / row["mirror_path"]
        if path.is_symlink() or not path.resolve().is_relative_to(base.resolve()):
            raise ValueError(f"{name}: retained path escapes the mirror")
        body = path.read_bytes()
        if len(body) != row.get("bytes") or hashlib.sha256(body).hexdigest() != row.get("sha256"):
            raise ValueError(f"{name}: captured body size/hash mismatch")
        document(name, body)
    return manifest


def capture(root: Path, fetch=fetch_public) -> dict:
    # Obtain and check the entire generation before touching retained evidence.
    rows, bodies = [], {}
    for name, (path, filename) in DOCUMENTS.items():
        url = ORIGIN + path
        body, media_type, final_url = fetch(url)
        if media_type != "application/json" or final_url != url or len(body) > LIMIT:
            raise ValueError(f"{name}: unexpected source response")
        document(name, body)
        bodies[filename] = body
        rows.append({"name": name, "source_url": url, "source_final_url": final_url,
                     "source_status": 200, "source_content_type": media_type,
                     "captured_at": utc_now(), "bytes": len(body),
                     "sha256": hashlib.sha256(body).hexdigest()})
    gen = generation_id(rows)
    for row in rows:
        row["mirror_path"] = f"generations/{gen}/{DOCUMENTS[row['name']][1]}"
    manifest = {"schema": SCHEMA, "evidence_class": "HISTORICAL_PUBLIC_DISCOVERY_SNAPSHOT",
                "authority_effect": "NONE", "live_payment_authorization": False,
                "snapshot_warning": WARNING, "generation": gen, "documents": rows}
    base = root / MIRROR
    base.mkdir(parents=True, exist_ok=True)
    parent = base / "generations"
    parent.mkdir(exist_ok=True)
    target = parent / gen
    if target.is_symlink() or parent.is_symlink() or (base / "current.json").is_symlink():
        raise ValueError("symlinked mirror publication paths refused")
    with tempfile.TemporaryDirectory(prefix=".capture-", dir=base) as tmp:
        staging = Path(tmp) / gen
        staging.mkdir()
        for filename, body in bodies.items():
            (staging / filename).write_bytes(body)
        if target.exists():
            if not target.is_dir() or any((target / n).is_symlink() or (target / n).read_bytes() != b for n, b in bodies.items()):
                raise ValueError("existing immutable generation differs from its digest")
        else:
            staging.rename(target)
        pointer = Path(tmp) / "current.json"
        pointer.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        # One pointer switches only after all immutable bodies are complete.
        pointer.replace(base / "current.json")
    return validate(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--capture", action="store_true", help="GET the three public source documents")
    mode.add_argument("--verify", action="store_true", help="verify retained evidence offline; no HTTP")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        result = capture(args.root) if args.capture else validate(args.root)
    except (OSError, ValueError, KeyError, TypeError, http.client.HTTPException) as exc:
        print(json.dumps({"failure_code": "DISCOVERY_MIRROR_CAPTURE_OR_VALIDATION_FAILED",
            "failed_predicate": str(exc),
            "required_evidence_or_repair": "Restore the last complete mirror or review and recapture the three public source documents.",
            "retry_entrypoint": "scripts/capture_8374_discovery_mirrors.py --capture, then --verify",
            "owning_existing_goal": "BUILD-Q-54 ecosystem leg; native binding UNBOUND",
            "next_attempt": "After source/publication-path repair; do not use a snapshot for a paid request."}, indent=2))
        return 1
    print(json.dumps({"status": "PASS", "generation": result["generation"], "documents": 3,
        "evidence_class": result["evidence_class"], "live_payment_authorization": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
