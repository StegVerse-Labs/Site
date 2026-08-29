#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECT = ROOT / "assets" / "hil-direct-upload-v1.js"
RECEIPT = ROOT / "hil-receipt.html"
HANDOFF = ROOT / "docs" / "HIL_SITE_MIRROR_HANDOFF.md"


def require(text: str, marker: str, failures: list[str], label: str) -> None:
    if marker not in text:
        failures.append(f"{label} missing invariant: {marker}")


def main() -> int:
    direct = DIRECT.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    failures: list[str] = []

    for forbidden in (
        "requireReadyReceiver",
        "await requireReadyReceiver",
        "const READINESS = '/api/hil/readiness'",
    ):
        if forbidden in direct:
            failures.append(f"direct upload retains readiness-first gate: {forbidden}")

    for marker in (
        "stegverse.hil.intr_ingress_envelope/v1",
        "stegverse.intr.hop_receipt/v1",
        "stegverse.hil.intr_egress_envelope/v1",
        "HIL_CUSTODY_TVC_INTERLOCK_ADMISSION",
        "body.append('intr_ingress_envelope'",
        "await validateIntrReceiptChain(result.intr_receipt_chain, envelope)",
        "intr_ingress_envelope: ingressEnvelope",
        "transport_grants_execution_authority: false",
        "authority_transfer: false",
    ):
        require(direct, marker, failures, "direct upload")

    if "/api/hil/readiness" in receipt:
        failures.append("receipt retry path still waits for receiver readiness")

    for marker in (
        "Continuing the existing InTr upload operation",
        "record.intr_ingress_envelope",
        "body.append('intr_ingress_envelope'",
        "setTimeout(()=>retry(current,{automatic:true})",
        "addEventListener('online'",
        "visibilitychange",
        "READY_FOR_INTERLOCK_ADMISSION",
        "HIL_CUSTODY_TVC_INTERLOCK_ADMISSION",
    ):
        require(receipt, marker, failures, "receipt continuation")

    for marker in (
        "SUBMISSION-TRIGGERED INTR DOUBLE-INTERLOCK",
        "DEVICE -> HIL_INGRESS",
        "HIL_INGRESS -> HIL_CUSTODY",
        "HIL_CUSTODY -> TVC_HIL_LIFECYCLE",
        "always-on receiver prerequisite: false",
        "manual resubmission prerequisite: false",
    ):
        require(handoff, marker, failures, "handoff")

    if failures:
        print("HIL_INTR_SUBMISSION_CONTRACT_FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("HIL_INTR_SUBMISSION_CONTRACT_PASS")
    print("submit_is_activation_event=true")
    print("receiver_readiness_precondition=false")
    print("same_operation_retry=true")
    print("manual_resubmission_prerequisite=false")
    print("always_on_receiver_prerequisite=false")
    print("transport_protocol=InTr")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
