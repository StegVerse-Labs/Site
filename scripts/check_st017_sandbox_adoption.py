#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "templates/sandbox-first/site.sandbox-profile.json"
RUNNER = ROOT / "scripts/run_sandbox_validation.py"
WORKFLOW = ROOT / ".github/workflows/validate.yml"
ADOPTION = ROOT / "docs/ST017_SITE_ADOPTION_HANDOFF.md"
SOURCE = ROOT / "docs/SITE_MIRROR_HANDOFF.md"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--structural-only", action="store_true")
    parser.parse_args()
    errors: list[str] = []

    for path in [PROFILE, RUNNER, WORKFLOW, ADOPTION, SOURCE]:
        if not path.exists():
            errors.append("missing:" + str(path.relative_to(ROOT)))

    if PROFILE.exists():
        data = json.loads(PROFILE.read_text(encoding="utf-8"))
        command_ids = [item.get("id") for item in data.get("commands", [])]
        if data.get("repository") != "StegVerse-Labs/Site":
            errors.append("profile_repository_mismatch")
        for required in [
            "compile-python",
            "write-workflow-inventory",
            "validate-workflow-inventory",
            "validate-application",
            "validate-st017-adoption",
        ]:
            if required not in command_ids:
                errors.append("profile_missing:" + required)

    if WORKFLOW.exists():
        text = WORKFLOW.read_text(encoding="utf-8")
        for marker in [
            "st017-sandbox:",
            "python scripts/run_sandbox_validation.py",
            "site-st017-sandbox-report",
            "needs: st017-sandbox",
        ]:
            if marker not in text:
                errors.append("workflow_missing:" + marker)

    if ADOPTION.exists():
        text = ADOPTION.read_text(encoding="utf-8")
        for marker in [
            "SANDBOX: NOT_RUN",
            "PUBLIC_OUTPUT: NOT_VERIFIED",
            "No release tag is authorized.",
        ]:
            if marker not in text:
                errors.append("adoption_missing:" + marker)

    if errors:
        print("SITE ST-017 ADOPTION: FAIL - " + ", ".join(errors))
        return 1
    print("SITE ST-017 ADOPTION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
