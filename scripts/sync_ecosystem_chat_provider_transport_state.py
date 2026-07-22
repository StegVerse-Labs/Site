#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL = ROOT / "docs" / "ECOSYSTEM_CHAT_BUILD_GOAL.md"
ACTIVE = ROOT / "docs" / "ECOSYSTEM_CHAT_ACTIVE_BUILDING.md"
MARKER = "## Provider TLS and ledger verification update — 2026-07-22"
CYCLE = "docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING_CYCLE_2026-07-22_PROVIDER_TLS_LEDGER.md"

GOAL_SECTION = f"""

---

{MARKER}

- LLM-adapter PR #33 merged as `08e06a7b39ce8bf80d9de9b296e973debbe121ba`.
- Validation run `29882127078` and Architecture Guard run `29882127069` passed.
- The canonical broker completed trusted HTTPS transport to the exact StegVerse provider JSON contract using a test fixture.
- Explicit hostname allowlisting, bearer authentication, transition/run identity continuity, broker provider status `USED`, provider receipt construction, and SQLite provider-ledger persistence are VERIFIED with the test fixture.
- The focused test executed through the existing `tests/test_provider_usage.py` suite and existing validation workflow.
- Detailed cycle record: `{CYCLE}`.

### Current blocker

No provenance-approved GGUF model has yet been loaded and executed through this verified TLS/broker path. Real local model generation, provider-usage Master-Records custody and reconstruction, immutable activation, Site activation, and downstream propagation remain UNPROVEN.

### Next executable integration step

Install one approved GGUF through the existing bounded model intake, launch the existing StegVerse provider composition with machine-owned TLS and runtime authentication, and execute the same broker path with real local model generation. Retain the first exact inference, usage, custody, reconstruction, or activation failure.

### Manual user action requirement

False for routine repository work. Model provenance and machine execution authority remain separate runtime boundaries.
"""

ACTIVE_SECTION = f"""

---

{MARKER}

### Work performed

- Reused the canonical governed provider broker and existing provider-usage validation surface.
- Added one focused TLS provider fixture test and bound it through the existing test suite.
- Verified HTTPS trust, authentication, identity continuity, broker receipt creation, and provider-ledger persistence.

### Runtime evidence

- Merge: `08e06a7b39ce8bf80d9de9b296e973debbe121ba`
- Validation: `29882127078` — SUCCESS
- Architecture Guard: `29882127069` — SUCCESS
- Cycle record: `{CYCLE}`

### State classification

- HTTPS provider transport: VERIFIED with test fixture
- Provider authentication: VERIFIED with test fixture
- Broker provider status `USED`: VERIFIED with test fixture
- Provider receipt creation: VERIFIED with test fixture
- Provider usage ledger persistence: VERIFIED with test fixture
- Real GGUF inference: UNPROVEN
- Provider-usage custody/reconstruction: UNPROVEN
- Immutable activation, Site activation, propagation: UNPROVEN

### Non-progress

The deterministic fixture does not prove model loading or token generation and is not counted as a real provider response.

### Removals proposed but not performed

None. `StegVerse-Labs/governed-llm` PR #3 remains retained and unmerged.

### Goal delta

TLS transport and local provider-ledger persistence advanced to VERIFIED with a test fixture. No live provider or activation gate advanced.
"""


def append_once(path: Path, section: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    path.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return True


def main() -> int:
    changed = [append_once(GOAL, GOAL_SECTION), append_once(ACTIVE, ACTIVE_SECTION)]
    print(f"ECOSYSTEM CHAT PROVIDER TRANSPORT STATE SYNC: {'UPDATED' if any(changed) else 'UNCHANGED'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
