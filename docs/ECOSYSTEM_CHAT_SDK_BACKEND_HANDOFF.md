# Ecosystem Chat SDK Backend Handoff

## Purpose

This handoff defines the next backend integration step for the text-only Ecosystem Chat browser gateway.

The Site page is now a user-facing form and preview surface. The backend must remain the governed intake boundary for StegVerse-org/SDK submission.

## Current Site-side state

```text
Browser form: installed
Closed-choice dropdowns: installed
Manifest window: installed
Receipt window: installed
Three-layer SDK payload fixture: installed
Local correctness check: installed
Live backend submission: not installed
Authority-issued receipt: not installed
```

## Required backend entry behavior

The backend intake path must accept only a payload that preserves these three layers:

```text
fields
manifest
receipt_window
```

The backend must reject or fail closed when:

1. the submitted payload is missing any layer;
2. the manifest is not derived from the submitted fields;
3. the receipt window is not derived from the submitted fields and manifest;
4. closed-vocabulary fields contain values outside the allowed set;
5. `site_receipt_authority` is anything other than `false`;
6. the generated JSON is not correct at submission time;
7. the submission target is not `StegVerse-org/SDK`.

## Allowed closed-vocabulary values

| Field | Allowed values |
|---|---|
| `target_entry_point` | `StegVerse-org/SDK` |
| `input_mode` | `text_form` |
| `requested_route` | `Site`, `StegVerse-002`, `formalism-tests`, `Continuity`, `Publisher`, `Unknown` |
| `receipt_expectation` | `none`, `sdk_intake_receipt_requested` |
| `submission_posture` | `draft`, `ready_for_submission` |

## Canonical input fixture

Use this Site fixture as the backend acceptance example:

```text
fixtures/ecosystem-chat/sdk-form-payload.example.json
```

The fixture is not a proof receipt. It is a submission-shape example for the SDK intake boundary.

## Backend response requirement

The backend must return a bounded response containing:

```text
accepted
routed_module
receipt_id
next_action
errors
```

Before authority issuance, `receipt_id` must remain `null`.

## Authority boundary

Site does not issue proof receipts.

Site does not determine final execution authority.

StegVerse-org/SDK may accept the browser payload only after backend correctness checks pass.

Any authority-issued receipt must come from the governed SDK-side intake path, not from the Site browser surface.

## Done condition

This backend handoff is complete when:

1. Site has an installed SDK form and generated preview windows;
2. Site has a canonical SDK form payload fixture;
3. the checker validates the Site-side contract and fixture structure;
4. the workflow runs the checker on relevant changes;
5. a future SDK backend implementation can consume the fixture without changing the Site-side payload contract.
