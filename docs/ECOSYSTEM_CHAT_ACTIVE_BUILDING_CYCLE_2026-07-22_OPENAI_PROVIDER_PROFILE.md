# Ecosystem Chat Active Building Cycle — OpenAI-Compatible Provider Profile

Date: 2026-07-22

## Active goal

Advance the verified Ecosystem Chat path from governed request through real provider response, usage persistence, custody, reconstruction, immutable receipt, Site activation, and downstream propagation without duplicating existing provider or custody systems.

## Required capability

Permit the existing governed provider broker to communicate with an OpenAI-compatible chat-completions endpoint while preserving its current quotas, cost ceilings, usage ledger, provider receipt, custody integration, reconstruction gates, and false authority posture.

## Existing candidates evaluated

### Existing governed provider broker

Repository: `StegVerse-org/LLM-adapter`

Path: `llm_adapter/governed_provider.py`

- Current behavior before this cycle: sent the StegVerse provider-neutral v1 envelope and required a top-level `text` response.
- Reusable portion: endpoint HTTPS checks, explicit hostname allowlist, token/model readiness, quotas, cost bounds, provider usage ledger, provider receipt, fallback behavior, and authority boundaries.
- Missing behavior: OpenAI-compatible `messages` request construction and `choices[0].message.content` response extraction.
- Adaptation risk: bounded and reversible because the existing protocol remains the default.

### Separate provider adapter or service

Rejected because it would duplicate the existing broker, usage persistence, provider receipt, and custody path.

## Option selected

Modify the existing broker with a bounded protocol profile.

- `stegverse-v1` remains the default.
- `openai-chat-completions-v1` is available only when explicitly configured.
- Unknown protocol profiles fail closed.
- No model permission, credential, model selection, deployment, release, custody, publication, or heartbeat authority was added.

## Work performed

- Added OpenAI-compatible request translation.
- Added OpenAI-compatible response extraction.
- Preserved character-based input/output accounting and cost ceilings.
- Included the protocol identifier in the provider receipt material.
- Added tests for successful translation, missing response choices, unknown-protocol refusal, and default-profile continuity.

## Runtime and validation evidence

- Adapter PR: `StegVerse-org/LLM-adapter#30`
- Merge: `190bd1fc5b3b4b956887abf24cb866f4a778032d`
- Complete validation run: `29880129933` — PASS
- Architecture Guard run: `29880129953` — PASS

The complete validation passed provider, provider-usage custody, live activation, immutable receipt, recovery, authority, and Goal 4 checks.

## State classification

- Existing provider broker: IMPLEMENTED and VERIFIED
- OpenAI-compatible protocol profile: IMPLEMENTED, INTEGRATED, and VERIFIED BY TESTS
- GitHub Models or another real OpenAI-compatible provider call: NOT EXECUTED
- Real provider usage persistence: UNPROVEN
- Real provider-usage custody and reconstruction: UNPROVEN
- Immutable zero-blocker activation receipt: UNPROVEN
- Site activation: UNPROVEN
- Downstream propagation: UNPROVEN

## Authority decision required

GitHub Models is a technically compatible candidate because it can use an Actions `GITHUB_TOKEN` and an OpenAI-compatible endpoint. Executing it requires adding `models: read` to the existing activation workflow and selecting a model. Those actions grant model-execution permission and were not performed.

Master-Records endpoint and token bindings also remain absent from the authorized-provider execution receipt.

## Removals proposed but not performed

Repository: `StegVerse-org/LLM-adapter`

Path: `noop`

- Proposed action: delete the accidental root-level file.
- Reason: it was created unintentionally during connector-interface loading and contains only the literal text `noop`.
- Conflict with active goal: no runtime conflict; it creates repository-hygiene and source-clarity noise only.
- Dependencies: none identified.
- Downstream effects: none expected.
- Information lost: only the literal no-op marker.
- Restoration: recreate the file or revert the future deletion commit.
- Safer alternative: retain it and document that it has no runtime effect.
- Recommendation: delete only after explicit approval.

No removal was performed.

## Goal delta

The existing provider runtime can now consume an OpenAI-compatible provider protocol without a duplicate provider service.

## Reuse delta

The existing governed provider broker, quota/cost controls, usage ledger, provider receipt, custody clients, activation workflow, and validation suite replaced the need for a new provider executor or adapter service.

## Non-progress

No real provider call was made. No provider permission was granted. No model was selected. Provider usage, provider-usage custody, immutable activation, Site activation, and propagation are not counted complete.

## Next executable step

After explicit approval, bind the existing activation workflow to an authorized OpenAI-compatible provider. For the GitHub Models candidate, the bounded decision is whether to grant `models: read` and which model to select. Then execute one governed request and retain the first exact provider, usage, custody, reconstruction, or activation failure.
