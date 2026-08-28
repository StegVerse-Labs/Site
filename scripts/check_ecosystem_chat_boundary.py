#!/usr/bin/env python3
"""Validate the user-first Ecosystem Chat surface and shared conversational runtime boundary."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ecosystem-chat.html"
VA_RUNTIME = ROOT / "assets" / "ecosystem-chat-va-runtime.js"
SIMPLE_RUNTIME = ROOT / "assets" / "ecosystem-chat-simple.js"
PROJECTION = ROOT / "api" / "va-claim-assistant" / "runtime-projection.json"
REGISTRY = ROOT / "data" / "va-claim-assistant" / "source-registry.json"
BRIDGE = ROOT / "stegos-bootstrap" / "ecosystem-chat-bridge.html"

REQUIRED_PAGE = [
    "How can I help?",
    "Ask in your own words.",
    'id="chatLog"',
    'id="chatForm"',
    'id="messageInput"',
    "Math help",
    "Can you help me understand how to solve this equation?",
    "How do I get a VA home loan?",
    "Community Care",
    "VA health care",
    "assets/ecosystem-chat-va-runtime.js",
    "assets/ecosystem-chat-simple.js",
    'id="mathImageInput"',
    'type="file"',
    'accept="image/png,image/jpeg,image/webp,image/heif,image/heic"',
    "Add math image",
]
FORBIDDEN_PUBLIC = [
    "raw_shell_allowed",
    "authority_required=true",
    "receipt_required_for_execution",
    "Ecosystem LLM routing bands",
    "Heartbeat / standing visualization",
    "SDK manifest preview",
    "Restricted admin",
    "mode=local-simulation",
    "Governed Transition Preview",
    "Current capability:",
    "SOURCE-GROUNDED",
    "fail-closed",
]
REQUIRED_SHARED_RUNTIME = [
    "COORDINATED_VA_RESOURCES_LLM",
    "ADMITTED_OFFICIAL_VA_ONLY",
    "validProjection",
    "custody_state==='RECORDED'",
    "reconstruction_state==='PASS'",
    "private_document_context:false",
    "filing_requested:false",
    "authority_escalation_rejected",
    "executeDeviceRaw",
    "askGeneral",
    "askMath",
    "isMath",
    "mathPrompt",
    "mathematics-educator",
    "ecosystemMathHistory",
    "governed_math_solver",
    "math_verifier",
    "CANDIDATE_ONLY_NOT_EXECUTED",
    "execution_authority:false",
    "source_image",
    "interpreted_mathematical_transcription",
    "window.EcosystemRuntime=api",
    "deterministicGeneralCapability",
    "device_clock",
    "device-local-deterministic",
    "stegverse.device-local-deterministic-execution.v1",
    "formatDeviceClock",
    "sha256Hex",
    "ecosystemLatestDeterministicReceipt",
    "deterministic_execution:true",
    "model_execution:false",
    "reconstructed_output:reconstructedOutput",
    "same_execution:sameExecution",
    "reconstruction_state:sameExecution?'PASS':'FAIL'",
    "receipt_sha256:receiptSha256",
    "MATH_ACTIVATION_URL",
    "governedArithmeticCandidate",
    "loadVerifiedMathRuntime",
    "executeGovernedMathCandidate",
    "stegverse.site.math_solver_activation.v1",
    "math_runtime_not_activated",
    "stegverse:steggate:canonical:three-layer:v1",
    "StegVerse-Labs/StegCore",
    "/api/math-solver/v1/readiness",
    "/api/math-solver/v1/solve",
    "payload.disposition!=='ALLOW'",
    "payload.execution_state!=='EXECUTED'",
    "payload.executor_invoked!==true",
    "math_execution_evidence_incomplete",
    "governed-math-solver",
    "governed_tool_execution:true",
    "authority_effect:'NONE'",
    "reviewMathImage",
    "sha256File",
    "/api/attachments/v1/readiness",
    "/api/attachments/v1/intake",
    "/api/math-solver/v1/image-review",
    "stegverse.attachment-receipt.v1",
    "stegverse.math-image-review.v1",
    "EXACT_BYTES_PRESERVED",
    "transcription.state!=='NOT_PRODUCED'",
    "transcription.content!==null",
    "transcription.is_source_fact!==false",
    "transcription.source_image_remains_immutable!==true",
    "credential_authority!=='TV/TVC'",
    "github_token_runtime_authority!=='NONE'",
    "math_attachment_authority_escalation",
    "math_image_review_authority_escalation",
    "governed-math-image-review",
    "transcription_state:'NOT_PRODUCED'",
    "const deterministic=await deterministicGeneralCapability(message)",
    "isLiveWeatherRequest",
    "dynamicDataCapabilityGap",
    "requestWeatherPosition",
    "selectForecastPeriods",
    "formatForecastPeriod",
    "liveWeatherCapability",
    "https://api.weather.gov/points/",
    "source_role:'DATA_ONLY_NO_EXECUTION_AUTHORITY'",
    "exact_coordinates_persisted:false",
    "stegverse.live-weather-evidence.v1",
    "ecosystemLatestWeatherReceipt",
    "const weather=await liveWeatherCapability(message)",
    "capability:'live_weather'",
    "same_execution!==true",
    "reconstruction_state!=='PASS'",
]
REQUIRED_GENERAL_CLIENT = [
    "runtime.askGeneral(message)",
    "runtime.askMath(message)",
    "runtime?.isMath?.(message)",
    "Thinking…",
    "response.dataset.executionReceipt=result.receipt",
    "response.dataset.reconstructionState=result.reconstruction_state||''",
    "result.model_execution===false?'deterministic-capability':'model'",
    "runtime.reviewMathImage(mathImage)",
    "Math image: ",
    "mathematical transcription has not been produced or admitted yet",
    "response.dataset.attachmentHash=result.attachment_hash",
    "response.dataset.transcriptionState=result.transcription_state",
]
FORBIDDEN_GENERAL_CLIENT = [
    "I can currently give live conversational help with VA benefits and claims here.",
]


def read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    page = read(PAGE)
    runtime = read(VA_RUNTIME)
    simple = read(SIMPLE_RUNTIME)
    bridge = read(BRIDGE)
    read(PROJECTION)
    registry = read(REGISTRY)

    missing = [token for token in REQUIRED_PAGE if token not in page]
    if missing:
        raise AssertionError("ecosystem-chat.html missing user-facing contract: " + ", ".join(missing))
    exposed = [token for token in FORBIDDEN_PUBLIC if token.lower() in page.lower()]
    if exposed:
        raise AssertionError("ecosystem-chat.html exposes implementation terminology: " + ", ".join(exposed))
    missing_runtime = [token for token in REQUIRED_SHARED_RUNTIME if token not in runtime]
    if missing_runtime:
        raise AssertionError("shared runtime bridge missing gate: " + ", ".join(missing_runtime))
    missing_general = [token for token in REQUIRED_GENERAL_CLIENT if token not in simple]
    if missing_general:
        raise AssertionError("general conversation client is not bound to shared specialty runtime: " + ", ".join(missing_general))
    canned = [token for token in FORBIDDEN_GENERAL_CLIENT if token in simple]
    if canned:
        raise AssertionError("general conversation still uses canned capability response")
    if "stegverse-device-local-bridge" not in bridge or "reconstruction_state" not in bridge:
        raise AssertionError("device-local bridge does not expose reconstructed execution evidence")
    if page.lower().count('type="file"') != 1 or 'id="mathImageInput"' not in page:
        raise AssertionError("public Ecosystem Chat must expose exactly one bounded Math image input")
    for token in ("privateDocumentInput", "medicalRecordInput", "generalAttachmentInput"):
        if token in page:
            raise AssertionError("private/general document upload remains unadmitted")
    if "await runtime.askMath('Using the uploaded math image" in simple:
        raise AssertionError("image review must not become unadmitted mathematical transcription")
    if "VA-HOME-LOANS" not in registry or "VA-COMMUNITY-CARE" not in registry or "VA-HEALTH-CARE" not in registry:
        raise AssertionError("VA source registry missing broad user-facing routes")
    print("ECOSYSTEM_CHAT_SHARED_CONVERSATIONAL_RUNTIME_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
