# Ecosystem Chat Session Archive — 2026-07-13

## Disposition

This session may be archived after this record is committed.

## Decisions preserved

- Ecosystem Chat is the user-facing StegVerse Ecosystem LLM interface, not a generic chatbot.
- The live governed gateway belongs to the Ecosystem Chat path.
- Every interaction should expose transparent routing/load bands: `intra`, `inter`, `research`, `provider`, `solver`, and `receipt`.
- The `research` band represents networked sources outside the ecosystem when necessary.
- The `solver` band is a first-class math-problem solver path.
- Cost and usage reporting belong to Ecosystem Chat telemetry and ecosystem statistics.
- Older live-gateway drafts are treated as superseded by the latest gateway candidate.
- ST-016 and cross-repo consistency scanning remain organizational validation surfaces rather than runtime chat components.

## Completed work

- Added routing-band visualization and solver preview to `ecosystem-chat.html`.
- Added local interaction-profile generation to `assets/ecosystem-chat.js`.
- Updated request, response, and SDK-form fixtures with interaction telemetry.
- Extended boundary and contract checkers to validate interaction telemetry and solver support.
- Added `docs/ECOSYSTEM_CHAT_INTERACTION_TELEMETRY.md`.
- Added local preview backend contract at `backend/ecosystem_chat_gateway_preview.py`.
- Added preview checker at `scripts/check_ecosystem_chat_gateway_preview.py`.
- Added and registered `ecosystem-chat-gateway-preview-check-v1`.
- Added `docs/ECOSYSTEM_CHAT_GATEWAY_PREVIEW_STATUS.md`.

## Remaining work

- Wire `scripts/check_ecosystem_chat_gateway_preview.py` into `scripts/run_site_task.py validate` when a permitted update path succeeds.
- Preserve the single-primary-path Site preview boundary.
- Connect the future live gateway, provider clients, cost model, usage metrics, research routing, and math solver behind the governed backend boundary.
- Keep `receipt_id` null until an authority-bearing backend receipt path exists.
- Verify Site validation and all-local task execution through the normal repository validation path.

## Blockers and ownership

- Previous direct attempts to update `scripts/run_site_task.py`, `docs/SITE_MIRROR_HANDOFF.md`, and `docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md` were blocked by the connector safety layer.
- The unresolved validator wiring is durably represented by the active declared task and this archive record.
- No active session-specific task claim remains in this conversation.
- Successor Site work should begin from `docs/SITE_MIRROR_HANDOFF.md`, this archive record, the active headless-task registry, and the gateway-preview status document.

## Pending validation and observation

- Run `python scripts/check_ecosystem_chat_contract.py`.
- Run `python scripts/check_ecosystem_chat_boundary.py`.
- Run `python scripts/check_ecosystem_chat_gateway_preview.py`.
- Run `python scripts/run_site_task.py validate` after validator wiring is installed.

## Permitted continuation scope

Continuation may modify only the declared Site preview, validation, fixture, task, documentation, and future governed backend integration surfaces while preserving the no-authority public Site boundary.

## Final loss test

All decisions, completed changes, blockers, remaining actions, ownership state, validation requirements, and continuation constraints unique to this session are preserved in durable repository records. No future action requires access to the conversation transcript.
