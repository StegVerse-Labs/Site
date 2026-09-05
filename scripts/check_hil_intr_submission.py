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
        "response.json().catch(() => ({ detail: 'invalid_ingress_response' }))",
    ):
        if forbidden in direct:
            failures.append(f"direct upload retains forbidden/lossy gate: {forbidden}")

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

    for marker in (
        "async function parseIngressResponse(response)",
        "response.headers.get('content-type')",
        "const text = await response.text()",
        "response.redirected === true",
        "final_url_scope",
        "final_path",
        "response_class",
        "NON_JSON_HTML",
        "NON_JSON_TEXT",
        "EMPTY",
        "OTHER",
        "const result = await parseIngressResponse(response)",
    ):
        require(direct, marker, failures, "bounded ingress diagnostics")

    for forbidden in (
        "response_body",
        "response_text",
        "finalUrl.search",
        "finalUrl.hash",
    ):
        if forbidden in direct:
            failures.append(f"bounded ingress diagnostics expose forbidden response/URL material: {forbidden}")

    if "/api/hil/readiness" in receipt:
        failures.append("receipt retry path still waits for receiver readiness")

    for forbidden in (
        "r.json().catch(()=>({detail:'invalid_ingress_response'}))",
        "response.json().catch(() => ({ detail: 'invalid_ingress_response' }))",
        "finalUrl.search",
        "finalUrl.hash",
        "response_body",
        "response_text",
    ):
        if forbidden in receipt:
            failures.append(f"receipt retry retains lossy/forbidden diagnostic behavior: {forbidden}")

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
        "function normalizeContentType(value)",
        "function classifyIngressResponse(contentType,text)",
        "function ingressResponseDiagnostic(response,contentType,responseClass)",
        "async function parseIngressResponse(response)",
        "response.headers.get('content-type')",
        "const text=await response.text()",
        "response.redirected===true",
        "final_url_scope",
        "final_path",
        "response_class",
        "NON_JSON_HTML",
        "NON_JSON_TEXT",
        "EMPTY",
        "OTHER",
        "const result=await parseIngressResponse(r)",
        "record.last_ingress_diagnostic=result",
        "record.record_state='INTR_TRANSPORT_PENDING'",
        "const originalOperationId=intent.operation_id",
        "buildTransportIntent(actual,provenance,originalOperationId)",
        "stored_intr_transport_operation_identity_changed",
    ):
        require(receipt, marker, failures, "receipt continuation")

    # Tab/window lifetime must never be the persistence layer. The receipt page
    # must reconstruct its working state from durable browser storage every time
    # it is opened, and verify exact bytes again before retry.
    for marker in (
        "const RECORD_KEY='stegverse.hil.submissions.v1'",
        "DB_NAME='stegverse-hil-v3'",
        "STORE_NAME='response_files'",
        "JSON.parse(localStorage.getItem(RECORD_KEY)||'[]')",
        "rows.find(r=>r&&r.submission_id===id)||rows[0]||null",
        "indexedDB.open(DB_NAME,1)",
        ".objectStore(STORE_NAME).get(key)",
        "if(record.response_sha256&&actual!==record.response_sha256)throw Error('response_pdf_hash_mismatch')",
        "const f=await pdf(record)",
        "let intent=record.intr_transport_intent",
        "const originalOperationId=intent.operation_id",
    ):
        require(receipt, marker, failures, "tab-independent persisted-record continuity")

    for forbidden in (
        "sessionStorage.setItem(",
        "sessionStorage.getItem(",
        "window.name=",
    ):
        if forbidden in receipt:
            failures.append(f"receipt persistence depends on page/session lifetime: {forbidden}")

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
    print("bounded_invalid_ingress_diagnostics=true")
    print("bounded_receipt_retry_ingress_diagnostics=true")
    print("receipt_retry_transport_identity_reused=true")
    print("open_tab_required=false")
    print("page_lifetime_required=false")
    print("persisted_record_reconstruction=true")
    print("persisted_exact_bytes_reverified_before_retry=true")
    print("arbitrary_ingress_response_body_persisted=false")
    print("transport_protocol=InTr")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
