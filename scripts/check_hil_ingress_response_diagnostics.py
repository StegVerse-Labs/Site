#!/usr/bin/env python3
from pathlib import Path

CLIENT = Path("assets/hil-direct-upload-v1.js")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> None:
    text = CLIENT.read_text(encoding="utf-8")

    required = (
        "async function parseIngressResponse(response)",
        "response.headers.get('content-type')",
        "const text = await response.text()",
        "function classifyIngressResponse(contentType, text)",
        "function ingressResponseDiagnostic(response, contentType, responseClass)",
        "response.redirected === true",
        "final_url_scope",
        "final_path",
        "response_class",
        "'NON_JSON_HTML'",
        "'NON_JSON_TEXT'",
        "'EMPTY'",
        "'OTHER'",
        "const result = await parseIngressResponse(response)",
    )
    for marker in required:
        require(marker in text, f"missing marker: {marker}")

    require(
        "response.json().catch(() => ({ detail: 'invalid_ingress_response' }))" not in text,
        "legacy lossy invalid_ingress_response fallback remains",
    )
    require("response_body" not in text, "arbitrary response body persistence marker present")
    require("response_text" not in text, "arbitrary response text persistence marker present")
    require("finalUrl.search" not in text, "query-string material must not enter diagnostics")
    require("finalUrl.hash" not in text, "URL fragments must not enter diagnostics")
    require(
        "custody_scope: 'PARTICIPANT_DEVICE_FALLBACK'" in text,
        "pending ingress must retain participant-device custody scope",
    )
    require(
        "state: 'INTR_TRANSPORT_PENDING'" in text,
        "pending ingress state must remain fail closed",
    )

    print("PASS: HIL ingress diagnostics are bounded and fail closed")


if __name__ == "__main__":
    main()
