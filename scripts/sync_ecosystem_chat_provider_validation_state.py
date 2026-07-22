#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL = ROOT / "docs" / "ECOSYSTEM_CHAT_BUILD_GOAL.md"
ACTIVE = ROOT / "docs" / "ECOSYSTEM_CHAT_ACTIVE_BUILDING.md"
MARKER = "## Provider contract and model-intake update — 2026-07-22"
CYCLE = "docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING_CYCLE_2026-07-22_PROVIDER_CONTRACT_AND_MODEL_INTAKE.md"

GOAL_SECTION = f"""

---

{MARKER}

- `StegVerse-Labs/governed-llm` provider contract validation PR #1 merged as `e0f58b7a93d702bf8ace048dabf23c1c9f867be0`.
- The committed provider API contract passed 2/2 isolated tests for authenticated generation, identity preservation, SHA-256 receipts, and false authority fields.
- GitHub Actions run `29876624303` failed before exposing steps or logs and is retained as a separate runner failure.
- Provenance-bound local model intake PR #2 merged as `c0e88681ca69310b8c6e11461a1e8bc3cfb0e933`.
- Model intake passed 2/2 tests for exact manifest/digest installation and fail-closed mismatch handling.
- Provider validation receipt SHA-256: `066fdc2bd44a3ad909431b9b37784a6283471d1baef06becab4f0f3b09dbfc51`.
- Model-intake validation receipt SHA-256: `35097ab0a58377f686cacfb1e04136baff62851488d889815b47ba29eb6b8cf0`.
- Detailed cycle record: `{CYCLE}`.

### Current blocker

No provenance-approved real GGUF model and trusted local TLS material have been executed on an authorized StegVerse-controlled machine. Real provider generation, provider-usage persistence/custody/reconstruction, immutable activation, Site activation, and downstream propagation remain unproven.

### Next executable integration step

Install one approved GGUF through the merged bounded intake, start the existing StegVerse provider composition with machine-owned TLS and runtime authentication, and execute one governed request through the canonical gateway and Master-Records path.

### Manual user action requirement

False for routine repository work. Model provenance and machine execution authority remain separate runtime boundaries; no credential, model weight, or private key is requested through chat or committed to GitHub.
"""

ACTIVE_SECTION = f"""

---

{MARKER}

### Work performed

- Independently executed and retained the committed provider contract tests.
- Merged provider validation PR #1.
- Added and verified provenance-bound, atomic GGUF model intake.
- Merged model-intake PR #2.

### State classification

- Provider API/authentication/identity/non-authority contract: VERIFIED in isolated execution
- Model manifest, SHA-256, and atomic intake contract: VERIFIED
- Real GGUF installation and generation: UNPROVEN
- Gateway-to-provider HTTPS execution: UNPROVEN
- Provider-usage persistence/custody/reconstruction: UNPROVEN
- Immutable activation, Site activation, propagation: UNPROVEN

### Durable evidence

- Provider merge: `e0f58b7a93d702bf8ace048dabf23c1c9f867be0`
- Model-intake merge: `c0e88681ca69310b8c6e11461a1e8bc3cfb0e933`
- Provider receipt SHA-256: `066fdc2bd44a3ad909431b9b37784a6283471d1baef06becab4f0f3b09dbfc51`
- Model-intake receipt SHA-256: `35097ab0a58377f686cacfb1e04136baff62851488d889815b47ba29eb6b8cf0`
- Cycle record: `{CYCLE}`

### Goal delta

Provider and model-intake contracts advanced to verified. No live provider or activation gate advanced.

### Removals proposed but not performed

None.
"""


def append_once(path: Path, section: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    path.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return True


def main() -> int:
    changed = [append_once(GOAL, GOAL_SECTION), append_once(ACTIVE, ACTIVE_SECTION)]
    print(f"ECOSYSTEM CHAT PROVIDER VALIDATION STATE SYNC: {'UPDATED' if any(changed) else 'UNCHANGED'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
