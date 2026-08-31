#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required = [
    ROOT / "docs" / "MY_KV_DIRECTORY_LANDING_MIRROR_HANDOFF.md",
    ROOT / "my-kv.html",
    ROOT / "my-kv-directory.html",
    ROOT / "assets" / "my-kv-directory.js",
    ROOT / "assets" / "my-kv-portable-direct-source-bridge.js",
    ROOT / "tests" / "my-kv-directory.test.cjs",
]

for path in required:
    if not path.exists():
        raise SystemExit(f"missing required My KV directory file: {path.relative_to(ROOT)}")

landing = (ROOT / "my-kv.html").read_text(encoding="utf-8")
browser = (ROOT / "my-kv-directory.html").read_text(encoding="utf-8")
js = (ROOT / "assets" / "my-kv-directory.js").read_text(encoding="utf-8")
portable = (ROOT / "assets" / "my-kv-portable-direct-source-bridge.js").read_text(encoding="utf-8")
generated = (ROOT / "assets" / "generated" / "site-browser-intr-connectors.js").read_text(encoding="utf-8")

for text in [
    "Your continuity directories",
    "Pictures & Media",
    "Music",
    "Email",
    "Finance",
    "Assets",
    "Liabilities",
]:
    if text not in landing and text not in js:
        raise SystemExit(f"missing My KV directory label/contract: {text}")

for canonical in [
    "03_Records/Finance",
    "03_Records/Assets",
    "03_Records/Liabilities",
    "03_Records/Email",
    "04_Media/Music",
    "04_Media/Pictures",
]:
    if canonical not in js:
        raise SystemExit(f"missing canonical directory mapping: {canonical}")

if "StegVerseKVDirectoryBridge" not in browser:
    raise SystemExit("directory browser must use canonical KV directory bridge")
if "StegVerseKVDirectSourceBridge" not in browser:
    raise SystemExit("directory browser must expose direct-source SKAP bridge")
if "StegVerseKVConnectionHealthBridge" not in landing:
    raise SystemExit("My KV landing must consume canonical connection-health bridge")
if "SKAP_VAULT" not in js or "direct_source_required" not in js:
    raise SystemExit("direct-source SKAP contract missing")

if "BRIDGE_UNAVAILABLE" not in js or "FAIL_CLOSED" not in js:
    raise SystemExit("directory source must preserve fail-closed behavior")
if "PORTABLE_OWNER_CONTROLLED_FILE_STAGING" not in portable:
    raise SystemExit("portable owner-controlled direct-source bridge missing")
for marker in ["QUEUED_FOR_KV_ADMISSION", "queueIntrMaterializationRequest", "credential_requirement:\"NONE\"", "canonical_kv_persistence_observed:false", "stegverse.kv.portable-direct-source-inline-payload/v1", "portable_payload:inlinePayload", "content_base64"]:
    if marker not in portable:
        raise SystemExit(f"portable direct-source staging contract missing: {marker}")
for marker in ["buildIntent(\"device-kv\"", "buildMaterializationRequest", "{portable_payload:inlinePayload}"]:
    if marker not in portable:
        raise SystemExit(f"portable direct-source generated InTr usage missing: {marker}")
for marker in [
    '"device-kv"',
    '"source":{"boundary":"DEVICE_SYSTEM","subsystem":"Device:KnowledgeVaultClient"}',
    '"destination":{"boundary":"KV","subsystem":"KnowledgeVault:Interlock"}',
    '"downstream_owner_ref":"StegVerse-Labs/continuity-vault-kit#79"',
    '"materialization_extension_fields":["portable_payload"]',
]:
    if marker not in generated:
        raise SystemExit(f"canonical generated DEVICE_KV contract missing: {marker}")
if "assets/my-kv-portable-direct-source-bridge.js" not in browser:
    raise SystemExit("directory page must load portable direct-source fallback")
if "KnowledgeVault:DirectSourceIngress" in portable or "continuity-vault-kit#108" in portable:
    raise SystemExit("portable direct-source packet must target canonical resident DEVICE_KV ingress")
if "inline://materialization_request.portable_payload" not in portable:
    raise SystemExit("portable direct-source packet must carry resident-consumable inline payload")
for marker in ["REVALIDATION_REQUIRED", "credential_material_present", "provider_operation_authorized", "connection-health-request"]:
    if marker not in js:
        raise SystemExit(f"connection-health contract missing: {marker}")

for forbidden in ["type=\"password\"", "access_token", "refresh_token", "private_key"]:
    if forbidden == "type=\"password\"" and forbidden in landing + browser:
        raise SystemExit("secret-bearing input field prohibited")

print("My KV directory static checks: PASS")
