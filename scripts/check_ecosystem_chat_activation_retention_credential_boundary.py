#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Consolidation visibility trigger: no semantic or authority effect.
WORKFLOW = ROOT / ".github/workflows/ecosystem-chat-activation-retention.yml"
IMPORTER = ROOT / "scripts/import_ecosystem_chat_external_activation_states.py"


def require(value: bool, code: str) -> None:
    if not value:
        raise SystemExit(f"ECOSYSTEM_CHAT_ACTIVATION_RETENTION_CREDENTIAL_FAIL:{code}")


def main() -> int:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    importer = IMPORTER.read_text(encoding="utf-8")

    for forbidden in (
        "STEGVERSE_REPO_SYNC_TOKEN",
        "secrets.STEGVERSE_REPO_SYNC_TOKEN",
    ):
        require(forbidden not in workflow, f"workflow_forbidden:{forbidden}")
        require(forbidden not in importer, f"importer_forbidden:{forbidden}")

    for forbidden in (
        'headers["Authorization"]',
        "Bearer {token}",
        "github_contents=True",
        "os.getenv(",
    ):
        require(forbidden not in importer, f"importer_credential_path:{forbidden}")

    for required in (
        "https://raw.githubusercontent.com/StegVerse-org/LLM-adapter/main/reports/ecosystem-chat-destination-activation-state.json",
        "https://raw.githubusercontent.com/master-records/orchestration/main/reports/ecosystem-chat-custody-activation-state.json",
        '"ecosystem_chat_destination_activation_state"',
        '"ecosystem_chat_custody_activation_state"',
        "canonical_sha256",
        "manual_user_action_required",
        '"gates"',
    ):
        require(required in importer, f"importer_required:{required}")

    for required in (
        'cron: "11 * * * *"',
        "workflow_run:",
        "workflow_dispatch:",
        "scripts/import_ecosystem_chat_external_activation_states.py",
        "scripts/check_ecosystem_chat_activation_retention_credential_boundary.py",
    ):
        require(required in workflow, f"workflow_required:{required}")


    # GitHub Actions is validation-only: no repository/runtime persistence authority.
    for forbidden in (
        "contents: write",
        "actions: write",
        "github-token:",
        "secrets.",
        "git push",
        "git commit",
        "actions/download-artifact@",
        "acquire_ecosystem_chat_live_activation_receipt.py",
        "import_ecosystem_chat_external_activation_states.py\n",
        "update_ecosystem_chat_activation_state.py",
    ):
        require(forbidden not in workflow, f"workflow_runtime_persistence_forbidden:{forbidden}")
    for required in (
        "permissions:\n  contents: read",
        "persist-credentials: false",
        "Validate activation-retention credential boundary",
        "Validate activation-receipt import source contract",
        "Validate checked-in activation-state consistency without mutation",
    ):
        require(required in workflow, f"workflow_validation_only_required:{required}")

    print("ECOSYSTEM_CHAT_ACTIVATION_RETENTION_CREDENTIAL_PASS:TV_TVC_ONLY_VALIDATION_NO_GITHUB_PERSISTENCE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
