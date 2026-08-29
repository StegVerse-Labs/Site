# Humans as the Interoperability Layer — Site Mirror Handoff

Updated: 2026-08-15
Repository: `StegVerse-Labs/Site`
Canonical branch: `main`

## Source-of-truth rule

This is the canonical participant-facing HIL continuation record in `StegVerse-Labs/Site`, subordinate to `docs/SITE_MIRROR_HANDOFF.md`.

Current authority order:

1. `docs/HIL_RUNTIME_PATH_RECONCILIATION.md`
2. `docs/HIL_POST_SUBMIT_CONTINUITY_MIRROR_HANDOFF.md`
3. `docs/HIL_MIRROR_HANDOFF.md`
4. `docs/HIL_END_TO_END_PROTOCOL.md`
5. `data/hil-experiment.json`
6. `data/hil-receiver-config.json`
7. `src/worker.js`
8. `data/session-work-claims.json`
9. `StegVerse-Labs/TVC/docs/HIL_TVC_MIRROR_HANDOFF.md`
10. `StegVerse-Labs/StegCore/docs/HIL_SESSION_CONSOLIDATION_MIRROR_HANDOFF.md`

Live repository state, claims, receipts, workflow evidence, runtime observations, TVC evidence, and StegCore lifecycle state supersede older prose.

The old Cloudflare/D1 GitHub-secret deployment attempt is historical evidence only. `docs/HIL_RUNTIME_PATH_RECONCILIATION.md` supersedes it for active implementation. No historical GitHub-secret path may be revived as HIL production authority.

## Active product goal

```text
goal_id: HIL-LIFECYCLE-ACTIVATION-001
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
participant_surface_authority: StegVerse-Labs/Site
exact_byte_custody_authority: StegVerse-Labs/TVC
cross_repository_lifecycle_validation: StegVerse-Labs/StegCore
```

No Site page, browser code, GitHub-hosted workflow, result packet, handoff, or projection may mint private-review, publication, release, Master Record, provider, wallet, or credential authority.

## Canonical runtime path

```text
participant on stegverse.org
-> same-origin GET /api/hil/readiness
-> same-origin POST /api/hil/submissions
-> src/worker.js
-> exact response PDF + HIL-RESPONSE-PROVENANCE-v1.1
-> persistent custody + post-persistence exact-byte reconstruction
-> HIL-RECEIVER-RECEIPT-v2
-> same-origin status/content retrieval
-> HIL-SUBMISSION-RESULT-PACKET-v1 projected first on hil-accepted.html
-> TVC lifecycle/private-review verification
-> separate publication authority
-> Site lifecycle projection
-> Master Records validation/release under its own authority
-> StegCore lifecycle verification
```

Canonical identities:

```text
Primary: v1.1
Primary SHA-256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Prompt: HIL-PROMPT-v1.1
Prompt SHA-256: cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
Provenance: HIL-RESPONSE-PROVENANCE-v1.1
Receiver receipt: HIL-RECEIVER-RECEIPT-v2
Registry: HIL_REGISTRY
Custody backend: portable-sqlite-chunks-v1
```

## Post-submit continuity — COMPLETE / MERGED

`HIL-POST-SUBMIT-CONTINUITY-001` is complete for its bounded source/integration scope.

```text
PR: #274
merge: e5c4e70ccf341768940dbcedbf3171e921e28344
claim: RELEASED / MERGED_INTO_CANONICAL_WORKSTREAM
handoff: docs/HIL_POST_SUBMIT_CONTINUITY_MIRROR_HANDOFF.md
```

The repaired participant path is:

```text
governed submission succeeds
-> receipt proves EXACT_BYTES_PERSISTED + RECORDED
-> hil-accepted.html?submission_id=<id>
-> FIRST CONTENT: HIL-SUBMISSION-RESULT-PACKET-v1
   -> receipt identity
   -> independently retrieved exact PDF
   -> submitted/retrieved SHA-256
   -> exact-byte PASS
   -> provenance/lifecycle state
   -> explicit false authority fields
-> NEXT LIFECYCLE CONTENT below it
```

The prior public client used `/api/hil/upload`, a route not implemented by the canonical worker. PR #274 aligned the public client with `/api/hil/readiness` and `/api/hil/submissions`. Receiver failure remains a clearly non-custodial participant-device fallback (`LOCAL_FALLBACK_PENDING_RESUBMISSION`) routed to `hil-receipt.html`.

Final source/integration evidence:

```text
HIL Post-Submit Continuity run 31872738022: SUCCESS
Check HIL v1 Upload Surface run 31872738030: SUCCESS
Check HIL v1.1 Release run 31872738020: SUCCESS
Site Handoff Orchestrator run 31872738026: SUCCESS
Ecosystem Heartbeat Orchestration run 31872738024: SUCCESS
Cloudflare Workers build ec0dd15a-f6cc-4637-9bea-9a2f79ac8c1e: SUCCESS
PR #274 merge e5c4e70ccf341768940dbcedbf3171e921e28344
```

## Genuine participant evidence already preserved

TVC remains authoritative for exact-byte custody evidence. At least one genuine participant artifact predates the repaired public path:

```text
submission_id: HIL-20260731-GPT56-001
TVC receipt: HIL-TVC-1442c8407e6de8c6
state: RECONSTRUCTED_HASH_VERIFIED
private_review: pending under TVC #8
publication_authorized: false
release_authorized: false
master_record_created: false
```

That artifact came through a connected-file path, not the later managed-return email route.

## Current owners / collision boundaries

```text
StegVerse-Labs/Site#81
  owner: live same-origin receiver/readiness/runtime activation and observation

StegVerse-Labs/Site#67
  owner: participant lifecycle projection/integration

StegVerse-Labs/TVC#8
  owner: exact-byte lifecycle + authenticated private review

StegVerse-Labs/StegCore#41
  owner: cross-repository lifecycle consistency and next-action coordination

master-records/orchestration
  owner: candidate validation/release under independent predicates
```

The machine-owned pre-work admission gate remains `SITE-PREWORK-CLAIM-GATE-MACHINE-001` in `data/session-work-claims.json`. The completed HIL post-submit claim is retained there as released provenance and no longer blocks new nonconflicting work.

## Product activation denominator

Full HIL lifecycle activation requires 8 gates:

```text
1 canonical v1.1 source + post-submit integration
2 live governed same-origin receiver readiness
3 authentic governed participant submission + exact-byte receipt on current path
4 authenticated private review
5 separately authenticated publication
6 validated Site lifecycle projection
7 Master Record validation/release under independent authority
8 StegCore/downstream lifecycle verification
```

Current source-of-truth state before direct live re-observation:

```text
1 source/integration: COMPLETE
2 live readiness after merge: MUST BE DIRECTLY REOBSERVED
3 historical genuine custody: COMPLETE for HIL-20260731-GPT56-001; current repaired public path submission not yet observed
4 private review: PENDING TVC #8
5 publication: PENDING separate authority
6 lifecycle projection: PENDING Site #67
7 Master Record: PENDING independent authority
8 downstream lifecycle verification: PENDING
```

Do not infer product activation from source merge or hosted CI. The next executable Site action is direct runtime observation under Site #81 against the current main deployment. It must emit an inspectable READY/RETRY/REVIEW_REQUIRED/FAILED receipt and preserve TV/TVC-only authority.

## Session consolidation

The previously chat-only post-submit requirement is now fully durable and merged. The session no longer owns unique source implementation for this requirement. Remaining value is distinct activation/reconciliation support across Site #81, Site #67, TVC #8, StegCore #41, heartbeat/runtime owners, and the separately active StegFin goal.


## 2026-08-26 legacy validator reconciliation

Site Task Runner run `33024379805`, started from successful Bootstrap run `33024359623`, advanced through the repaired Ecosystem Chat traversal and gateway/receipt validators and then failed at `scripts/check_hil_experiment.py`.

The failure was validator drift:

```text
stale requirement: active public page contains "Approved presentation"
historical source: v0.5 review-candidate presentation
current canonical public surface: HIL v1.1 governed intake
canonical Primary SHA-256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
canonical Prompt SHA-256: cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
classification: VALIDATOR_DRIFT
product/runtime failure: false
```

Canonical repair owner: `StegVerse-Labs/Site#506`.

The compatibility validator now delegates the canonical v1.1 release and upload-surface validators and separately verifies that the v0.5 review evidence remains preserved, approved, and explicitly non-canonical. It no longer requires historical review-candidate presentation copy on the active v1.1 public page.

This repair does not alter custody, intake readiness, private review, publication, Master Record, provider, credential, release, or activation authority.

Required completion:

```text
#506 exact-head Site/HIL validation: pending
merge: pending
next Site Task Runner advance beyond HIL compatibility gate: pending
public HIL runtime activation: unchanged / still separately gated
```


## 2026-08-27 consolidation reconciliation

Live repository inspection supersedes the older validator-pending and legacy Cloudflare-owner statements above where they conflict.

Bounded validator repair:
- Site#506 compatibility-validator repair merged at `3538beebbbeab37550ad62fb1e9c2d1e7e9788a1`.
- Later Bootstrap `33044633784` and Site Task Runner `33044661032` completed SUCCESS with no failed steps at source main `4a13c991dcfb83eccee3fb57cbf41de866466f0e`.
- Later full Task Runner success `33045293923` reconfirmed the repaired path.
- Site#506 is CLOSED/COMPLETED.
- `data/tasks/SITE-HIL-V1-1-VALIDATOR-506.json` is reconciled to `RELEASED / SATISFIED_BY_EXISTING_STATE` at Site commit `3755a70af907209b07f07746b4d07c3be2590bbd`.

Legacy activation owner:
- Site#158 is CLOSED / SUPERSEDED_NOT_PLANNED.
- `data/tasks/HIL-V1.1-ACTIVATION-001.json` is reconciled at commit `0ee517853108464f1f2ab6c8e63f864b0c578e76` to preserve the old Cloudflare/D1 path as historical provenance only.
- Missing Cloudflare Actions values are not current activation prerequisites and must not be reintroduced as Site/GitHub production authority.

Current HIL activation owners remain:
- Site#81 — live sovereign receiver/readiness/runtime observation;
- Site#67 — participant lifecycle projection;
- TVC#8 — exact-byte lifecycle and authenticated private review;
- StegCore#41 — cross-repository lifecycle coordination;
- master-records/orchestration — independent validation/release.

Current activation boundary remains nonterminal:
`resident receiver READY -> admitted public HTTPS rendezvous -> direct Site readiness observation -> genuine browser submission with HIL-RECEIVER-RECEIPT-v2 -> restart exact-byte proof -> TVC private review -> separately authenticated publication -> Site projection -> Master Records release -> downstream verification`.

No product activation, publication, release, custody, provider, credential or Master Records authority is inferred from validator completion or stale-owner retirement.


## 2026-08-27 participant copy-control repair

Observed on iPhone at the public `hil-study-launch.html` surface: the **Copy exact prompt** control could fail when the page is reached over an insecure HTTP origin because `navigator.clipboard.writeText` is restricted to secure contexts.

Bounded repair on branch `fix/hil-study-copy-prompt-ios`:
- retain the secure-context Clipboard API path when available;
- add a legacy textarea + `execCommand('copy')` fallback for iOS/HTTP compatibility;
- if both copy paths are blocked, select the exact prompt in-page and instruct the participant to use the browser's native Copy action;
- no custody, publication, credential, receipt, or lifecycle authority is changed.

Repair commit: `2584e5c62f4233ff9de4351aeeff8770a835106d`.

Important adjacent observation: the screenshot exposing the failure shows an `http://stegverse.org/.../hil-study-launch.html` origin. The page's Web Crypto hashing path is secure-context-sensitive as well, so HTTPS enforcement/observation remains a separate runtime hardening item and must not be inferred complete from this copy-control repair.


## 2026-08-27 participant-path correction

A live participant check exposed a material UX/state inconsistency: the canonical HIL page already contained the governed `Submit Response Packet` control backed by `assets/hil-direct-upload-v1.js` and same-origin `/api/hil/readiness` + `/api/hil/submissions`, but the study launch/announcement surfaces still routed participants into `hil-managed-return.html` as though participant-managed PDF+JSON/email transport were the primary path.

That presentation was incorrect for the current canonical architecture.

Corrected participant hierarchy:

```text
PRIMARY
hil-study-announcement.html / hil-study-launch.html
-> humans-as-interoperability-layer.html#submit
-> Submit Response Packet
-> readiness + canonical identity checks
-> same-origin governed submission attempt
-> HIL-RECEIVER-RECEIPT-v2 on success

FALLBACK ONLY
hil-managed-return.html
-> local PDF/package verification
-> participant-managed share/email handoff
-> no governed custody claim
```

Source correction branch: `fix/hil-primary-direct-submit-20260827`.

Files corrected:
- `hil-study-announcement.html` — exposes direct `Submit response` as primary and labels managed return as fallback.
- `hil-study-launch.html` — primary CTA now routes to governed Site submission; package generation is fallback tooling.
- `hil-managed-return.html` — explicitly marked fallback-only and includes a prominent return path to direct Site submission.

Verification rule tightened: HIL participant intake MUST NOT be described as complete merely because package generation, local hash verification, share-sheet, or email fallback works. Current-path participant submission is proven only by a directly observed governed receiver transaction returning a valid receiver receipt and the required exact-byte evidence.

This correction changes participant routing/UX truth only. It does not claim live receiver READY, current-path governed custody, private review, publication, Master Record release, or product activation.


## 2026-08-27 local fallback recovery repair

A genuine participant direct-submission attempt reached the canonical HIL upload client but the governed receiver was not READY, producing a real `LOCAL_FALLBACK_PENDING_RESUBMISSION` record. The participant screenshot showed:

```text
device storage verified: true
StegVerse custody: NOT_YET_RECEIVED
record state: LOCAL_FALLBACK_PENDING_RESUBMISSION
```

Inspection found an additional continuity defect in the receipt surface: `assets/hil-direct-upload-v1.js` writes verified fallback bytes to IndexedDB `stegverse-hil-v3` and records the key at `response_storage.key`, while `hil-receipt.html` still attempted to read IndexedDB `stegverse-hil-v2` and `response_object_key`. This could truthfully report verified local storage while failing to reopen the exact stored PDF.

Repair:
- receipt retrieval now uses the current `stegverse-hil-v3` store and `response_storage.key`, with legacy-key compatibility;
- reopened local bytes are SHA-256 verified against the participant record before view/download;
- new fallback records persist the exact provenance manifest and compatibility storage key;
- future fallback records expose a one-action governed retry that reuses the exact locally verified PDF + stored provenance after receiver READY;
- existing fallback records created before provenance persistence remain recoverable for exact PDF view/download and are explicitly routed to manual resubmission because original participant provenance choices cannot be safely reconstructed.

This repair does not convert the observed local fallback into custody. The observed participant record remains `NOT_YET_RECEIVED` until a real `HIL-RECEIVER-RECEIPT-v2` is returned and verified.


## 2026-08-29 SUBMISSION-TRIGGERED INTR DOUBLE-INTERLOCK

The participant-facing HIL submission contract is corrected so the **Submit** action itself begins the governed transport transaction. A pre-existing READY receiver is no longer a prerequisite to starting upload work.

Canonical sequence:

```text
participant taps Submit
-> browser validates exact PDF and canonical provenance
-> browser creates a durable HIL InTr ingress envelope
-> exact packet + ingress envelope are submitted immediately
-> receiving HIL ingress boundary validates exact hashes
-> receiver issues canonical InTr hop receipt:
     DEVICE -> HIL_INGRESS
-> exact PDF/provenance are persisted and re-read
-> receiver issues second chained InTr receipt:
     HIL_INGRESS -> HIL_CUSTODY
     prior_receipt_hash = first receipt hash
-> receiver persists a TVC-bound egress Interlock envelope:
     HIL_CUSTODY -> TVC_HIL_LIFECYCLE
     prior_receipt_hash = custody receipt hash
-> TVC must issue its own receipt only after actual admission
```

Required invariants:

```text
transport_protocol: InTr
always-on receiver prerequisite: false
manual bootstrap prerequisite: false
second user-operated device prerequisite: false
manual resubmission prerequisite: false
receiver readiness check before submit: false
same InTr operation preserved across retry: true
blind duplicate custody: prohibited
transport grants execution authority: false
authority transfer: false
GitHub runtime authority: NONE
credential authority: TV/TVC
```

Browser source:
- `assets/hil-direct-upload-v1.js` creates the ingress envelope before network transport and submits it as `intr_ingress_envelope`.
- A failed/ambiguous transport keeps the exact PDF, provenance, and InTr operation identity together in the participant record.
- `hil-receipt.html` automatically continues that same operation on load/online/foreground without waiting for a separate readiness probe. Manual retry remains an immediate override, not a required workflow.
- The browser accepts custody only after validating the complete receiver-returned InTr chain and the TVC-bound egress envelope.

Receiver source authority remains `StegVerse-org/LLM-adapter`. The receiver is responsible for issuing transport/custody receipts only after the corresponding boundary is actually verified. The browser may create the ingress Interlock request but may not self-issue a false receiver delivery receipt.

The third transition remains separately governed:

```text
HIL_CUSTODY -> TVC_HIL_LIFECYCLE
```

The HIL receiver creates and persists the egress Interlock envelope automatically, but it **must not** claim TVC admission. The existing TVC HIL lifecycle is responsible for validating that envelope/receipt chain and issuing the next receipt when custody is actually admitted.

This supersedes older Site text that described the valid runtime order as:

```text
receiver READY -> participant submit
```

The canonical order is now:

```text
participant submit -> InTr ingress Interlock -> receiving Interlock/custody -> downstream Interlock
```

Source/CI does not establish a live transport event or TVC admission.


## 2026-08-29 submission-triggered Universal Interlock/InTr transport

The prior activation sequence that required receiver READY before participant submission is superseded as an architectural prerequisite.

Canonical participant transport is now:

```text
tap Submit
-> hash exact PDF + canonical provenance
-> create stegverse.universal-intr-transport/v1
   source = DEVICE_SYSTEM / Site:HIL
   destination = STEGOS_ECOSYSTEM / HIL:Ingress
-> persist exact packet + transport intent locally before treating ambiguous transport as failure
-> POST the exact packet + same transport intent
-> receiving Interlock verifies exact payload binding
-> receiving boundary emits DEVICE_SYSTEM -> STEGOS_ECOSYSTEM InTr receipt
-> HIL ingress opens chained HIL:Ingress -> HIL:Custody Interlock
-> HIL custody receipt is chained to the ingress receipt
-> receiver durably creates HIL:Custody -> TVC:HIL-Lifecycle next Interlock intent
-> TVC admission remains separately receipted by TVC
```

Availability semantics:

```text
event_triggered = true
always_on_application_receiver_required = false
second_user_device_required = false
receiver_unavailable = DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION
exact_packet_transport_retry_allowed = true
blind_consequence_retry_allowed = false
```

The participant-facing client no longer performs a receiver-readiness preflight before Submit. A failed/ambiguous POST leaves the exact PDF, provenance, and exact transport intent on the device in `INTR_TRANSPORT_PENDING`. The receipt page automatically retries that same hash-bound transport intent on page load/network return/visibility return; it does not mint a new operation identity and does not require manual resubmission for current-format records.

A transport retry is not a blind consequence retry. Receiver/TVC/private-review/publication/Master-Records consequences remain separately governed and idempotent under their own receipts.

Current source state on this lane:

```text
Site universal transport intent generation: IMPLEMENTED_ON_BRANCH
readiness-before-Submit dependency: REMOVED_ON_BRANCH
automatic exact-intent retry: IMPLEMENTED_ON_BRANCH
receiver receipt-chain validation: IMPLEMENTED_ON_BRANCH
next TVC Interlock intent validation: IMPLEMENTED_ON_BRANCH
runtime transport observation: NOT CLAIMED
TVC lifecycle admission: NOT CLAIMED
```

## 2026-08-29 exact pre-transport staging + materialization request

The participant path now closes the browser/network ambiguity window before the direct HIL POST begins.

On **Submit**, the browser performs this ordering:

```text
hash exact PDF
-> build canonical HIL provenance
-> build one stegverse.universal-intr-transport/v1 intent
-> derive one stegverse.universal-intr-materialization-request/v1
   downstream_owner_ref = StegVerse-Labs/.github#246
-> write PDF bytes + provenance + transport intent + materialization request to IndexedDB
-> read back and independently re-hash/recompare the staged objects
-> only then attempt direct POST /api/hil/submissions
```

The materialization request is deterministic from the same transport intent, operation, packet, payload hash and destination used by the merged StegOS materialization seam (StegVerse-Labs/StegOS@5ac248c223c9233cb741cda7a2856c30b0afb017). It preserves:

```text
state = QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION
event_triggered = true
always_on_receiver_required = false
second_user_device_required = false
request_grants_execution_authority = false
claim_or_fence_minted = false
transport_grants_execution_authority = false
credential_authority = TV/TVC
github_token_runtime_authority = NONE
authority_effect = NONE_REQUEST_ONLY
```

A successful direct receiver transaction marks the participant record local materialization disposition as SATISFIED_BY_DIRECT_RECEIVER_RECEIPT; it does not convert the browser into a receiver or issue a TVC receipt.

If the direct POST is unavailable or ambiguous, the exact pre-staged packet remains INTR_TRANSPORT_PENDING with the same materialization ID and request hash. The receipt/recovery page preserves that request through later exact-intent retry. It does not mint a new transport operation.

This closes the source-level pre-transmission durability gap. It does not prove that the materialization request was transported from browser IndexedDB into a sovereign StegOS runtime, consumed by the .github materialization consumer, or followed by authentic HIL/TVC receipts. Those are still runtime observations.
