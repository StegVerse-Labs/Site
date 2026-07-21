#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL = ROOT / "docs" / "ECOSYSTEM_CHAT_BUILD_GOAL.md"
ACTIVE = ROOT / "docs" / "ECOSYSTEM_CHAT_ACTIVE_BUILDING.md"
MARKER = "## StegVerse-owned provider-node update — 2026-07-21"
CYCLE = "docs/ECOSYSTEM_CHAT_ACTIVE_BUILDING_CYCLE_2026-07-21_STEGVERSE_PROVIDER_NODE.md"

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


def append_once(path: Path, section: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    path.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return True


def main() -> int:
    changed = [append_once(GOAL, GOAL_SECTION), append_once(ACTIVE, ACTIVE_SECTION)]
    print(f"ECOSYSTEM CHAT PROVIDER NODE STATE SYNC: {'UPDATED' if any(changed) else 'UNCHANGED'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
