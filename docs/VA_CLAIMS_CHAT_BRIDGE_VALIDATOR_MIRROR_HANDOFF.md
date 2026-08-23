# VA Claims Chat Bridge Validator Mirror Handoff

Updated: 2026-08-22
Repository: `StegVerse-Labs/Site`
Issue: `#439`
Claim: `SITE-VA-CLAIMS-CHAT-BRIDGE-VALIDATOR-CONSISTENCY-439-20260822`
Branch: `claim/site-va-claims-chat-bridge-validator-439`
State: `IMPLEMENTATION_IN_PROGRESS`

## Goal

Reconcile the released VA Claims Chat bridge validator with the canonical veteran-first public-UI contract so the bridge and surface validators no longer require opposite states for the same internal label.

## Source of truth and ownership

Parent product handoff: `docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`.
Canonical bridge task: `data/tasks/SITE-VA-COORDINATED-LLM-BRIDGE-002.json`.

That bridge task is already:

```text
state: COMPLETE
claim_state: RELEASED_COMPLETE_PENDING_RUNTIME_ACTIVATION
runtime_projection.state: BLOCKED
runtime_projection.active: false
authority_effect: false
activation_effect: false
```

Its runtime activation remains separately owned by Site #113 / StegVerse-org/LLM-adapter#90 / Master Records. #439 owns only the released bridge-validator consistency assertion.

## Proven contradiction

Site #434 / PR #438 exact merge-ref validation on head `00d0a0e0e5f0f587834c6e9fe937366ed0390875` produced:

```text
VA Claims Chat Surface Validation
run 32608567184 / job 97117620348: PASS

VA Claims Chat LLM Bridge
run 32608567211 / job 97117620315: FAIL
VA_CLAIMS_CHAT_LLM_BRIDGE_FAIL:chat_truthful_inactive_label
```

The two validators contradicted one another on the exact string `SOURCE-GROUNDED PROCEDURAL HELP`:

- `scripts/validate_va_claims_chat_surface.py` explicitly rejects it as `technical_or_internal_ui_token_present`, because veteran-facing UI must not expose internal capability/governance labels.
- the old `scripts/validate_va_claims_chat_llm_bridge.py` explicitly required the same string.

The bridge task itself records an earlier merged-main validator failure caused by stale governance-heavy veteran-facing copy, followed by a validator repair. This is validator drift, not reopened runtime work.

## Ownership separation established by #439

The first #439 implementation changed the bridge assertion from “label must appear” to “label must be absent.” Exact PR #440 run `32608937713` then correctly exposed an ordering cycle: current `main` still contains the old label because Site #434 has not merged its page correction yet, so #439 could not merge first while asserting page-label absence.

The correct separation is:

```text
scripts/validate_va_claims_chat_surface.py
  owns veteran-facing public-UI policy, including exclusion of internal labels

scripts/validate_va_claims_chat_llm_bridge.py
  owns runtime projection, runtime bridge binding, fail-closed authority checks,
  disabled upload/filing boundary, and proof that it is attached to the intended
  veteran-facing Claims Chat surface
```

Accordingly, the bridge validator must assert neither presence nor absence of `SOURCE-GROUNDED PROCEDURAL HELP`. The dedicated surface validator remains the sole validator for that UI-policy rule. This eliminates the dependency cycle without weakening any runtime or authority gate.

## Required retained bridge validation

- every runtime projection precondition unchanged;
- `active=false` required for the current projection;
- blocked/review/retry state required;
- endpoint and activation/execution receipt hashes null while inactive;
- private upload false;
- private retrieval false;
- filing false;
- authority and activation effects false;
- synthetic active-projection negative tests unchanged;
- runtime bridge marker checks unchanged;
- bridge include required in `va-claims-chat.html`;
- disabled private-upload/automated-filing boundary required;
- veteran-facing marker `Ask a VA claims question in your own words` required;
- no assertion in the bridge validator about the internal-label token;
- `va-claims-chat.html` and `.github/workflows/va-claims-chat-surface.yml` remain owned by #434 and are not mutated by #439.

## Completion gate

Release requires the repaired bridge validator itself to PASS on exact-head PR validation, claim/orchestration gates to PASS, integration to merge, and durable release evidence to be recorded here and in `data/session-work-claims.json`. After #439 releases, #434 must rebase onto that exact main and prove both validators PASS together before its own merge. #439 grants no runtime/provider/custody/upload/filing/activation authority.
