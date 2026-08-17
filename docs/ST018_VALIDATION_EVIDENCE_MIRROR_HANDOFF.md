# ST-018 Validation Evidence Mirror Handoff

## Canonical authority

```text
goal_id: SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817
repository: StegVerse-Labs/Site
canonical_branch: main
active_branch: claim/site-st018-github-token-retirement-20260817
canonical_issue: Site#141
parent_cleanup: Site#268
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_actions_runtime_control_plane_authority: NONE
claim_state: CLAIMED_FOR_IMPLEMENTATION
implementation_state: IMPLEMENTED_PENDING_VALIDATION
```

ST-018 deterministic source contract remains `validation_manifests/repository-core.json`, `schemas/validation-execution-receipt.schema.json`, and `scripts/capture_validation_manifest.py`.

## Installed correction

`.github/workflows/capture-validation-evidence.yml` is credential-clean deterministic validation only:

```text
permissions: {}
actions/checkout: REMOVED
actions/setup-python: REMOVED
actions/upload-artifact: REMOVED
issues: write: REMOVED
GH_TOKEN/github.token: REMOVED
issue mutation: REMOVED
anonymous exact-SHA public source fetch: INSTALLED
credential-bearing environment refusal: INSTALLED
deterministic manifest execution: RETAINED
local ephemeral receipt enforcement: RETAINED
custody authority: NONE
```

GitHub-hosted validation remains non-authorizing and does not prove factual truth, admissibility, publication, deployment, release, standing, certification, runtime activation, HIL activation, StegFin execution, or wallet authority.

## Release requirements

`ST018_CREDENTIAL_REFUSAL=PASS`, `ST018_SOURCE_FETCH=PASS`, `ST018_VALIDATION=PASS`, `SESSION_WORK_CLAIMS_PASS`, Site Handoff PASS, Ecosystem Heartbeat PASS, Site Bootstrap PASS, StegFin projection PASS, exact-head merge, claim release, Site #141 reconciliation, and cost-containment handoff update.

Do not restore a GitHub/project/provider token merely to make validation pass. TV/TVC remains credential authority; USER_ONLY remains sole StegFin signer/broadcaster; do not use Render.
