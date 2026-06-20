# Ecosystem Chat Activation Status

## Status

`ecosystem-chat.html` is installed as a text-only browser command surface for StegVerse build and governance requests.

The page is currently in local-simulation mode. It does not call a live backend and does not issue proof receipts.

The SDK Entry Form is installed as a browser-side user input surface for the StegVerse-org/SDK entry point if and only if the generated manifest window and receipt window remain distinct from the fillable fields and are determined correct at submission time.

## Current installed surface

| Surface | State |
|---|---|
| Public page | Installed: `ecosystem-chat.html` |
| Browser script | Installed: `assets/ecosystem-chat.js` |
| Gateway contract | Installed: `docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md` |
| Form gateway model | Installed: `docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md` |
| SDK form payload fixture | Installed: `fixtures/ecosystem-chat/sdk-form-payload.example.json` |
| SDK backend response fixture | Installed: `fixtures/ecosystem-chat/sdk-backend-response.example.json` |
| Gateway fixtures | Installed: `fixtures/ecosystem-chat/request.example.json` and `fixtures/ecosystem-chat/response.example.json` |
| Static checker | Installed: `scripts/check_ecosystem_chat_contract.py` |
| Workflow gate | Installed: `github/workflows/check-ecosystem-chat.yml` path shown without leading dot |
| iOS path mapping | Installed: `iosnoperiod/iosnoperiod.md` and `iosnoperiod/workflow-map.json` |

## Browser form state

```text
Fillable fields state: installed
Closed-choice dropdown state: installed
Manifest window state: installed
Receipt window state: installed
Submission correctness check state: installed locally
SDK payload fixture state: installed
SDK backend response fixture state: installed
SDK backend submission state: not installed
```

## Boundary

Site remains a public mirror and command surface only.

The console may collect text input, classify local route posture, display local transcript hashes, preserve a bounded browser transcript, generate form-derived manifest and receipt-window previews, and call a governed backend gateway when that gateway exists.

The console must not issue proof receipts, claim deployment authority, or replace StegVerse-002, formalism-tests, Continuity, StegVerse-org/SDK, or any other authority-bearing ecosystem component.

The manifest window and receipt window are generated previews. They are not proof receipts.

## Verification command

```bash
python scripts/check_ecosystem_chat_contract.py
```

Expected output:

```text
Ecosystem Chat contract check passed.
```

## Next activation milestone

Create the governed backend gateway for:

```text
POST /api/ecosystem-chat
```

The backend must accept the existing request contract, apply route policy, dispatch to the correct ecosystem handler, and return a bounded response with either an authority-issued receipt ID or an explicit `null` receipt state.

The StegVerse-org/SDK intake path must accept the three-layer SDK form payload only after correctness is determined at submission time:

```text
fields
manifest
receipt_window
```

The SDK backend response must preserve `receipt_id: null` until backend authority is connected.

## Activation state

```text
Page state: installed
Script state: installed
Contract state: installed
Form model state: installed
Fixture state: installed
SDK form state: installed
SDK backend response fixture state: installed
Check state: installed
Workflow state: installed
Backend gateway state: not installed
SDK backend submission state: not installed
Authority-issued receipt state: not installed
Overall state: pre-backend activation
```
