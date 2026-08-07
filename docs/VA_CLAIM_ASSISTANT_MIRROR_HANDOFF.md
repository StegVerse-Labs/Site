# VA Claim Assistant Mirror Handoff

## Identity and authority

```text
Goal ID: SV-VA-DUAL-FLOW-001
Active continuation goal: SV-VA-COORDINATED-LLM-002
Final planned goal: SV-VA-SECURE-DOCUMENTS-003
Originating session goal: replace text-heavy VA claims guidance with IKEA-style instructions for veterans who are uncomfortable online
Repository: StegVerse-Labs/Site
Branch: main
Canonical issue: StegVerse-Labs/Site#113
Document module issue: StegVerse-Labs/Site#116
LLM runtime owner: StegVerse-org/LLM-adapter#90
Canonical handoff: docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
Repository collision authority: docs/SITE_MIRROR_HANDOFF.md and data/site-orchestration-state.json
Public instruction page: va-disability-claim-guide.html
Focused walkthrough: va-claims-guided-workflow.html
Help surface: va-claims-chat.html
```

No guide, walkthrough, chat, validator, receipt, deployment, provider output, or custody record grants authority to adjudicate, diagnose, rate, sign, represent, or file a claim. The veteran retains submission authority.

## Required goal sequence

```text
GOAL 1 — COMPLETE: IKEA-style dual-flow instruction system
GOAL 2 — ACTIVE: coordinated VA Resources LLM
GOAL 3 — QUEUED FINAL: secure document retrieval and upload modules
```

Goal 2 must be activated before Goal 3 becomes the active public implementation target. Goal 3 interfaces and safety contracts may be developed without activation, but public upload and private retrieval remain disabled until both the coordinated LLM and document-module exit gates are proven.

## Goal 1 — completed presentation system

The veteran-facing instruction path follows `SEE -> DO -> CONFIRM`: one visual, a few action words, DONE, and optional focused help. The primary instruction page preserves all steps and completion state; the walkthrough opens the matching selected step and shares the same state.

| Task ID | Requirement | State | Evidence |
|---|---|---|---|
| SV-VA-DF-001 | Remove internal telemetry and text-heavy primary copy | COMPLETE | `9a6d69c902d47382ebf58b5997869b6e77c0ea73`, `5f1188287283afa1ce8fac66211610e82ece7604` |
| SV-VA-DF-002 | All six cards on one primary page | COMPLETE | `5f1188287283afa1ce8fac66211610e82ece7604` |
| SV-VA-DF-003 | DONE, dimming, summary, reset | COMPLETE | `5f1188287283afa1ce8fac66211610e82ece7604` |
| SV-VA-DF-004 | Help routes to exact step | COMPLETE | six `?step=N` routes |
| SV-VA-DF-005 | Focused one-step walkthrough | COMPLETE | `1fdf7e52edc8e0d53918411626ed41e2e642ce9d` |
| SV-VA-DF-006 | Shared persistent completion state | COMPLETE | `vaClaimsStepStateV1` |
| SV-VA-DF-007 | Return / continue-help controls | COMPLETE | `1fdf7e52edc8e0d53918411626ed41e2e642ce9d` |
| SV-VA-DF-008 | Automated dual-flow validation | COMPLETE / MACHINE_OWNED | run `31134444619` PASS |
| SV-VA-DF-009 | Retained validation receipt | COMPLETE / MACHINE_OWNED | artifact `8977344125`, `sha256:84cf875ef5028cd1ddfe17d95d37c0184537654c6cec44bc7a3e43bf3dce3481` |
| SV-VA-DF-010 | Public activation of instruction pages | COMPLETE / MACHINE_OWNED | GitHub Pages deployment `5786525421` success |

## Goal 2 — coordinated VA Resources LLM

```text
Goal ID: SV-VA-COORDINATED-LLM-002
Canonical runtime owner: StegVerse-org/LLM-adapter#90
Site projection owner: StegVerse-Labs/Site#113
Provider preflight repair: COMPLETE / RELEASED
Permission-bearing provider execution: BLOCKED by VACP-ADAPTER-AUTHORIZED-EXECUTION-005
Site bridge implementation: COMPLETE / RELEASED_IMPLEMENTED_PENDING_RUNTIME_ACTIVATION
Public coordinated LLM activation: INCOMPLETE
```

### Canonical runtime capability already implemented

`StegVerse-org/LLM-adapter` already owns the VA Claims Chat profile, provider-neutral session shape, deterministic route classifier, governed route generators, admitted-source filtering, citation/provenance fields, privacy guards, execution-evidence schema, and runtime contract. The adapter rejects raw veteran documents; `document_organization` accepts only sanitized derived context from Site#116.

Canonical adapter records:

```text
StegVerse-org/LLM-adapter#90
docs/VA_CLAIM_ASSISTANT_GOVERNED_RETRIEVAL_HANDOFF.md
docs/VA_CLAIMS_CHAT_RUNTIME_MIRROR_HANDOFF.md
tasks/VACP-ADAPTER-AUTHORIZED-EXECUTION-005.json
```

### Provider preflight repair — completed and activated

PR `StegVerse-org/LLM-adapter#120` is merged. Its hosted-path defect was repaired without weakening provider boundaries.

```text
validator repair commit: 8864b77d867b5be13fbddb46172be1081b373325
PR merge commit: 8fb86f92f70f23c1042d4f2eb782e1a3a6797b65
PR hosted-path run: 31135075848 — SUCCESS
PR canonical preflight run: 31135075851 — SUCCESS
PR artifact: 8977604080
PR artifact digest: sha256:4f5a4910e1b38f0338cc810057c1ddd55e982c670bf41747ac7102be2a3a7367
main canonical preflight run: 31136792639 — SUCCESS
main admission job: 92737815150 — SUCCESS
main preflight job: 92737868886 — SUCCESS
main final artifact: 8978250994
main final artifact digest: sha256:d88c07cff1f7b58fe34e0921ef0098b55e5d35df18ea2d729fb62701f4688ce3
main admission artifact: 8978245231
main admission artifact digest: sha256:c0796e64aa11d4e58283a3c9bd6dd326a4b582ac7493e730b9e14222186df9c9
released task commit: acaed090dab900541d65289c8e0daa7e62b645b8
```

Preflight state remains correctly `CONFIGURATION_REQUIRED`; that is not a preflight failure. Provider permission was not requested and provider execution was not observed.

### Permission-bearing execution lane — blocked by explicit authority

Canonical task:

`StegVerse-org/LLM-adapter/tasks/VACP-ADAPTER-AUTHORIZED-EXECUTION-005.json`

The task is `BLOCKED`, claimant null. Its release condition requires all of the following in the authorized runtime:

1. hosted preflight `READY_FOR_EXPLICIT_AUTHORIZED_EXECUTION` with `GITHUB_ACTIONS_WORKFLOW` observation;
2. protected `STEGVERSE_MASTER_RECORDS_ENDPOINT` binding;
3. protected `STEGVERSE_MASTER_RECORDS_ALLOWED_HOSTS` binding;
4. protected `STEGVERSE_MASTER_RECORDS_TOKEN` binding;
5. a valid, unexpired VA-specific provider authority receipt for the exact caller commit;
6. fresh single-use TVC admission;
7. hosted PII runtime PASS.

Only after those conditions may its workflow-dispatch-only lane request `models: read`, execute at most one provider request with maximum cost USD 0.10, and write the privacy-minimized execution receipt. Credentials or configuration presence alone are not authority.

### Site runtime bridge — implemented fail-closed

Task:

`data/tasks/SITE-VA-COORDINATED-LLM-BRIDGE-002.json`

Canonical PR: `StegVerse-Labs/Site#175`. Closed unmerged PR #174 is superseded by #175 because the original branch did not map to the repository root handoff workload. PR #175 is a VA-specific slice of the canonical Site workload:

`Accept canonical events from the governed gateway instead of constructing them from DOM messages`

Installed surfaces:

```text
va-claims-chat.html
assets/va-claims-chat-runtime.js
api/va-claim-assistant/runtime-projection.json
scripts/validate_va_claims_chat_llm_bridge.py
.github/workflows/va-claims-chat-llm-bridge.yml
data/tasks/SITE-VA-COORDINATED-LLM-BRIDGE-002.json
```

Behavior:

- guided-card help remains local and deterministic;
- general questions can cross the runtime bridge only after the projection is receipt-verified;
- current projection is `BLOCKED`, `active=false`, `endpoint=null`;
- verified activation requires HTTPS endpoint, valid activation and execution receipt hashes, custody `RECORDED`, reconstruction `PASS`, evidence references, and all authority/document/filing flags false;
- invalid or unavailable projection cannot make a governed runtime call;
- browser sends no private-document context and requests no filing;
- credentials are omitted from browser fetch;
- responses claiming authority or activation effects are rejected;
- private document upload, private retrieval, and filing remain disabled.

Pre-release validation evidence for PR #175:

```text
bridge workflow run: 31137334846 — SUCCESS
bridge artifact: 8978452539
bridge artifact digest: sha256:af2c2dc82a305552aee52d91e626f2165662d11274f464a8be020f56e4084765
Site handoff orchestrator run: 31137334825 — SUCCESS
orchestrator job: 92739572284 — SUCCESS
VA guided workflow run: 31137334893 — SUCCESS
Site Bootstrap Validate run: 31137335003 — SUCCESS
ST-017 job: 92739532937 — SUCCESS
bootstrap job: 92739568601 — SUCCESS
```

The implementation claim is released as `RELEASED_IMPLEMENTED_PENDING_RUNTIME_ACTIVATION`. Merge and merged-main verification remain required before this Site slice is considered integrated.

### Goal 2 activation gates

Goal 2 is activated only when all are true:

1. a real provider-backed VA request completes through the governed adapter;
2. the request is classified into a governed VA route;
3. external factual support uses admitted official VA sources only;
4. response evidence preserves proposition-level citations, authority classes, retrieval/effective dates, contradiction/uncertainty labeling, and false-authority flags;
5. provider execution emits a stable privacy-minimized secret-free receipt;
6. Master Records returns custody `RECORDED` and reconstruction `PASS` for real execution evidence;
7. a dedicated HTTPS VA runtime endpoint is receipt-verified;
8. Site runtime projection is changed from BLOCKED to VERIFIED only from those receipts;
9. public `va-claims-chat.html` uses the governed runtime for general questions;
10. one deployed Site -> adapter -> Site question is directly observed and receipt-correlated.

The existing generic Ecosystem Chat gateway is not a substitute for the VA-specific endpoint because it exposes a different routing/request contract.

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

Required modules and exit gates:

- consent-bound upload intake;
- malware/type/size validation;
- encrypted temporary storage with retention and deletion state;
- stable file hash and document index;
- page-level extraction and citation anchors;
- privacy classification and redaction controls;
- user-record facts separated from inference and official authority;
- favorable, unfavorable, conflicting, and unresolved evidence retained;
- secure retrieval scoped to the active veteran session;
- contradiction and missing-evidence views;
- custody and reconstruction references;
- deterministic receipts and fail-closed public activation;
- representative multi-document fixture with stable hashes and page citations;
- deployed runtime receipt before upload controls become public.

Issue `StegVerse-Labs/Site#116` remains the canonical document implementation owner. Goal 3 must not expose a public upload control merely because interfaces, schemas, or fixtures exist.

## Claims, convergence, and ownership

```text
Dual-flow presentation implementation: COMPLETE / RELEASED
Dual-flow validation and deployment: COMPLETE / MACHINE_OWNED
LLM profile / route / source-grounding layers: COMPLETE or IMPLEMENTED in LLM-adapter#90
Hosted provider preflight repair: COMPLETE / RELEASED
Permission-bearing provider execution: BLOCKED / UNCLAIMED until explicit release conditions clear
Site runtime bridge implementation: COMPLETE / RELEASED_IMPLEMENTED_PENDING_RUNTIME_ACTIVATION
Site runtime bridge integration: PR #175 pending merge/main verification
Coordinated VA LLM activation: INCOMPLETE
Secure document modules: QUEUED under Site#116
Automated filing: INACTIVE / FAIL-CLOSED
```

Do not create a competing provider-execution lane, infer provider authority, expose secret values, replace Master Records custody with local persistence, or use the generic Ecosystem Chat endpoint as VA activation evidence.

## Machine-owned continuation

```text
Site bridge validator: .github/workflows/va-claims-chat-llm-bridge.yml
Root Site admission/ownership guard: scripts/site_handoff_orchestrator.py
Site canonical validation: Site Bootstrap Validate workflow
Adapter provider preflight: .github/workflows/va-claim-assistant-provider-preflight.yml
Adapter authorized execution: tasks/VACP-ADAPTER-AUTHORIZED-EXECUTION-005.json (blocked until exact release condition)
Runtime implementation owner: StegVerse-org/LLM-adapter#90
Site projection owner: StegVerse-Labs/Site#113
Secure document owner after Goal 2 activation: StegVerse-Labs/Site#116
Custody/reconstruction owner: master-records/orchestration#15 for expanded-route execution evidence
```

## Requirements transferred from the originating session

- IKEA-style main path: see one thing, do one thing, confirm one thing;
- more than a few words belongs outside the primary instruction path;
- all steps visible on the primary page;
- DONE and Help me with this on every step;
- DONE dims the card and brightens completion;
- help opens the same step in a focused walkthrough;
- walkthrough returns to instruction or continues into step-specific help;
- both pages share persistent completion state;
- the chat must become a coordinated VA Resources LLM rather than remain browser-scripted;
- coordinated LLM is Goal 2;
- secure document retrieval/upload is the final Goal 3;
- external VA facts require admitted official VA support;
- document upload and retrieval remain off while Goal 2 is unverified;
- activation must be proven independently from file presence, tests, workflow success, or deployment presence.

`MERGED INTO: StegVerse-Labs/Site/docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`

## Current executable inventory

| Task | Owner/location | Claim state | Completion | Validation | Integration | Next executable action |
|---|---|---|---|---|---|---|
| Dual-flow veteran instructions | Site public pages | RELEASED_COMPLETE | COMPLETE | PASS | DEPLOYED | machine regression validation |
| Hosted VA preflight repair | LLM-adapter task `VACP-PREFLIGHT-HOSTED-EXECUTION-008` | RELEASED_COMPLETE | COMPLETE | hosted/main PASS | COMPLETE | regression observation |
| Authorized single VA provider request | LLM-adapter `VACP-ADAPTER-AUTHORIZED-EXECUTION-005` | BLOCKED / unclaimed | NOT STARTED | preconditions partially proven | NOT INTEGRATED | execute only when its machine release condition becomes true |
| Site coordinated-LLM bridge | Site task `SITE-VA-COORDINATED-LLM-BRIDGE-002`, PR #175 | RELEASED_IMPLEMENTED_PENDING_RUNTIME_ACTIVATION | IMPLEMENTED | PR checks PASS | PR MERGE PENDING | merge after updated-head checks, verify main |
| Runtime projection activation | `api/va-claim-assistant/runtime-projection.json`, Site#113 | BLOCKED | NOT ACTIVE | fail-closed validator PASS | NOT INTEGRATED | bind only verified runtime receipts/endpoints |
| Deployed Site-to-VA-runtime observation | Site#113 + LLM-adapter#90 | BLOCKED | MISSING | NOT OBSERVED | NOT INTEGRATED | execute after projection VERIFIED |
| Secure document modules | Site#116 | QUEUED | PARTIAL CONTRACTS ONLY | NOT RELEASED | NOT ACTIVE | become active after Goal 2 activation |

## Archive conditions and measures

This session is not archive-ready. The original presentation goal is fully durable, but active Goal 2 still requires real authorized provider execution, custody/reconstruction, a verified VA endpoint, Site projection activation, and deployed end-to-end observation. Final Goal 3 remains queued and incomplete.

Deleting this thread now would remove an active execution lane while PR #175 still requires merge/main validation and before the final document goal is completed or activated through its durable owner.

```text
Goal 1 presentation: COMPLETE
Goal 2 coordinated LLM: ACTIVE / NOT ACTIVATED
Goal 3 secure documents: QUEUED / NOT ACTIVATED
session requirement transfer: COMPLETE
session consolidation: ACTIVE / NOT ARCHIVE-READY
```
