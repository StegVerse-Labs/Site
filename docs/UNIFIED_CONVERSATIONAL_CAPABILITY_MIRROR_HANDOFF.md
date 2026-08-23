# Unified Conversational Capability Mirror Handoff

## Source of truth

This is the authoritative continuation record for the shared Site conversational topology and `StegVerse-Labs/Site#239`.

```text
Goal: one primary governed conversational surface with specialty capability families
Repository: StegVerse-Labs/Site
Canonical branch: main
Canonical issue: StegVerse-Labs/Site#239
Primary public surface: ecosystem-chat.html
Shared runtime owner: StegVerse-org/LLM-adapter
Device-local execution surface: StegOS service-worker bridge
VA specialty owner: StegVerse-Labs/Site#113
Mathematics specialty owner: StegVerse-Labs/Site#240
HIL owner: StegVerse-Labs/Site#81/#136/#243
Canonical StegGate owner: StegVerse-Labs/StegCore#68
```

## Product topology

```text
user request
-> ecosystem-chat.html
-> shared intent/context classification
-> capability family selection
-> admitted runtime/evidence/tool path
-> conversational response
-> separately admitted transition/action only when required
```

Capability families remain `general_ecosystem`, `vacc_va`, `mathematics_educator`, and `hil_experiment`. Dedicated pages may remain deep workspaces or protocol destinations, but they do not create another primary provider/runtime authority.

## Shared browser/device-local runtime

PR #402 merged the ordinary non-VA conversation onto the same admitted StegOS device-local inference bridge used by the primary shared surface:

```text
merge: ad0ecdf1b502fda1abb375067da96710c01ec804
shared runtime client: assets/ecosystem-chat-va-runtime.js
primary client: assets/ecosystem-chat-simple.js
bridge: stegos-bootstrap/ecosystem-chat-bridge.html
boundary validator: scripts/check_ecosystem_chat_boundary.py
```

The bridge result is rejected unless `same_execution: true` and `reconstruction_state: PASS`. Browser/device-local proof remains distinct from resident sovereign-carrier proof.

## Typed state/task propagation

Canonical upstream state:

```text
StegVerse-Labs/.github/control/state-projections/unified-conversational-capability.json
StegVerse-Labs/.github/control/task-projections/unified-conversational-capability.json
canonical state hash: b01c9197a735eed4f5a460320db1fec01ea5a232d0a4fd87884809ac7d47e3b7
```

Site-local state mirror:

```text
data/state-projections/unified-conversational-capability.json
commit: 5710cc35d064efc7940310a27356c75b9ba22538
canonical normalized hash: b01c9197a735eed4f5a460320db1fec01ea5a232d0a4fd87884809ac7d47e3b7
```

The Math and HIL task endpoints carry top-level `source_state_vector_ref` and `source_state_hash`, opting them into the WorkerCoordinator stale-state preclaim guard. Missing, unreadable, out-of-root, or changed canonical state fails closed before worker selection, claim, or fencing.

## State-alignment evidence through transition 003

```text
001: ALIGN-UNIFIED-CONVERSATION-TASK-PROJECTION-001 — custodied + hosted validated
002: ALIGN-UNIFIED-CONVERSATION-SITE-ENDPOINTS-002 — Site Math/HIL endpoint materialization
003: ALIGN-UNIFIED-CONVERSATION-SITE-PRECLAIM-BINDING-003 — Site-local state + enforceable preclaim binding
```

Transition 003 packet is `.github@42178202dddd134564f18958e3ef4ce7b6d50303`; Master Records custody is `11062ac51a2f1b4be22dde9baf4657ada5ed6db5`, reconstruction PASS, authority NONE. Hosted all-object reverification for transitions 002/003 remains a separate evidence predicate.

## Mathematics specialty — resident source consumption installed

The released upstream specialty profile is `StegVerse-org/LLM-adapter/profiles/math-educator-specialty.v1.json` at upstream release commit `878c5b4c30214da9a74f5bf0a2ca0fe38cb25a12`. Site#240 now consumes that specialty through the existing shared conversation/runtime rather than a second provider/runtime lane.

Installed bounded slice:

```text
assets/ecosystem-chat-va-runtime.js
  commit: 6c1acfc02bc0abd69a01daf7338f68323f056478
  adds deterministic Math intent/continuity routing, educator prompting, separate Math history,
  and non-authorizing governed_math_solver/math_verifier candidates

assets/ecosystem-chat-simple.js
  commit: 005035a56b36a75c38fb8e61270918624d6a8e1d
  routes Math messages to askMath while preserving VA interception and one primary chat

ecosystem-chat.html
  commit: 6f05dd2127558bfb17e6bd8570274429f86be83c
  exposes ordinary-language Math help from the primary surface

scripts/check_ecosystem_chat_boundary.py
  commit: 2cb79bcc1d73b4776384b9228041faae1fadafb7
  proves shared-runtime Math routing, candidate-only tool authority, and image/transcription separation boundary

scripts/check_ecosystem_chat_application.py
  commit: f5f8e145c49622711ade0920dc04460e424ea1c2
  now includes the shared-chat boundary in canonical Site application validation

data/tasks/UNIFIED-CONVERSATION-MATH-SPECIALTY-001.json
  commit: bef3ac521344b2732085858af0c5ae8f444c573a
  state: RESIDENT_SOURCE_CONSUMPTION_INSTALLED_HOSTED_REVERIFY_PENDING
```

The Math slice does **not** auto-execute `governed_math_solver` or `math_verifier`; both remain `CANDIDATE_ONLY_NOT_EXECUTED`. A calculated answer is not proof authority. The prompt boundary keeps `source_image` distinct from `interpreted_mathematical_transcription`, but public attachment intake is still pending its separately admitted privacy/attachment path.

## Dual-view collision reconciliation

The old overlapping PR #407 is closed unmerged as superseded. The canonical dual-view repair is already complete through PR #425 and release commit `d9ce13c8a95d178ad66a93b649b918a7911958c3`; the repository task records all observed release gates SUCCESS. Current `ecosystem-chat.html` retains the required `#console + .chat-shell` binding and the dual-view renderer while also carrying the Math entry. Do not resurrect #407.

## HIL state

The HIL specialty projection remains state-bound and separately owned by #81/#136/#243. A separate worker has merged the sovereign receiver discovery correction on current main. Do not duplicate or infer live HIL receiver/participant activation from the projection or discovery repair.

## Public UI requirement

```text
ordinary language first
technical competency assumption: none
internal architecture hidden by default
contextual links/actions only when useful
no public worker/runtime/receipt jargon unless needed for a user-visible limitation
```

## Authority / collision boundary

- Do not create a second primary conversational surface.
- Do not create a second VACC or Math provider/runtime lane.
- Do not duplicate HIL participant/runtime authority.
- Do not duplicate heartbeat, TVC route authority, StegGate, or Master Records custody authority.
- No NON-TV/TVC secret/token.
- Model output grants no execution authority.
- Source installation, validation success, or custody does not equal product activation.

## Current evidence state

```text
unified topology reconciliation: MERGED
browser/device-local general execution mechanism: PROVEN_PREVIOUSLY
Math shared-runtime source consumption: INSTALLED
Math canonical application validation binding: INSTALLED
Math hosted exact-head validation: PENDING
Math solver/verifier governed execution: NOT YET EXECUTED
Math attachment/image intake: NOT YET ADMITTED ON PRIMARY SURFACE
HIL state-bound projection: INSTALLED_SEPARATE_OWNER
resident sovereign carrier: PENDING_DISTINCT_PROOF
product activation: INCOMPLETE
```

## Next executable work

1. Observe the push-triggered Site Bootstrap/canonical application validation containing `f5f8e145...` and the Math boundary; repair only the first exact failure without weakening gates.
2. Emit/custody append-only transition 004 for the Math resident source-consumption state change; hosted proof may remain explicitly pending until observed.
3. After source validation, advance the next bounded Math slice: separately admitted attachment/image intake or governed solver/verifier execution with replayable receipts; do not auto-execute tools.
4. Continue HIL live receiver/participant proof under its existing owners and resident-carrier proof under its distinct lane.
5. Propagate to Publisher/admissibility-wiki/stegguardian-wiki only after real release/activation predicates are satisfied.
