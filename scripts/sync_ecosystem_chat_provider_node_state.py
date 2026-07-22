#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL = ROOT / "docs" / "ECOSYSTEM_CHAT_BUILD_GOAL.md"
ACTIVE = ROOT / "docs" / "ECOSYSTEM_CHAT_ACTIVE_BUILDING.md"
MARKER = "## StegVerse-owned provider-node update — 2026-07-21"
VALIDATION_MARKER = "## Provider contract and model-intake update — 2026-07-22"
OPENAI_MARKER = "## OpenAI-compatible provider profile update — 2026-07-22"
CYCLE = "docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING_CYCLE_2026-07-21_STEGVERSE_PROVIDER_NODE.md"
VALIDATION_CYCLE = "docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING_CYCLE_2026-07-22_PROVIDER_CONTRACT_AND_MODEL_INTAKE.md"
OPENAI_CYCLE = "docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING_CYCLE_2026-07-22_OPENAI_PROVIDER_PROFILE.md"

GOAL_SECTION = f"""

---

{MARKER}

This section supersedes only the earlier statement that no repository-owned provider endpoint implementation existed.

- `StegVerse-Labs/governed-llm` now contains a StegVerse-owned local GGUF inference service.
- The service implements the existing `LLM-adapter` governed provider JSON contract at authenticated `POST /generate`.
- Model bytes remain local to StegVerse-controlled node storage; the engine does not call a hosted inference API.
- The provider emits identity-bound usage metadata and a SHA-256 provider receipt while keeping authority, execution, and publication flags false.
- `compose.stegverse-provider.yaml` connects the provider to the canonical `LLM-adapter` gateway over HTTPS.
- The existing broker remains responsible for allowlisting, credentials, quota, cost, output limits, usage persistence, Master-Records custody, and fallback.
- Standard `REQUESTS_CA_BUNDLE` trust binding is reused; HTTPS verification is not disabled.
- Provider-node validation PR: https://github.com/StegVerse-Labs/governed-llm/pull/1
- Detailed cycle record: `{CYCLE}`.

### Current blocker

No authorized StegVerse-controlled machine has yet executed the provider composition with locally retained GGUF model bytes and locally trusted TLS material. Real model output, provider usage persistence, provider-usage custody, reconstruction, immutable activation, Site activation, and downstream propagation remain unproven.

### Next executable integration step

Run the existing `compose.stegverse-provider.yaml` composition on an authorized StegVerse node with provenance-approved local model bytes and trusted TLS material. Execute one governed request through the canonical gateway and retain the first exact model, TLS, provider, persistence, custody, reconstruction, or activation-receipt failure.

### Manual user action requirement

False for routine repository work. Model provenance and machine execution authority remain separate runtime boundaries; no credential, model weight, or private key is requested through chat or committed to GitHub.
"""

ACTIVE_SECTION = f"""

---

{MARKER}

### Work performed

- Reused the existing `LLM-adapter` provider broker and canonical gateway.
- Implemented local GGUF inference in the existing empty `StegVerse-Labs/governed-llm` repository.
- Added authenticated HTTPS generation, identity echoes, usage metadata, SHA-256 receipts, non-authority enforcement, container packaging, and integrated composition.
- Reused standard `REQUESTS_CA_BUNDLE` trust behavior rather than modifying or weakening the broker.

### State classification

- StegVerse provider service: IMPLEMENTED
- Gateway/provider composition: INTEGRATED in source and configuration
- Repository CI: UNPROVEN because the observed validation run exposed no job steps or logs
- Real model execution: UNPROVEN
- Provider-usage persistence/custody/reconstruction: UNPROVEN
- Immutable activation, Site activation, and propagation: UNPROVEN

### Durable evidence

- Repository: https://github.com/StegVerse-Labs/governed-llm
- Validation PR: https://github.com/StegVerse-Labs/governed-llm/pull/1
- Cycle record: `{CYCLE}`

### Removals proposed but not performed

None.

### Goal delta

A StegVerse-owned provider endpoint implementation and canonical gateway composition now exist.

### Non-progress

No real model response or provider-usage custody evidence was produced, so runtime completion does not increase.
"""

VALIDATION_GOAL_SECTION = f"""

---

{VALIDATION_MARKER}

- Governed provider validation PR #1 merged as `e0f58b7a93d702bf8ace048dabf23c1c9f867be0`.
- The committed provider API contract passed 2/2 isolated tests for authenticated generation, identity preservation, SHA-256 receipts, and false authority fields.
- GitHub Actions run `29876624303` failed before exposing steps or logs and remains a separate runner failure.
- Provenance-bound model-intake PR #2 merged as `c0e88681ca69310b8c6e11461a1e8bc3cfb0e933`.
- Model intake passed 2/2 isolated tests for exact manifest/digest installation and fail-closed mismatch handling.
- Provider validation receipt SHA-256: `066fdc2bd44a3ad909431b9b37784a6283471d1baef06becab4f0f3b09dbfc51`.
- Model-intake receipt SHA-256: `35097ab0a58377f686cacfb1e04136baff62851488d889815b47ba29eb6b8cf0`.
- Detailed cycle record: `{VALIDATION_CYCLE}`.

### Current blocker

No provenance-approved real GGUF model and trusted local TLS material have been executed on an authorized StegVerse-controlled machine. Real provider generation, provider-usage persistence/custody/reconstruction, immutable activation, Site activation, and downstream propagation remain unproven.

### Next executable integration step

Install one approved GGUF through the merged bounded intake, start the existing StegVerse provider composition with machine-owned TLS and runtime authentication, and execute one governed request through the canonical gateway and Master-Records path.

### Manual user action requirement

False for routine repository work. Model provenance and machine execution authority remain separate runtime boundaries.
"""

VALIDATION_ACTIVE_SECTION = f"""

---

{VALIDATION_MARKER}

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
- Cycle record: `{VALIDATION_CYCLE}`

### Goal delta

Provider and model-intake contracts advanced to verified. No live provider or activation gate advanced.

### Removals proposed but not performed

None.
"""

OPENAI_GOAL_SECTION = f"""

---

{OPENAI_MARKER}

This section supersedes only the statement that the existing governed provider broker could not communicate with an OpenAI-compatible chat-completions endpoint.

- LLM-adapter PR #30 merged as `190bd1fc5b3b4b956887abf24cb866f4a778032d`.
- `stegverse-v1` remains the default provider protocol.
- The bounded `openai-chat-completions-v1` profile translates the existing governed request into the OpenAI-compatible chat-completions wire format and maps the response back into the existing provider result and receipt path.
- Unknown protocol profiles fail closed.
- Existing endpoint allowlisting, HTTPS enforcement, quota, cost, local usage persistence, custody, reconstruction, receipt, and false-authority boundaries remain in force.
- Complete validation run `29880129933` and Architecture Guard run `29880129953` passed.
- Detailed cycle record: `{OPENAI_CYCLE}`.

### Current blocker

No OpenAI-compatible provider has been authorized for execution. The GitHub Models candidate requires `models: read` permission and an explicit model selection. The authorized-provider receipt also reports that Master-Records endpoint and token bindings are absent.

### Next executable integration step

After explicit authority approval, bind the existing live-activation workflow to an authorized OpenAI-compatible provider and execute one governed request. For the GitHub Models candidate, the bounded decision is whether to grant `models: read` and which model to select. Retain the first exact provider, usage, custody, reconstruction, or activation failure.

### Manual user action requirement

False for routine repository work. A provider-execution permission and model-selection decision is required before the GitHub Models candidate can be activated.
"""

OPENAI_ACTIVE_SECTION = f"""

---

{OPENAI_MARKER}

### Work performed

- Reused and extended the existing governed provider broker instead of creating a provider service or executor.
- Added a bounded OpenAI-compatible request/response profile.
- Preserved the default StegVerse provider contract and all existing runtime controls.
- Added fail-closed tests for missing choices and unsupported protocols.

### Components modified

- `StegVerse-org/LLM-adapter/llm_adapter/governed_provider.py`
- `StegVerse-org/LLM-adapter/tests/test_governed_provider.py`

### Runtime evidence

- Merge: `190bd1fc5b3b4b956887abf24cb866f4a778032d`
- Complete validation: `29880129933`
- Architecture Guard: `29880129953`

### State classification

- OpenAI-compatible provider profile: IMPLEMENTED, INTEGRATED, VERIFIED BY TESTS
- Real OpenAI-compatible provider call: UNPROVEN
- Provider usage persistence/custody/reconstruction from real use: UNPROVEN
- Immutable activation, Site activation, and propagation: UNPROVEN

### Removals proposed but not performed

The accidental root-level `StegVerse-org/LLM-adapter/noop` file is proposed for deletion only after explicit approval. It contains only `noop`, has no dependencies or runtime effect, and can be restored by recreating the file or reverting the future deletion commit. No removal was performed.

### Goal delta

The canonical broker can now consume an OpenAI-compatible provider protocol without duplicating provider, usage, custody, or receipt systems.

### Reuse delta

Existing broker, quota/cost enforcement, provider receipt, usage ledger, custody clients, activation workflow, and validation suite replaced the need for a separate adapter service.

### Non-progress

No model-execution permission was granted, no model was selected, and no real provider call occurred.

### Next executable step

Present and resolve the bounded provider-execution decision, then run the existing activation path and retain the first exact failure.
"""


def append_once(path: Path, marker: str, section: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return False
    path.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return True


def main() -> int:
    changed = [
        append_once(GOAL, MARKER, GOAL_SECTION),
        append_once(ACTIVE, MARKER, ACTIVE_SECTION),
        append_once(GOAL, VALIDATION_MARKER, VALIDATION_GOAL_SECTION),
        append_once(ACTIVE, VALIDATION_MARKER, VALIDATION_ACTIVE_SECTION),
        append_once(GOAL, OPENAI_MARKER, OPENAI_GOAL_SECTION),
        append_once(ACTIVE, OPENAI_MARKER, OPENAI_ACTIVE_SECTION),
    ]
    print(f"ECOSYSTEM CHAT PROVIDER NODE STATE SYNC: {'UPDATED' if any(changed) else 'UNCHANGED'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
