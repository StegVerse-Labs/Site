#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECT = ROOT / "assets" / "hil-direct-upload-v1.js"
GENERATED = ROOT / "assets" / "generated" / "site-browser-intr-connectors.js"
RECEIPT = ROOT / "hil-receipt.html"
HANDOFF = ROOT / "docs" / "HIL_SITE_MIRROR_HANDOFF.md"


def require(text: str, marker: str, failures: list[str], label: str) -> None:
    if marker not in text:
        failures.append(f"{label} missing invariant: {marker}")


def main() -> int:
    direct = DIRECT.read_text(encoding="utf-8")
    generated = GENERATED.read_text(encoding="utf-8")
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
        "stegverse.universal-intr-transport/v1",
        "stegverse.universal-intr-materialization-request/v1",
        "stegverse.intr.hop_receipt/v1",
        "DEVICE_SYSTEM",
        "STEGOS_ECOSYSTEM",
        "HIL:Ingress",
        "HIL:Custody",
        "TVC:HIL-Lifecycle",
        "HIL_CUSTODY_TVC_INTERLOCK_ADMISSION",
        "body.append('intr_transport_intent'",
        "await validateIntrReceiptChain(result.intr_receipt_chain, envelope)",
        "intr_transport_intent: transportIntent",
        "intr_materialization_request: staged.materializationRequest",
        "local_pretransport_staged: true",
        "stageTransportPacket(file, bytes, digest, provenance, transportIntent)",
        "request_grants_execution_authority:false",
        "claim_or_fence_minted:false",
        'github_token_runtime_authority:"NONE"',
        '"downstream_owner_ref":"StegVerse-Labs/.github#246"',
        "event_triggered:true",
        "always_on_receiver_required:false",
        "second_user_device_required:false",
        "exact_packet_transport_retry_allowed:true",
        "blind_consequence_retry_allowed:false",
        "transport_grants_execution_authority:false",
        "authority_transfer:false",
    ):
        require(direct + generated, marker, failures, "direct upload + generated connector")

    if "/api/hil/readiness" in receipt:
        failures.append("receipt retry path still waits for receiver readiness")

    for marker in (
        "Continuing the existing InTr transport intent",
        "record.intr_transport_intent",
        "record.intr_materialization_request",
        "SATISFIED_BY_DIRECT_RECEIVER_RECEIPT",
        "body.append('intr_transport_intent'",
        "setTimeout(()=>retry(current,{automatic:true})",
        "addEventListener('online'",
        "visibilitychange",
        "HIL_CUSTODY_TVC_INTERLOCK_ADMISSION",
        "always-on application receiver",
    ):
        require(receipt, marker, failures, "receipt continuation")

    for marker in (
        "submission-triggered Universal Interlock/InTr transport",
        "DEVICE_SYSTEM / Site:HIL",
        "STEGOS_ECOSYSTEM / HIL:Ingress",
        "HIL:Ingress -> HIL:Custody",
        "HIL:Custody -> TVC:HIL-Lifecycle",
        "always_on_application_receiver_required = false",
        "second_user_device_required = false",
        "exact_packet_transport_retry_allowed = true",
        "blind_consequence_retry_allowed = false",
    ):
        require(handoff, marker, failures, "handoff")

    if failures:
        print("HIL_INTR_SUBMISSION_CONTRACT_FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("HIL_INTR_SUBMISSION_CONTRACT_PASS")
    print("submit_is_transport_event=true")
    print("receiver_readiness_precondition=false")
    print("pretransport_exact_packet_staged=true")
    print("materialization_request_staged=true")
    print("same_operation_retry=true")
    print("manual_resubmission_prerequisite=false")
    print("always_on_receiver_prerequisite=false")
    print("transport_protocol=InTr")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
