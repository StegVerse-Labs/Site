# Child-Safe Networking Mirror Handoff

This file is the current task source of truth for governed child-safe networking in `StegVerse-Labs/Site`.

## Active goals

```text
SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT
State: COMPLETE — GitHub Pages built and canonical public-route verifier passed.

SITE-0004-CHILD-MODE-GOVERNANCE-TOGGLE
State: COMPLETE — repository-native validator recorded MODE_TOGGLE=NORMAL_MODE_CHILD_MODE.

SITE-0005-CHILD-SAFETY-BOUNDARY-HISTORY
Goal: keep the public child-safety surface as a current boundary specification and law-comparison record, with all later boundary adjustments appended at the bottom with rationale.
State: READY_FOR_MACHINE_COMPLETION_CHECK.
```

Repository: `StegVerse-Labs/Site`
Branch: `main`

## Authoritative files

```text
child-safety-demo.html
children-safe-networking.html
docs/CHILD_MODE_REGULATORY_GOVERNANCE.md
data/tasks/SITE-0002-CHILD-SAFETY-DEMO.json
data/tasks/SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT.json
data/tasks/SITE-0004-CHILD-MODE-GOVERNANCE-TOGGLE.json
data/tasks/SITE-0005-CHILD-SAFETY-BOUNDARY-HISTORY.json
scripts/check_child_safety_demo.py
scripts/check_child_safety_public_deployment.py
.github/workflows/verify-child-safety-public-deployment.yml
docs/CHILD_SAFE_NETWORKING_MIRROR_HANDOFF.md
repository-task-observation.report.json
data/site-orchestration-state.json
```

## Completed evidence

```text
SITE-0001-PERSONAL-DATA-CONTROL: COMPLETE
SITE-0002-CHILD-SAFETY-DEMO: COMPLETE
SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT: COMPLETE
  GitHub Pages repository status: built
  Pages build: 1137699817
  Canonical target: https://stegverse.org/child-safety-demo.html
  Verification workflow run: 31188562057
  Verification conclusion: success

SITE-0004-CHILD-MODE-GOVERNANCE-TOGGLE: COMPLETE
  CHILD_SAFETY_DEMO=PASS
  MODE_TOGGLE=NORMAL_MODE_CHILD_MODE
  MODE_AUTHORITY=VERIFIED_POLICY_STATE_REQUIRED_IN_PRODUCTION
```

## Current public purpose

The child-safety page is not framed as a liability waiver. It is a public statement of the boundary as presently configured and a comparison between that boundary and current/proposed child-safety law.

The purpose is to demonstrate a policy proposition that can be tested rather than merely asserted:

```text
If the risk-bearing activity can be deterministically refused
while bounded communication, learning, creativity, collaboration,
and known-person networking remain available,
then capability governance is a plausible alternative that lawmakers
should evaluate alongside or in lieu of complete bans.
```

The page therefore exposes both the positive capabilities retained and the risky capabilities denied, and gives visitors a repeatable ALLOW / DENY / REVIEW_REQUIRED interaction surface.

## Boundary-history rule

`child-safety-demo.html` now includes a bottom-of-page `Boundary Change Record`.

The rule is append-only:

```text
new policy/law/technical change
-> retain previous public entry
-> append new date
-> state exact boundary change
-> state rationale
-> update legal/policy comparison where relevant
-> validate required markers
```

Changes must not silently rewrite prior rationale. Git history remains the immutable source-level history; the public append-only record provides an understandable chronology for users, parents, regulators, and lawmakers.

Initial entries dated 2026-08-07 record:

1. establishment of the bounded Normal Mode / Child Mode profile;
2. establishment of the public append-only boundary-transparency rule.

## Mode contract

The public interface presents an obvious two-position control:

```text
NORMAL MODE
<->
CHILD MODE
```

`NORMAL MODE` represents the general/adult-capable service experience.

`CHILD MODE` represents a materially different capability profile. It is not a visual theme or ordinary parental-control styling.

Critical authority rule:

```text
VISIBLE TOGGLE != AGE AUTHORITY
VISIBLE TOGGLE != LEGAL ELIGIBILITY
VISIBLE TOGGLE != PARENTAL CONSENT
```

In production, a toggle interaction may request a service-mode transition, but the runtime must evaluate verified eligibility, jurisdiction, guardian authority where required, policy version, and applicable law before changing authority.

## Child Mode protective baseline

```text
ALLOW / preserve when boundary is established:
- known friend/family messaging
- approved-friend collaboration
- learning/creative participation
- report and block

DENY / remove authority where applicable:
- unknown-person unsolicited direct contact
- public social exposure / broad discoverability
- public self-livestreaming under protective minor policy
- precise-location disclosure by default
- behavioral advertising / child profiling
- cross-service tracking
- engagement-optimized infinite recommender
```

The system must not treat parental approval of one bounded purpose as blanket permission for unrelated capabilities.

## Regulatory comparison — checked 2026-08-07

### United States

COPPA applies special privacy/parental-consent obligations for children under 13 on covered services. Engineering comparison: privacy-preserving age assurance, purpose limitation, parental authority where required, minimized age evidence, no child behavioral-advertising business model, and deletion/retention controls.

### Australia

Since 2025-12-10, covered age-restricted social-media platforms must take reasonable steps to prevent Australians under 16 from creating or keeping accounts. Self-declared birthdate alone is not the intended assurance model. Standalone messaging and online gaming are among excluded service categories, while social-media-style feature growth may change classification.

Engineering comparison: the child-facing service must be genuinely bounded rather than the same covered social-media account behind cosmetic controls.

### United Kingdom

The UK government announced an under-16 social-media ban on 2026-06-15 and announced restrictions targeting harmful features including livestreaming and strangers contacting children.

Engineering comparison: verified age/eligibility state, non-bypassable restricted capability, stranger-contact/livestream boundaries, and auditable evidence.

## Determinacy target

For the same verified age state, jurisdiction, guardian state, policy version, and capability request, the governed system should produce the same decision until a recorded policy revision changes the boundary.

A regulator or lawmaker should be able to test the service and confirm that unavailable authority remains unavailable even when the user requests it.

## Regulatory evidence chain target

```text
privacy-preserving age assurance
-> jurisdiction + age-band eligibility assertion
-> CHILD_MODE authority state
-> guardian authority where required
-> known-contact graph
-> capability request
-> policy evaluation
-> ALLOW / DENY / REVIEW_REQUIRED
-> execution only after ALLOW
-> immutable decision/mode receipt
-> abuse reporting / escalation
-> custody / reconstruction
-> redacted transparency projection
```

## Required distinction

```text
Normal/Child visible toggle: IMPLEMENTED AND VALIDATED IN DEMO
Child capability enforcement: REAL WITHIN DEMO
Public canonical route: VERIFIED
Public boundary/law comparison: IMPLEMENTED
Public append-only boundary history: IMPLEMENTED; machine observation pending SITE-0005
Authoritative production mode switching: NOT YET ESTABLISHED
Production age assurance: NOT YET ESTABLISHED
Production parental authorization: NOT YET ESTABLISHED
Production identity/contact verification: NOT YET ESTABLISHED
Production moderation/grooming detection: NOT YET ESTABLISHED
Production abuse escalation: NOT YET ESTABLISHED
Production cryptographic receipts/custody: NOT YET ESTABLISHED
```

## Cross-repository propagation rule

This Site work remains an implementation/communications projection. Once the production mode/eligibility contract becomes normative, pertinent semantics should be evaluated for propagation to the canonical Publisher, admissibility, guardian, and other consumers identified by live handoffs. Do not claim propagation until directly applied and verified.

## Next integration goal

After `SITE-0005` completes machine observation, the next directly related integration goal remains:

```text
CHILD-MODE-AUTHORITY-RUNTIME
privacy-preserving age assertion
+ non-bypassable mode authority
+ capability manifest
+ guardian/known-contact authority
+ immutable mode-transition receipts
```

Before implementation, locate the canonical runtime owner and applicable mirror handoff; do not create a competing implementation if another repository/session already owns overlapping runtime work.

## Completeness

```text
SITE-0002 demo: 100% implemented and validated
SITE-0003 public deployment: 100% verified
SITE-0004 governed mode toggle: 100% implemented and machine-validated
SITE-0005 boundary-history surface: implemented; repository-native validation pending
Public demo slice scaffolding/stubs: 0
Next production runtime goal: not yet implemented
```
