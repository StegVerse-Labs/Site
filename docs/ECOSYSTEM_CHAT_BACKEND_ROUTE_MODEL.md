# Ecosystem Chat Backend Route Model

## Purpose

The Ecosystem Chat and StegVerse AI entry surfaces should not compete. They should become one user-facing entry point backed by route-specific backend handlers.

The user should see one primary StegVerse AI window. Behind that window, the backend decides which purpose path applies.

## Route families

```text
chat_answer
  -> direct StegVerse LLM answer candidate

llm_comparison
  -> StegVerse response plus external model comparison panes

ecosystem_explanation
  -> explain StegVerse concepts, components, and state

sdk_access_guidance
  -> explain SDK access, manifests, receipts, permissions, and next steps

sdk_intake_candidate
  -> prepare SDK intake packet / manifest preview

governance_review
  -> classify authority, admissibility, evidence, receipt, and reconstruction posture

runtime_status
  -> explain runtime, adapter, micro-node, and capability status

documentation_route
  -> route to public docs, wiki, proofs, papers, or runbooks

restricted_admin
  -> deny or require separate authority for secrets, shell, credentials, repo mutation, permissions, releases, or destructive tasks
```

## One-window contract

```text
User input
-> normalize request
-> classify route family
-> preserve original claim/request
-> determine whether evidence or authority is required
-> return StegVerse response first
-> return route guidance and SDK guidance when relevant
-> return external comparison panes only as non-authoritative comparison
-> attach receipt/reconstruction preview when available
```

## Backend response shape

```json
{
  "response_id": "preview-response-id",
  "primary_route": "chat_answer | llm_comparison | sdk_access_guidance | governance_review | restricted_admin",
  "stegverse_response": "primary governed response candidate",
  "route_guidance": "why this route was selected",
  "sdk_guidance": "how SDK access or intake applies, if relevant",
  "comparison_outputs": [
    {
      "provider": "ChatGPT",
      "authority": false,
      "response": "comparison output or unavailable"
    },
    {
      "provider": "Claude",
      "authority": false,
      "response": "comparison output or unavailable"
    }
  ],
  "governance": {
    "governed_candidate": true,
    "authority_issued": false,
    "receipt_id": null,
    "reconstruction_available": false
  }
}
```

## Relationship to existing page sections

The current Ecosystem Chat page sections become backend routes or expandable details:

```text
SDK Entry Form -> sdk_intake_candidate
Console -> one-window StegVerse AI entry
Gateway contract -> backend contract details
Guardrails -> governance/restricted-admin route rules
Receipt window -> governance metadata panel
Manifest window -> SDK/governed-transition candidate panel
```

## Boundary

The backend route model is not execution authority. It defines request classification and response structure. Consequential actions still require governed transition review, authority checks, receipts, and reconstruction evidence.
