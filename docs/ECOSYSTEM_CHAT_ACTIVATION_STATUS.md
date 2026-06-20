# Ecosystem Chat Activation Status

## Status

`ecosystem-chat.html` is installed as a text-only browser command surface for StegVerse build and governance requests.

The page is currently in local-simulation mode. It does not call a live backend and does not issue proof receipts.

## Current installed surface

| Surface | State |
|---|---|
| Public page | Installed: `ecosystem-chat.html` |
| Browser script | Installed: `assets/ecosystem-chat.js` |
| Gateway contract | Installed: `docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md` |
| Static checker | Installed: `scripts/check_ecosystem_chat_contract.py` |
| Workflow gate | Installed: `github/workflows/check-ecosystem-chat.yml` path shown without leading dot |
| iOS path mapping | Installed: `iosnoperiod/iosnoperiod.md` and `iosnoperiod/workflow-map.json` |

## Boundary

Site remains a public mirror and command surface only.

The console may collect text input, classify local route posture, display local transcript hashes, preserve a bounded browser transcript, and call a governed backend gateway when that gateway exists.

The console must not issue proof receipts, claim deployment authority, or replace StegVerse-002, formalism-tests, Continuity, or any other authority-bearing ecosystem component.

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

## Activation state

```text
Page state: installed
Script state: installed
Contract state: installed
Check state: installed
Workflow state: installed
Backend gateway state: not installed
Authority-issued receipt state: not installed
Overall state: pre-backend activation
```
