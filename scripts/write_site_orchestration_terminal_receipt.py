#!/usr/bin/env python3
"""Write a fail-closed terminal receipt for one Site orchestration transition."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "site-orchestration-terminal-receipt.json"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def normalized_status(value: str, *, success: set[str]) -> str:
    cleaned = value.strip().upper()
    if not cleaned:
        return "NOT_OBSERVED"
    return "PASS" if cleaned in success else "FAIL"


def main() -> int:
    task = load_json(ROOT / "reports" / "site-task-diagnostic.json")
    live = load_json(ROOT / "reports" / "external-chat-live-verification.json")
    activation = load_json(ROOT / "reports" / "external-chat-activation-evidence.json")

    source = env("STEGVERSE_ORCHESTRATION_SOURCE", "unknown")
    source_run_id = env("STEGVERSE_ORCHESTRATION_SOURCE_RUN_ID")
    transition_sha = env("STEGVERSE_ORCHESTRATION_SHA")
    current_run_id = env("GITHUB_RUN_ID")
    current_attempt = env("GITHUB_RUN_ATTEMPT", "1")
    event_name = env("GITHUB_EVENT_NAME")

    task_state = normalized_status(str(task.get("status", "")), success={"PASS", "PASSED", "SUCCESS"})
    mutation_state = normalized_status(env("STEGVERSE_GENERATED_STATE_RESULT"), success={"PASS", "SUCCESS", "UNCHANGED", "COMMITTED"})
    deployment_result = env("STEGVERSE_PAGES_DEPLOYMENT_RESULT")
    deployment_state = (
        "NOT_OWNED_BY_TASK_RUNNER"
        if deployment_result.upper() == "NOT_OWNED_BY_TASK_RUNNER"
        else normalized_status(deployment_result, success={"PASS", "SUCCESS"})
    )
    live_state = normalized_status(str(live.get("result", "")), success={"PASS", "PASSED", "SUCCESS", "VERIFIED"})

    orchestrated = event_name == "workflow_run" and source == "site-bootstrap-validate"
    required_states = [task_state, mutation_state, live_state]
    if orchestrated and all(state == "PASS" for state in required_states):
        terminal_state = "COMPLETED"
    elif orchestrated and any(state == "FAIL" for state in required_states):
        terminal_state = "FAILED"
    elif orchestrated:
        terminal_state = "INCOMPLETE_EVIDENCE"
    else:
        terminal_state = "VALIDATION_ONLY"

    payload = {
        "schema": "stegverse.site.orchestration-terminal-receipt.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "transition": {
            "source": source,
            "source_run_id": source_run_id or None,
            "validated_commit_sha": transition_sha or None,
            "worker_run_id": current_run_id or None,
            "worker_run_attempt": current_attempt,
            "event_name": event_name or None,
        },
        "stages": {
            "site_task": {
                "state": task_state,
                "failed_validator": task.get("failed_validator"),
                "failure_class": task.get("failure_class"),
                "exit_code": task.get("exit_code"),
            },
            "generated_state_mutation": {"state": mutation_state},
            "pages_deployment": {
                "state": deployment_state,
                "owner": "NATIVE_GITHUB_PAGES_WORKFLOW",
                "task_runner_deployment_authority": False,
            },
            "live_route_verification": {
                "state": live_state,
                "failure_class": live.get("failure_class"),
            },
            "activation_evidence": {
                "result": activation.get("result", "NOT_OBSERVED"),
                "evidence_sha256": activation.get("evidence_sha256"),
            },
        },
        "supersession": {
            "policy": "CANCEL_IN_PROGRESS",
            "superseded": env("STEGVERSE_TRANSITION_SUPERSEDED", "false").lower() == "true",
        },
        "terminal_state": terminal_state,
        "authority_effect": "NONE",
        "boundaries": [
            "workflow completion is not activation authority",
            "native GitHub Pages workflow is sole github-pages deployment owner",
            "Site Task Runner has no github-pages deployment authority",
            "terminal receipt is not custody",
            "terminal receipt is not downstream mutation authority",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"SITE ORCHESTRATION TERMINAL RECEIPT: {terminal_state}")
    print(f"receipt={REPORT.relative_to(ROOT)}")
    print(f"receipt_sha256={payload['receipt_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
