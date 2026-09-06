from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "steglearn" / "index.html"
HANDOFF = ROOT / "docs" / "STEGLEARN_SITE_MIRROR_HANDOFF.md"

failures = []

def require(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)

require(PAGE.exists(), "missing steglearn/index.html")
require(HANDOFF.exists(), "missing docs/STEGLEARN_SITE_MIRROR_HANDOFF.md")

if PAGE.exists():
    page = PAGE.read_text(encoding="utf-8")
    for marker in [
        'href="https://stegverse.org/steglearn"',
        'id="vision"',
        'id="purpose"',
        'id="guidelines"',
        'id="roadmap"',
        'id="curriculum"',
        'StegVerse Foundations',
        'Maximize becoming without capture',
        'Capability is not authority',
        'AI SiteFlow',
        'generated media remains downstream',
        'External learning ecosystem',
        'reciprocal, explicitly bounded educational relationships',
        'https://github.com/StegVerse-Labs/StegLearn',
    ]:
        require(marker.lower() in page.lower(), f"page missing marker: {marker}")

    for number in range(1, 13):
        require(f'>{number:02d}<' in page, f"missing curriculum module number {number:02d}")

    require(page.count('status current') == 1, "exactly one curriculum module must be MATERIALIZED")
    require(page.count('>ROADMAP</span>') == 11, "modules 02-12 must remain ROADMAP")
    require('>MATERIALIZED</span>' in page, "module 01 materialized marker missing")

    boundary_markers = [
        'does not claim accreditation',
        'completed AI SiteFlow integration',
        'completion of roadmap modules that remain under development',
    ]
    for marker in boundary_markers:
        require(marker.lower() in page.lower(), f"boundary missing: {marker}")

if HANDOFF.exists():
    handoff = HANDOFF.read_text(encoding="utf-8")
    for marker in [
        'PASS_FOR_STATIC_PUBLIC_STEGLEARN_ORIENTATION_SURFACE',
        'NO_ROOT_README_CHANGE_REQUIRED',
        'SOURCE_LANDING_PAGE_IMPLEMENTED_VALIDATION_PENDING',
        'StegVerse-Labs/StegLearn/STEGLEARN_MIRROR_HANDOFF.md',
        'docs/STEGVERSE_FOUNDATIONS_MIRROR_HANDOFF.md',
        'generation 15',
    ]:
        require(marker.lower() in handoff.lower(), f"handoff missing marker: {marker}")

if failures:
    print("STEGLEARN_LANDING_VALIDATION_FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("STEGLEARN_LANDING_VALIDATION_PASS")
print("STEGLEARN_LANDING_AUTHORITY_EFFECT=NONE")
print("STEGLEARN_LANDING_RUNTIME_ACTIVATION_CLAIM=false")
