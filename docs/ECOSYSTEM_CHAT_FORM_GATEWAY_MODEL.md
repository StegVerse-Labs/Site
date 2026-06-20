# Ecosystem Chat Form Gateway Model

## Purpose

This document defines the browser gateway form model for a future StegVerse-org/SDK entry point.

The browser form is acceptable as a user-facing input surface if and only if the generated manifest and receipt-window JSON remain distinct from the fillable fields and are determined correct at submission time.

## Core distinction

| Layer | Role | Authority |
|---|---|---|
| Fillable form fields | User-facing input controls | No receipt authority |
| Manifest window | Generated JSON preview derived from the fields | Preview only before submission |
| Receipt window | Generated receipt-intent JSON derived from the fields and manifest | Preview only before submission |
| Submission check | Determines whether the manifest and receipt-window JSON are correct at submission time | Gateway admissibility check, not Site proof authority |
| StegVerse-org/SDK entry point | Receives the accepted payload after the submission check | SDK-side intake authority according to SDK rules |

## Field behavior

Fields that represent a strictly limited choice must be rendered as dropdown-style controls.

Free text fields may be text inputs or text areas only when the field cannot be represented as a closed vocabulary.

Every field change must regenerate the manifest window and receipt window from the current field state.

The user must not directly edit the generated manifest or receipt-window JSON in the normal submission path.

## Submission rule

The browser gateway may submit to the StegVerse-org/SDK entry point only when:

1. the form fields are complete;
2. the manifest window was generated from the current field state;
3. the receipt window was generated from the current field state and manifest;
4. the generated JSON is syntactically valid;
5. the gateway determines the generated JSON correct at the time of submission;
6. the submitted payload preserves the distinction between fields, manifest, and receipt-window content.

## Non-authority rule

The Site browser gateway does not issue proof receipts.

The Site browser gateway does not determine final execution authority.

The Site browser gateway prepares and submits user input to the SDK entry point only after local correctness checks pass.

## Initial dropdown candidates

| Field | Allowed values |
|---|---|
| `target_entry_point` | `StegVerse-org/SDK` |
| `input_mode` | `text_form` |
| `requested_route` | `Site`, `StegVerse-002`, `formalism-tests`, `Continuity`, `Publisher`, `Unknown` |
| `receipt_expectation` | `none`, `sdk_intake_receipt_requested` |
| `submission_posture` | `draft`, `ready_for_submission` |

## Initial text candidates

| Field | Purpose |
|---|---|
| `user_request` | User-entered request text. |
| `declared_goal` | User-facing goal for the request. |
| `operator_note` | Optional note for the SDK intake context. |

## Generated manifest shape

```json
{
  "target_entry_point": "StegVerse-org/SDK",
  "input_mode": "text_form",
  "requested_route": "Site",
  "user_request": "continue building Site",
  "declared_goal": "text-only ecosystem command console",
  "operator_note": "",
  "source_surface": "StegVerse-Labs/Site/ecosystem-chat.html"
}
```

## Generated receipt-window shape

```json
{
  "receipt_expectation": "sdk_intake_receipt_requested",
  "submission_posture": "ready_for_submission",
  "site_receipt_authority": false,
  "manifest_correct_at_submission": true,
  "submission_target": "StegVerse-org/SDK"
}
```

## Done condition for the browser model

The browser model is ready when the Site page contains:

1. fillable form fields;
2. dropdown controls for all closed-vocabulary fields;
3. a generated manifest window;
4. a generated receipt-window preview;
5. a submission correctness check;
6. an explicit non-authority boundary;
7. a payload that can be handed to the StegVerse-org/SDK entry point.
