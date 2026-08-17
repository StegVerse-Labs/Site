# ST-018 Validation Evidence Mirror Handoff

## Canonical authority

```text
goal_id: SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817
repository: StegVerse-Labs/Site
canonical_branch: main
canonical_issue: Site#141
parent_cleanup: Site#268
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_actions_runtime_control_plane_authority: NONE
claim_state: MERGED_INTO_CANONICAL_WORKSTREAM
implementation_state: COMPLETE_RELEASED
release_pr: #346
release_commit: 69f1f89e09b6b4e4d2d89267d3c148435df9b061
final_head: a16f58fd2f138825f674afb714826b7af91fe331
```

ST-018 deterministic source contract remains `validation_manifests/repository-core.json`, `schemas/validation-execution-receipt.schema.json`, and `scripts/capture_validation_manifest.py`.

## Released correction

`.github/workflows/capture-validation-evidence.yml` is now credential-clean deterministic validation only:

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

Exact release evidence recorded in `data/session-work-claims.json`:

```text
Capture Validation Evidence: 32051470522 SUCCESS
Ecosystem Heartbeat Orchestration: 32051470520 SUCCESS
Site Handoff Orchestrator: 32051470664 SUCCESS
Site Bootstrap Validate: 32051470819 SUCCESS
credential refusal: PASS
exact public source fetch: PASS
declared validator receipt enforcement: PASS
artifact custody: NONE
issue-comment custody: NONE
authority_effect: false
runtime_activation_effect: false
custody_authority_effect: false
```

## Completion-contract correction

The historical Site #141 issue body and older comments named a GitHub-hosted artifact ID/digest and issue-comment custody as completion evidence. Those mechanics are superseded by the current TV/TVC-only credential policy and are not valid authority or completion requirements.

The deterministic ST-018 manifest/schema/receipt validators remain authoritative. GitHub-hosted validation may remain only credential-clean and non-authorizing. Any actual custody must be established by an explicitly authorized StegVerse/Master Records custody contract; it is not inferred from a GitHub artifact, issue comment, source merge, or CI success.

The repository heartbeat contract remains the credential-free machine observation surface where applicable. This release does not claim factual truth, admissibility, publication, deployment, release authority, standing, certification, runtime activation, HIL activation, StegFin execution, or wallet authority.

## Session consolidation

The credential-clean ST-018 remediation is complete and durably transferred to current `main`, `data/session-work-claims.json`, Site #141, and parent cleanup Site #268. No chat-owned implementation or validation claim remains for this remediation.

Any future ST-018 work must start from the then-current handoff/issue state and must not restore GitHub/project/provider tokens or GitHub-hosted custody semantics.
