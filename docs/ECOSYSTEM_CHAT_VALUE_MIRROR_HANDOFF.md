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
data/ecosystem-chat-value-projection-permissions.fixture.json
data/ecosystem-chat-value-browser-behavior.fixture.json
data/ecosystem-chat-value-expectations.i18n.json
scripts/check_ecosystem_chat_value_claims.py
scripts/check_ecosystem_chat_value_claim_history.py
scripts/check_ecosystem_chat_value_projection_permissions.py
scripts/check_ecosystem_chat_value_browser_behavior.py
scripts/check_ecosystem_chat_value_renderer.py
scripts/check_ecosystem_chat_value_integration.py
ecosystem-chat-value.html
assets/ecosystem-chat-value-claims.js
assets/ecosystem-chat-value-integration.js
assets/ecosystem-chat-hps.js direct loader and navigation integration
scripts/check_ecosystem_chat_application.py transitive value-validation binding
```

## Governed value progression

```text
submitted
-> recognized
-> attributed
-> realized
-> distributable
-> settled
```

A prompt may be both:

```text
request for intelligence
+
contribution of intelligence
```

No stage is advanced by token count, prompt length, message count, model cost, or self-reported importance.

## Implemented renderer behavior

```text
Conversation projection
Governed-record projection
Split projection
Direct governed value panel inside ecosystem-chat.html
Stable claim_id, submission_event_id, and history_event_id correlation
Formatted governed inspection
Raw JSON/JSONL inspection
Claim, history, and projection-permission export
Source, consent/reuse, materiality, uncertainty, reward-class, and dispute display
Consent-change, revocation, and dispute history rendering
Captured-versus-derived inspection
Explicit allowed and denied downstream destinations
Default-deny downstream projection posture
Mandatory redaction and minimum-disclosure markers
Visible non-payable expectation boundary
Locale-aware English, Spanish, Simplified Chinese, and Traditional Chinese projection
Fail-closed original governed records when localized display is unavailable
```

## Captured-versus-derived and projection permission model

Every value claim now has exactly one projection-permission record containing:

```text
claim_id
submission_event_id
information_class = captured | derived
captured_source_refs
derivation_refs
projection.default = deny
allowed_destinations
denied_destinations
purpose_refs
policy_refs
consent_refs
redaction_required = true
minimum_disclosure = true
expires_at
reason
```

Known downstream destinations are explicitly classified:

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

The permission validator requires every known destination to be either allowed or denied, never both. Interaction-only information cannot be projected downstream. Bounded captured information may reach no more than one named destination and only for a stated purpose. Derived information requires derivation evidence and remains default-deny, redacted, and minimum-disclosure.

## Stage-history and consent model

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

## Multilingual expectation management

Native governed wording is implemented for:

```text
en
es
zh-Hans
zh-Hant
```

Each projection preserves:

```text
claim preserved != value proven
recognized influence != ownership or exclusivity
distributable value != payment
sensitive information != automatic value multiplier
consent and reuse scope remain binding
```

## Validation chain

```text
check_ecosystem_chat_application.py
-> check_ecosystem_chat_value_claims.py
-> check_ecosystem_chat_value_renderer.py
   -> check_ecosystem_chat_value_claim_history.py
   -> check_ecosystem_chat_value_integration.py
      -> check_ecosystem_chat_value_projection_permissions.py
      -> check_ecosystem_chat_value_browser_behavior.py
```

The static browser-behavior contract covers:

```text
direct panel load
locale switching
stable selection and canonical correlation
stage-history rendering
projection-permission rendering
raw-mode switching
export behavior
fail-closed behavior
```

Static markers are verified. Actual browser execution remains unobserved.

## Fail-closed rejection conditions

```text
claim, history, or behavior identifiers are duplicated
required evidence, consent, policy, purpose, or source references are missing
stage requirements are skipped
stage history does not begin at submitted
non-stage events change effective stage
timestamps are out of order
confidence is outside 0..1
realized value lacks baseline or measurement
payment-like distribution lacks policy, contract, or allocation
settlement lacks a settlement receipt
interaction-only information permits downstream projection
captured information asserts derivation references
derived information lacks derivation references
a destination is both allowed and denied
any known destination is left unclassified
redaction or minimum disclosure is disabled
revoked claims attempt later-stage advancement
activity-only submitted claims assert payable reward
direct integration assets are not loaded
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
projection permission != publication authority
allowed destination != completed downstream ingestion
captured record != reusable record
derived record != independently verified derivation
```

## Verification posture

```text
Value-claim contract: IMPLEMENTED
Claim fixture: IMPLEMENTED
Stage-history, consent, revocation, and dispute fixture: IMPLEMENTED
Captured-versus-derived projection permission fixture: IMPLEMENTED
Projection permission validator: IMPLEMENTED AND TRANSITIVELY BOUND
Static direct-panel browser behavior fixture and validator: IMPLEMENTED AND TRANSITIVELY BOUND
Multilingual expectation fixture: IMPLEMENTED FOR en, es, zh-Hans, zh-Hant
Claim validator: IMPLEMENTED AND BOUND INTO CANONICAL APPLICATION VALIDATION
Stage-history reconstruction validator: IMPLEMENTED AND TRANSITIVELY BOUND
Standalone synchronized renderer: IMPLEMENTED ON FEATURE BRANCH
Direct ecosystem-chat.html value panel integration: IMPLEMENTED THROUGH EXISTING HPS LOADER
Stage-history and projection-permission rendering/export: IMPLEMENTED
Locale-aware expectation selection: IMPLEMENTED
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
Add executable browser behavior tests for direct panel loading, locale switching, bidirectional selection, stage ordering, consent narrowing, revocation, dispute, raw-mode switching, exports, and non-payable status.
Observe the complete validation chain and direct panel in CI and on a deployed Site preview.
Retain the first exact browser, localization, fixture, permission, or validation failure.
```

Destination `StegVerse-org/LLM-adapter`:

```text
Create canonical value-claim events upstream.
Produce stable claim_id, history_event_id, and event_id bindings.
Hash and sign claim-stage transitions.
Evaluate consent, policy, admissibility, reuse scope, captured-versus-derived posture, and downstream projection permission before projection.
Emit recognition, attribution, realization, distribution, consent-change, revocation, dispute, projection-permission, and settlement events.
```

Destination `master-records/orchestration`:

```text
Custody claim lineage, evidence, policy, contract, allocation, consent, revocation, dispute, projection permission, and settlement records.
Reconstruct stage progression and reject skipped, unsupported, or post-revocation transitions.
Verify captured-versus-derived lineage and downstream permission posture.
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
1. Add executable browser behavior testing or the strongest available deterministic interaction harness.
2. Observe the transitively bound validation chain in CI and retain the first exact failure.
3. Bind claims to gateway-origin canonical events when the upstream contract becomes available.
4. Keep all claim advancement and downstream projection preview-only until canonical gateway events, custody, reconstruction, authorized distribution, and settlement are verified.
5. Propagate the completed contract and expectation boundary to Publisher and both wiki projections only after Site validation passes.
```

## Release posture

```text
Standalone value-claim inspection slice: FEATURE-COMPLETE FOR STATIC PREVIEW
Direct Ecosystem Node integration: IMPLEMENTED ON FEATURE BRANCH
Captured-versus-derived projection permissions: IMPLEMENTED ON FEATURE BRANCH
Multilingual expectation projection: IMPLEMENTED ON FEATURE BRANCH
Claim, renderer, permission, and behavior validation-chain binding: COMPLETE
Stage-history/consent/revocation/dispute validation: COMPLETE
Executable browser observation: PENDING
CI observation: PENDING
Deployment observation: PENDING
Release/tag readiness: NOT YET REACHED
```
