# VA Privacy Preprocessor Actions Fanout Mirror Handoff

Updated: 2026-08-22
Repository: `StegVerse-Labs/Site`
Issue: `#424`
Claim: `SITE-VA-PRIVACY-PREPROCESSOR-CLOCK-RETIREMENT-424-20260822`
State: `IMPLEMENTATION_IN_PROGRESS`

## Goal

Retire the completed PII-RDY-01/02/03 privacy-preprocessor's separate six-hour GitHub-hosted clock, repository writeback, and 90-day artifact custody while retaining its existing manual/PR/main source validation and fail-closed privacy semantics.

## Canonical boundary

`docs/VA_PII_REALIGNMENT_READINESS_MIRROR_HANDOFF.md` is authoritative. PII-RDY-01, PII-RDY-02, and PII-RDY-03 are COMPLETE. The unresolved PII-RDY-08/09 machine observer is a different workflow: `.github/workflows/va-pii-realignment-readiness.yml`, which retains its own six-hour cadence. This task must not modify or replace that observer.

Canonical VACC inventory also records VCA-011 as COMPLETE with the Site-to-adapter privacy boundary complete. This Actions carrier repair does not complete PII-RDY-04/05/07/08/09 and grants no product/runtime/public activation authority.

## Pre-repair carrier

`.github/workflows/va-private-document-privacy-preprocessor.yml` currently has:

```text
schedule: 23 */6 * * *
permissions: contents: write
repository writeback: seven execution/readiness files
artifact custody: 90 days
checkout/setup-python actions: yes
cancel-in-progress: false
```

## Required retained validation

- `workflow_dispatch` retained;
- existing `pull_request` source validation retained;
- existing bounded main-push source validation retained;
- exact PR merge-ref or push SHA acquired anonymously;
- credential-bearing environments fail closed;
- immutable processor commit remains derived from Git history;
- privacy preprocessor executes;
- PII-RDY-01/02/03 observers execute;
- all three readiness records remain COMPLETE;
- `model_called=false`;
- `public_upload_enabled=false`;
- negative admission cases blocked;
- advanced malware scanner still required before public activation;
- generated evidence/readiness changes are ephemeral and restored;
- no repository writeback or artifact custody;
- no GitHub-token production/runtime authority;
- TV/TVC remains credential authority;
- no Render.

## Collision boundaries

- Do not modify `.github/workflows/va-pii-realignment-readiness.yml` or its PII-RDY-08/09 observer.
- Do not claim PII-RDY-04/05/07/08/09 complete.
- Do not modify Site #116 / Site #113 product/runtime/public-activation semantics.
- Do not modify `.github/workflows/validate.yml` while Site #388 claims it.

## Completion gate

The repaired workflow itself must pass exact-head PR validation, repository orchestration/claim gates must pass except for independently proven pre-existing failures, integration must merge, this handoff and the claim registry must record release evidence, and Site #424 must close. Workflow success remains validation evidence only.
