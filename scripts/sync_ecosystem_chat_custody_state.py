#!/usr/bin/env python3
"""Append verified Ecosystem Chat runtime advances to both authoritative Site records."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL = ROOT / "docs" / "ECOSYSTEM_CHAT_BUILD_GOAL.md"
ACTIVE = ROOT / "docs" / "ECOSYSTEM_CHAT_ACTIVE_BUILDING.md"
CUSTODY_MARKER = "## Authoritative custody and reconstruction update — 2026-07-21"
PROVIDER_MARKER = "## Authorized provider runtime integration update — 2026-07-21"
CUSTODY_CYCLE = "docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING_CYCLE_2026-07-21_CUSTODY_RECONSTRUCTION.md"
PROVIDER_CYCLE = "docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING_CYCLE_2026-07-21_AUTHORIZED_PROVIDER_RUNTIME.md"

CUSTODY_GOAL_SECTION = f"""

---

{CUSTODY_MARKER}

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
- Detailed cycle record: `{CUSTODY_CYCLE}`.

### Current blocker

No repository-owned runtime currently binds an authorized real-provider HTTPS endpoint, allowlisted hostname, credential, and model into the canonical portable-node path. The existing live-activation workflow only probes an already-running gateway and does not own provider credentials.

### Next executable integration step

Run the existing provider broker with an already-authorized provider configuration, execute one governed request through the same verified custody path, and repair only the first exact provider, usage-persistence, provider-usage custody, reconstruction, or activation-receipt failure.

### Manual user action requirement

False for routine repository work. A real-provider credential/execution boundary must already be authorized before it can be activated.
"""

CUSTODY_ACTIVE_SECTION = f"""

---

{CUSTODY_MARKER}

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
- Detailed cycle record: `{CUSTODY_CYCLE}`

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

PROVIDER_GOAL_SECTION = f"""

---

{PROVIDER_MARKER}

This section supersedes only the earlier statement that no repository-owned runtime could bind an authorized provider configuration.

- LLM-adapter PR #29 merged as `2d1533644d9e589fd441ba37a1bc4095ae5f4100`.
- The existing Ecosystem Chat Live Activation workflow now consumes only the canonical authorized provider and Master-Records configuration fields.
- A real execution must prove provider `USED`, provider receipt issuance, provider-usage persistence, provider-usage custody, transition custody `RECORDED`, reconstruction `PASS`, and false authority flags.
- Missing configuration produces a hash-bound `CONFIGURATION_REQUIRED` receipt without exposing secret values.
- Fallback text cannot satisfy the provider verifier.
- Validation run `29867306026` and current-mainline validation run `29867888624` exercised the integration; Architecture Guard run `29867888688` passed.
- No main-branch authorized-provider execution receipt had been retained at the latest observation. Real provider execution therefore remains UNPROVEN.
- Detailed cycle record: `{PROVIDER_CYCLE}`.

### Current blocker

The repository has not yet retained evidence that an authorized provider endpoint, token, model, Master-Records endpoint, and Master-Records token were simultaneously available to the canonical runtime.

### Next executable integration step

Allow the existing live-activation workflow to consume already-authorized configuration and inspect its first retained receipt. Repair only the first provider transport, response-contract, usage-persistence, provider-usage custody, transition-custody, reconstruction, or activation failure.

### Manual user action requirement

False for routine repository work. No credential value is requested through chat or committed to a repository. Provider and custody authorization must originate through the established secret-owning boundary.
"""

PROVIDER_ACTIVE_SECTION = f"""

---

{PROVIDER_MARKER}

### Work performed

- Extended the existing live-activation workflow instead of creating a provider executor.
- Reused the provider broker, usage ledger, provider-usage custody client, transition custody client, combined gateway, receipt retention, and activation verifier.
- Added a fail-closed verifier that rejects provider fallback, missing provider receipts, missing usage persistence, missing usage custody, failed transition custody or reconstruction, and any authority escalation.
- Rebound stale StegDeploy validation contracts to the already-installed image-publication v2 contract.

### Components modified

- `StegVerse-org/LLM-adapter/.github/workflows/ecosystem-chat-live-activation.yml`
- `StegVerse-org/LLM-adapter/scripts/verify_stegdeploy_runtime.py`
- `StegVerse-org/LLM-adapter/scripts/check_stegdeploy_image_receipt_retention.py`
- `StegVerse-org/LLM-adapter/tests/test_live_activation_automation_contract.py`

### Bounded verifier added

- `StegVerse-org/LLM-adapter/scripts/verify_authorized_provider_activation.py`
- `StegVerse-org/LLM-adapter/tests/test_authorized_provider_activation_verifier.py`

The verifier is an adapter to existing runtime outputs, not a new provider, gateway, custody service, receipt authority, or scheduler.

### Runtime evidence

- Merge: `2d1533644d9e589fd441ba37a1bc4095ae5f4100`
- Original green validation: `29867306026`
- Current-mainline validation: `29867888624`
- Architecture Guard: `29867888688`

### State classification

- Authorized provider runtime binding: INTEGRATED
- Configuration-presence evaluation: IMPLEMENTED
- Fail-closed provider/custody verifier: VERIFIED BY TESTS
- Real governed provider response: UNPROVEN
- Provider-usage persistence and custody: UNPROVEN IN REAL EXECUTION
- Immutable activation receipt: UNPROVEN
- Site activation: UNPROVEN
- Downstream propagation: UNPROVEN

### Removals proposed but not performed

None. LLM-adapter PR #27 remains retained and open after its branch-history conflict; no implementation was deleted or closed.

### Goal delta

The existing runtime can now execute the full authorized provider path automatically when established configuration exists. Before this cycle, no repository-owned workflow could bind that configuration to the canonical gateway.

### Reuse delta

Existing provider, usage, custody, reconstruction, workflow, receipt, and activation components eliminated the need for a new provider executor, deployment service, or receipt family.

### Non-progress

No real provider call or provider-usage custody event is counted complete because no main-branch execution receipt has yet been retained.

### Next executable step

Inspect the first repository-retained authorized-provider activation receipt and repair its first exact blocker.
"""


def append_once(path: Path, marker: str, section: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return False
    path.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return True


def main() -> int:
    changed = [
        append_once(GOAL, CUSTODY_MARKER, CUSTODY_GOAL_SECTION),
        append_once(ACTIVE, CUSTODY_MARKER, CUSTODY_ACTIVE_SECTION),
        append_once(GOAL, PROVIDER_MARKER, PROVIDER_GOAL_SECTION),
        append_once(ACTIVE, PROVIDER_MARKER, PROVIDER_ACTIVE_SECTION),
    ]
    print(f"ECOSYSTEM CHAT STATE SYNC: {'UPDATED' if any(changed) else 'UNCHANGED'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
