# Ecosystem KV coordination review — source candidate

Parent Goal Task ID: `STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001`.
Canonical handoff: `StegVerse-Labs/.github/docs/STEGVERSE_WORKSPACE_ANY_DEVICE_KV_SURFACE_MIRROR_HANDOFF.md`.
Site handoff: `docs/WORKSPACE_INTEROPERABILITY_MIRROR_HANDOFF.md`.
Owner request: existing Workspace review features for the Ecosystem KV held on Google Drive.

This is a **candidate consumer interface**, not an admitted producer contract or live integration.
The canonical parent is PROPOSED / UNCLAIMED at pickup; COSV `10500000110000`.
An isolated source PR, local tests and CI do not change that state.

## Placement and ownership

`workspace.html` remains the existing shell. Its Developer Workspace contains an
Ecosystem KV review card, reached through KV Review navigation. This scoped review
does not create a fourth sovereign KV type, replace Organization Workspace, or imply
that every developer is allowed to see ecosystem coordination data.

The existing StegOS owner defines Workspace semantics; continuity-vault-kit owns KV
projection semantics. The existing authorized integration/custody writer remains the
only writer. Google Drive is custody, not caller authentication or transition authority.
Site adds no source/provider calls, database, browser authority, hosted service,
assistant, credential manager, polling loop, or iOS application.

## Candidate delivery seam

Only the existing owner-controlled `StegVerseWorkspaceKVBridge` may supply:

```javascript
await bridge.loadEcosystemCoordinationReview({
  workspace_type: 'DEVELOPER', kv_scope: 'ECOSYSTEM'
});
// returns { projection, context }
// context: { workspace_type, kv_scope, principal_id, workspace_id }
```

**This method is not implemented by this PR.** The personal loader is never substituted.
Without it the card reports `ECOSYSTEM_REVIEW_OWNER_BRIDGE_NOT_BOUND`, not an empty queue.
The producer/delivery owner must authenticate and authorize the caller independently,
select only its allowed Ecosystem scope, verify the authentic projection ingress,
enforce revocation and continuity/replay rules, and bind `context` to that verified
caller. Returning matching context fields or receipt locators is not authentication.
Site checks supplied field consistency; it does not verify the delivery, receipts,
Registry truth, owner decisions or independent replay. Its output explicitly states
`FILED_SUPPORT_ONLY_NOT_PAGE_VERIFIED`, `REPLAY_STATUS_UNKNOWN`, `action_eligible:false`.

The owner must emit `stegverse:ecosystem-review-invalidated` on the existing document
when scope, grant or principal is invalidated. The card clears records and drafts on
that event and on every context switch. New requests invalidate old data immediately;
late responses cannot repopulate another context or overwrite a newer refresh.
The product does not claim runtime revocation has been wired or observed.

## Candidate projection

Schema: `stegverse.kv.ecosystem-coordination-review-projection/v1`.
The full executable shape is validated in `assets/workspace-ecosystem-review.js`.
Tests construct synthetic fixtures in memory; no live KV contents are committed.

| Field | Required meaning |
| --- | --- |
| `workspace_type`, `kv_scope`, `kv_account` | DEVELOPER, ECOSYSTEM, stegverse@gmail.com; no Personal KV fallback |
| `projection_metadata` | Existing metadata schema; source observation time, immutable revision, provenance locator, caller-bound owner/workspace, ACTIVE grant, authority NONE |
| `queue` | HAS_WORK / EMPTY / ERROR / UNKNOWN, source locator, observation time, read completeness and error disposition |
| `reviews[]` | One review per canonical task identity; unknown identities must be reconciled by the producer rather than invented by Site |
| `credential_material_present`, `provider_operation_authorized`, `workspace_grants_authority` | Exactly false |
| `authority_effect` | Exactly NONE |

Each review contains exactly `goal`, `inputs`, `evidence`, `facts`, `checks`, `continuity`:

- `goal`: task_id, recorded coordination state, COSV, canonical handoff locator,
  Registry source locator and immutable source revision. This is projected state,
  not a new Registry registration, task admission, or live Registry lookup.
- `inputs`: original input locator, immutable revision, sha256 digest and filing time;
  original private bodies are not copied into this view.
- `evidence`: locator/digest, filed evidence state, author, independent verifier and
  verification locator. VERIFIED requires a distinct non-author verifier and filed
  verification reference. `evidence_class` and `completion_evidence_contract_version`
  are either both null, or a canonical class and `v1`. These are filed support,
  not page proof.
- `facts`: statement, category, evidence state, work state and evidence IDs. Categories
  cover owner form/binding, authority, task/handoff/claim, manifest, native execution,
  negative controls, independent replay, runtime ownership and continuity. Missing
  categories appear UNKNOWN / UNKNOWN. COMPLETED requires filed support, explicit
  `evidence_class`, and `completion_evidence_contract_version: v1`; each supporting
  record must carry that exact class and contract. Missing/untyped support, invented
  classes, and promotion from source/merge/CI evidence into runtime/end-to-end evidence
  are refused. UI and drafts display the filed completion class. VERIFIED requires
  independently filed VERIFIED evidence. Verification never implies completion.
- `checks`: identity includes task, goal revision, original input ID/digest/revision,
  predicate and rule revision. Duplicate records preserve all result locators; changed
  versions and errors/conflicts require review. Same-version matches are advisory
  duplicate-suggestion suppression, not a replay or authentication gate.
- `continuity`: filed source, next step, responsible existing owner, canonical handoff.

Queue EMPTY requires a complete read. ERROR requires all six fields: failure_code,
failed_predicate, required_evidence_or_repair, retry_entrypoint, owning_existing_goal,
next_attempt. A failed read never becomes EMPTY. Stale snapshots retain visible
timestamps and STALE labels; absent or revoked sources withhold all records.

## Drafts and effects

The card generates coordination updates, issue comments, evidence gaps and next-session
summaries. They remain ephemeral, unsubmitted text until copied by the user. No report
is filed, claim created, owner bound, task admitted, runtime executed, repository changed
or governed record written by this feature. No check is performed by grouping prior
filed checks. Copying text does not make it a receipt or permission.

## Owner integration and acceptance still required

1. CVK/StegOS owners reconcile this candidate with their current projection contracts;
   adopt or amend the exact schema and existing DEVICE_KV dispatch class. No new
   authoritative writer or alternate ingress is authorized by this document.
2. The existing coordination ingestion owner projects newly filed inputs, revisions,
   source completeness, errors and empty dispositions through its authorized custody
   path. Do not reinterpret document titles or narration as verified evidence.
3. Deliver it through the authenticated, scoped existing bridge seam, with producer-side
   grant/replay checks and invalidation. Preserve no-personal/no-cross-user leakage.
4. Non-author review and exact-head checks precede protected integration by the existing
   authorized owner. Production publication remains the existing governed route.
5. Observe a real Ecosystem KV input/revision, negative control, empty/error read,
   context switch, revocation and replay refusal on the authorized device path; retain
   authentic receipts and readback. Fixtures and source tests discharge none of these.

Local check: `node --test tests/workspace-ecosystem-review.test.cjs`.

## Runtime invariants — intentional state-transition operating model

Runtime is manifest-directed attempted state transition. Read/synchronization requests
are actions under this model as well as writes: calling a read-only view does not
create an exemption from manifest selection or the existing authority path. Local
filtering/draft presentation is non-authoritative UI state; it does not append or
constitute a sovereign transition. This source candidate adds no transition engine.

| Invariant | Requirement for this build and its existing runtime owners |
| --- | --- |
| Intent and processing | The admitted manifest selects capability, installed bound route and destination; neither UI/provider/model identity nor a prior result selects processing. |
| Runtime reality | Each transition inside an Organization emits its Organization receipt, manifest-directed append under its Organization ledger lock. That ledger root is runtime reality. |
| Destination | Existence is sufficient under the canonical ingress/egress contract. Receiver liveness, an always-on listener, external machine, second device, or connected-device inventory is never a transition predicate. |
| Unavailable receiver | Preserve the existing durable queue or event-ephemeral materialization disposition; do not add a polling or waiting prerequisite. A missing displayed projection is not proof that a transition failed or did not occur. |
| Attempt and observation | An actual admitted attempt returns its authentic ALLOW/DENY/FAIL_CLOSED and receipts. Without an authentic attempt, preserve UNKNOWN_NOT_AUTHENTICALLY_OBSERVED; the UI's WITHHELD/unavailable code is not a fabricated native disposition. |
| Claims and verification | WorkerCoordinator alone issues execution claim/fence. KV/SKAP alone verifies the user; TV/TVC owns credentials. Account, principal fields, device, transport, browser state and CI are not user verifiers or runtime authority. |
| Master Records | Organization records and reconstruction only; neither a runtime-reality authority nor a gate awaited by a transition. Reconstruction may be required only where explicitly declared for that evidence result. |
| Complete lifecycle | Bind original initiator/request, manifest, selected capability/route, declared transitions/custody/replay, Publisher when declared, SDK return assembly, applicable final StegVerse-side egress, Interlock/InTr egress and authentic far-side caller consequence/receipt. Local staging or UI rendering is not terminal communication completion. |
| Nonconformance | Before runtime adoption, either conform or obtain the existing Registry owner's recorded, bounded exemption with actionable non-ALLOW and review/expiry. A candidate document or missing implementation is not an exemption or authority grant. |
| Completion language | Contract v1 and the exact native evidence class are required. SOURCE_IMPLEMENTED, MERGED, CI_VALIDATED, SANDBOX_RUNTIME_OBSERVED, EXTERNAL_PROVIDER_OBSERVED, MASTER_RECORDS_RECONSTRUCTED and END_TO_END remain distinct; the page never promotes one into another. |

These requirements govern producer/bridge adoption and review. They do not require
waiting for an observer or Master Records to make an Organization transition real.
The page remains unable to verify native receipts; the producer must enforce actual
manifest/claim/admission/Organization-receipt bindings through existing components.

Reviewed current source anchors (StegVerse-Labs/.github):

- `TASK_REGISTRY_CANONICAL_INVARIANTS.md`, blob `1f9669a991c5a05bf6701583ca6f3b551e713770`.
- `data/task-registry-global-invariants.json`, blob `208177e09d7b515d19e073dd962832742e6da6a5`.
- `data/organization-role-runtime-reality-deployment.json`, blob `ca7b20b9b84af4fcead9f0aa838a56f7bab3826d`.
- `docs/CANONICAL_SOUTHBOUND_COMMUNICATION_LIFECYCLE.md`, blob `48458719de0bb6f6d1fd943a7ce48f09cfdcb229`.
