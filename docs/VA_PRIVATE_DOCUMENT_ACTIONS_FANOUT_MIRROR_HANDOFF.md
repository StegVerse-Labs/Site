# VA Private Document Actions Fanout Mirror Handoff

Updated: 2026-08-22
Repository: `StegVerse-Labs/Site`
Issue: `#420`
Claim: `SITE-VA-PRIVATE-DOCUMENT-HOURLY-FIXTURE-RETIREMENT-420-20260822`
Branch: `claim/site-va-private-document-hourly-fixture-retirement-420`
State: `IMPLEMENTATION_IN_PROGRESS`

## Goal

Retire the completed VCA-008 deterministic private-document fixture's hourly GitHub-hosted clock, repository writeback, and artifact custody while preserving bounded source-change/manual validation.

## Canonical product boundary

`data/va-claim-assistant/session-execution-inventory.json` records VCA-008 as:

```text
owner: StegVerse-Labs/Site#116
claim_state: COMPLETE
completion_state: COMPLETE_VALIDATED_BOUNDED_RUNTIME
validation_state: MAIN_WORKFLOW_SUCCESS
integration_state: PUBLIC_UPLOAD_DISABLED
next_action: null
```

This Actions task does not own Site #116 secure-document product/runtime/public activation, private-upload enablement, provider runtime, Master Records custody, claimant/submission authority, or VACC Goal 2/3 completion.

## Pre-repair cost/fanout state

`.github/workflows/va-private-document-runtime.yml` currently has:

```text
schedule: 41 * * * *
minimum scheduled starts: 24/day
permissions: contents: write
checkout/setup-python hosted actions: yes
repository writeback: data/va-claim-assistant/private-document-runtime-receipt.json
artifact custody: 30 days
cancel-in-progress: false
```

The deterministic receipt is already verified and public upload remains disabled. The indexed persistence commit is `f893970c91ce265d510e0611e72cefb4894316f9` (`receipt: persist VA private document runtime validation [skip ci]`, 2026-08-07). A static completed fixture does not require an hourly clock to manufacture progress.

## Required retained semantics

- `workflow_dispatch` retained;
- main-push validation retained for intake schema, deterministic fixture, processor, and workflow source;
- exact source acquired anonymously;
- credential-bearing execution fails closed;
- deterministic processor executes;
- generated receipt is ephemeral;
- require `public_upload_enabled=false`;
- require `raw_documents_published=false`;
- require every authority flag false;
- require non-empty missing-evidence output and stable assessment hash;
- require `activation_effect=false`;
- no repository writeback or artifact custody;
- no GitHub-token runtime/production authority;
- TV/TVC remains credential authority;
- no Render.

## Collision boundaries

- Do not modify `.github/workflows/va-document-evidence.yml` while PR #263 owns that surface.
- Do not modify `.github/workflows/validate.yml` while Site #388 claims it.
- Do not change Site #116 product/runtime/public-activation semantics.
- Do not enable private upload, filing, or claimant/submission authority.

## Completion gate

Source implementation is not completion. Release requires exact merge-ref Site claim/orchestration validation, integration merge, durable evidence in this handoff and the claim registry, and issue #420 closure. A workflow pass remains validation evidence only and cannot establish VACC runtime or activation.
