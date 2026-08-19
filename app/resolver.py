"""Site-side TV/TVC authority resolver.

This module deliberately does not return credential values to Site consumers.
Private source materialization and mutation authority belong to TV/TVC-owned
execution surfaces.  Site may resolve non-secret capability metadata and emit
secret-free blocked/dry-run receipts only.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any


class CredentialExportProhibited(RuntimeError):
    """Raised when a Site consumer attempts to obtain raw credential material."""


def stegtvc_resolve(*, use_case: str, module: str) -> dict[str, Any]:
    """Resolve non-secret authority metadata without minting or exporting a token."""
    operation = str(use_case or "").strip()
    consumer = str(module or "").strip()
    if not operation or not consumer:
        raise ValueError("use_case and module are required")

    capability = (
        "tvc.private-source-read.v1"
        if operation in {"github-read", "private-source-read"}
        else "SEPARATE_TV_TVC_MUTATION_CAPABILITY_REQUIRED"
    )
    return {
        "resolution": "BOUNDARY_RESOLVED",
        "credential_authority": "TV/TVC",
        "consumer_repository": "StegVerse-Labs/Site",
        "consumer_module": consumer,
        "use_case": operation,
        "provider": "TVC_BOUNDARY",
        "capability": capability,
        "consumer_credential_export_allowed": False,
        "github_generated_credential_substitution_allowed": False,
        "non_tv_tvc_credential_allowed": False,
        "mutation_authority": False,
    }


def stegtvc_resolve_credential(*, use_case: str, module: str) -> str:
    """Fail closed: Site consumers may never receive raw TV/TVC credential values."""
    metadata = stegtvc_resolve(use_case=use_case, module=module)
    raise CredentialExportProhibited(
        "consumer credential export prohibited; execute the operation inside an "
        f"admitted TV/TVC boundary ({metadata['capability']})"
    )


def stegtvc_emit_resolution_receipt(
    *,
    use_case: str,
    module: str,
    resolved: dict[str, Any],
    credential_resolved: bool,
    gcat_decision: str | None = None,
) -> dict[str, Any]:
    """Emit only non-secret boundary evidence."""
    body = {
        "schema": "stegverse.tvc_resolution_receipt.v2",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "credential_authority": "TV/TVC",
        "consumer_repository": "StegVerse-Labs/Site",
        "module": module,
        "use_case": use_case,
        "capability": resolved.get("capability"),
        "resolution": "BLOCKED" if credential_resolved else "BOUNDARY_RESOLVED",
        "credential_value_exposed": False,
        "consumer_credential_export_allowed": False,
        "mutation_authority": False,
        "gcat_decision": gcat_decision,
    }
    body["receipt_hash"] = "sha256:" + sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return body


# Compatibility export used by stegtvc_client.py.
stegtvc_resolve = stegtvc_resolve
