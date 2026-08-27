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


## 2026-08-24 insecure-origin runtime failure evidence and repair

A real iPhone Messages browser submission loaded the public chat on an `http://stegverse.org/...system-chat.html` URL and submitted `What time is it?`. The page rendered, but the general capability returned the generic local failure message.

The source cause is bounded and reproducible from the topology: general conversation calls the StegOS Service Worker local-intercept bridge, while an insecure non-localhost origin cannot provide the required secure Service Worker execution context.

Repair lane:

```text
claim: SITE-ECOSYSTEM-CHAT-SECURE-CONTEXT-20260824
branch: fix/ecosystem-chat-secure-context-20260824
source repair: ecosystem-chat.html redirects non-localhost HTTP loads to the equivalent HTTPS URL before conversational runtime initialization
credential authority: TV/TVC
GitHub-token runtime authority: NONE
authority effect: NONE
activation effect: false
```

Completion remains open until canonical validation passes, the change merges and deploys, the public page is observed on HTTPS, and a real browser request returns a reconstructed response. The source repair alone is not runtime proof or product activation.


## 2026-08-24 reconstructed-but-irrelevant response evidence

A post-#483 iPhone submission on the HTTPS public surface reached the device-local executor and returned a reconstructed response, proving that the secure-context startup, Service Worker intercept, task fence, and response transport were active. The response to `What time is it?` was nevertheless unrelated governance prose.

Root cause:

```text
stegverse-reference-lm-v1 is a bounded second-order reference model
training corpus is a single StegVerse governance paragraph
production_llm_equivalent: false
transport/runtime proof: observed
semantic adequacy for the user request: FAIL
```

Repair lane:

```text
claim: SITE-ECOSYSTEM-CHAT-SEMANTIC-CLOCK-20260824
branch: fix/ecosystem-chat-semantic-clock-20260824
device-local clock capability: installed in the Site-owned shared conversational client
canonical reference-model projection: unchanged; no competing model/runtime authority created
unrelated governance-prose clock response: bypassed by deterministic clock classification
authority effect: NONE
activation effect: false
```

This advances the evidence state from runtime unavailable to runtime executed with a semantic failure. Completion remains open until exact-head validation, merge, deployment, and a new iPhone observation show a relevant clock response with reconstructed execution evidence. A bounded clock repair does not make the reference model a production conversational LLM. The exact StegOS/reference-model projection remains unchanged; admitted genuinely conversational local-model integration remains the next runtime goal under the existing micro-node-runtime/TVC/LLM-adapter owners.

## 2026-08-27 deterministic clock evidence-contract reconciliation

Live inspection after PR #484 proved that the deployed asset contained the clock repair, but exposed a structural mismatch in the active claim: `deterministicGeneralCapability()` returned before `executeDeviceRaw()`. The response could therefore be semantically correct while carrying no reconstructed execution evidence. A screenshot alone could not satisfy the claim as written.

The bounded continuation preserves the execution distinction:

```text
claim: SITE-ECOSYSTEM-CHAT-SEMANTIC-CLOCK-20260824
continuation branch: fix/ecosystem-chat-clock-evidence-20260827
clock execution kind: deterministic capability
model_execution: false
receipt input: request + output + epoch + locale + timezone + reconstructed output
receipt digest: SHA-256
same-execution reconstruction: required PASS
receipt persistence: sessionStorage + EcosystemRuntime.status()
public DOM evidence: response data attributes; internal jargon remains hidden
authority effect: NONE
activation effect: false
```

This does not turn the deterministic clock into model inference and does not replace the canonical StegOS Service Worker or `StegVerse-002/micro-node-runtime` evidence owner. The already-observed post-#483 response remains proof that the Service Worker/model path executed and reconstructed; the clock receipt proves only the separately admitted deterministic capability execution.

Release remains open until exact-head validation passes, the repair merges and deploys, and a real iPhone clock request returns the correct device time with the machine-visible deterministic receipt. Genuinely conversational local-model integration remains the next distinct goal under the existing micro-node-runtime/TVC/LLM-adapter owners.


## 2026-08-27 hosted Math validation observation

The earlier `Math hosted exact-head validation: PENDING` statement is now superseded by later canonical Site evidence for the installed source boundary:

- canonical Math application-binding commit `f5f8e145c49622711ade0920dc04460e424ea1c2` is an ancestor of Site source head `4a13c991dcfb83eccee3fb57cbf41de866466f0e`;
- `.github/workflows/validate.yml` directly executes `scripts/check_ecosystem_chat_application.py`;
- that application validator directly executes `scripts/check_ecosystem_chat_boundary.py`, which owns the shared Math routing/candidate-only/image-transcription boundary;
- Bootstrap run `33044633784` completed SUCCESS;
- subsequent Site Task Runner `33044661032` completed SUCCESS with no failed steps;
- later full Site Task Runner `33045293923` also completed SUCCESS.

Therefore the installed shared-runtime Math source boundary has hosted validation evidence. This does not execute `governed_math_solver` or `math_verifier`, admit attachment/image intake, prove mathematical correctness authority, or activate the product.

Because this is a material evidence/task-state advance relative to alignment transition 004, the append-only state-language chain must record the next task transition as 005+ before the Math machine task is promoted beyond its previous state. Do not rewrite transition 004.

Next Math boundary:
1. emit/custody the append-only 005+ alignment transition for hosted source-validation evidence;
2. then separately admit either governed solver/verifier execution with replayable receipt or attachment/image intake under privacy/attachment authority;
3. keep solver/verifier candidate-only until actual admitted execution evidence exists.


## 2026-08-27 Math source-validation gate complete

Append-only alignment transition `ALIGN-UNIFIED-CONVERSATION-MATH-HOSTED-VALIDATION-005` was emitted at `.github@4157dbca945cc13d02b756559ccab5219cba6af9` and custodied at `master-records/orchestration@1b3966d7a346133af57aea6bf35922002979023c`.

Master Records hosted run `33120909226` / job `98687235580` then completed SUCCESS with the repository pytest suite. The canonical all-custody test iterates every state-alignment custody object through the verifier. Persisted result: 325 tests, 0 failures, 0 errors.

The Math machine task is now:
```text
Site commit: 5fdeff1fd3341d4487176f507b6cf54bbaa3d709
state: RESIDENT_SOURCE_CONSUMPTION_HOSTED_VALIDATED_TOOL_EXECUTION_PENDING
projection_state: CONSUMED_BY_RESIDENT_SOURCE_HOSTED_VALIDATED
governed_math_solver: CANDIDATE_ONLY_NOT_EXECUTED
math_verifier: CANDIDATE_ONLY_NOT_EXECUTED
attachment/image intake: NOT YET ADMITTED
activation_effect: NONE
```

Next Math work is no longer another source-validation pass. Admit exactly one bounded next slice under the existing shared runtime: replayable solver/verifier execution OR privacy-governed attachment/image intake. Any material state advance becomes append-only transition 006+.


## 2026-08-27 governed Math Solver unified-consumer installation

The next source slice is now installed under the existing shared conversational runtime; no second Math runtime or evaluator was created.

Source changes:
- `1f16a9116b44996d6611fd9a69766cb325d015db` — `askMath` detects only narrow user-requested arithmetic candidates and invokes the canonical Math Solver only after a verified Site activation receipt;
- `e9bec934942e09ee8c0e899b65649ec5e0ea3598` — Site activation receipt consumption fails closed unless the complete LLM-adapter observer check set, StegVerse runtime authority, TV/TVC credential authority, and GitHub-token runtime authority NONE are proven;
- `8df5129845c23fa5755299379ac1cea8bd378416` — canonical shared-runtime validator locks the governed solver/StegGate identity and evidence requirements;
- `577e3fc1475b00ad7ec8ad6725e4dc1fb8eabef2` — active Math worker reconciled from stale Render-host repair to sovereign carrier observation;
- `a2f9e4ed9ee0834a7e26f24661386a13ed4bb8b5` — legacy hourly/writeback Math activation workflow reduced to validation/evidence transport only;
- `1714524a5db47f0fdaaef079338534a4472aa5df` — workflow inventory reconciled;
- `c1c9663490b0d35203bde53379c96aa908df59e2` — Math task state projected to `GOVERNED_SOLVER_CONSUMER_INSTALLED_HOSTED_REVERIFY_PENDING`.

Alignment:
- transition 006 emitted at `.github@9901f7ae1993421fe8f51eda48a5eb591c7cb669`;
- Master Records custody accepted at `7ab374d88a6e047fb76ba84c163f4b7660cce240`;
- hosted Site and Master Records reverification remain pending.

Current runtime truth is unchanged: `receipts/math-solver-public-runtime.latest.json` remains BLOCKED / STEGVERSE_RUNTIME_UNAVAILABLE. No actual governed solver execution is claimed. The next runtime boundary remains eligible StegVerse carrier readiness -> governed solve -> replay -> COMPLETE runtime receipt -> Site direct consumption/observation.


## 2026-08-27 governed Math consumer hosted validation complete

The installed governed-solver consumer is now hosted-validated at exact Site head `4e6a9f920971902fce98fc17fb1d78cf68a0e2b3`.

Evidence:
- Math Solver public activation validation `33121892595` / job `98690515902`: SUCCESS;
- Site Bootstrap `33121892559` / job `98690515240`: SUCCESS;
- Master Records all-object custody validation `33121586481` / job `98689500256`: SUCCESS, 326 tests / 0 failures / 0 errors;
- Math task projection commit `153454fc8f73d0b6387b1779920aa34babf59e46`.

Current state:
```text
governed solver consumer: IMPLEMENTED + HOSTED VALIDATED
alignment transition 006: EMITTED + CUSTODIED + HOSTED VALIDATED
actual Math Solver carrier observation: PENDING
actual governed solver execution: NOT OBSERVED
current LLM-adapter runtime receipt: BLOCKED until newer evidence says otherwise
activation effect: NONE
```

The next executable Math boundary is no longer Site source construction. It is canonical LLM-adapter#132 observation of an eligible StegVerse Service Gateway/portable-node carrier, followed by a COMPLETE runtime receipt and then fail-closed Site consumption of that exact receipt.
