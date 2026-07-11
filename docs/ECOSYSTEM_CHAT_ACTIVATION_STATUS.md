# Ecosystem Chat Activation Status

## Status

`ecosystem-chat.html` is installed as a text-only governed chat preview for StegVerse build and governance requests.

The page is currently in local-simulation mode. It does not call a live backend, execute shell commands, accept credentials, perform repository writes, or issue proof receipts.

The page now has one public primary path: a user reads the boundary, tries the governed chat preview, and receives local route classification. Technical SDK/gateway details remain available, but only as a secondary collapsible technical section.

The SDK Entry Form is installed as a browser-side technical preview for the StegVerse-org/SDK entry point if and only if the generated manifest window and receipt window remain distinct from the fillable fields and are determined correct at submission time.

The Site-side activation surface is complete for pre-backend handoff. Remaining activation belongs to the governed SDK/backend implementation boundary.

## Current installed surface

| Surface | State |
|---|---|
| Public page | Installed: `ecosystem-chat.html` |
| Browser script | Installed: `assets/ecosystem-chat.js` |
| Single-entry UX contract | Installed and guarded: one primary governed chat preview entry, technical details collapsible |
| Gateway contract | Installed: `docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md` |
| Form gateway model | Installed: `docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md` |
| Boundary check doc | Installed: `docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md` |
| SDK backend handoff | Installed: `docs/ECOSYSTEM_CHAT_SDK_BACKEND_HANDOFF.md` |
| README discovery | Installed and guarded: `README.md` references activation status, boundary doc, both checkers, declared task, registry, and both direct commands |
| SDK form payload fixture | Installed: `fixtures/ecosystem-chat/sdk-form-payload.example.json` |
| SDK backend response fixture | Installed: `fixtures/ecosystem-chat/sdk-backend-response.example.json` |
| Gateway fixtures | Installed: `fixtures/ecosystem-chat/request.example.json` and `fixtures/ecosystem-chat/response.example.json` |
| Contract checker | Installed and aligned: `scripts/check_ecosystem_chat_contract.py` checks the boundary task path, activation-status boundary state, and README command discovery |
| Boundary verifier | Installed and aligned: `scripts/check_ecosystem_chat_boundary.py` checks page, single-entry UX, docs, README command discovery, activation status, fixtures, declared task, and registry |
| Declared boundary task | Installed: `data/headless-tasks/ecosystem-chat-boundary-check-v1.json` |
| Headless task registry | Installed: `data/headless-task-registry-v1.json` contains active `ecosystem-chat-boundary-check-v1` |
| Workflow gate | Installed: `github/workflows/check-ecosystem-chat.yml` path shown without leading dot |
| iOS path mapping | Installed: `iosnoperiod/iosnoperiod.md` and `iosnoperiod/workflow-map.json` |

## Browser form state

```text
Primary public path state: single governed chat preview entry
Technical details state: collapsible secondary section
Fillable fields state: installed
Closed-choice dropdown state: installed
Manifest window state: installed
Receipt window state: installed
Submission correctness check state: installed locally
No-shell boundary state: installed
No-credential boundary state: installed
Restricted-admin routing state: installed
Authority-required manifest state: installed
Receipt-required execution state: installed
SDK payload fixture state: installed
SDK backend response fixture state: installed
SDK backend submission state: not installed
```

## Machine-readable boundary declarations

```yaml
raw_shell_allowed: false
authority_required: true
rate_limit_required: true
receipt_required_for_execution: true
restricted_admin_route: "Restricted admin"
```

These declarations describe the Site preview boundary only. They do not grant execution, repository mutation, deployment, receipt issuance, or ecosystem-wide authority.

## UX contract

The public page must not return to a multi-entry console or task-launcher shape.

```text
Required:
- one primary hero action to try the governed chat preview
- one secondary hero action explaining the boundary
- local chat classification remains the visible primary interaction
- SDK/gateway details remain under a collapsible technical section
- Site remains preview-only

Forbidden:
- multiple competing hero actions such as SDK form, console, guardrails, trust status, gateway contract, form model, boundary check, and verification guide all presented together as primary options
- public framing as a control panel, task launcher, demo index, shell, receipt issuer, or repo admin surface
```

## Boundary

Site remains a public mirror and user advancement surface only.

The console may collect text input, classify local route posture, display local transcript hashes, preserve a bounded browser transcript, generate form-derived manifest and receipt-window previews, identify restricted administration requests, and call a governed backend gateway when that gateway exists.

The console must not issue proof receipts, execute shell commands, accept credentials, expose tokens, perform repository writes, delete branches, edit workflows, claim deployment authority, or replace StegVerse-002, formalism-tests, Continuity, StegVerse-org/SDK, repo-standards, or any other authority-bearing ecosystem component.

The manifest window and receipt window are generated previews. They are not proof receipts.

## Verification chain

```text
scripts/check_ecosystem_chat_contract.py
  -> confirms the page, script, docs, fixtures, workflow/iOS surfaces, README command discovery, and boundary-task references preserve the contract.

scripts/check_ecosystem_chat_boundary.py
  -> confirms the no-shell/no-credential/authority-required/receipt-required boundary and single-entry UX contract across page, docs, README command discovery, activation status, fixtures, declared task, and registry.

data/headless-tasks/ecosystem-chat-boundary-check-v1.json
  -> declares the boundary verifier as ordinary_analysis with expected inputs including activation status and both checkers.

data/headless-task-registry-v1.json
  -> keeps ecosystem-chat-boundary-check-v1 active.
```

## Verification commands

Contract check:

```bash
python scripts/check_ecosystem_chat_contract.py
```

Expected output:

```text
Ecosystem Chat contract check passed.
```

Boundary and UX check:

```bash
python scripts/check_ecosystem_chat_boundary.py
```

Expected output contains:

```json
{
  "ok": true,
  "boundary": "no-shell/no-credential/authority-required/receipt-required",
  "ux_contract": "single-primary-governed-chat-preview-entry"
}
```

Declared task:

```text
ecosystem-chat-boundary-check-v1
```

Declared task path:

```text
data/headless-tasks/ecosystem-chat-boundary-check-v1.json
```

Registry path:

```text
data/headless-task-registry-v1.json
```

## Next activation milestone

Create the governed backend gateway for:

```text
POST /api/ecosystem-chat
```

The backend must accept the existing request contract, apply route policy, enforce validation and rate limits, reject raw command execution, reject or route credential/destructive administration intent to restricted review, dispatch only to approved ecosystem handlers, and return a bounded response with task status and either an authority-issued receipt ID or an explicit `null` receipt state.

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
Single-entry UX contract state: installed and guarded
Boundary check doc state: installed
README discovery state: installed and guarded
SDK backend handoff state: installed
Fixture state: installed
SDK form state: installed
SDK backend response fixture state: installed
Contract check state: installed and aligned with boundary task
Boundary verifier state: installed with single-entry UX guard
Declared task state: installed
Registry state: installed
Workflow state: installed
No-shell boundary state: installed
No-credential boundary state: installed
Restricted-admin routing state: installed
Site-side pre-backend handoff state: complete
Backend gateway state: not installed
SDK backend submission state: not installed
Authority-issued receipt state: not installed
Overall state: Site-side complete; SDK/backend activation pending
```
