# StegVerse: Ephemeral Browser → LLM Session → Ecosystem Chat

Review draft — September 26, 2026
Status: Architecture and integration review; authentic end-to-end execution not verified.

Every canonical task this review cites is declared in
`data/reviews/ephemeral-browser-llm-ecosystem-chat.v1.json` and checked by
`scripts/check_review_canonical_task_refs.py` against an observed snapshot of the canonical
Task Registry. A citation of a task the registry does not carry, or an assertion of a state
the registry does not hold, fails CI.

## 1. Purpose

Define the relationship between the governed ephemeral browser, authorized LLM session,
Organization Records, Master Records, and Ecosystem Chat feedback. This is a review proposal,
not evidence that the complete runtime path has executed.

## 2. Existing related goals and tasks

Reconciled against `StegVerse-Labs/.github` main at generation 259.

| Canonical task | Registry state | Responsibility |
|---|---|---|
| `KV-BOUND-EPHEMERAL-BROWSER-PROJECTION-001` | ACTIVE | KV continuity boundary; StegOS runtime node; StegBrowser browser-capability node. |
| `EPHEMERAL-STEGBROWSER-EXTERNAL-AI-ACTIVATION-001` | PROPOSED | First governed on-demand external OpenAI task through the existing StegBrowser ephemeral lease and LLM Adapter, then a separately attributable Anthropic/Claude task, independent of native MyKV installation. |
| `STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001` | ACTIVE | Live manifest-bound InTr ingress execution on the browser substrate. |
| `STEG-BROWSER-RESIDENT-RECEIPT-TRANSPORT-001` | ACTIVE | Resident receipt transport out of the browser substrate. |
| `STEGOS-LOCAL-AI-ENTITY-CHATGPT-001` | PROPOSED | First ChatGPT-powered governed resident participant; distinct from a generic LLM inference request. |
| `ORGANIZATION-BATCH-CUSTODY-REPLAY-001` | ACTIVE | Original organization-level WORKER, TASK and ORGANIZATION_SEQUENCE readback and reconstruction. |

### 2.1 Superseded and unregistered references

An earlier draft of this review anchored on three identifiers that do not survive
reconciliation. They are recorded here rather than deleted, so the correction is auditable.

| Cited | Observed | Disposition |
|---|---|---|
| `STEG-BROWSER-ECOSYSTEM-EPHEMERAL-001` | Not in the registry: no canonical task record, no registry entry. | Do not cite. The same identifier previously sat in two Stage 1 public benchmarks and was removed in Site #1463 for the same reason. Whatever source merged under this name, the registry carries no such task. |
| `STEG-BROWSER-EPHEMERAL-RUNTIME-BINDING-001` | SUPERSEDED, not ACTIVE. Its own record names `continuation_task_id: STEG-BROWSER-RUNTIME-CONSUMPTION-001`, which is RETIRED. | Neither is a live owner. The browser substrate rows above are live and carry the same COSV `40000100100000`. |
| `SHWP-ECOSYSTEM-CHAT-INFERENCE-001` | No canonical task record and no registry entry; appears only as `adjacent_task_refs` in five other tasks. | Cannot carry a COSV, because no record exists to hold one. An earlier draft attributed COSV `50000000100000` to it; that vector is held by `MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001`. Resolve which was meant before relying on either. |

### 2.2 Open drift outside this review

`STEG-BROWSER-RUNTIME-CONSUMPTION-001` is RETIRED in the canonical registry, yet Site holds
an active claim on it (`SITE-KV-ENTRYPOINT-INTR-LAUNCHER-20260914`,
`CLAIMED_FOR_IMPLEMENTATION`). Not a defect of this review, and not corrected here — it is the
claim holder's to resolve — but it bears on §5 and would surface at the first authentic test.

## 3. Proposed integrated workflow

```
Ecosystem Chat request
    ↓
KV continuity and request identity
    ↓
Interlock/InTr admission + WorkerCoordinator claim/fence
    ↓
Purpose-bound ephemeral StegBrowser lease
    + separately authorized LLM session / provider route
    ↓
Bounded browser actions + governed inference + usage measurement
    ↓
Organization Records: WORKER → TASK → ORGANIZATION_SEQUENCE
    ↓
Master Records organization records and independent reconstruction
    ↓
Ecosystem Chat authorized response, feedback and evidence reference
    ↓
Browser/LLM session termination and applicable destruction evidence
```

The sequence is a logical evidence flow, not a claim that all operations must be serialized.
Close/destruction must occur on success, refusal, expiry and failure as applicable; its receipt
must also enter the governed evidence chain.

**Closure is blocking unless a named policy says otherwise.** An earlier draft allowed a
response to be displayed before archival closure "only if the applicable policy explicitly
permits that distinction", without naming such a policy. Until one is named and cited here by
identifier, display does not precede closure — otherwise the permission is the seam through
which "displayed" silently becomes "recorded".

## 4. Why Organization Records is mandatory to review

Organization Records is the cross-component execution history, not an optional copy of a chat
transcript. It preserves the association among the original request, task, worker, browser
lease, LLM session, governing disposition, execution and feedback. Without original
organization-level evidence, an LLM answer alone cannot establish that the browser and
inference were part of the same authorized task, nor reconstruct their ordering.

The three required views are:

- **WORKER**: original claim, fence, executor identity and actual worker events.
- **TASK**: request identity, admissions/refusals, browser/LLM linkage, bounded execution, usage and feedback status.
- **ORGANIZATION_SEQUENCE**: exact predecessor-linked ordering of the original organization events across participating components.

Record non-ALLOW outcomes as explicit dispositions where observed. Preserve
`UNKNOWN_NOT_AUTHENTICALLY_OBSERVED` for inaccessible original evidence rather than inventing
ALLOW, DENY, FAIL_CLOSED or completion.

## 5. Authority and custody boundaries

- **KV**: private continuity and applicable identity context; browser-local storage is not the continuity root.
- **Interlock/InTr**: admission and governed state transitions.
- **WorkerCoordinator**: original task claim and fencing authority.
- **StegBrowser**: bounded temporary browser capability, not independent execution or credential authority.
- **StegOS / LLM adapter**: admitted execution surface and provider-neutral inference transport.
- **TV/TVC**: credential and provider authority; raw credentials are never persisted in leases or receipts.
- **Organization Records**: original cross-component worker/task/organization event history.
- **Master Records**: organization records/reconstruction, including reconciliation and independent reconstruction; the Organization owns observed reality, and Master Records must not fabricate absent organization events.
- **Ecosystem Chat**: conversational surface and authorized feedback recipient, not a substitute for the original execution record.

No second user-operated device, duplicate runtime, parallel ledger or duplicate task is
introduced by this review.

## 6. Acceptance criteria for the combined workflow

1. Verify current canonical Task Registry state, Goal IDs, COSVs and each applicable mirror handoff before implementation.
2. Submit one original request through the existing authorized ingress, with authentic identity and request binding rather than caller-editable origin assertions.
3. Obtain actual Interlock/InTr disposition and, if admitted, original WorkerCoordinator claim/fence.
4. Materialize a purpose-, origin-, action- and time-bounded ephemeral browser lease; establish the separately admitted LLM session and provider route.
5. Obtain an authentic bounded browser action and a real governed inference response; capture measured usage and explicit execution outcomes.
6. Persist and retrieve the original WORKER, TASK and ORGANIZATION_SEQUENCE records, **and demonstrate the readback rejects a wrong linkage**: the retrieval must fail, for this invocation, when the browser lease, LLM session, task and worker fence are not the ones bound to it. A record that merely exists does not satisfy this criterion.
7. Independently reconstruct the same interaction from organization records through Master Records, including the applicable organization-record and transition checks.
8. Return the authorized answer/feedback and evidence reference to Ecosystem Chat; verify delivery separately from generation.
9. End the browser/session according to its lease contract; retain the applicable terminal destruction/close evidence and organization-sequence successor.
10. Demonstrate an independent non-ALLOW path (for example expiry or revocation), with explicit refusal, prevented action and reconstruction where observable.

Merged source, successful CI, generated receipts and an available endpoint are none of them
authentic resident execution, original organization readback, Master Records PASS, feedback
delivery or session destruction.

## 7. Current evidence and review decisions

At canonical Registry generation 259, `STEGOS-LOCAL-AI-ENTITY-CHATGPT-001` and
`EPHEMERAL-STEGBROWSER-EXTERNAL-AI-ACTIVATION-001` are both PROPOSED. The Ecosystem Chat
same-device handoff describes source projection as released, with authentic device
checkout/inference, measured usage and same-execution reconstruction unobserved. These are
dated observations, not a claim about later state; the reference block records the generation
they were taken at.

`EPHEMERAL-STEGBROWSER-EXTERNAL-AI-ACTIVATION-001` states this review's workflow almost in
full, and its expected evidence predicates correspond closely to §6 including the non-ALLOW
path. Whether it owns this work, or this review describes something that must be distinguished
from it, is the first question for its owners — not a question this review may answer for them.

Review questions:

1. Which existing component writes each original organization event, and which existing authorized interface reads the organization history?
2. What exact correlation keys bind the browser lease, LLM session, original task, worker fence and feedback event without exposing secrets?
3. Which dispositions require organization-level persistence before feedback may be returned, and which closure operations may follow asynchronously — under which named policy?
4. Does the existing Organization Records readback expose all three required views and their immediate predecessors for this specific invocation, and does it reject a wrong linkage (§6.6)?
5. What is the exact authorized host-to-resident invocation route for the first authentic test?
6. Does `EPHEMERAL-STEGBROWSER-EXTERNAL-AI-ACTIVATION-001` own this workflow, and if not, what distinguishes them?

## 8. Next execution step

Reuse existing browser, LLM, Organization Records and Master Records owners. Trace the first
missing integration predicate and implement only the minimal correction under its native owner.
Then obtain one original authorized browser/LLM interaction, original organization readback,
independent reconstruction and verified Ecosystem Chat feedback; separately test
expiry/revocation refusal. Preserve UNKNOWN wherever authentic evidence is inaccessible.

## Authority boundary

This document is a review. It emits no COSV, writes no Master Records, grants no execution or
publication authority, and promotes no benchmark or milestone. Its reference block is
`OBSERVED_NOT_AUTHORIZING`.
