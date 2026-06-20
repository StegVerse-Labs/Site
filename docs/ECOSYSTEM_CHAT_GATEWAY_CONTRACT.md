# Ecosystem Chat Gateway Contract

## Purpose

This document defines the activation boundary for the text-only StegVerse Ecosystem Chat page.

The browser page may collect text input, classify local route posture, display local transcript hashes, and call a backend gateway when one exists.

The browser page must not become proof authority, transition authority, accreditation authority, or autonomous deployment authority.

## SDK entry IFF rule

The browser gateway may act as an acceptable user-facing input into the StegVerse-org/SDK entry point if and only if:

1. fillable form fields generate text only into the manifest window and receipt window;
2. the manifest window and receipt window remain generated previews, not proof receipts;
3. fields with strictly limited choices are rendered as dropdown-style controls;
4. the generated manifest and receipt-window JSON are determined correct at the time of submission;
5. the submitted payload preserves the distinction between form fields, generated manifest JSON, and generated receipt-window JSON.

Detailed browser form model: `docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md`.

## Done condition

The text-only console is activation-ready when:

1. `ecosystem-chat.html` loads without a build step.
2. `assets/ecosystem-chat.js` runs in local simulation mode when no backend is connected.
3. A backend can later expose `POST /api/ecosystem-chat` without changing the public page contract.
4. Gateway responses include a routed module, bounded response, next action, and receipt identifier or explicit null receipt state.
5. Site continues to identify itself as a public mirror and command surface only.

## Request contract

```http
POST /api/ecosystem-chat
Content-Type: application/json
```

```json
{
  "message": "continue building Site",
  "session_id": "browser-session-id",
  "repo": "StegVerse-Labs/Site",
  "goal": "text-only ecosystem command console"
}
```

Canonical example: `fixtures/ecosystem-chat/request.example.json`.

## Response contract

```json
{
  "response": "Bounded user-facing response text.",
  "routed_module": "Site",
  "receipt_id": null,
  "next_action": "Send this request to the Site handler once governed backend routing is active."
}
```

Canonical example: `fixtures/ecosystem-chat/response.example.json`.

## Route vocabulary

| Route | Use |
|------|-----|
| `Site` | Public pages, navigation, mirrors, public proof surfaces, documentation. |
| `StegVerse-002` | Governed deployment posture, intake state, clean-slate work entity. |
| `formalism-tests` | Proof/test authority references, formalism validation, admissibility checks. |
| `Continuity` | Receipt chain concepts, replay context, state continuity language. |
| `Publisher` | Paper mirror source posture, manifest regeneration, publication boundaries. |
| `Unknown` | Fallback when no safe route is available. |

## Fail-closed behavior

If the gateway is unavailable, malformed, or returns a non-OK HTTP status, the browser must fall back to local classification and clearly display that no authority-issued receipt was created.

## Receipt boundary

Local transcript hashes are not proof receipts. They are local browser transcript identifiers only.

Only the appropriate governed backend authority may issue a proof receipt.

## Next backend milestone

Create a governed gateway service that accepts the request contract, applies route policy, dispatches to the correct ecosystem handler, and returns a bounded response with either an authority-issued receipt ID or an explicit `null` receipt state.
