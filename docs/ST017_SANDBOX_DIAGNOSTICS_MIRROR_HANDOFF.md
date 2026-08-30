# ST-017 Sandbox Diagnostics Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#627`
Branch: `fix/st017-sandbox-diagnostics-627`
State: EXACT_HEAD_HOSTED_VALIDATION_PASS_MERGE_PENDING
Authority effect: NONE
Activation effect: false

## Purpose

Expose the already-captured bounded stdout/stderr tail for the first failed ST-017 sandbox
child command so hosted fail-closed validation identifies the real checker failure.

## Owned files

- `scripts/run_sandbox_validation.py`
- `tests/test_run_sandbox_validation_diagnostics.py`
- `docs/ST017_SANDBOX_DIAGNOSTICS_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-st017-sandbox-diagnostics-627.json`

## Invariants

- command order and arguments unchanged;
- expected exits unchanged;
- timeout unchanged;
- sandbox exclusions unchanged;
- first failure still stops execution;
- report schema and verdict semantics unchanged;
- output tails remain bounded to the existing 5,000-character capture;
- common credential-bearing authorization headers are redacted before console emission;
- no artifact transport, repository mutation, credential, authority, or activation is added.

## Trigger

PR #626 passes exact release-claim validation, handoff orchestration, heartbeat, and local
ST-017, but hosted Site Bootstrap reports only `validate-application: FAIL` without the
captured child output needed to identify the failing checker.

## Local validation evidence

- `python3 tests/test_run_sandbox_validation_diagnostics.py` -> `ST017_SANDBOX_DIAGNOSTICS_TEST_PASS`
- `python3 scripts/run_sandbox_validation.py` -> `SITE ST-017 SANDBOX: PASS`
- diagnostic output remains bounded and credential-redacted
- Site Bootstrap run `33290479592`: PASS
- Site Handoff Orchestrator run `33290479595`: PASS
- Ecosystem Heartbeat run `33290479616`: PASS

## Completion

- deterministic diagnostic test passes;
- local ST-017 still passes;
- exact-head hosted gates pass;
- PR merges;
- PR #626 bootstrap rerun yields either PASS or an actionable exact child failure.
