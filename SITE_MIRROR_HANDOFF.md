# Site Mirror Handoff

## Current source of truth

This file is the documentation mirror handoff source of truth for `StegVerse-Labs/admissibility-wiki/docs/` until superseded.

## Active goal

Goal 3: Governed LLM end-to-end demonstrator public documentation and Site mirror sync.

The Site documentation layer should reflect the governed LLM demonstrator only after the runtime and SDK handoffs are present:

```text
StegVerse-org/LLM-adapter/LLM_ADAPTER_MIRROR_HANDOFF.md
StegVerse-org/StegVerse-SDK/STEGVERSE_SDK_MIRROR_HANDOFF.md
StegVerse-Labs/admissibility-wiki/ADMISSIBILITY_MIRROR_HANDOFF.md
StegVerse-Labs/admissibility-wiki/docs/SITE_MIRROR_HANDOFF.md
```

## Current proof path

```text
fixture query
-> LLM-adapter governed session packet
-> SDK validation
-> SDK intake routing
-> SDK manifest binding
-> SDK receipt handoff
-> wiki public demo overview
-> Site navigation and deployment verification
```

## Source repositories

```text
StegVerse-org/LLM-adapter
  -> runtime demonstrator source
  -> emits governed session demo packet

StegVerse-org/StegVerse-SDK
  -> SDK intake and receipt handoff verification source
  -> validates demo packet and binds receipt handoff

StegVerse-Labs/admissibility-wiki
  -> public doctrine, demo overview, verification, deployment status, and archive handoff
```

## Existing governed LLM Site pages

```text
docs/governance/governed-llm-reconstructive-search.md
docs/governance/governed-llm-activation-map.md
docs/governance/governed-llm-site-verification.md
docs/governance/governed-llm-deployment-status.md
docs/governance/governed-llm-archive-handoff.md
```

## Files authorized for Goal 3 Site mirror work

```text
docs/governance/governed-llm-demo-overview.md
docs/governance/governed-llm-demo-verification.md
scripts/check_governed_llm_demo_docs.py
sidebars.js update
README.md update
```

## Required invariant

```text
site_claims_live_provider_governance == false
site_claims_execution_authority == false
site_claims_external_indexing == false
site_claims_master_record_persistence == false
demo_is_fixture_first == true
adapter_and_sdk_remain_source_of_implementation_truth == true
```

## Local verification commands

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
npm run build
```

## Deployment verification command

```bash
python scripts/check_governed_llm_deployment_status.py
```

Expected deployed result after Pages publishes:

```text
GOVERNED LLM DEPLOYMENT: PASS - deployed pages reachable
```

## Boundary

```text
Site mirror publication is not provider governance.
Site mirror publication is not execution authority.
Site mirror publication is not commit-time standing.
Site mirror publication is not master-record persistence.
Site mirror publication is not external indexing.
```

## Installation order

```text
1. Confirm LLM_ADAPTER_MIRROR_HANDOFF.md is installed in LLM-adapter.
2. Confirm STEGVERSE_SDK_MIRROR_HANDOFF.md is installed in StegVerse-SDK.
3. Confirm ADMISSIBILITY_MIRROR_HANDOFF.md is installed in admissibility-wiki.
4. Install or update this SITE_MIRROR_HANDOFF.md in docs/.
5. Install governed LLM demo overview and verification pages.
6. Update sidebar and README references.
7. Run local verification.
8. Run deployment verification after Pages publishes.
```

## Current archive posture

Not archive-ready until the governed LLM demo overview and demo verification pages are installed, linked in navigation, and locally verified.

Once local verification passes, the Site mirror work may be archived as repo-local complete, with deployed GitHub Pages confirmation tracked separately.
