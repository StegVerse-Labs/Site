# ST-017 Sandbox PR Context Isolation Mirror Handoff

Updated: 2026-08-29

```text
goal_id: SITE-ST017-SANDBOX-PR-CONTEXT-622
issue: StegVerse-Labs/Site#622
repository: StegVerse-Labs/Site
branch: fix/st017-sandbox-pr-context-622-20260829
state: IMPLEMENTED_ON_BRANCH_VALIDATION_PENDING
authority_effect: NONE
activation_effect: false
credential_authority: TV/TVC
github_runtime_authority: NONE
```

## Defect

ST-017 intentionally copies Site into a temporary repository sandbox without `.git`. Before this repair, child commands inherited the parent GitHub Actions PR/ref/run environment. `site_handoff_orchestrator.py` therefore entered pull-request ownership mode inside a sandbox that intentionally lacked the Git history required to prove a terminalization-only claim transition.

This produced a false sandbox failure after the real parent PR ownership/orchestration checks had already passed.

## Repair

`scripts/run_sandbox_validation.py` now derives an explicit child environment that removes GitHub Actions, GitHub PR/ref/run/token and runner-specific context before executing sandbox commands. Ordinary local environment values remain available. The child environment declares:

```text
STEGVERSE_SANDBOX_ISOLATION=LOCAL_REPOSITORY_ONLY
STEGVERSE_GITHUB_RUNTIME_AUTHORITY=NONE
STEGVERSE_CREDENTIAL_AUTHORITY=TV/TVC
```

The parent workflow still performs actual PR claim admission, credential refusal and Site orchestration before ST-017. This repair does not weaken those gates; it prevents an isolated portable-repository test from re-adjudicating GitHub PR ownership without `.git`.

## Evidence boundary

Source/tests:

```text
scripts/run_sandbox_validation.py
tests/test_run_sandbox_validation_environment.py
```

Required hosted evidence before merge:

```text
focused environment regression: PASS
Site Handoff Orchestrator: PASS
Ecosystem Heartbeat Orchestration: PASS
Site Bootstrap Validate: PASS
ST-017 validate-application: PASS
```

No deployment, HIL runtime, transport, custody, review, publication or release authority is created by this lane.
