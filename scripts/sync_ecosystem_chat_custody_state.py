#!/usr/bin/env python3
"""Append the latest verified Ecosystem Chat custody state to both authoritative records."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL = ROOT / "docs" / "ECOSYSTEM_CHAT_BUILD_GOAL.md"
ACTIVE = ROOT / "docs" / "ECOSYSTEM_CHAT_ACTIVE_BUILDING.md"
MARKER = "## Authoritative custody and reconstruction update — 2026-07-21"
CYCLE = "docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING_CYCLE_2026-07-21_CUSTODY_RECONSTRUCTION.md"

GOAL_SECTION = f"""

---

{MARKER}

This section supersedes only earlier statements that authenticated transition custody and reconstruction were unproven.

- Master-Records PR #3 merged as `421da84784888e3dc9bb98a7b2b47a1518f0eee0`.
- Runtime Evidence Validation run `29865690620` passed the real canonical gateway-to-custody round trip.
- Authenticated transition custody is VERIFIED with `RECORDED` status and an issued Master-Records reference.
- Transition reconstruction is VERIFIED with `PASS` status.
- Runtime artifact `8509093886` has digest `sha256:3ceabaf70a454d3192fab1c0b6200700c132ec19bcf32345ad688e66d9b175fd`.
- Custody-stack artifact `8509097445` has digest `sha256:2c8292476adaa15e9bb02d107cc8dcf10e6cd3c7caa252b9b828e844d94414b6`.
- Custody activation-state artifact `8509100922` has digest `sha256:e41451646435c964bc0dc8b02fc543cbebed7b61ea7526ff6cd9ed7179447ae5`.
- Provider execution remained `DISABLED_FAIL_CLOSED`; real provider response and provider-usage custody/reconstruction remain UNPROVEN.
- Immutable zero-blocker activation receipt, Site `ACTIVATION_COMPLETE`, and downstream propagation remain UNPROVEN.
- Detailed cycle record: `{CYCLE}`.

### Current blocker

No repository-owned runtime currently binds an authorized real-provider HTTPS endpoint, allowlisted hostname, credential, and model into the canonical portable-node path. The existing live-activation workflow only probes an already-running gateway and does not own provider credentials.

### Next executable integration step

Run the existing provider broker with an already-authorized provider configuration, execute one governed request through the same verified custody path, and repair only the first exact provider, usage-persistence, provider-usage custody, reconstruction, or activation-receipt failure.

### Manual user action requirement

False for routine repository work. A real-provider credential/execution boundary must already be authorized before it can be activated.
"""

ACTIVE_SECTION = f"""

---

{MARKER}

### Work performed

- Reused the canonical LLM-adapter gateway and the owned Master-Records custody service.
- Extended the existing Master-Records Runtime Evidence Validation workflow; no workflow was added.
- Executed one real governed transition round trip with run-scoped custody credentials.
- Verified authenticated custody `RECORDED`, Master-Records reference issuance, transition reconstruction `PASS`, identity continuity, and false authority fields.

### Existing capabilities reused

- `StegVerse-org/LLM-adapter/llm_adapter/combined_gateway.py`
- `StegVerse-org/LLM-adapter/llm_adapter/master_records_client.py`
- `master-records/orchestration/services/master_records_custody_api.py`
- Existing transition store, final receipt, custody-stack verifier, reconstruction response, tests, export receipt, and activation-state writer

### Runtime evidence

- Merge: `421da84784888e3dc9bb98a7b2b47a1518f0eee0`
- Run: `29865690620`
- Runtime artifact: `8509093886`, digest `sha256:3ceabaf70a454d3192fab1c0b6200700c132ec19bcf32345ad688e66d9b175fd`
- Custody-stack artifact: `8509097445`, digest `sha256:2c8292476adaa15e9bb02d107cc8dcf10e6cd3c7caa252b9b828e844d94414b6`
- Activation-state artifact: `8509100922`, digest `sha256:e41451646435c964bc0dc8b02fc543cbebed7b61ea7526ff6cd9ed7179447ae5`
- Detailed cycle record: `{CYCLE}`

### State classification

- Authenticated transition custody: VERIFIED
- Transition reconstruction: VERIFIED
- Real governed provider response: UNPROVEN
- Provider-usage persistence, custody, and reconstruction: UNPROVEN
- Immutable activation receipt: UNPROVEN
- Site activation: UNPROVEN
- Downstream propagation: UNPROVEN

### Removals proposed but not performed

None. Site PR #34 remains open and unmerged after proving a private cross-repository checkout boundary. No branch, file, workflow, or implementation was closed or removed.

### Goal delta

Authenticated transition custody and reconstruction advanced from implemented/unproven to executed and verified.

### Reuse delta

Existing custody, gateway, receipt, reconstruction, workflow, and test capabilities eliminated the need for a new custody service, adapter, workflow, or host.

### Non-progress

Provider execution remained disabled, so provider-usage custody, immutable activation, Site activation, and propagation are not counted complete.

### Next executable step

Bind an already-authorized real provider to the existing broker and execute the same path through provider usage persistence and custody.
"""


def append_once(path: Path, section: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    path.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return True


def main() -> int:
    changed = [append_once(GOAL, GOAL_SECTION), append_once(ACTIVE, ACTIVE_SECTION)]
    print(f"ECOSYSTEM CHAT CUSTODY STATE SYNC: {'UPDATED' if any(changed) else 'UNCHANGED'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
