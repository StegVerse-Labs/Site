# Ecosystem Chat Value Mirror Handoff

## Source of truth

This file is the continuation record for governed chat-submitted value claims within `StegVerse-Labs/Site`.

The repository-wide source of truth remains `docs/SITE_MIRROR_HANDOFF.md`. This record narrows the active subgoal without replacing repository-wide activation ownership.

## Active goal

```text
Preserve a user's governed chat submission as a traceable value claim,
separate information contribution from compute consumption,
advance claims only through evidence-bound stages,
and keep all prototype estimates visibly non-payable until authorized distribution and settlement exist.
```

## Implemented

```text
docs/ECOSYSTEM_CHAT_VALUE_CLAIM_CONTRACT.md
data/ecosystem-chat-value-claims.fixture.json
data/ecosystem-chat-value-claim-history.fixture.json
data/ecosystem-chat-value-expectations.i18n.json
scripts/check_ecosystem_chat_value_claims.py
scripts/check_ecosystem_chat_value_claim_history.py
scripts/check_ecosystem_chat_value_renderer.py
scripts/check_ecosystem_chat_value_integration.py
ecosystem-chat-value.html
assets/ecosystem-chat-value-claims.js
assets/ecosystem-chat-value-integration.js
assets/ecosystem-chat-hps.js direct loader and navigation integration
scripts/check_ecosystem_chat_application.py transitive value-validation binding
```

The contract and renderer distinguish:

```text
submitted
recognized
attributed
realized
distributable
settled
```

They also distinguish:

```text
request for intelligence
from
contribution of intelligence
```

The standalone and directly integrated renderers provide:

```text
Conversation projection
Governed-record projection
Split projection
Direct governed value panel inside ecosystem-chat.html
Stable claim_id, submission_event_id, and history_event_id correlation
Formatted governed inspection
Raw JSON/JSONL inspection
Claim and stage-history export
Source, consent/reuse, materiality, uncertainty, reward-class, and dispute display
Consent-change, revocation, and dispute history rendering
Visible non-payable expectation boundary
Locale-aware English, Spanish, Simplified Chinese, and Traditional Chinese projection
Fail-closed original governed records when localized display is unavailable
```

The multilingual expectation fixture includes native governed wording for:

```text
en
es
zh-Hans
zh-Hant
```

It preserves the distinctions:

```text
claim preserved != value proven
recognized influence != ownership or exclusivity
value distributable != payment
sensitive information != automatic value multiplier
consent and reuse scope remain binding
```

The stage-history fixture and validator cover:

```text
ordered one-stage-at-a-time progression
consent narrowing without silent record mutation
revocation without historical deletion
post-revocation advancement rejection
competing claims and open dispute events
reconstructed current-stage verification
stable history_event_id uniqueness
evidence, consent, policy, and reuse references
```

The canonical Site application validation chain reaches the complete value slice transitively:

```text
check_ecosystem_chat_application.py
-> check_ecosystem_chat_value_claims.py
-> check_ecosystem_chat_value_renderer.py
   -> check_ecosystem_chat_value_claim_history.py
   -> check_ecosystem_chat_value_integration.py
```

The validators fail closed when:

```text
claim or history identifiers are duplicated
required evidence, consent, or policy references are missing
stage requirements are skipped
stage history does not begin at submitted
non-stage events change the effective stage
timestamps are out of order
confidence is outside 0..1
realized value lacks baseline or measurement
payment-like distribution lacks policy, contract, or allocation
settlement lacks a settlement receipt
interaction-only information is advanced to distributable
revoked claims attempt later-stage advancement
activity-only submitted claims assert payable reward
direct integration assets are not loaded by ecosystem-chat.html
required multilingual governed wording is absent
any fixture attempts to assert authority
```

## Authority boundary

```text
claim preserved != value proven
value recognized != ownership proven
attribution != exclusivity
realized benefit != distributable value
distributable value != payment
prototype estimate != royalty
browser fixture != custody
validator PASS != settlement authority
renderer correlation != causal proof
JSON export != authenticated custody
revocation event != historical erasure
dispute event != claim resolution
localized projection != rewritten canonical record
direct Site integration != gateway-origin value event
```

No token count, prompt length, message count, model cost, or self-reported importance can independently advance a claim.

Personal or private information is not presumed more valuable merely because it is sensitive. Originality, relevance, causal influence, lawful consent, bounded reuse, measurable improvement, scarcity, and avoided cost or harm require evidence.

## Verification posture

```text
Value-claim contract: IMPLEMENTED
Claim fixture: IMPLEMENTED
Stage-history, consent, revocation, and dispute fixture: IMPLEMENTED
Multilingual expectation fixture: IMPLEMENTED FOR en, es, zh-Hans, zh-Hant
Claim validator: IMPLEMENTED AND BOUND INTO CANONICAL APPLICATION VALIDATION
Stage-history reconstruction validator: IMPLEMENTED AND TRANSITIVELY BOUND
Standalone synchronized renderer: IMPLEMENTED ON FEATURE BRANCH
Direct ecosystem-chat.html value panel integration: IMPLEMENTED THROUGH EXISTING HPS LOADER
Stage-history rendering and export: IMPLEMENTED
Locale-aware expectation selection: IMPLEMENTED
Direct integration validator: IMPLEMENTED AND TRANSITIVELY BOUND
Browser execution: NOT YET OBSERVED IN CI OR DEPLOYED PREVIEW
Gateway-origin value-claim events: NOT YET IMPLEMENTED
Value-claim custody and reconstruction: NOT YET IMPLEMENTED
Authorized distribution: NOT YET IMPLEMENTED
Settlement: NOT YET IMPLEMENTED
Authority effect: NONE
```

## Remaining Site work

Destination `StegVerse-Labs/Site`:

```text
Bind fixture claims to live canonical event_id values after gateway-origin events exist.
Add captured-versus-derived posture and downstream projection permission controls to value records.
Add browser behavior tests for direct panel loading, locale switching, bidirectional selection, stage ordering, consent narrowing, revocation, dispute, raw-mode switching, exports, and non-payable status.
Observe the complete validation chain and direct panel on CI and a deployed Site preview.
Retain the first exact browser, localization, fixture, or validation failure.
```

Destination `StegVerse-org/LLM-adapter`:

```text
Create canonical value-claim events upstream.
Produce stable claim_id, history_event_id, and event_id bindings.
Hash and sign claim-stage transitions.
Evaluate consent, policy, admissibility, reuse scope, captured-versus-derived posture, and downstream projection permission before projection.
Emit recognition, attribution, realization, distribution, consent-change, revocation, dispute, and settlement events.
```

Destination `master-records/orchestration`:

```text
Custody claim lineage, evidence, policy, contract, allocation, consent, revocation, dispute, and settlement records.
Reconstruct stage progression and reject skipped, unsupported, or post-revocation transitions.
Return authenticated reconstruction and disclosure receipts.
```

Downstream after verified activation:

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

## Next machine action

```text
1. Add captured-versus-derived and downstream projection permission fields, fixtures, rendering, and fail-closed validation.
2. Add direct-panel browser behavior fixtures or tests without creating a second authoritative record.
3. Observe the transitively bound validation chain in CI and retain the first exact failure.
4. Keep all claim advancement preview-only until canonical gateway events, custody, reconstruction, and authorized settlement are verified.
5. Propagate the completed contract and expectation boundary to Publisher and both wiki projections only after Site validation passes.
```

## Release posture

```text
Standalone value-claim inspection slice: FEATURE-COMPLETE FOR STATIC PREVIEW
Direct Ecosystem Node integration: IMPLEMENTED ON FEATURE BRANCH
Multilingual expectation projection: IMPLEMENTED ON FEATURE BRANCH
Claim and renderer validation-chain binding: COMPLETE
Stage-history/consent/revocation/dispute validation: COMPLETE
CI observation: PENDING
Deployment observation: PENDING
Release/tag readiness: NOT YET REACHED
```
