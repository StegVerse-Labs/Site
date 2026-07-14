# Minimal Reproducible Agentic Governance Experiment

## Experiment identifier

```text
experiment_id: SV-TTU-MRE-001
name: Commit-Time Authority Reconstruction Under Drift
status: SPECIFICATION_READY_IMPLEMENTATION_PENDING
```

## Purpose

Test whether an independent verifier can reconstruct the correct commit-time decision for an agent action when policy, delegation, identity, evidence freshness, or execution context changes between proposal and commit.

The experiment is intentionally runnable on a local machine before any request for institutional accelerated-computing access. Scaling work is a later phase.

This specification does not imply Texas Tech or NVIDIA participation, endorsement, access, or validation.

## Primary hypothesis

A verifier using canonical artifacts and explicit commit-time inputs can deterministically produce `ALLOW`, `DENY`, or `FAIL_CLOSED` without trusting the original agent runtime's asserted decision.

## Falsification criteria

The hypothesis fails for a case when any of the following occurs:

1. two conforming verifier runs over identical canonical inputs produce different decisions;
2. the verifier cannot identify the policy, delegation, identity, evidence, or context version used at commit time;
3. a stale or invalid artifact produces `ALLOW` when the expected result is `DENY` or `FAIL_CLOSED`;
4. the reconstructed decision depends on an unrecorded runtime assertion;
5. the receipt cannot bind input hashes, decision, reason codes, verifier version, and post-state hash;
6. a negative case is accepted because a required field is silently defaulted.

## Action under test

```text
action: release_dataset_summary
target: bounded_research_output
actor: agent_alice
requested_scope: project_alpha.summary.publish
execution_boundary:
  network: deny_except_declared_sink
  filesystem: read_declared_inputs_write_receipt_only
  credentials: none
  external_side_effects: publication_sink_only_after_allow
```

The action is illustrative and must use synthetic data. No private, controlled, institutional, medical, export-controlled, or production data is permitted.

## Canonical input set

```text
experiment/
  manifest.json
  actors.json
  policies.json
  delegations.json
  evidence.json
  execution_context.json
  transition_request.json
  expected_outcomes.json
  cases/
    case_001_valid_allow.json
    case_002_policy_drift_deny.json
    case_003_expired_delegation_deny.json
    case_004_stale_evidence_fail_closed.json
    case_005_identity_mutation_deny.json
    case_006_boundary_expansion_deny.json
  verifier/
    verify.py
  receipts/
  reports/
```

Every JSON artifact must use deterministic canonicalization before hashing. The canonicalization rule and implementation version must be recorded in `manifest.json`.

## Required cases

### Case 001 — Valid authority and admissible transition

- actor identity matches the delegation subject;
- policy is active at commit time;
- delegation includes the requested action, target, and scope;
- evidence is fresh;
- execution context remains within declared boundaries.

Expected result:

```text
ALLOW
```

### Case 002 — Policy drift before commit

- proposal references policy version 1;
- policy version 2 becomes authoritative before commit;
- version 2 prohibits the requested action or scope.

Expected result:

```text
DENY
reason_code: POLICY_NOT_VALID_AT_COMMIT
```

### Case 003 — Delegation expiration

- delegation is valid at proposal time;
- validity window expires before commit.

Expected result:

```text
DENY
reason_code: DELEGATION_EXPIRED
```

### Case 004 — Evidence freshness cannot be established

- required evidence has no trusted observation time, exceeds the freshness limit, or its hash cannot be resolved.

Expected result:

```text
FAIL_CLOSED
reason_code: EVIDENCE_FRESHNESS_UNRESOLVED
```

### Case 005 — Identity mutation

- the actor identifier remains the same;
- the authoritative identity or key binding changes before commit;
- the delegation does not bind the new identity state.

Expected result:

```text
DENY
reason_code: IDENTITY_BINDING_CHANGED
```

### Case 006 — Execution-boundary expansion

- the proposed action is otherwise authorized;
- the execution context adds an undeclared network sink, credential, filesystem write, actuator, or external side effect.

Expected result:

```text
DENY
reason_code: EXECUTION_BOUNDARY_EXCEEDED
```

## Decision semantics

```text
ALLOW:
  all required authority, policy, delegation, evidence, admissibility, and boundary predicates resolve true

DENY:
  sufficient canonical evidence proves at least one required predicate false

FAIL_CLOSED:
  a required predicate cannot be established from canonical evidence
```

Missing fields, unresolved pointers, unsupported canonicalization versions, hash mismatches, and unknown required artifact types must not default to `ALLOW`.

## Required receipt

Each run must emit a machine-readable receipt containing at least:

```json
{
  "schema": "stegverse.governance.experiment.receipt.v1",
  "experiment_id": "SV-TTU-MRE-001",
  "case_id": "case_001_valid_allow",
  "run_id": "<unique-run-id>",
  "started_at": "<RFC3339>",
  "committed_at": "<RFC3339>",
  "canonicalization": {
    "spec": "<identifier>",
    "implementation_sha256": "<sha256>"
  },
  "input_hashes": {},
  "verifier": {
    "name": "<name>",
    "version": "<version>",
    "source_sha256": "<sha256>"
  },
  "decision": "ALLOW|DENY|FAIL_CLOSED",
  "reason_codes": [],
  "expected_decision": "ALLOW|DENY|FAIL_CLOSED",
  "matches_expected": true,
  "authority_reconstructed": true,
  "runtime_assertion_trusted": false,
  "execution_boundary_checked": true,
  "post_state_sha256": "<sha256>"
}
```

## Verification procedure

1. Validate the manifest and required file inventory.
2. Canonicalize each input artifact using the declared specification.
3. Verify all declared hashes and references.
4. Resolve the commit timestamp and authoritative artifact versions.
5. Reconstruct actor identity and key binding at commit time.
6. Reconstruct policy validity and applicable rules.
7. Reconstruct delegation validity, scope, action, and target.
8. Evaluate evidence freshness and integrity.
9. Evaluate transition admissibility.
10. Evaluate execution-boundary compliance.
11. Emit the decision and reason codes.
12. Compare the result with `expected_outcomes.json`.
13. Emit the receipt and a human-readable report.
14. Re-run each case at least twice and compare receipt decision fields and post-state hashes.

## Initial workload profile

Local baseline:

```text
cases: 6
agents: 1
policies: 2 versions
identities: 2 states
runs_per_case: 10
expected_total_runs: 60
input_size: less than 10 MB
accelerator_required: no
```

Scaling phases:

```text
Phase 1: 100 agents, 1,000 transitions, 10 policy perturbations
Phase 2: 1,000 agents, 100,000 transitions, concurrent model-serving workload
Phase 3: 10,000+ agents, repeated simulations, large evidence graph, adversarial perturbation matrix
```

Accelerated computing becomes relevant in Phase 2 or Phase 3 when model inference, simulation concurrency, evidence-graph processing, or repeated perturbation sweeps dominate runtime. Governance verification itself must remain testable independently of a specific accelerator platform.

## Measurements

Required measurements:

- decision correctness against expected outcomes;
- determinism across repeated runs;
- false-allow count;
- false-deny count;
- unresolved/FAIL_CLOSED count;
- verifier latency per transition;
- throughput in transitions per second;
- peak memory;
- receipt bytes per transition;
- evidence-storage growth;
- coordination overhead as agent count increases;
- time to independently reconstruct a completed run.

## Acceptance criteria

The minimal experiment reaches implementation-complete status only when:

1. all six canonical cases exist;
2. expected outcomes are machine-readable;
3. the verifier rejects malformed and incomplete inputs;
4. repeated runs are deterministic for decision and reason codes;
5. every case emits a complete receipt;
6. no false `ALLOW` occurs in negative cases;
7. run instructions work from a clean environment;
8. artifact paths and immutable commit references are recorded in the evidence map;
9. limitations and non-claims remain visible;
10. an independent implementation or reviewer can reproduce the result before any claim of independent reconstruction.

## Current state and next build

```text
specification: complete
fixtures: not yet installed
verifier: not yet installed
expected_outcomes: not yet installed
receipts: not yet generated
independent reproduction: not started
```

Next build actions:

1. create the canonical JSON schemas and six fixtures;
2. implement a standard-library verifier;
3. add malformed-input and missing-artifact negative tests;
4. generate local receipts and reports;
5. attach immutable paths, hashes, and evidence maturity levels to the evidence map;
6. request independent reproduction only after the local package passes.
