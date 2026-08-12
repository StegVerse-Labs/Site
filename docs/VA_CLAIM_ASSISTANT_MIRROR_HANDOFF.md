# VA Claim Assistant Mirror Handoff

## Identity

```text
Goal family: SV-VA
Originating session goal: replace text-heavy VA claims guidance with a veteran-controlled, stepwise VA Claims Guide plus conversational VA Claims Chat (VACC)
Repository: StegVerse-Labs/Site
Branch: main
Canonical issue: StegVerse-Labs/Site#113
Secure-document owner: StegVerse-Labs/Site#116
Claimant/submission binding contract: StegVerse-Labs/Site#180
Canonical runtime owner: StegVerse-org/LLM-adapter#90
Authorized provider task: StegVerse-org/LLM-adapter/tasks/VACP-ADAPTER-AUTHORIZED-EXECUTION-005.json
Custody/reconstruction owner: master-records/orchestration#15
Canonical handoff: docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
Latest originating-session transfer receipt: docs/receipts/vacc-pcp-timeline-reconciliation-session-transfer-2026-08-12.md
```

No Site surface, model output, receipt, deployment, authentication event, or validator grants authority to adjudicate, diagnose, rate, represent, sign, or file a VA claim. The veteran remains claimant, fact confirmer, certifier, and submission authority unless an independently authorized representative acts within an admitted scope.

## Required goal sequence

```text
GOAL 1 — SV-VA-DUAL-FLOW-001 — COMPLETE
GOAL 2 — SV-VA-COORDINATED-LLM-002 — ACTIVE / BLOCKED AT AUTHORIZED REAL PROVIDER EXECUTION
GOAL 3 — SV-VA-SECURE-DOCUMENTS-003 — QUEUED PUBLIC ACTIVATION / CONTRACTS AND PRIVACY PREPROCESSOR PARTIALLY COMPLETE
GOAL 4 — SV-VA-FINAL-SUBMISSION-FALLBACK-004 — COMPLETE
```

Goal 2 must activate before Goal 3 public private-document controls become active. Goal 3 contracts, synthetic fixtures, privacy preprocessing, and validators may advance while public upload/retrieval/filing remain fail-closed.

## Authoritative Site files and surfaces

```text
va-disability-claim-guide.html
va-claims-guided-workflow.html
va-claims-chat.html
assets/va-claims-chat-runtime.js
api/va-claim-assistant/runtime-projection.json
data/va-claim-assistant/chat-capability-state.json
data/tasks/SITE-VA-COORDINATED-LLM-BRIDGE-002.json
scripts/check_va_claim_guide.py
scripts/validate_va_claims_guide_surface.py
scripts/test_va_guided_workflow_contract.py
scripts/validate_va_claims_chat_llm_bridge.py
scripts/validate_va_claims_chat_surface.py
.github/workflows/va-guided-workflow-validation.yml
.github/workflows/va-claims-chat-llm-bridge.yml
.github/workflows/va-claims-chat-surface.yml
```

## Canonical session requirement consolidation

Site issue #177 is closed complete and transferred all earlier originating-session requirements into #113, #116, #178-#184, LLM-adapter#90, and master-records/orchestration#15. Over-decomposed duplicate children #185-#214 were closed into those canonical owners.

The 2026-08-12 PCP timeline-reconciliation session requirement is durably transferred by `docs/receipts/vacc-pcp-timeline-reconciliation-session-transfer-2026-08-12.md` into canonical Goal-3 owner Site#116. It adds chronology-reconciliation and explicit inclusion-purpose records for veteran-prepared clinician-facing syntheses without copying claimant medical facts into the public repository or treating those syntheses as independent medical opinions.

Transferred invariants:

```text
Guide = deterministic step-by-step veteran path
VACC = conversational execution/help layer
redirect-only authoritative-source retrieval by default
source authentication and ordinary record download = source -> veteran-controlled device
separately controlled original/submission artifact retains stable provenance
model review uses privacy-minimized sanitized/tokenized derivative where feasible
direct identity mapping stays outside ordinary model context
evidence facts remain page/source bound and separated from inference/contradiction/unresolved state
claim language may be generated only from supported facts
no fabricated diagnosis/nexus/event/onset/severity/limitation facts
no unsupported percentage targeting or award-size optimization
veteran retains claim selection, fact confirmation, certification, and submission authority
appointed accredited representative remains representative of record
VA-authenticated claimant/claim binding occurs only at an independently authorized submission boundary
authentication alone != veteran approval
ID.me/Login.gov branding or decorative stamp != independent document-ownership proof
VACC/service-organization/commercial use must be machine-verifiable in provenance
public success metric = administrative workload reduction while preserving evidentiary/legal integrity
regulatory self-help vs representation classification remains an explicit gate until authoritative evidence resolves it
veteran-prepared syntheses may organize/reconcile chronology but are not independent nexus or diagnosis evidence
later diagnostic language must not be projected backward absent qualified medical support
chronology reconciliation must preserve competing mechanisms, adverse evidence, contradictions, and unresolved items
underlying contemporaneous provider records remain preferred primary evidence where available
every admitted synthesized chronology item must preserve an explicit purpose-of-inclusion record
```

## Goal 1 — veteran-facing deterministic Guide — COMPLETE

The main path is `SEE -> DO -> CONFIRM`. It exposes six ordered steps, persistent shared completion state (`vaClaimsStepStateV1`), DONE gating, focused help, and mobile-first instructions.

The latest Step 6 contract is no longer merely “open Claims Chat.” It now covers final claim submission as described under Goal 4.

## Goal 2 — coordinated VA Resources LLM — ACTIVE / BLOCKED

### Canonical runtime owner

`StegVerse-org/LLM-adapter#90` owns route classification, admitted official VA-source retrieval, source/citation fields, privacy guard, provider execution, execution receipts, and runtime behavior.

Canonical runtime records:

```text
StegVerse-org/LLM-adapter/docs/VA_CLAIM_ASSISTANT_GOVERNED_RETRIEVAL_HANDOFF.md
StegVerse-org/LLM-adapter/docs/VA_CLAIMS_CHAT_RUNTIME_MIRROR_HANDOFF.md
StegVerse-org/LLM-adapter/tasks/VACP-ADAPTER-AUTHORIZED-EXECUTION-005.json
StegVerse-org/LLM-adapter/receipts/va-claim-assistant-provider-execution-preflight.json
```

The adapter rejects raw veteran documents. `document_organization` accepts only validated sanitized derived context.

### Site bridge — COMPLETE / DEPLOYED FAIL-CLOSED

`data/tasks/SITE-VA-COORDINATED-LLM-BRIDGE-002.json` is implemented and merged. General questions may cross the browser bridge only after `api/va-claim-assistant/runtime-projection.json` becomes receipt-verified. Guided assistance remains local/deterministic while blocked.

Current projection must remain:

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

### Authorized provider execution — BLOCKED / CLAIMANT NULL

Canonical task:

`StegVerse-org/LLM-adapter/tasks/VACP-ADAPTER-AUTHORIZED-EXECUTION-005.json`

Current machine-observable blockers:

```text
authorized_configuration_missing:STEGVERSE_MASTER_RECORDS_ALLOWED_HOSTS
authorized_configuration_missing:STEGVERSE_MASTER_RECORDS_ENDPOINT
authorized_configuration_missing:STEGVERSE_MASTER_RECORDS_TOKEN
provider_execution_authority_missing_or_invalid
```

Required release state:

```text
preflight state: READY_FOR_EXPLICIT_AUTHORIZED_EXECUTION
observation source: GITHUB_ACTIONS_WORKFLOW
privacy runtime: PASS
fresh single-use TVC admission: valid
protected Master Records configuration: present without secret disclosure
exact-caller VA provider authority: approved and unexpired
```

Machine observer:

```text
workflow: StegVerse-org/LLM-adapter/.github/workflows/va-claim-assistant-provider-preflight.yml
schedule: every six hours
claimant while blocked: null
external session ownership: not permitted
```

Do not create a competing provider-execution lane. Configuration presence alone is not authority.

### Goal 2 activation gates

All are required:

1. one real provider-backed VA request completes through the governed adapter;
2. request is classified into a governed VA route;
3. external factual claims use admitted official VA sources only;
4. response preserves proposition-level citations, authority classes, retrieval/effective dates, contradiction/uncertainty labels, and false-authority flags;
5. provider execution emits a stable privacy-minimized secret-free receipt;
6. Master Records returns custody `RECORDED` and reconstruction `PASS` for real execution evidence;
7. a dedicated HTTPS VA runtime endpoint is receipt-verified;
8. Site projection changes from BLOCKED to VERIFIED only from those receipts;
9. public `va-claims-chat.html` uses that governed runtime for general questions;
10. one deployed Site -> adapter -> Site question is directly observed and receipt-correlated.

The generic Ecosystem Chat endpoint does not satisfy VA activation unless it meets this VA-specific contract.

## Goal 3 — secure document/evidence lifecycle — QUEUED PUBLIC ACTIVATION

Canonical owner: Site#116. Child contracts: #178-#184.

Required lifecycle:

```text
authoritative-source redirect and retrieval success/failure receipt
veteran-controlled deliberate upload into governed intake
malware/type/size validation
encrypted temporary storage with retention/deletion/revocation state
stable original artifact hash and document index
sanitized/tokenized derivative with original-to-derived hash linkage
synthetic PII leakage regression
page-level record facts and citation anchors
privacy classification and redaction controls
record fact vs official-source fact vs inference vs contradiction vs unresolved state
chronology reconciliation with source-bound inclusion-purpose record
symptom/report date separated from later diagnosis/recognition/treatment date
medication authorization period separated from actual refill availability/exhaustion
competing mechanism and access-barrier preservation
retrospective diagnosis prohibition unless qualified medical linkage supports it
unresolved orders/referrals/monitoring remain unresolved until source evidence proves completion
evidence-to-criteria and claim-language provenance
evidence completeness/review receipt
packet manifest and download integrity receipt
packet-ready state distinct from submission state
actor/provenance schema and workload-reduction metrics
VA-authenticated claimant binding only at authorized submission boundary
final submission-confirmation correlation receipt
deterministic multi-document fixtures and fail-closed receipts
```

Canonical chronology-reconciliation transfer receipt:

`docs/receipts/vacc-pcp-timeline-reconciliation-session-transfer-2026-08-12.md`

Contracts and controlled-production-equivalent privacy preprocessing have advanced through merged PRs #227 and #230. Public private-document upload, retrieval, model review, and filing remain disabled until the applicable Goal 2, privacy, runtime, custody, reconstruction, malware, and authority gates pass.

## Goal 4 — final VA.gov submission fallback — COMPLETE

Until VACC has an independently authorized VA.gov filing connection, the mandatory final fallback is the official VA.gov 21-526EZ flow:

`https://www.va.gov/disability/file-disability-claim-form-21-526ez/veteran-information`

Current veteran-facing completion sequence:

```text
VACC prepares/reviews the final packet when its governed document path is active
-> if no authorized connected VA submission exists, open official VA.gov 21-526EZ
-> veteran signs in to VA.gov
-> veteran uploads required packet/supporting files as directed
-> veteran reviews the claim
-> veteran certifies and submits
-> Step 6 DONE only when final_claim_packet_ready AND va_submission_confirmed
```

A future receipt-verified VACC-to-VA.gov filing path may replace this fallback only when it returns an authoritative VA submission confirmation and independently satisfies filing-specific authority/custody requirements.

Implementation evidence:

```text
canonical PR: StegVerse-Labs/Site#232
merge commit: 5386e9c7ea570588c75bdeaac6dfa1f39730858d
superseded PR: #231 — closed unmerged after main divergence
```

Changed surfaces:

```text
va-disability-claim-guide.html
va-claims-guided-workflow.html
va-claims-chat.html
```

Changed deterministic validators:

```text
scripts/check_va_claim_guide.py
scripts/validate_va_claims_guide_surface.py
scripts/test_va_guided_workflow_contract.py
```

Pre-merge evidence:

```text
VA Guided Workflow Validation run 31156831454 — SUCCESS
VA Claim Guide Workers run 31156831494 — SUCCESS
VA Claims Chat LLM Bridge run 31156831516 — SUCCESS
Site Handoff Orchestrator run 31156831606 — SUCCESS
VA governed product goals run 31156831533 — SUCCESS
Site Bootstrap job 92798104498 — SUCCESS
```

The hosted guided-workflow receipt emitted:

```text
schema_version: 2.4.0
state: PASS
fallback_active_until_authorized_connected_submission: true
fallback_submission_url: official VA.gov 21-526EZ URL
step_6_done_requires:
  - final_claim_packet_ready
  - va_submission_confirmed
errors: []
```

Post-merge evidence:

```text
VA Claims Guide surface run 31156930390 — SUCCESS
head_sha: 5386e9c7ea570588c75bdeaac6dfa1f39730858d
```

Cloudflare Git integration also reported successful deployment during PR #232 validation. Deployment evidence does not itself grant filing authority or prove a connected VA submission runtime.

## Execution inventory

| Task | Canonical owner/location | Claim state | Completion | Validation | Integration | Next executable action |
|---|---|---|---|---|---|---|
| SV-VA-DUAL-FLOW-001 deterministic Guide | Site#113 / public pages | COMPLETE / RELEASED | COMPLETE | PASS | DEPLOYED | regression observation |
| SV-VA-COORDINATED-LLM-002 Site bridge | Site#113 / bridge task | COMPLETE_PENDING_RUNTIME | COMPLETE | PASS | MERGED + deployed fail-closed | consume verified runtime evidence when available |
| VACP-ADAPTER-AUTHORIZED-EXECUTION-005 | LLM-adapter#90 / task JSON | BLOCKED / claimant null | NOT EXECUTED | preflight fail-closed | NOT INTEGRATED | machine observer waits for protected config + exact provider authority |
| Goal 2 runtime projection activation | Site#113 / runtime-projection.json | BLOCKED | NOT ACTIVE | fail-closed PASS | NOT ACTIVE | bind only real execution/custody receipts + HTTPS endpoint |
| Goal 2 deployed end-to-end observation | Site#113 + LLM-adapter#90 | BLOCKED | MISSING | NOT OBSERVED | NOT INTEGRATED | execute after projection VERIFIED |
| SV-VA-SECURE-DOCUMENTS-003 | Site#116 + #178-#184 | QUEUED / canonical | PARTIAL | contract/privacy PASS evidence exists | public activation disabled | continue only through canonical machine/issue lanes |
| SV-VA-PCP-TIMELINE-RECONCILIATION-005 | Site#116 + transfer receipt | MERGED_INTO_CANONICAL_WORKSTREAM | REQUIREMENT TRANSFER COMPLETE | receipt + handoff bound | integrated into Goal 3 requirements | implement only through canonical Goal-3 document pipeline |
| SV-VA-FINAL-SUBMISSION-FALLBACK-004 | Site#113/#116/#180 | COMPLETE / RELEASED | COMPLETE | PASS | MERGED | regression observation |

## Active claims and collision boundaries

```text
Site fallback implementation claim: RELEASED by merged PR #232
Site bridge implementation claim: RELEASED_COMPLETE_PENDING_RUNTIME_ACTIVATION
Provider execution task claimant: null while BLOCKED
Goal 2 runtime owner: StegVerse-org/LLM-adapter#90
Goal 2 Site projection owner: StegVerse-Labs/Site#113
Goal 3 owner: StegVerse-Labs/Site#116
PCP chronology-reconciliation requirement: MERGED into Site#116 / no separate implementation claim
Originating-session consolidation owner: closed Site#177
```

Do not infer authority, expose secret values, replace Master Records custody with local persistence, enable upload/retrieval early, treat deployment success as runtime activation, or revive superseded PR #231.

## Machine-owned continuation

```text
Site Guide validation: .github/workflows/va-guided-workflow-validation.yml
Site Guide workers: repository-owned VA Claim Guide worker workflow
Site bridge validator: .github/workflows/va-claims-chat-llm-bridge.yml
Site surface validator: .github/workflows/va-claims-chat-surface.yml
Root Site ownership guard: scripts/site_handoff_orchestrator.py
Site canonical validation: Site Bootstrap Validate
Adapter provider preflight: .github/workflows/va-claim-assistant-provider-preflight.yml
Adapter authorized execution task: tasks/VACP-ADAPTER-AUTHORIZED-EXECUTION-005.json
Runtime owner: StegVerse-org/LLM-adapter#90
Projection owner: StegVerse-Labs/Site#113
Secure-document owner: StegVerse-Labs/Site#116
Custody/reconstruction owner: master-records/orchestration#15
```

## Validation commands

```text
python scripts/check_va_claim_guide.py
python scripts/validate_va_claims_guide_surface.py
python scripts/test_va_guided_workflow_contract.py
python scripts/validate_va_claims_chat_llm_bridge.py
python scripts/validate_va_claims_chat_surface.py
python scripts/site_handoff_orchestrator.py
python scripts/check_ecosystem_heartbeat_orchestration.py
```

Hosted workflow/job evidence is authoritative over chat claims.

## Integration and propagation obligations

Goal 2 propagation occurs only after real runtime evidence exists:

```text
LLM-adapter execution/privacy receipt -> master-records/orchestration#15 custody/reconstruction
Master Records returned receipt + verified runtime evidence -> Site#113 runtime projection
Site VERIFIED projection -> deployed VA Claims Chat end-to-end observation
```

No Publisher, admissibility-wiki, or stegguardian-wiki propagation is currently required for the VA Guide/fallback milestone unless a live contract later names those consumers.

## Duplicate/convergence disposition

```text
PR #231: SUPERSEDED / closed unmerged
PR #232: canonical fallback implementation / merged
Site#177: originating-session requirement consolidation / COMPLETE and closed
Goal 2 provider execution: MERGED INTO canonical LLM-adapter#90 machine-owned lane
Goal 3 secure documents: MERGED INTO canonical Site#116 + #178-#184 lanes
SV-VA-PCP-TIMELINE-RECONCILIATION-005: MERGED INTO canonical Site#116 via docs/receipts/vacc-pcp-timeline-reconciliation-session-transfer-2026-08-12.md
```

## Session consolidation and archive condition

The broader VACC program is not complete: Goal 2 real-provider activation remains blocked and Goal 3 public document/submission capability remains gated. Those incomplete goals are fully assigned to durable repository-native owners, task records, machine observers, issues, and release conditions.

The originating conversations that introduced the final VA.gov fallback and PCP timeline-reconciliation requirement no longer need to remain active after their transfer receipts and this handoff update are merged and referenced from the canonical owners. Archiving those conversations does not mean VACC is complete; it means no unique execution state remains only in chat.

Canonical continuation:

```text
StegVerse-Labs/Site/docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
StegVerse-Labs/Site/docs/receipts/vacc-pcp-timeline-reconciliation-session-transfer-2026-08-12.md
StegVerse-Labs/Site#113
StegVerse-Labs/Site#116
StegVerse-Labs/Site#180
StegVerse-org/LLM-adapter#90
StegVerse-org/LLM-adapter/tasks/VACP-ADAPTER-AUTHORIZED-EXECUTION-005.json
master-records/orchestration#15
```

## Percentages

Goal-2 activation denominator remains the ten explicit activation gates above.

```text
Goal 1 deterministic Guide: 100%
Goal 4 final-submission fallback: 100%
Goal 2 task/gate completion: 6/10 = 60%
Goal 2 developed-file completion: 10/12 = 83%
Goal 2 validation completion: 8/10 = 80%
Goal 2 integration completion: 5/7 = 71%
Goal 2 propagation completion: 2/4 = 50%
Goal 2 activation: 6/10 = 60%
Originating-session requirement transfer: 5/5 = 100%
Conversation archival readiness after transfer merge/reference: true
```
