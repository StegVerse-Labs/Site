# Ecosystem Chat Gateway Contract

## Purpose

This document defines the activation boundary for the StegVerse Ecosystem Chat page.

Ecosystem Chat is a user advancement surface. It accepts user goals, classifies route posture, displays generated local preview windows, and may call a governed backend gateway when one exists.

Ecosystem Chat is not a public terminal. It must not execute arbitrary shell commands, expose credentials, mutate repositories, delete branches, edit workflows, alter permissions, issue proof receipts, issue transition authority, issue accreditation authority, or perform autonomous deployment authority.

## Public boundary

The public page may:

1. collect text-only user advancement requests;
2. classify the request into a known route or `Unknown`;
3. identify restricted administration requests;
4. generate manifest and receipt-window previews;
5. preserve a local transcript hash;
6. submit an allowlisted task request to a backend gateway when one exists.

The public page must not:

1. accept raw shell as an executable instruction;
2. accept secrets, tokens, credentials, deploy keys, or private infrastructure material;
3. expose GitHub CLI, GitHub token, workflow, branch, release, collaborator, webhook, or repository administration authority;
4. claim that local hashes are proof receipts;
5. imply that prototype, pending, or concept features are operational authority.

## SDK entry IFF rule

The browser gateway may act as an acceptable user-facing input into the StegVerse-org/SDK entry point if and only if:

1. fillable form fields generate text only into the manifest window and receipt window;
2. the manifest window and receipt window remain generated previews, not proof receipts;
3. fields with strictly limited choices are rendered as dropdown-style controls;
4. the generated manifest and receipt-window JSON are determined correct at the time of submission;
5. the submitted payload preserves the distinction between form fields, generated manifest JSON, and generated receipt-window JSON;
6. raw shell execution is explicitly disabled;
7. credential input is rejected or ignored;
8. allowed-task status is determined before execution;
9. restricted administration requests require separate authority review;
10. any accepted execution path returns status and receipt data.

Detailed browser form model: `docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md`.

## Done condition

The text-only console is activation-ready when:

1. `ecosystem-chat.html` loads without a build step.
2. `assets/ecosystem-chat.js` runs in local simulation mode when no backend is connected.
3. A backend can later expose `POST /api/ecosystem-chat` without changing the public page contract.
4. Gateway responses include a routed module, bounded response, task status, next action, and receipt identifier or explicit null receipt state.
5. Site continues to identify itself as a public mirror and user advancement surface only.
6. The page and local JavaScript both state that raw shell is disabled and authority is required before execution.

## Request contract

```http
POST /api/ecosystem-chat
Content-Type: application/json
```

```json
{
  "message": "continue building Site",
  "session_id": "browser-session-id",
  "requested_route": "Site",
  "goal": "user advancement console with governed task boundaries",
  "execution_model": "allowlisted_task_request_only",
  "raw_shell_allowed": false,
  "authority_required": true,
  "rate_limit_required": true,
  "receipt_required_for_execution": true
}
```

Canonical example: `fixtures/ecosystem-chat/request.example.json`.

## Response contract

```json
{
  "response": "Bounded user-facing response text.",
  "routed_module": "Site",
  "task_status": "preview_only",
  "receipt_id": null,
  "next_action": "Send this request to the Site handler only after governed backend routing validates allowed-task status."
}
```

Canonical example: `fixtures/ecosystem-chat/response.example.json`.

## Task status vocabulary

| Status | Meaning |
|---|---|
| `preview_only` | Browser-local classification or non-executing gateway response. No external mutation occurred. |
| `rejected` | Gateway rejected the request because validation, authority, scope, rate limit, or allowed-task status failed. |
| `pending_authority` | Request may be valid in concept but requires restricted review before execution. |
| `accepted_for_execution` | Gateway accepted an allowlisted task for execution and must return or later attach receipt data. |

## Route vocabulary

| Route | Use |
|------|-----|
| `Site` | Public pages, navigation, mirrors, public proof surfaces, documentation. |
| `repo-standards` | Allowed task definitions, reusable standards, maintenance manifests, and governed remediation rules. |
| `StegVerse-002` | Governed deployment posture, intake state, clean-slate work entity. |
| `formalism-tests` | Proof/test authority references, formalism validation, admissibility checks. |
| `Continuity` | Receipt chain concepts, replay context, state continuity language. |
| `Publisher` | Paper mirror source posture, manifest regeneration, publication boundaries. |
| `Restricted admin` | Credential, branch, workflow, permission, release, or destructive maintenance requests requiring separate authority before execution. |
| `Unknown` | Fallback when no safe route is available. |

## Restricted administration examples

The gateway must treat these classes as restricted and must not execute them from a public request alone:

1. branch or tag deletion;
2. repository deletion or archival;
3. force-push or history rewrite;
4. workflow creation, deletion, or disabling;
5. secret, token, credential, deploy-key, or webhook access;
6. collaborator, permission, team, or branch-protection changes;
7. release deletion or package publishing changes;
8. DNS, Pages, deployment, or infrastructure setting changes.

Restricted administration may still be represented as a governed task request, but only after the proper authority layer determines scope, allowed-task status, confirmation requirements, and receipt obligations.

## Fail-closed behavior

If the gateway is unavailable, malformed, rate-limited, unauthorized, out of scope, or returns a non-OK HTTP status, the browser must fall back to local classification and clearly display that no external execution occurred and no authority-issued receipt was created.

If the gateway detects shell syntax, credential material, destructive administration intent, or unsupported task scope, it must return `rejected` or `pending_authority`; it must not attempt partial execution.

## Receipt boundary

Local transcript hashes are not proof receipts. They are local browser transcript identifiers only.

Only the appropriate governed backend authority may issue a proof receipt.

Any accepted execution path must either return an authority-issued receipt identifier or explicitly report that receipt issuance is pending, failed, or not applicable.

## Next backend milestone

Create a governed gateway service that accepts the request contract, applies route policy, enforces validation and rate limits, rejects raw command execution, dispatches only to approved ecosystem handlers, and returns a bounded response with task status and either an authority-issued receipt ID or an explicit `null` receipt state.
