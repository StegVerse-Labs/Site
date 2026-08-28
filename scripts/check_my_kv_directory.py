#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required = [
    ROOT / "docs" / "MY_KV_DIRECTORY_LANDING_MIRROR_HANDOFF.md",
    ROOT / "my-kv.html",
    ROOT / "my-kv-directory.html",
    ROOT / "assets" / "my-kv-directory.js",
    ROOT / "tests" / "my-kv-directory.test.cjs",
]

for path in required:
    if not path.exists():
        raise SystemExit(f"missing required My KV directory file: {path.relative_to(ROOT)}")

landing = (ROOT / "my-kv.html").read_text(encoding="utf-8")
browser = (ROOT / "my-kv-directory.html").read_text(encoding="utf-8")
js = (ROOT / "assets" / "my-kv-directory.js").read_text(encoding="utf-8")

for text in [
    "Your continuity directories",
    "Pictures & Media",
    "Music",
    "Email",
    "Finance",
]:
    if text not in landing and text not in js:
        raise SystemExit(f"missing My KV directory label/contract: {text}")

for canonical in [
    "03_Records/Finance",
    "03_Records/Email",
    "04_Media/Music",
    "04_Media/Pictures",
]:
    if canonical not in js:
        raise SystemExit(f"missing canonical directory mapping: {canonical}")

if "StegVerseKVDirectoryBridge" not in browser:
    raise SystemExit("directory browser must use canonical KV directory bridge")

if "BRIDGE_UNAVAILABLE" not in js or "FAIL_CLOSED" not in js:
    raise SystemExit("directory source must preserve fail-closed behavior")

for forbidden in ["type=\"password\"", "access_token", "refresh_token", "private_key"]:
    if forbidden == "type=\"password\"" and forbidden in landing + browser:
        raise SystemExit("secret-bearing input field prohibited")

print("My KV directory static checks: PASS")
