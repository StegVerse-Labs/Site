#!/usr/bin/env python3
"""Verify the Conectrr runtime projection and immutable import boundary."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
NODE = ROOT / "assets" / "ecosystem-node-views.js"
LOADER = ROOT / "assets" / "conectrr-interop.js"
FIXTURE = ROOT / "data" / "conectrr-independent-evaluation.fixture.json"
BROWSER_CHECK = ROOT / "scripts" / "check_conectrr_browser_projection.py"
EXPORT_CHECK = ROOT / "scripts" / "check_conectrr_export_replay.py"
LIVE_CHECK = ROOT / "scripts" / "check_conectrr_live_routes.py"
LIVE_WORKFLOW = ROOT / ".github" / "workflows" / "conectrr-live-verification.yml"

REQUIRED_NODE = [
    "importCanonicalEvents",
    "duplicate imported event_id",
    "unresolved parent_event_id",
    "JSON.parse(JSON.stringify(event))",
    "eventIndex.has(event.event_id)",
    "assets/conectrr-interop.js",
]
REQUIRED_LOADER = [
    "conectrr-independent-evaluation.fixture.json",
    "source_event",
    "downstream_event",
    "structuredClone",
    "source mutated during import",
    "api.importCanonicalEvents([source, decision])",
    "conectrrInterop",
    "conectrrBrowserTest",
    "conectrrExportReplay",
    "verifyExportReplay",
]


def missing(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return [f"missing file: {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    return [f"{path.relative_to(ROOT)} missing: {needle}" for needle in needles if needle not in text]


def run_check(path: Path) -> str | None:
    if not path.exists():
        return f"missing validator: {path.relative_to(ROOT)}"
    completed = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return None if completed.returncode == 0 else completed.stdout.rstrip()


def main() -> int:
    errors = []
    errors.extend(missing(NODE, REQUIRED_NODE))
    errors.extend(missing(LOADER, REQUIRED_LOADER))
    if not FIXTURE.exists():
        errors.append("missing independent evaluation fixture")
    for check in (BROWSER_CHECK, EXPORT_CHECK):
        failure = run_check(check)
        if failure:
            errors.append(failure)
    if not LIVE_CHECK.exists():
        errors.append("missing deployed publication verifier")
    if not LIVE_WORKFLOW.exists():
        errors.append("missing deployed publication workflow")
    if errors:
        print("CONECTRR_RUNTIME_PROJECTION_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("CONECTRR_RUNTIME_PROJECTION_CHECK=PASS")
    print("source_event=evidence")
    print("downstream_event=decision")
    print("import_semantics=clone_then_freeze")
    print("rendering=source_and_decision")
    print("correlation=bidirectional_stable_event_id")
    print("export_replay=json_and_jsonl")
    print("deployed_publication_verification=declared")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
