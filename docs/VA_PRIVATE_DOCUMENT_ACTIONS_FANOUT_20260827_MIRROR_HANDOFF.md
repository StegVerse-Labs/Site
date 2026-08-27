# VA Private Document Actions Fanout — 2026-08-27 Mirror Handoff

## Authority and supersession

This is the newest continuation overlay for `docs/VA_PRIVATE_DOCUMENT_ACTIONS_FANOUT_MIRROR_HANDOFF.md`. It supersedes only the stale post-merge observability boundary in that historical handoff; the historical implementation and merge evidence remain authoritative.

```text
repository: StegVerse-Labs/Site
issue: Site#420
claim: SITE-VA-PRIVATE-DOCUMENT-HOURLY-FIXTURE-RETIREMENT-420-20260822
workflow: .github/workflows/va-private-document-runtime.yml
merge_commit: a8d6e1bf28291ff6ba7f0838950e6800760b7adf
state: SOURCE_REPAIRED_INTEGRATED_PASS_PENDING
credential_authority: TV/TVC
runtime_authority_effect: NONE
product_authority_effect: NONE
```

## Newly observable exact integrated execution

The current GitHub reader can enumerate arbitrary workflow runs by exact head SHA. The merge-triggered run previously described as unobservable is now directly observed:

```text
run: 32604657387
workflow_name: VA Private Document Fixture Validation
event: push
head_branch: main
head_sha: a8d6e1bf28291ff6ba7f0838950e6800760b7adf
job: 97107875859
job_name: validate-private-intake
run_conclusion: failure
```

Substantive execution steps all passed:

```text
credential refusal: PASS
anonymous exact-source fetch: PASS
preinstalled Python: PASS
bounded private-document fixture execution: PASS
privacy and authority boundaries: PASS
```

The only failed step was `Confirm validation-only containment`.

## Exact false-positive cause

The final containment step read the workflow file itself and searched the raw text for forbidden marker strings that were also embedded literally in its own Python `forbidden = [...]` list. Therefore the checker necessarily found its own source text and failed.

The observed failure is a deterministic validator false positive, not evidence that hourly scheduling, GitHub-token authority, repository writeback, artifact custody, checkout/setup-python actions, or git mutation remained operational.

## Source repair — 2026-08-27

The checker now constructs each forbidden marker from string fragments, preserving the same effective marker values while preventing the marker literals from appearing contiguously in the checker source itself.

```text
repair commit: 20ac25d8460022a206129d0762ff6638527a7659
current workflow blob after repair: a810093782d73d395a82dbc7337a479946bb7ee4
hosted validation intentionally triggered by repair commit: NONE ([skip ci])
```

The exact commit diff changes only the marker construction in `Confirm validation-only containment`; the private-document fixture behavior and authority boundaries are unchanged.

## Current completion boundary

The source defect is IMPLEMENTED but the lane is not yet VALIDATED/RELEASED/COMPLETE. Remaining requirement:

1. Cause one exact integrated execution of the repaired workflow without adding recurring fanout.
2. Require every workflow step, including `Confirm validation-only containment`, to PASS.
3. Record exact run/job/head evidence here and in the claim registry.
4. Release the claim and close Site#420 only after that PASS.

No user action, credential entry, provider activation, iPhone action, private-upload activation, runtime activation, custody action, filing action, or claimant authority is required for this remediation.
