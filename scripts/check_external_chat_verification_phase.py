#!/usr/bin/env python3
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLICATION = ROOT / "scripts" / "check_ecosystem_chat_application.py"
WORKFLOW = ROOT / ".github" / "workflows" / "site-task-runner.yml"
LIVE_CHECK = "scripts/check_external_chat_live_routes.py"


def fail(message: str) -> int:
    print(f"EXTERNAL CHAT VERIFICATION PHASE: FAIL - {message}")
    return 1


def declares_post_deployment(application: str) -> bool:
    """Confirm the application result declares POST_DEPLOYMENT independent of formatting."""
    try:
        tree = ast.parse(application)
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        pairs = {}
        for key, value in zip(node.keys, node.values):
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                if isinstance(value, ast.Constant):
                    pairs[key.value] = value.value
        if pairs.get("live_route_verification_phase") == "POST_DEPLOYMENT":
            return True
    return False


def main() -> int:
    for path in (APPLICATION, WORKFLOW):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    application = APPLICATION.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    command_section = application.split("COMMANDS:", 1)[-1].split("def execute", 1)[0]
    if LIVE_CHECK in command_section:
        return fail("live-route check must not run in pre-deployment application COMMANDS")
    if not declares_post_deployment(application):
        return fail("application result must declare POST_DEPLOYMENT live verification")

    required_workflow_markers = [
        "Deploy Pages",
        "Verify External Chat public surfaces",
        "python scripts/check_external_chat_live_routes.py",
        "Upload External Chat live verification receipt",
        "site/reports/external-chat-live-verification.json",
        "if: always()",
        "Mutation required disabled",
    ]
    for marker in required_workflow_markers:
        if marker not in workflow:
            return fail(f"workflow missing marker: {marker}")

    if workflow.index("Verify External Chat public surfaces") < workflow.index("Deploy Pages"):
        return fail("External Chat live verification must follow Pages deployment")
    if workflow.index("Upload External Chat live verification receipt") < workflow.index("Verify External Chat public surfaces"):
        return fail("live receipt upload must follow live verification")

    print("EXTERNAL CHAT VERIFICATION PHASE: PASS (local checks pre-deploy; live checks post-deploy)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
