# Ecosystem Chat Gateway Contract

## Purpose

This document defines the activation boundary for the text-only StegVerse Ecosystem Chat page.

The browser page may collect text input, classify local route posture, display local transcript hashes, and call a backend gateway when one exists.

The browser page must not become proof authority, transition authority, accreditation authority, or autonomous deployment authority.

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

## Response contract

```json
{
  "response": "Bounded user-facing response text.",
  "routed_module": "Site",
  "receipt_id": null,
  "next_action": "Send this request to the Site handler once governed backend routing is active."
}
```

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
