# VA Claim Assistant Mirror Handoff

## Identity

```text
Goal family: SV-VA
Originating session goal: replace text-heavy VA claims guidance with IKEA-style veteran instructions
Repository: StegVerse-Labs/Site
Branch: main
Canonical issue: StegVerse-Labs/Site#113
Final document-module issue: StegVerse-Labs/Site#116
Canonical runtime owner: StegVerse-org/LLM-adapter#90
Custody/reconstruction owner: master-records/orchestration
Canonical handoff: docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
```

No surface, model output, receipt, custody record, deployment, or validator grants authority to adjudicate, diagnose, rate, represent, sign, or file a VA claim. Veteran submission authority remains preserved.

## Required goal sequence

```text
GOAL 1 — SV-VA-DUAL-FLOW-001 — COMPLETE
GOAL 2 — SV-VA-COORDINATED-LLM-002 — ACTIVE
GOAL 3 — SV-VA-SECURE-DOCUMENTS-003 — QUEUED FINAL
```

Goal 2 must activate before Goal 3 becomes the active public implementation target. Goal 3 contracts may advance without exposing upload or retrieval controls.

## Authoritative files and surfaces

```text
va-disability-claim-guide.html
va-claims-guided-workflow.html
va-claims-chat.html
assets/va-claims-chat-runtime.js
api/va-claim-assistant/runtime-projection.json
data/va-claim-assistant/chat-capability-state.json
data/tasks/SITE-VA-COORDINATED-LLM-BRIDGE-002.json
scripts/validate_va_claims_chat_llm_bridge.py
scripts/validate_va_claims_chat_surface.py
.github/workflows/va-claims-chat-llm-bridge.yml
.github/workflows/va-claims-chat-surface.yml
```

## Goal 1 — completed IKEA-style instruction system

The veteran-facing main path is `SEE -> DO -> CONFIRM`: one visual, a few action words, DONE, and optional focused help. The primary page shows all six steps, persists `vaClaimsStepStateV1`, dims completed cards, and routes Help to the exact selected walkthrough step. The walkthrough shows one selected step, shares completion state, returns to the instruction page, or continues into step-specific help.

Evidence:

```text
primary checklist/shared state: 5f1188287283afa1ce8fac66211610e82ece7604
focused walkthrough: 1fdf7e52edc8e0d53918411626ed41e2e642ce9d
dual-flow validation run: 31134444619 — PASS
validation artifact: 8977344125
artifact digest: sha256:84cf875ef5028cd1ddfe17d95d37c0184537654c6cec44bc7a3e43bf3dce3481
GitHub Pages deployment: 5786525421 — success
```

Claim state: `RELEASED_COMPLETE`.

## Goal 2 — coordinated VA Resources LLM

### Canonical runtime owner

`StegVerse-org/LLM-adapter#90` owns the governed VA runtime: route classification, admitted VA-source retrieval, source/citation fields, privacy guard, provider execution, execution receipts, and provider-side runtime behavior.

Canonical runtime records:

```text
StegVerse-org/LLM-adapter/docs/VA_CLAIM_ASSISTANT_GOVERNED_RETRIEVAL_HANDOFF.md
StegVerse-org/LLM-adapter/docs/VA_CLAIMS_CHAT_RUNTIME_MIRROR_HANDOFF.md
StegVerse-org/LLM-adapter/tasks/VACP-ADAPTER-AUTHORIZED-EXECUTION-005.json
StegVerse-org/LLM-adapter/receipts/va-claim-assistant-provider-execution-preflight.json
```

The adapter rejects raw veteran documents. `document_organization` may later consume only sanitized derived context from Site#116.

### Provider preflight — COMPLETE / RELEASED

PR `StegVerse-org/LLM-adapter#120` is merged.

```text
validator repair: 8864b77d867b5be13fbddb46172be1081b373325
PR merge: 8fb86f92f70f23c1042d4f2eb782e1a3a6797b65
focused hosted run: 31135075848 — SUCCESS
main preflight run: 31136792639 — SUCCESS
released task commit: acaed090dab900541d65289c8e0daa7e62b645b8
```

Latest preflight observation is repository-native and fail-closed. Fresh TVC admission works. Provider permission was not requested and provider execution was not observed.

### Authorized provider execution — BLOCKED / UNCLAIMED

Canonical task:

`StegVerse-org/LLM-adapter/tasks/VACP-ADAPTER-AUTHORIZED-EXECUTION-005.json`

Current release blockers are authoritative:

```text
protected Master Records allowed-host binding missing
protected Master Records endpoint binding missing
protected Master Records token binding missing
valid unexpired exact-caller VA provider authority missing
```

The latest hosted preflight already proves `GITHUB_ACTIONS_WORKFLOW` observation and fresh single-use TVC admission. The task may not be claimed or executed until every protected configuration and authority condition is true in the authorized runtime. Credential/configuration presence alone is not authority.

When released, that workflow-dispatch-only lane may request `models: read`, perform at most one provider request with maximum cost USD 0.10, write a privacy-minimized execution receipt, and transfer execution/privacy evidence to Master Records and Site#113.

### Site runtime bridge — COMPLETE / MERGED / DEPLOYED FAIL-CLOSED

Task: `data/tasks/SITE-VA-COORDINATED-LLM-BRIDGE-002.json`.

PR `StegVerse-Labs/Site#175` is merged to `main`.

```text
merge commit: a92fe510602678b54381c2bb34fe0e35e50ad1d9
bridge implementation head: 430167614417c7fde39709afbb8a9d0ed2a46482
premerge bridge run: 31137334846 — SUCCESS
premerge Site orchestrator run: 31137334825 — SUCCESS
premerge guided workflow run: 31137334893 — SUCCESS
premerge Site bootstrap run: 31137335003 — SUCCESS
```

The first merged-main `VA Claims Chat surface` run `31138834894` failed because its legacy validator required retired governance-heavy copy and visible disabled controls. The user-facing page was not reverted. The validator was repaired to enforce the new fail-closed runtime contract:

```text
validator repair commit: a9cb6487a3e7799b7dfd66ffa4a0cc193ea16408
VA Claims Chat surface run: 31139914262 — SUCCESS
Render service: stegverse-va-claim-guide
Render deploy: dep-d9qjp0j7uimc73fks6t0 — live
Render deployed commit: a9cb6487a3e7799b7dfd66ffa4a0cc193ea16408
```

The Site bridge is therefore integrated and deployed, but the coordinated LLM itself remains inactive. Direct canonical-domain runtime observation from the current execution environment was unavailable because DNS resolution failed; deployment evidence must not be misreported as end-to-end runtime activation.

Current projection remains intentionally:

```text
state: BLOCKED
active: false
endpoint: null
private_document_upload_active: false
private_document_retrieval_active: false
filing_active: false
authority_effect: false
activation_effect: false
```

General questions can cross the browser bridge only after the projection becomes receipt-verified. Guided-card assistance remains local and deterministic while blocked.

### Goal 2 activation gates

All ten are required:

1. one real provider-backed VA request completes through the governed adapter;
2. request is classified into a governed VA route;
3. external factual claims use admitted official VA sources only;
4. response preserves proposition-level citations, source authority classes, retrieval/effective dates, contradiction/uncertainty labels, and false-authority flags;
5. provider execution emits a stable privacy-minimized secret-free receipt;
6. Master Records custody returns `RECORDED` and reconstruction `PASS` for real execution evidence;
7. a dedicated HTTPS VA runtime endpoint is receipt-verified;
8. Site projection changes from BLOCKED to VERIFIED only from those receipts;
9. public `va-claims-chat.html` uses that governed runtime for general questions;
10. one deployed Site -> adapter -> Site question is directly observed and receipt-correlated.

The generic Ecosystem Chat endpoint is not accepted as VA activation evidence unless it satisfies the VA-specific request, routing, source, receipt, custody, and projection contract.

## Goal 3 — secure document retrieval and upload modules

```text
Goal ID: SV-VA-SECURE-DOCUMENTS-003
Canonical Site owner: StegVerse-Labs/Site#116
Runtime privacy/retrieval dependency: StegVerse-org/LLM-adapter
Custody/reconstruction dependency: master-records/orchestration
State: QUEUED_FINAL
Public upload: DISABLED
Private retrieval: DISABLED
```

Required exit inventory:

```text
consent-bound upload intake
malware/type/size validation
encrypted temporary storage with retention/deletion state
stable file hash and document index
page-level extraction and citation anchors
privacy classification and redaction controls
user-record facts separated from inference and official authority
favorable, unfavorable, conflicting, and unresolved evidence retention
session-scoped secure retrieval
contradiction and missing-evidence views
custody and reconstruction references
deterministic fail-closed receipts
representative multi-document fixture with stable hashes/page citations
deployed runtime receipt before public upload activation
```

## Execution inventory

| Task | Owner / location | Claim state | Completion | Validation | Integration | Next executable action |
|---|---|---|---|---|---|---|
| IKEA dual-flow instructions | Site public pages | RELEASED_COMPLETE | COMPLETE | PASS | DEPLOYED | machine regression observation |
| Hosted provider preflight | LLM-adapter preflight task | RELEASED_COMPLETE | COMPLETE | hosted/main PASS | COMPLETE | regression observation |
| Site coordinated-LLM bridge | Site `SITE-VA-COORDINATED-LLM-BRIDGE-002` | RELEASED_COMPLETE_PENDING_RUNTIME_ACTIVATION | COMPLETE | PASS | MERGED + RENDER DEPLOYED | consume verified runtime evidence when available |
| Authorized single provider execution | LLM-adapter `VACP-ADAPTER-AUTHORIZED-EXECUTION-005` | BLOCKED / claimant null | NOT EXECUTED | preflight proves remaining blockers | NOT INTEGRATED | protected config + exact provider authority must become true |
| Runtime projection activation | Site `api/va-claim-assistant/runtime-projection.json` | BLOCKED | NOT ACTIVE | fail-closed PASS | NOT ACTIVE | bind only real execution/custody receipts and HTTPS endpoint |
| Deployed end-to-end VA chat observation | Site#113 + LLM-adapter#90 | BLOCKED | MISSING | NOT OBSERVED | NOT INTEGRATED | execute after projection VERIFIED |
| Secure document modules | Site#116 | QUEUED | PARTIAL CONTRACTS ONLY | NOT RELEASED | NOT ACTIVE | becomes active after Goal 2 activation |

## Active claims and collision boundaries

```text
Site bridge implementation claim: RELEASED
Provider execution task claimant: null while BLOCKED
Goal 2 runtime owner: StegVerse-org/LLM-adapter#90
Goal 2 Site projection owner: StegVerse-Labs/Site#113
Goal 3 owner: StegVerse-Labs/Site#116
```

Do not create a competing provider-execution lane, infer provider authority, expose secret values, replace Master Records custody with local persistence, enable upload/retrieval early, or treat deployment success as runtime activation.

## Machine-owned continuation

```text
Site bridge validator: .github/workflows/va-claims-chat-llm-bridge.yml
Site surface validator: .github/workflows/va-claims-chat-surface.yml
Root Site ownership guard: scripts/site_handoff_orchestrator.py
Site canonical validation: Site Bootstrap Validate
Adapter provider preflight: .github/workflows/va-claim-assistant-provider-preflight.yml
Adapter authorized execution task: VACP-ADAPTER-AUTHORIZED-EXECUTION-005
Runtime owner: StegVerse-org/LLM-adapter#90
Projection owner: StegVerse-Labs/Site#113
Final secure-document owner: StegVerse-Labs/Site#116
Custody/reconstruction owner: master-records/orchestration
```

## Validation commands / deterministic checks

```text
python scripts/validate_va_claims_chat_llm_bridge.py
python scripts/validate_va_claims_chat_surface.py
python scripts/check_va_claim_guide.py
python scripts/site_handoff_orchestrator.py
```

Hosted workflow/job evidence is authoritative over local claims when available.

## Integration and propagation obligations

Goal 2 requires propagation only after real runtime execution evidence exists:

```text
LLM-adapter execution receipt -> master-records/orchestration custody/reconstruction
LLM-adapter verified runtime evidence -> StegVerse-Labs/Site#113 runtime projection
Site verified projection -> deployed VA Claims Chat observation
```

No Publisher, admissibility-wiki, or stegguardian-wiki propagation is required for this VA presentation/runtime milestone unless a live contract later names those consumers.

## Session-specific requirements transferred

```text
IKEA-style main path: see one thing, do one thing, confirm one thing
few words only on primary instructions
all steps visible on primary page
DONE + Help me with this per step
DONE dims card and brightens completion
help opens exact walkthrough step
walkthrough returns to instruction or continues help
shared completion state
chat must become coordinated VA Resources LLM, not remain scripted
coordinated LLM is Goal 2
secure document retrieval/upload is final Goal 3
official VA facts require admitted authoritative support
upload/retrieval remain disabled until their gates pass
activation must be proven independently from file/test/workflow/deployment presence
```

`MERGED INTO: StegVerse-Labs/Site/docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`

## Archive conditions

This session is not archive-ready. Goal 1 is complete, but Goal 2 still requires protected-authority release, real provider execution, custody/reconstruction, verified HTTPS VA runtime projection, and deployed end-to-end observation. Goal 3 remains queued and incomplete.

The session may be archived only after Goal 2 and Goal 3 are completed, explicitly superseded, or fully transferred to durable machine-owned workstreams with no unique session execution responsibility remaining.

## Percentages

Denominator for Goal 2: 10 activation gates listed above.

```text
task completion: 6/10 = 60%
developed-file completion: 10/12 = 83%
validation completion: 8/10 = 80%
integration completion: 5/7 = 71%
propagation completion: 2/4 = 50%
goal activation: 6/10 = 60%
session requirement transfer: 3/3 = 100%
archival readiness: false
```
