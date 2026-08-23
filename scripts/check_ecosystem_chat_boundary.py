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
    "same_execution!==true",
    "reconstruction_state!=='PASS'",
]
REQUIRED_GENERAL_CLIENT = [
    "runtime.askGeneral(message)",
    "runtime.askMath(message)",
    "runtime?.isMath?.(message)",
    "Thinking…",
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
    if 'type="file"' in page.lower():
        raise AssertionError("public Ecosystem Chat must not expose private document upload before activation")
    if "VA-HOME-LOANS" not in registry or "VA-COMMUNITY-CARE" not in registry or "VA-HEALTH-CARE" not in registry:
        raise AssertionError("VA source registry missing broad user-facing routes")
    print("ECOSYSTEM_CHAT_SHARED_CONVERSATIONAL_RUNTIME_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
