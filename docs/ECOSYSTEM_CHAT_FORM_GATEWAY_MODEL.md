# Ecosystem Chat Form Gateway Model

## Purpose

This document defines the browser gateway form model for a future StegVerse-org/SDK entry point.

The browser form is acceptable as a user-facing input surface if and only if the generated manifest and receipt-window JSON remain distinct from the fillable fields and are determined correct at submission time.

The form is not a shell, credential surface, repository administration panel, proof authority, transition authority, accreditation authority, or autonomous deployment authority.

## Core distinction

| Layer | Role | Authority |
|---|---|---|
| Fillable form fields | User-facing input controls | No receipt, shell, credential, or execution authority |
| Manifest window | Generated JSON preview derived from the fields | Preview only before submission |
| Receipt window | Generated receipt-intent JSON derived from the fields and manifest | Preview only before submission |
| Submission check | Determines whether the manifest and receipt-window JSON are locally complete and structurally correct at submission time | Gateway admissibility check, not Site proof authority |
| StegVerse-org/SDK entry point | Receives the accepted payload after the submission check | SDK-side intake authority according to SDK rules |
| Governed backend gateway | Evaluates allowed-task status, authority, rate limits, scope, and receipt obligations before execution | May route only approved tasks |

## Field behavior

Fields that represent a strictly limited choice must be rendered as dropdown-style controls.

Free text fields may be text inputs or text areas only when the field cannot be represented as a closed vocabulary.

Every field change must regenerate the manifest window and receipt window from the current field state.

The user must not directly edit the generated manifest or receipt-window JSON in the normal submission path.

Free text fields must not be treated as executable command input. If a user enters shell syntax, credential material, or destructive administration intent, the form output remains text-only and the request must be routed to `Restricted admin`, `pending_authority`, or rejection by the backend gateway.

## Submission rule

The browser gateway may submit to the StegVerse-org/SDK entry point only when:

1. the form fields are complete;
2. the manifest window was generated from the current field state;
3. the receipt window was generated from the current field state and manifest;
4. the generated JSON is syntactically valid;
5. the gateway determines the generated JSON correct at the time of submission;
6. the submitted payload preserves the distinction between fields, manifest, and receipt-window content;
7. `raw_shell_allowed` is `false`;
8. `authority_required` is `true`;
9. `rate_limit_required` is `true`;
10. `receipt_required_for_execution` is `true`;
11. restricted administration requests are identified before execution.

## Non-authority rule

The Site browser gateway does not issue proof receipts.

The Site browser gateway does not determine final execution authority.

The Site browser gateway does not execute shell commands, accept credentials, expose GitHub tokens, perform repository writes, delete branches, edit workflows, change permissions, publish releases, or mutate infrastructure.

The Site browser gateway prepares and submits user input to the SDK entry point only after local correctness checks pass.

## Restricted administration rule

The form must preserve, not execute, requests involving:

1. branch, tag, release, or repository deletion;
2. force-push or history rewrite;
3. workflow creation, deletion, disabling, or modification;
4. secret, token, credential, deploy-key, or webhook access;
5. collaborator, team, permission, or branch-protection changes;
6. DNS, Pages, deployment, package publishing, or infrastructure setting changes.

These requests may be represented as governed task requests only after the proper authority layer determines scope, allowed-task status, confirmation requirements, and receipt obligations.

## Initial dropdown candidates

| Field | Allowed values |
|---|---|
| `target_entry_point` | `StegVerse-org/SDK` |
| `input_mode` | `text_form` |
| `requested_route` | `Site`, `repo-standards`, `StegVerse-002`, `formalism-tests`, `Continuity`, `Publisher`, `Restricted admin`, `Unknown` |
| `receipt_expectation` | `none`, `local_preview_only`, `sdk_intake_receipt_requested`, `authority_issued_receipt_required` |
| `submission_posture` | `draft`, `ready_for_submission`, `restricted_review_required` |

## Initial text candidates

| Field | Purpose |
|---|---|
| `user_request` | User-entered request text. Text only; not executable shell. |
| `declared_goal` | User-facing goal for the request. |
| `operator_note` | Optional note for the SDK intake context. Must not contain secrets, tokens, credentials, or private infrastructure material. |

## Generated manifest shape

```json
{
  "target_entry_point": "StegVerse-org/SDK",
  "input_mode": "text_form",
  "requested_route": "Site",
  "detected_route": "Site",
  "task_status": "preview_only",
  "raw_shell_allowed": false,
  "authority_required": true,
  "rate_limit_required": true,
  "receipt_required_for_execution": true,
  "restricted_admin_review_required": false,
  "user_request": "continue building Site",
  "declared_goal": "user advancement console with governed task boundaries",
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
  "site_shell_authority": false,
  "site_credential_authority": false,
  "manifest_correct_at_submission": true,
  "submission_target": "StegVerse-org/SDK",
  "execution_allowed_from_site": false,
  "authority_required_before_execution": true,
  "receipt_required_for_execution": true,
  "correctness_errors": []
}
```

## Canonical payload fixture

The canonical SDK form payload fixture is `fixtures/ecosystem-chat/sdk-form-payload.example.json`.

The fixture preserves all three layers:

1. `fields`;
2. `manifest`;
3. `receipt_window`.

## Done condition for the browser model

The browser model is ready when the Site page contains:

1. fillable form fields;
2. dropdown controls for all closed-vocabulary fields;
3. a generated manifest window;
4. a generated receipt-window preview;
5. a submission correctness check;
6. an explicit non-authority boundary;
7. an explicit no-shell and no-credential boundary;
8. an authority-required and receipt-required execution boundary;
9. restricted administration routing;
10. a payload that can be handed to the StegVerse-org/SDK entry point without granting Site execution authority.
