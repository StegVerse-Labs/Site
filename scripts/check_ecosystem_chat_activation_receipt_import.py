#!/usr/bin/env python3
"""Validate the automated adapter-to-Site activation evidence path."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(path: str, needles: tuple[str, ...]) -> list[str]:
    target = ROOT / path
    if not target.exists():
        return [f"missing:{path}"]
    text = target.read_text(encoding="utf-8")
    return [f"{path}:missing:{needle}" for needle in needles if needle not in text]


def main() -> int:
    failures: list[str] = []
    failures += require(
        "scripts/acquire_ecosystem_chat_live_activation_receipt.py",
        (
            "ecosystem-chat-live-activation.verified.json",
            "ecosystem-chat-live-activation-status.json",
            "pending_status_digest_mismatch",
            '"source_blockers"',
            '"source_gates"',
            "receipt_digest_mismatch",
            "provider_usage_custody",
            "transition_reconstructability",
            '"manual_user_action_required": False',
            '"authority_granted": False',
        ),
    )
    failures += require(
        "scripts/acquire_external_framework_catalog.py",
        (
            "acquire_ecosystem_chat_live_activation_receipt.py",
            "acquire_activation_receipt()",
            "adapter live activation receipt was rejected",
        ),
    )
    failures += require(
        "scripts/update_ecosystem_chat_activation_state.py",
        (
            "ecosystem-chat-destination-activation-receipt.json",
            "VERIFIED_SOURCE_RECEIPT_IMPORTED",
            '"master_records_custody"',
            '"reconstructability_pass"',
            '"legacy_destination_activation"',
        ),
    )
    if failures:
        for failure in failures:
            print(f"ECOSYSTEM_CHAT_ACTIVATION_RECEIPT_IMPORT_FAIL:{failure}")
        return 1
    print("ECOSYSTEM_CHAT_ACTIVATION_RECEIPT_IMPORT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
