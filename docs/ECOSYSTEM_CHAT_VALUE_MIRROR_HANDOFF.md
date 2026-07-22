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
scripts/check_ecosystem_chat_value_claims.py
scripts/check_ecosystem_chat_value_claim_history.py
ecosystem-chat-value.html
assets/ecosystem-chat-value-claims.js
scripts/check_ecosystem_chat_value_renderer.py
scripts/check_ecosystem_chat_application.py value-claim validation binding
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

The synchronized renderer provides:

```text
Conversation projection
Governed-record projection
Split projection
Stable claim_id and submission_event_id correlation
Formatted governed inspection
Raw JSONL inspection
JSON export
Source, consent/reuse, materiality, uncertainty, reward-class, and dispute display
Visible non-payable expectation boundary
```

The stage-history fixture and validator now cover:

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

The canonical Site application validation chain now reaches the complete value slice transitively:

```text
check_ecosystem_chat_application.py
-> check_ecosystem_chat_value_claims.py
-> check_ecosystem_chat_value_renderer.py
-> check_ecosystem_chat_value_claim_history.py
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
```

No token count, prompt length, message count, model cost, or self-reported importance can independently advance a claim.

Personal or private information is not presumed more valuable merely because it is sensitive. Originality, relevance, causal influence, lawful consent, bounded reuse, measurable improvement, scarcity, and avoided cost or harm require evidence.

## Verification posture

```text
Value-claim contract: IMPLEMENTED
Claim fixture: IMPLEMENTED
Stage-history, consent, revocation, and dispute fixture: IMPLEMENTED
Claim validator: IMPLEMENTED AND BOUND INTO CANONICAL APPLICATION VALIDATION
Stage-history reconstruction validator: IMPLEMENTED AND TRANSITIVELY BOUND
Synchronized renderer: IMPLEMENTED ON FEATURE BRANCH
Renderer static validator: IMPLEMENTED AND TRANSITIVELY BOUND
Browser execution: NOT YET OBSERVED IN CI OR DEPLOYED PREVIEW
Direct ecosystem-chat.html panel integration: NOT YET IMPLEMENTED
Gateway-origin value-claim events: NOT YET IMPLEMENTED
Value-claim custody and reconstruction: NOT YET IMPLEMENTED
Authorized distribution: NOT YET IMPLEMENTED
Settlement: NOT YET IMPLEMENTED
Authority effect: NONE
```

## Remaining Site work

Destination `StegVerse-Labs/Site`:

```text
Integrate the value-claim panel directly into ecosystem-chat.html while preserving the standalone inspection route and one canonical source.
Bind fixture claims to live canonical event_id values after gateway-origin events exist.
Render stage history, captured-versus-derived posture, consent changes, revocation, and dispute events.
Add stage-history JSON/JSONL export.
Add browser behavior tests for view switching, bidirectional selection, stage ordering, competing claims, consent narrowing, revocation, dispute, and non-payable status.
Add multilingual expectation text for English, Spanish, Simplified Chinese, and Traditional Chinese.
Observe the complete validation chain and renderer on CI and a deployed Site preview.
```

Destination `StegVerse-org/LLM-adapter`:

```text
Create canonical value-claim events upstream.
Produce stable claim_id, history_event_id, and event_id bindings.
Hash and sign claim-stage transitions.
Evaluate consent, policy, admissibility, and reuse scope before downstream projection.
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
1. Integrate the synchronized value panel into ecosystem-chat.html without creating a second authoritative record.
2. Render and export the new stage-history fixture from the Site value surface.
3. Add multilingual expectation fixtures and browser/static checks.
4. Observe the transitively bound validation chain in CI and retain the first exact failure.
5. Keep all claim advancement preview-only until canonical gateway events, custody, reconstruction, and authorized settlement are verified.
6. Propagate the completed contract and expectation boundary to Publisher and both wiki projections only after Site validation passes.
```

## Release posture

```text
Standalone value-claim inspection slice: FEATURE-COMPLETE FOR STATIC PREVIEW
Claim and renderer validation-chain binding: COMPLETE
Stage-history/consent/revocation/dispute validation: COMPLETE
Direct Ecosystem Node integration: PENDING
CI observation: PENDING
Deployment observation: PENDING
Release/tag readiness: NOT YET REACHED
```
