"""
TVC Ingestion Dependency Gate
==============================
Called by bundle_ingest.py when a bundle's manifest declares
a runtime_package dependency.

Calls tvc.ingestion.dependency.gate.stegentity before allowing
installation of any bundle that depends on the StegEntity runtime.

Integration point in bundle_ingest.py:

    from tools.tvc_ingestion_gate import check_runtime_dependency

    # After classify_bundle returns ALLOW, before file installation:
    runtime_pkg = manifest.get("bundle_manifest", {}).get("runtime_package")
    if runtime_pkg:
        gate_result = check_runtime_dependency(runtime_pkg)
        if gate_result["decision"] != "ALLOW":
            return gate_result["decision"], gate_result["basis"]

Usage:
    from tools.tvc_ingestion_gate import check_runtime_dependency
    result = check_runtime_dependency("stegentity")
    # result["decision"]: ALLOW | DENY | FAIL_CLOSED | SANDBOX
    # result["basis"]: human-readable reason
    # result["tvc_status"]: ok | tvc_not_found | lifecycle_denied | ...
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


# TVC task that gates ingestion dependencies
TVC_GATE_TASK = "tvc.ingestion.dependency.gate.stegentity"

# Known task → package mapping (extend as more packages are registered)
PACKAGE_GATE_TASKS: dict[str, str] = {
    "stegentity": "tvc.ingestion.dependency.gate.stegentity",
}

# Lifecycle decision → ingestion decision mapping
# Mirrors TVC lifecycle enforcement table
LIFECYCLE_TO_INGESTION: dict[str, str] = {
    "ALLOW":       "ALLOW",
    "SANDBOX":     "SANDBOX",
    "DENY":        "DENY",
    "FAIL_CLOSED": "FAIL_CLOSED",
}


def find_tvc_dispatcher() -> Path | None:
    candidates = []
    env_root = os.environ.get("TVC_ROOT", "")
    if env_root:
        candidates.append(Path(env_root) / "tools" / "task_dispatcher.py")
    for rel in ["../TVC", "../../TVC", "TVC"]:
        candidates.append(Path(rel) / "tools" / "task_dispatcher.py")
    return next((p for p in candidates if p.exists()), None)


def check_runtime_dependency(package: str) -> dict:
    """
    Gate a runtime dependency through TVC package registry.

    Returns:
        decision: ALLOW | DENY | FAIL_CLOSED | SANDBOX | SKIP_NO_TVC
        basis:    human-readable reason
        tvc_status: ok | tvc_not_found | task_failed | ...
    """
    task = PACKAGE_GATE_TASKS.get(package)
    if not task:
        # Unknown package — fail closed
        return {
            "decision": "FAIL_CLOSED",
            "basis": f"Runtime package '{package}' not in TVC registry gate map.",
            "tvc_status": "unknown_package",
            "package": package,
        }

    dispatcher = find_tvc_dispatcher()
    if not dispatcher:
        # TVC not available — skip gate, log warning
        # Not a hard failure: bundle_ingest can continue but should note this
        return {
            "decision": "SKIP_NO_TVC",
            "basis": (
                f"TVC dispatcher not found. "
                f"Dependency gate for '{package}' skipped. "
                f"Set TVC_ROOT for full governance."
            ),
            "tvc_status": "tvc_not_found",
            "package": package,
        }

    try:
        proc = subprocess.run(
            [sys.executable, str(dispatcher), task],
            capture_output=True, text=True, timeout=60,
            cwd=str(dispatcher.parent.parent),
        )
    except subprocess.TimeoutExpired:
        return {
            "decision": "FAIL_CLOSED",
            "basis": f"TVC dependency gate task '{task}' timed out.",
            "tvc_status": "tvc_timeout",
            "package": package,
        }
    except Exception as e:
        return {
            "decision": "FAIL_CLOSED",
            "basis": f"TVC dependency gate error: {e}",
            "tvc_status": "tvc_error",
            "package": package,
        }

    if proc.returncode != 0:
        return {
            "decision": "FAIL_CLOSED",
            "basis": f"TVC gate task exited {proc.returncode}: {proc.stderr[:200]}",
            "tvc_status": "task_failed",
            "package": package,
        }

    try:
        dispatch = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {
            "decision": "FAIL_CLOSED",
            "basis": "TVC gate task output was not valid JSON.",
            "tvc_status": "parse_error",
            "package": package,
        }

    if dispatch.get("status") != "ok":
        return {
            "decision": "FAIL_CLOSED",
            "basis": f"TVC gate task status: {dispatch.get('status')}",
            "tvc_status": dispatch.get("status", "unknown"),
            "package": package,
        }

    result = dispatch.get("result", {})
    # The gate task returns a decision field
    gate_decision = result.get("decision", result.get("gate_decision", ""))
    ingestion_decision = LIFECYCLE_TO_INGESTION.get(gate_decision, "FAIL_CLOSED")

    return {
        "decision": ingestion_decision,
        "basis": (
            f"TVC dependency gate for '{package}': "
            f"lifecycle={gate_decision} → ingestion={ingestion_decision}"
        ),
        "tvc_status": "ok",
        "package": package,
        "gate_decision": gate_decision,
        "gate_result": result,
    }


def gate_bundle_dependencies(bundle_manifest: dict) -> dict:
    """
    Check all runtime dependencies declared in a bundle manifest.
    Returns combined result: ALLOW only if all dependencies pass.

    Usage in bundle_ingest.py:
        from tools.tvc_ingestion_gate import gate_bundle_dependencies
        gate = gate_bundle_dependencies(manifest)
        if gate["decision"] != "ALLOW":
            return gate["decision"], gate["basis"]
    """
    # Check bundle-manifest.json format
    runtime_pkg = bundle_manifest.get("runtime_package")
    if not runtime_pkg:
        # Also check nested structures
        deps = bundle_manifest.get("dependencies", {})
        runtime_pkg = deps.get("runtime_package")

    if not runtime_pkg:
        return {
            "decision": "ALLOW",
            "basis": "No runtime_package dependency declared.",
            "tvc_status": "no_dependency",
        }

    result = check_runtime_dependency(runtime_pkg)

    # SKIP_NO_TVC is treated as ALLOW with a warning — not a hard block
    if result["decision"] == "SKIP_NO_TVC":
        return {
            "decision": "ALLOW",
            "basis": result["basis"],
            "tvc_status": "tvc_not_found",
            "warning": "TVC not available — dependency gate skipped",
        }

    return result
