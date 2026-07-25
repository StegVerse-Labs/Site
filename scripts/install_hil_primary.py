#!/usr/bin/env python3
"""Install the approved HIL Primary PDF only when its exact identity matches.

The script is deliberately fail-closed. It accepts either the original PDF bytes
or a base64 text file, verifies the fixed approved size and SHA-256, writes the
canonical repository artifact, updates the experiment manifest, and emits an
installation receipt. No state changes occur unless every check passes.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_SIZE = 109_210
EXPECTED_SHA256 = "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946"
ARTIFACT_PATH = Path("data/hil-primary-v0.5-review.pdf.b64")
MANIFEST_PATH = Path("data/hil-experiment.json")
RECEIPT_PATH = Path("data/hil-primary-v0.5-installation-receipt.json")


def _decode_input(path: Path) -> bytes:
    raw = path.read_bytes()
    if raw.startswith(b"%PDF-"):
        return raw
    try:
        compact = b"".join(raw.split())
        decoded = base64.b64decode(compact, validate=True)
    except Exception as exc:  # noqa: BLE001 - convert all decoding failures to one boundary error
        raise SystemExit(f"input is neither a PDF nor valid base64: {exc}") from exc
    if not decoded.startswith(b"%PDF-"):
        raise SystemExit("decoded input does not begin with a PDF signature")
    return decoded


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        handle.write(data)
        temp_name = handle.name
    os.replace(temp_name, path)


def _encode_wrapped(data: bytes) -> bytes:
    encoded = base64.b64encode(data).decode("ascii")
    return ("\n".join(encoded[index:index + 76] for index in range(0, len(encoded), 76)) + "\n").encode("ascii")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="approved v0.5 PDF or its base64 representation")
    parser.add_argument("--verify-only", action="store_true", help="verify identity without writing repository state")
    args = parser.parse_args()

    payload = _decode_input(args.source)
    digest = hashlib.sha256(payload).hexdigest()
    if len(payload) != EXPECTED_SIZE:
        raise SystemExit(f"size mismatch: expected {EXPECTED_SIZE}, received {len(payload)}")
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"SHA-256 mismatch: expected {EXPECTED_SHA256}, received {digest}")

    if args.verify_only:
        print(json.dumps({"state": "VERIFIED", "size_bytes": len(payload), "sha256": digest}, indent=2))
        return 0

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    primary = manifest["primary_document"]
    if primary.get("sha256") != EXPECTED_SHA256:
        raise SystemExit("manifest Primary SHA-256 does not match the approved artifact")
    if primary.get("artifact_path") != str(ARTIFACT_PATH):
        raise SystemExit("manifest Primary artifact path does not match the canonical installation path")

    installed_at = datetime.now(timezone.utc).isoformat()
    primary["artifact_state"] = "VERIFIED"
    primary["canonical_state"] = "APPROVED_CONTENT_ARTIFACT_FROZEN"
    primary["size_bytes"] = len(payload)
    primary["verified_at"] = installed_at
    manifest["status"] = "APPROVED_PENDING_DEPLOYED_CONTROLLED_CYCLE"

    receipt = {
        "schema_version": "HIL-PRIMARY-INSTALLATION-RECEIPT-v1",
        "experiment_id": manifest.get("experiment_id"),
        "primary_version": primary.get("version"),
        "artifact_path": str(ARTIFACT_PATH),
        "size_bytes": len(payload),
        "sha256": digest,
        "installed_at": installed_at,
        "artifact_state": "VERIFIED",
        "content_substitution": False,
        "deployment_authority": False,
        "publication_authority": False,
        "master_record_append_authority": False,
    }

    _atomic_write(ARTIFACT_PATH, _encode_wrapped(payload))
    _atomic_write(MANIFEST_PATH, (json.dumps(manifest, indent=2) + "\n").encode("utf-8"))
    _atomic_write(RECEIPT_PATH, (json.dumps(receipt, indent=2) + "\n").encode("utf-8"))

    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
