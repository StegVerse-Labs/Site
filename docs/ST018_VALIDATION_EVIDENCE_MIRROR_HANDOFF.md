# ST-018 Validation Evidence Mirror Handoff

## Canonical authority

```text
goal_id: SITE-ST018-GITHUB-TOKEN-RETIREMENT-20260817
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#141
parent_workflow_minimization_issue: StegVerse-Labs/Site#268
active_claim: SITE-ST018-GITHUB-TOKEN-RETIREMENT-B17R1-20260817
active_branch: chore/site-st018-validation-consolidation-b17r1-20260817
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_actions_production_runtime_control_plane_authority: NONE
runtime_authority_effect: NONE
publication_authority_effect: NONE
release_authority_effect: NONE
```

## Retained deterministic contract

ST-018 remains defined by `validation_manifests/repository-core.json`, `schemas/validation-execution-receipt.schema.json`, `scripts/capture_validation_manifest.py`, `scripts/write_site_current_main_validation_receipt.py`, `scripts/check_site_current_main_validation_receipt_writer.py`, `scripts/check_site_current_main_validation_evidence.py`, and `data/tasks/SITE-ST018-VALIDATION-EVIDENCE.json`. B17R1 does not weaken the manifest, schema, validator, or authority ceiling.

## B17R1 transition

The former `.github/workflows/capture-validation-evidence.yml` is removed. It previously used `issues: write`, `actions/checkout@v4`, `actions/setup-python@v5`, `actions/upload-artifact@v4`, `GH_TOKEN=${{ github.token }}`, GitHub issue mutation, and GitHub-hosted artifact/native-main custody semantics.

Deterministic execution is consolidated into canonical credential-clean `.github/workflows/validate.yml` after anonymous exact-ref fetch and public jsonschema installation:

```text
python3 scripts/capture_validation_manifest.py
-> reports/validation-execution-receipt.json
-> require status == PASS
-> require every authority field == false
```

No ST-018 artifact upload, issue mutation, repository writeback, PAT, GitHub project token, provider secret, or TV/TVC credential export occurs. A receipt created during hosted validation is transient source-evidence unless a separately admitted StegVerse/Master Records custody contract persists it. GitHub artifacts and issue comments are not custody authority.

## Authority boundary

```text
credential_authority: TV/TVC
consumer_credential_requirement: NONE
github_token_runtime_authority: NONE
issue_mutation_authority: NONE
artifact_custody_authority: NONE
factual_truth_authority: NONE
admissibility_authority: NONE
publication_authority: NONE
deployment_authority: NONE
release_authority: NONE
runtime_activation_authority: NONE
```

Hosted validation remains source-behavior evidence only. GitHub platform metadata does not become a StegVerse project/runtime credential.

## Collision boundaries

- Do not weaken the declared validators or receipt schema.
- Do not claim ST-018 validation proves factual truth, admissibility, publication, deployment, release, standing, certification or runtime activation.
- Do not export TV/TVC credentials into GitHub Actions or introduce alternate GitHub/project/provider tokens.
- Do not modify active StegOS admitted-inference, HIL runtime/private-review, sovereign heartbeat/model, StegFin wallet, or Master Records authority paths.
- USER_ONLY remains the sole StegFin signing/broadcast authority.
- Do not use Render.

## B17R1 release requirements

```text
capture-validation-evidence.yml: ABSENT
validate.yml permissions: {}
validate.yml credential refusal: REQUIRED
ST-018 local receipt generation: PASS
ST-018 authority ceiling: all false
ST-018 GitHub artifact custody: NONE
ST-018 GitHub issue mutation: NONE
SESSION_WORK_CLAIMS_PASS
Site Handoff Orchestrator: PASS
Ecosystem Heartbeat Orchestration: PASS
Site Bootstrap Validate: PASS
Check StegFin Phone Projection: PASS
workflow inventory: 106 total / 3 canonical / 103 migration-required / 0 placeholders
```

After exact-head green validation, merge, reconcile Site #141 so completion no longer depends on GitHub artifacts/comments, release B17R1, and finalize `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`.

## Archive condition

This scoped task becomes archive-safe only after source merge, exact validation evidence, claim release and durable Site #141/cost-containment reconciliation. Product/runtime activation remains independent.
