# Site Activation Ledger Mirror Handoff

## Source of truth

This file is the current subordinate handoff and task source of truth for the Site activation-ledger workstream in `StegVerse-Labs/Site`.

The repository-wide authority boundary remains governed by `docs/SITE_MIRROR_HANDOFF.md`. This handoff may narrow activation claims but may not broaden them.

## Goal

```text
Goal: bind verified Ecosystem Chat activation evidence into one fail-closed ledger without granting deployment, execution, custody, release, or activation authority
Parent goal: fully functional governed Ecosystem Chat request-response, provider, custody, comparison, and cross-entry usage path
Current result: ACTIVATION_LEDGER_AND_ADVERSARIAL_GUARDS_INSTALLED_VALIDATION_OBSERVATION_PENDING
```

## Installed files

```text
docs/SITE_ACTIVATION_LEDGER.json
scripts/check_site_activation_ledger.py
scripts/test_site_activation_ledger.py
scripts/check_site_workflow_inventory.py
```

## Installed commits

```text
8a03a4f791f72a406d681f73ee0b1a400291e480  add fail-closed activation evidence ledger
4456971ae8ef7107e55d2eaba450cb074e7fdc17  add fail-closed activation ledger validator
e41558bb615cff21afc1707499c48fbee673534a  bind activation ledger validation into existing workflow path
0227019aaaf2c9661238624216a5fa1f79bd9313  make activation ledger validator regression-testable
1cd0a04dc1a7b08ee7ec227f2f21e59a5911f199  add adversarial activation ledger regression tests
8ccecf055fffa16175c5aa82321a5f2cd97c30f6  run adversarial tests in canonical validation path
55da6f9c9a3551ab6e3b16674fee69a987892023  create activation-ledger mirror handoff
```

## Current ledger state

```yaml
schema: stegverse.site.activation-ledger.v1
checkpoint: SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED
contract_status: PREPARED_NOT_DEPLOYED
activation_status: BLOCKED
live_transport_enabled: false
authority_granted: false
custody_recorded: false
release_authorized: false
```

## Gate inventory

```text
site_same_run_artifact_set: NOT_OBSERVED
llm_adapter_current_main_validation: NOT_OBSERVED
sdk_current_main_validation: NOT_OBSERVED
same_origin_authenticated_deployment: NOT_OBSERVED
live_endpoint_conformance: NOT_OBSERVED
master_records_authenticated_custody: NOT_OBSERVED
reconstructability: NOT_OBSERVED
```

## Validator and adversarial invariants

The canonical validation path now requires the ledger validator and adversarial regression suite. It preserves:

```text
exact schema, checkpoint, contract, and blocked activation state
all authority, custody, release, and live-transport booleans remain false
exact seven-gate inventory
only NOT_OBSERVED or VERIFIED gate states
same-run Site artifact evidence
null usage_api_base before authorized deployment
no browser secret surface
local persistence is not Master-Records custody
reconstructability requires PASS
all gates VERIFIED still requires a separate authorized transition
regression coverage for invalid and authority-escalating ledger mutations
fail closed when the validator or adversarial test file is missing
```

Expected repository-local outputs while activation remains blocked:

```text
site_activation_ledger:PASS_BLOCKED
activation-ledger adversarial tests: PASS
```

## Evidence already observed

Structural implementation evidence is recorded for:

```text
StegVerse-Labs/Site
StegVerse-org/LLM-adapter
StegVerse-org/StegVerse-SDK
master-records/orchestration
```

Structural source evidence and repository-local tests do not satisfy workflow, deployment, custody, reconstructability, or activation gates.

## Remaining work and ownership

```text
StegVerse-Labs/Site
  -> observe a current-main workflow containing 8ccecf055fffa16175c5aa82321a5f2cd97c30f6 or later
  -> verify activation-ledger validation and adversarial tests pass in that run
  -> verify the Site result, receipt, and manifest belong to one successful run
  -> update only evidence-backed gate states

StegVerse-org/LLM-adapter
  -> provide current-main green validation for the governed usage-session and system-boundary lifecycle
  -> provide authorized same-origin deployment evidence before Site conformance

StegVerse-org/StegVerse-SDK
  -> provide current-main green validation preserving the adapter-origin receipt tuple

master-records/orchestration
  -> provide authenticated custody receipt
  -> provide reconstructability PASS evidence

StegVerse-org/core-node-runtime-demo
  -> provide automatic runtime usage emission and governed route-result submission
```

## Permitted continuation scope

```text
observe workflow evidence
repair only the first exact repository-local failing validator or adversarial test
preserve the two-workflow inventory
update a gate only from authenticated evidence
retain every authority, custody, deployment, mutation, release, and activation non-claim
```

## Prohibited continuation claims

```text
source implementation != workflow validation
repository-local tests != current-main workflow evidence
workflow validation != deployment authority
SDK acceptance != admissibility
local persistence != Master-Records custody
SPE ALLOW != execution authority
receipt presence != reconstructability
all gates verified != automatic activation
```

No deployment, credential configuration, live transport, external mutation, custody claim, release, tag, or activation is authorized by this handoff.

## Next task

```text
1. Observe the first current-main workflow containing 8ccecf055fffa16175c5aa82321a5f2cd97c30f6 or later.
2. Confirm activation-ledger validation and adversarial tests pass.
3. Verify one same-run Site result, receipt, and manifest artifact set.
4. Repair only the first exact failing repository-local command without removing checks.
5. Keep every gate NOT_OBSERVED until its required authenticated evidence exists.
6. Propagate only verified evidence to Site, Publisher, admissibility-wiki, and stegguardian-wiki.
7. Do not tag or release while activation remains BLOCKED.
```

## Archive readiness

This handoff preserves the activation-ledger decisions, installed files and commits, adversarial coverage, current gate state, blockers, ownership, pending validation, permitted continuation scope, and non-claims. Earlier conversation context is not required for this workstream.
