# ST-017 Sandbox Diagnostics Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#627`
Branch: `fix/st017-sandbox-diagnostics-627`
State: COMPLETE_VALIDATED_MERGED_PR626_CONSUMED
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

## Merge and downstream consumption evidence

- implementation PR: `#670`
- merge commit: `dd74c42a567a75d8bb46319ed7773444a8f09b21`
- refreshed Site #581 release PR: `#673`
- refreshed release head Site Bootstrap run `33290588297`: PASS
- release merge commit: `0facf6b55b2f6a49e75215bb5efacf6924d5c35e`
- original stale PR `#626` was superseded; its underlying release transition was consumed successfully

## Completion

- deterministic diagnostic test passes;
- local ST-017 still passes;
- exact-head hosted gates pass;
- PR merges;
- PR #626 bootstrap rerun yields either PASS or an actionable exact child failure.
