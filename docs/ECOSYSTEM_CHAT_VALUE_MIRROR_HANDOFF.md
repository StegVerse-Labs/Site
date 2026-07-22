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

## Implemented in this cycle

```text
docs/ECOSYSTEM_CHAT_VALUE_CLAIM_CONTRACT.md
data/ecosystem-chat-value-claims.fixture.json
scripts/check_ecosystem_chat_value_claims.py
```

The contract now distinguishes:

```text
submitted
recognized
attributed
realized
distributable
settled
```

It also distinguishes:

```text
request for intelligence
from
contribution of intelligence
```

The fixture includes:

```text
private interaction-only user observation at submitted stage
confidential bounded-reuse correction at recognized stage
restricted licensed user record at provisional distributable stage
```

The validator fails closed when:

```text
claim identifiers are duplicated
required evidence is missing
stage requirements are skipped
confidence is outside 0..1
realized value lacks baseline or measurement
payment-like distribution lacks policy, contract, or allocation
settlement lacks a settlement receipt
interaction-only information is advanced to distributable
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
```

No token count, prompt length, message count, model cost, or self-reported importance can independently advance a claim.

Personal or private information is not presumed more valuable merely because it is sensitive. Originality, relevance, causal influence, lawful consent, bounded reuse, measurable improvement, scarcity, and avoided cost or harm require evidence.

## Remaining Site work

Destination `StegVerse-Labs/Site`:

```text
Bind the validator into canonical application validation.
Add a governed value-claim panel to ecosystem-chat.html.
Render claim stage, source posture, consent/reuse scope, materiality, uncertainty, reward class, dispute status, and non-payable boundary.
Link claims to canonical event_id values rather than rendered text.
Add captured-versus-derived inspection.
Add stage-history JSON/JSONL export.
Add browser tests for stage ordering, competing claims, consent narrowing, revocation, dispute, and non-payable status.
Add multilingual expectation text for English, Spanish, Simplified Chinese, and Traditional Chinese.
```

Destination `StegVerse-org/LLM-adapter`:

```text
Create canonical value-claim events upstream.
Produce stable claim_id and event_id bindings.
Hash and sign claim-stage transitions.
Evaluate consent, policy, admissibility, and reuse scope before downstream projection.
Emit recognition, attribution, realization, distribution, revocation, dispute, and settlement events.
```

Destination `master-records/orchestration`:

```text
Custody claim lineage, evidence, policy, contract, allocation, dispute, and settlement records.
Reconstruct stage progression and reject skipped or unsupported transitions.
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
1. Bind scripts/check_ecosystem_chat_value_claims.py into the Site validation chain.
2. Add the first human/governed synchronized claim renderer to ecosystem-chat.html.
3. Keep claim advancement preview-only until canonical gateway events, custody, reconstruction, and authorized settlement are verified.
4. Propagate the completed contract and expectation boundary to Publisher and both wiki projections only after Site validation passes.
```

## Release posture

```text
Contract: IMPLEMENTED
Fixture: IMPLEMENTED
Static validator: IMPLEMENTED, NOT YET OBSERVED IN CI
Browser renderer: NOT YET IMPLEMENTED
Gateway-origin claim events: NOT YET IMPLEMENTED
Custody and reconstruction: NOT YET IMPLEMENTED FOR VALUE CLAIMS
Authorized distribution: NOT YET IMPLEMENTED
Settlement: NOT YET IMPLEMENTED
Authority effect: NONE
```
