# MIR connection and round-trip technical guide mirror handoff

Updated: 2026-09-12
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/Site#1277`
Primary guide: `docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`
Reusable Task Component Model merge: `StegVerse-Labs/.github@b9f8e5153aa1651f2d7f043fb902eacb7c113ed9`
Goal Task component profile: `StegVerse-Labs/.github/data/goal-task-transport-profiles/MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001.json`
Global lifecycle contract: `StegVerse-Labs/.github/docs/CANONICAL_SOUTHBOUND_COMMUNICATION_LIFECYCLE.md`
SDK complete-manifest merge: `StegVerse-org/StegVerse-SDK@d3140a04e7405fe117c9808734d23a1027e68ead`
SDK Publisher-return binding merge: `StegVerse-org/StegVerse-SDK@6a1dd2c05425f61c9b7264abf26731dba27d583b`
LLM Adapter reusable egress merge: `StegVerse-org/LLM-adapter@7c7c43a0171360ce7ed4cc2873b29686147845ae`
Status: `ACTIVE / REUSABLE COMPONENT COMPOSITION RECONCILED / FINAL COMPLETION BLOCKED ON AUTHENTIC END-TO-END PROOF`

## Reusable Task Component reconciliation — 2026-09-12

The current Goal Task remains valid and retains its existing identity and COSV. No new Goal Task is required merely because reusable capabilities were identified.

Applying the canonical decomposition policy yields a score of `28`, above the `13+` threshold:

```text
STOP_SCOPE_GROWTH_AND_DECOMPOSE_BEFORE_ADDING_MORE_TASK_SPECIFIC_ORCHESTRATION
```

Active signals are repeated subflows, multiple authority crossings, multiple round trips, cross-repository spread, duplicated generic adapter risk, handoff-sequence growth, independent reusability, optional subprocesses, and independently provable evidence predicates.

Therefore the long MIR-specific orchestration sequence is now represented as a composition of reusable components. This changes source architecture/composition only; it does not change any runtime evidence state.

## Goal Task -> reusable component composition

```text
MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001
  -> RTC-MANIFEST-001
  -> RTC-GOVERNED-PROCESSING-002
  -> RTC-ROUNDTRIP-003                  [MIR historical/accounting round trip]
  -> RTC-EVIDENCE-CUSTODY-004
  -> RTC-PUBLISHER-005
  -> RTC-SDK-RETURN-006
  -> RTC-STEGVERSE-EGRESS-007
  -> RTC-INTERLOCK-INTR-TRANSPORT-008   [repeatable; three declared occurrences]
  -> RTC-FARSIDE-FINAL-009
```

For this Goal Task, `RTC-INTERLOCK-INTR-TRANSPORT-008` is required at three distinct points:

1. StegVerse -> MIR outbound transport;
2. MIR -> StegVerse return transport;
3. final StegVerse -> original initiator egress.

`RTC-ROUNDTRIP-003` is required once for the declared MIR historical/accounting request-response cycle. The component is reusable/repeatable globally, but this task does not force additional round trips merely because the maximal transport family permits them.

## Component ownership and evidence

### RTC-MANIFEST-001 — Manifest Intake and Binding

- existing: yes;
- canonical implementation/owner: StegVerse SDK complete-manifest contract;
- input: original request, complete manifest, task/COSV binding;
- output: validated manifest and declared evidence requirements;
- expected evidence: manifest hash/validation and task/COSV correlation;
- authority effect: none.

### RTC-GOVERNED-PROCESSING-002 — Governed Processing

- existing: yes;
- owner: manifest-selected StegVerse processor, with Interlock/InTr transition authority where applicable;
- input: admitted manifest plus `processing.capability` and `processing.route_id`;
- output: processor result and route receipts;
- evidence: installed-route resolution, processor receipt, no source-identity routing substitution.

### RTC-ROUNDTRIP-003 — Governed Round Trip

- existing: yes;
- owner split: Interlock/InTr for transitions, MIR for historical/accounting semantics, TV/TVC for required credentials;
- input: bounded MIR request and exact outbound correlation binding;
- output: MIR-native response plus extended receipt chain;
- evidence: outbound receipt, MIR ingress/evaluation evidence, MIR return receipt, exact request/response correlation;
- cardinality for this goal: one MIR historical/accounting round trip.

### RTC-EVIDENCE-CUSTODY-004 — Evidence Custody and Reconstruction

- existing: yes;
- owner: Master Records;
- input: authentic receipts and source-native evidence;
- output: custody/readback/reconstruction where requested;
- runtime evidence remains unobserved for this goal.

### RTC-PUBLISHER-005 — Publisher Projection

- existing: yes;
- owner: `GCAT-BCAT-Engine/Publisher`;
- input: authentic retained evidence plus manifest-declared presentation/evaluator requirement;
- output: canonical Publisher artifact-return;
- required by this Goal Task's complete-manifest proof, optional globally.

### RTC-SDK-RETURN-006 — SDK Return Assembly

- existing: yes; source implementation merged at `6a1dd2c05425f61c9b7264abf26731dba27d583b`;
- owner: StegVerse SDK;
- input: exact Publisher artifact-return plus original manifest receipt/initiator/projection/egress declaration;
- output: `stegverse.sdk.publisher-return-binding/v1` in `READY_FOR_FINAL_STEGVERSE_EGRESS_TRANSITION`;
- source validation does not prove runtime visitation.

### RTC-STEGVERSE-EGRESS-007 — Final StegVerse-side Egress Transition

- existing: yes; reusable `LLM_ADAPTER` framework implementation merged at `7c7c43a0171360ce7ed4cc2873b29686147845ae`;
- owner separation: LLM Adapter performs protocol/framing; Interlock/InTr owns the actual governed state transition;
- input: exact SDK return binding and manifest-declared egress surface;
- output: final StegVerse-side egress candidate plus exact InTr handoff;
- no provider-specific egress implementation may be reused as a substitute for a generic SDK result;
- source validation does not prove runtime visitation or InTr egress.

### RTC-INTERLOCK-INTR-TRANSPORT-008 — Interlock/InTr Transport

- existing: yes;
- owner: Interlock/InTr;
- input: governed packet/transition candidate plus TV/TVC credential material where applicable;
- output: authentic ingress/egress transition receipts bound to exact bytes;
- required three times for this task;
- no task-specific duplicate transport/materialization path is permitted.

### RTC-FARSIDE-FINAL-009 — Far-side Final Transition

- existing contract: yes;
- owner: far-side Interlock/InTr transition authority;
- input: authentic final egress plus original initiator lineage;
- output: far-side receive/final transition and caller receipt;
- terminal communication cannot be claimed before this evidence exists.

## Non-transport reusable/canonical dependencies

- Worker claim/fence: `WorkerCoordinator` only when runtime execution requires worker ownership.
- Credential/session handling: `TV/TVC` only.
- User verification: `KV/SKAP Vault` only.
- StegOS devices: interchangeable transport/execution nodes; never user verifiers or user-identity authorities.
- Runtime observation: existing resident runtime surfaces plus HeartBeat observability only.
- Framework translation: LLM Adapter for applicable framework paths; must reuse the selected transport components rather than create a parallel transport stack.
- Master Records: observed-reality custody/reconstruction only.
- GitHub: source/evidence coordination only; runtime authority `NONE`.

No device-local user verification is required or permitted by this composition.

## Duplicate orchestration superseded

The following task-specific patterns must not be extended further:

- MIR-specific Publisher -> SDK return assembly; reuse `RTC-SDK-RETURN-006` and the merged SDK implementation.
- MIR-specific generic framework final-egress transport; reuse `RTC-STEGVERSE-EGRESS-007` and the merged LLM Adapter framework implementation.
- MIR-specific duplicate InTr materialization/transport logic; reuse `RTC-INTERLOCK-INTR-TRANSPORT-008`.

Historical evidence and prior source provenance remain retained; supersession means future composition/reuse, not deletion of history.

## Newly identified reusable candidate

`callback_correlation` remains a canonical Reusable Task Component Model candidate. Exact response-to/original-request correlation is independently useful across MIR, external frameworks, providers, and callbacks. No standalone canonical component contract was found during this reconciliation, so this goal does **not** create a new Goal Task or duplicate a bespoke correlation subsystem. Until materialized canonically, the required exact correlation fields remain parameterized evidence within `RTC-ROUNDTRIP-003`.

## Runtime truth preserved

The Reusable Task Component Model does not upgrade evidence. Current authentic runtime state remains:

```text
qualifying outbound MIR transport observed: false
qualifying MIR ingress receipt observed: false
qualifying MIR evaluation observed: false
qualifying MIR return transport observed: false
qualifying StegVerse return ingress observed: false
Master Records runtime custody/readback for this round trip observed: false
Publisher runtime execution observed: false
SDK runtime return binding observed: false
final StegVerse-side runtime egress transition observed: false
Interlock/InTr final egress observed: false
far-side Interlock/InTr final transition observed: false
roundtrip verified: false
```

Source construction, reuse, CI, static compatibility, or merge status do not satisfy any of those predicates.

## Remaining Goal Task-specific completion predicates

This Goal Task remains incomplete until the reusable composition produces authentic evidence for the applicable predicates:

1. authentic StegVerse outbound InTr materialization to MIR;
2. authentic MIR-facing ingress receipt;
3. authentic MIR historical/accounting evaluation over the admitted payload;
4. authentic MIR-native return through designated InTr;
5. exact response-to/original-request correlation;
6. authentic StegVerse return InTr ingress;
7. canonical SDK manifest admission and manifest-selected processing receipt;
8. Master Records custody/readback/reconstruction when requested;
9. authentic Publisher execution when declared;
10. authentic SDK runtime return binding;
11. authentic final StegVerse-side egress transition;
12. authentic Interlock/InTr final egress;
13. authentic far-side final transition/caller-side receipt;
14. technical guide reconciled against exact observed runtime behavior.

## Non-negotiable communication invariant

For this MIR connection there is exactly one communication medium:

```text
DESIGNATED UNIVERSAL INTERLOCK / INTR TRANSPORT PROTOCOL
```

Email, Gmail, shared documents, Google Docs, PDFs, manually exchanged files, generic web forms, direct provider/API calls outside the designated InTr path, or any other out-of-band channel are non-qualifying for runtime, delivery, evaluation, return, or round-trip predicates.

A source-native MIR or StegVerse object may be the payload carried by the designated protocol. TV/TVC credential brokerage may support an authenticated transport operation but does not create an alternate communication path.

## Processing invariant

Source/provider/framework/adapter/device/transport identity must not select StegVerse processing semantics.

```text
admitted manifest
-> processing.capability
-> processing.route_id
-> installed-route resolution/admissibility
-> manifest-selected processor
```

## Current source state

- Reusable Task Component Model: merged at `b9f8e5153aa1651f2d7f043fb902eacb7c113ed9`.
- Canonical SOUTH lifecycle: merged.
- SDK complete-manifest contract: merged.
- SDK Publisher-return binding (`RTC-SDK-RETURN-006` implementation): merged at `6a1dd2c05425f61c9b7264abf26731dba27d583b`.
- LLM Adapter reusable generic SDK-return egress (`RTC-STEGVERSE-EGRESS-007` framework implementation): merged at `7c7c43a0171360ce7ed4cc2873b29686147845ae` after exact-head Work Mutation Safety, dedicated SOUTH validation, and repository-wide validation passed.
- Goal Task component profile/task-record reconciliation: `.github` PR #1654, exact-head control-plane validation required before merge.

## Next admissible work

1. validate and merge the Goal Task reusable-component profile/task-record reconciliation;
2. merge this Site handoff/claim reconciliation only after exact-head Site validation remains green;
3. stop adding task-specific transport/return machinery;
4. execute the MIR proof by invoking the selected reusable components in declared order;
5. retain authentic component evidence without inferring later components from earlier receipts;
6. reconcile the guide only from exact observed runtime.

## Completion boundary

This documentation goal remains `ACTIVE`. It must not become `COMPLETE` from reusable source construction, CI, merge state, or architecture reconciliation. Completion still requires the authentic end-to-end evidence listed above.
