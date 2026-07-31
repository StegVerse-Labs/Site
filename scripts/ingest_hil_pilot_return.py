#!/usr/bin/env python3
"""Verify an unchanged HIL response PDF and package; emit a non-custodial managed acknowledgment."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

PRIMARY = ("v1.1", "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462")
PROMPT = ("HIL-PROMPT-v1.1", "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value: dict) -> str:
    copy = dict(value)
    claimed = copy.pop("package_sha256", None)
    computed = digest(json.dumps(copy, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())
    if claimed and claimed != computed:
        raise ValueError(f"package canonical hash mismatch: claimed {claimed}, computed {computed}")
    return computed


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("package", type=Path)
    parser.add_argument("--local-receipt", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    pdf = args.pdf.read_bytes()
    package = json.loads(args.package.read_text(encoding="utf-8"))
    require(pdf.startswith(b"%PDF-"), "invalid PDF signature")
    pdf_hash = digest(pdf)
    require(package.get("response_pdf_sha256") == pdf_hash, "response PDF SHA-256 mismatch")
    require(package.get("response_pdf_size") == len(pdf), "response PDF size mismatch")
    require((package.get("canonical_paper_version"), package.get("canonical_paper_sha256")) == PRIMARY, "canonical paper identity mismatch")
    require((package.get("prompt_version"), package.get("prompt_sha256")) == PROMPT, "prompt identity mismatch")
    package_hash = canonical_hash(package)

    if args.local_receipt:
        receipt = json.loads(args.local_receipt.read_text(encoding="utf-8"))
        require(receipt.get("response_pdf_sha256") == pdf_hash, "local receipt PDF hash mismatch")
        require(receipt.get("package_sha256") == package_hash, "local receipt package hash mismatch")

    token = pdf_hash[:16].upper()
    acknowledgment = {
        "schema_version": "HIL-MANAGED-RECEIVING-ACKNOWLEDGMENT-v1",
        "acknowledgment_id": f"HIL-MRA-{token}",
        "acknowledged_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "return_mode": "PARTICIPANT_MANAGED_DIRECT_RETURN",
        "response_pdf": {"filename": args.pdf.name, "sha256": pdf_hash, "size_bytes": len(pdf)},
        "package": {"filename": args.package.name, "sha256": package_hash, "size_bytes": args.package.stat().st_size},
        "canonical_primary": {"version": PRIMARY[0], "sha256": PRIMARY[1]},
        "canonical_prompt": {"version": PROMPT[0], "sha256": PROMPT[1]},
        "verification": {"pdf_signature_valid": True, "pdf_sha256_valid": True, "pdf_size_valid": True, "package_canonical_hash_valid": True, "paper_identity_valid": True, "prompt_identity_valid": True},
        "custody_status": "MANAGED_RETURN_PRESERVED_NO_GOVERNED_CUSTODY",
        "registry_status": "NOT_REGISTERED", "review_status": "NOT_REVIEWED", "publication_status": "NOT_PUBLISHED",
        "claims_withheld": ["governed_receiver_custody", "registry_commit", "private_review_acceptance", "publication", "master_record_release"],
        "authority_effect": False,
    }
    args.output.write_text(json.dumps(acknowledgment, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status":"VERIFIED_MANAGED_RETURN","acknowledgment":str(args.output),"pdf_sha256":pdf_hash,"package_sha256":package_hash}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
