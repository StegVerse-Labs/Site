from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PATHS = ROOT / "docs" / "SITE_PUBLIC_PATHS.md"

REQUIRED = [
    "/governed-ecosystem.html",
    "/ecosystem-chat.html",
    "/humans-as-interoperability-layer.html",
    "/humans-as-interoperability-response.html?id=HIL-RESP-...",
    "/external-chat.html",
    "/external-review.html",
    "/governed-transitions.html",
    "StegVerse-Labs/admissibility-wiki",
    "docs/SITE_GOVERNED_ECOSYSTEM_STATUS.txt",
    "docs/HIL_SITE_MIRROR_HANDOFF.md",
    "scripts/check_site_governed_ecosystem_mirror.py",
    "scripts/check_hil_experiment.py",
    "scripts/check_external_chat_compatibility.py",
    "scripts/check_external_review_console.py",
    "external-chat-submission-contract.md",
    "data/hil-experiment.json",
    "data/hil-responses.json",
    "data/external-framework-catalog.json",
    "data/external-framework-catalog.receipt.json",
]

REQUIRED_FILES = [
    "humans-as-interoperability-layer.html",
    "humans-as-interoperability-response.html",
    "assets/hil-experiment.js",
    "assets/hil-response.js",
    "data/hil-experiment.json",
    "data/hil-responses.json",
    "data/schemas/hil-submission.schema.json",
    "data/schemas/hil-receiver-receipt.schema.json",
    "docs/HIL_SITE_MIRROR_HANDOFF.md",
    "scripts/check_hil_experiment.py",
    "external-chat.html",
    "external-review.html",
    "assets/external-chat.js",
    "assets/external-review.js",
    "scripts/check_external_chat_compatibility.py",
    "scripts/check_external_review_console.py",
    "data/external-framework-catalog.json",
    "data/external-framework-catalog.receipt.json",
]


def main():
    errors = []
    if not PUBLIC_PATHS.exists():
        errors.append("missing_public_paths")
        text = ""
    else:
        text = PUBLIC_PATHS.read_text(encoding="utf-8")
    for item in REQUIRED:
        if item not in text:
            errors.append("missing:" + item)
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.exists():
            errors.append("missing_file:" + relative)
    if errors:
        print("SITE PUBLIC PATHS: FAIL - " + ", ".join(errors))
        return 1
    print("SITE PUBLIC PATHS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
