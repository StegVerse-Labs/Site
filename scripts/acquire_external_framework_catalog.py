#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_OUT = ROOT / "data" / "external-framework-catalog.json"
RECEIPT_OUT = ROOT / "data" / "external-framework-catalog.receipt.json"
STATUS_OUT = ROOT / "data" / "external-framework-catalog-import-status.json"
ACTIVATION_IMPORTER = ROOT / "scripts" / "acquire_ecosystem_chat_live_activation_receipt.py"

DEFAULT_CATALOG_URL = "https://raw.githubusercontent.com/StegVerse-Labs/admissibility-wiki/main/docs/external-frameworks/external-chat-catalog.json"
DEFAULT_RECEIPT_URL = "https://raw.githubusercontent.com/StegVerse-Labs/admissibility-wiki/main/docs/external-frameworks/external-chat-catalog.receipt.json"


def canonical_bytes(payload: object) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def fetch_json(url: str) -> dict:
    outbound = urllib.request.Request(url, headers={"User-Agent": "StegVerse-Site-Catalog-Importer/1.0"})
    with urllib.request.urlopen(outbound, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def validate(catalog: dict, receipt: dict) -> None:
    if catalog.get("schema_version") != "1.0.0" or catalog.get("catalog_type") != "external_framework_compatibility_catalog":
        raise ValueError("catalog contract mismatch")
    frameworks = catalog.get("frameworks")
    if not isinstance(frameworks, list) or not frameworks:
        raise ValueError("catalog frameworks missing")
    ids = [item.get("framework_id") for item in frameworks]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("catalog framework IDs invalid or duplicated")
    digest = hashlib.sha256(canonical_bytes(catalog)).hexdigest()
    if receipt.get("receipt_type") != "external_framework_catalog_projection_receipt":
        raise ValueError("receipt type mismatch")
    if receipt.get("catalog_sha256") != digest:
        raise ValueError("catalog hash mismatch")
    if receipt.get("framework_count") != len(frameworks):
        raise ValueError("framework count mismatch")
    if receipt.get("projection_only") is not True:
        raise ValueError("catalog must remain projection-only")
    boundary = receipt.get("authority_boundary", {})
    for key in [
        "receipt_is_certification",
        "receipt_is_execution_authority",
        "receipt_is_publication_authority",
        "receipt_is_general_compatibility_proof",
    ]:
        if boundary.get(key) is not False:
            raise ValueError(f"authority boundary invalid: {key}")


def acquire_activation_receipt() -> None:
    result = subprocess.run(
        [sys.executable, str(ACTIVATION_IMPORTER)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(result.stdout, end="")
    if result.returncode != 0:
        raise RuntimeError("adapter live activation receipt was rejected")


def main() -> int:
    catalog_url = os.getenv("EXTERNAL_FRAMEWORK_CATALOG_URL", DEFAULT_CATALOG_URL)
    receipt_url = os.getenv("EXTERNAL_FRAMEWORK_CATALOG_RECEIPT_URL", DEFAULT_RECEIPT_URL)
    catalog_result = 0
    try:
        catalog = fetch_json(catalog_url)
        receipt = fetch_json(receipt_url)
        validate(catalog, receipt)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            catalog_tmp = temp / "catalog.json"
            receipt_tmp = temp / "receipt.json"
            catalog_tmp.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
            receipt_tmp.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
            CATALOG_OUT.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(catalog_tmp, CATALOG_OUT)
            shutil.copyfile(receipt_tmp, RECEIPT_OUT)
        status = {
            "schema_version": "1.0.0",
            "status_type": "external_framework_catalog_import_status",
            "state": "RECEIPTED_WIKI_CATALOG_IMPORTED",
            "source_catalog_url": catalog_url,
            "source_receipt_url": receipt_url,
            "catalog_sha256": receipt["catalog_sha256"],
            "framework_count": receipt["framework_count"],
            "hash_verified": True,
            "publication_authority": False,
            "certification_authority": False,
        }
        STATUS_OUT.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
        print(f"EXTERNAL FRAMEWORK CATALOG IMPORT: PASS ({receipt['framework_count']} frameworks)")
    except Exception as exc:
        status = {
            "schema_version": "1.0.0",
            "status_type": "external_framework_catalog_import_status",
            "state": "LOCAL_RECEIPTED_CATALOG_RETAINED",
            "hash_verified": False,
            "error": str(exc),
            "publication_authority": False,
            "certification_authority": False,
        }
        STATUS_OUT.parent.mkdir(parents=True, exist_ok=True)
        STATUS_OUT.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
        print(f"EXTERNAL FRAMEWORK CATALOG IMPORT: FALLBACK - {exc}")

    try:
        acquire_activation_receipt()
    except Exception as exc:
        print(f"ECOSYSTEM CHAT ACTIVATION RECEIPT IMPORT: FAIL - {exc}")
        catalog_result = 1
    return catalog_result


if __name__ == "__main__":
    raise SystemExit(main())
