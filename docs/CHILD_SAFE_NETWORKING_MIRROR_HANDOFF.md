# Child-Safe Networking Mirror Handoff

This file is the current task source of truth for governed child-safe networking in `StegVerse-Labs/Site`.

## Active goals

```text
SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT
State: COMPLETE — GitHub Pages built and canonical public-route verifier passed.

SITE-0004-CHILD-MODE-GOVERNANCE-TOGGLE
State: COMPLETE — repository-native validator recorded MODE_TOGGLE=NORMAL_MODE_CHILD_MODE.

SITE-0005-CHILD-SAFETY-BOUNDARY-HISTORY
Goal: maintain a public current-boundary/law-comparison surface with preserved rationale and newest-first descending chronology.
State: repository-native completion observation pending/active.

SITE-0006-CHILD-MODE-DELIVERY-OPERATION
Goal: explain and validate how the same Child Mode boundary is delivered and enforced on child-dedicated devices, shared devices with managed age-governed accounts, and guardian-controlled temporary device use.
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
data/tasks/SITE-0006-CHILD-MODE-DELIVERY-OPERATION.json
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

The child-safety page is not a liability waiver. It is a public statement of the boundary as presently configured, a comparison with current/proposed child-safety law, and a demonstration that specific risk-bearing activity can be deterministically refused while beneficial networking remains available.

```text
If risk-bearing activity can be deterministically refused
while bounded communication, learning, creativity, collaboration,
and known-person networking remain available,
then capability governance is a plausible alternative that lawmakers
should evaluate alongside or in lieu of complete bans.
```

## Boundary-history rule

The public `Boundary Change Record` is preserved and rendered newest-first:

```text
new policy/law/technical change
-> retain all previous public entries
-> insert newest entry at the top
-> state exact boundary change
-> state rationale
-> update legal/policy comparison where relevant
-> validate NEWEST_FIRST_DESCENDING_CHRONOLOGY
```

Changes must not silently rewrite prior rationale. Git history remains the immutable source-level history; the public record is the readable chronology.

## Mode contract

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

The visible switch may request a transition; the effective runtime mode is determined by verified eligibility, jurisdiction, device/account state, guardian authority where applicable, policy version, and law.

## Methods of delivery and operation

### Child-dedicated device

A device manufactured, provisioned, or enrolled for a child may be hard-bound to Child Mode at a trusted device-management or OS/security layer.

```text
DEVICE_BOOT
-> DEVICE_CLASS=CHILD_DEDICATED
-> CHILD_MODE_REQUIRED
-> protected capability manifest
-> prohibited capabilities unavailable
```

Normal Mode is absent or requires authorized reprovisioning outside the child's authority.

### Shared device with managed accounts

A device used by multiple people derives its effective boundary from the active authenticated account.

```text
ACCOUNT_LOGIN
-> verified account identity
-> age/eligibility state
-> jurisdiction + policy
-> effective service mode
-> account-scoped capability manifest
```

An age-governed child account enters Child Mode automatically. An eligible adult account may receive Normal Mode. Account switching is an authority transition, not merely a UI preference.

### Guardian-controlled temporary Child Mode

An adult account holder may place a general-purpose device/session into Child Mode before handing it to a child.

Changing into or out of this guardian-controlled mode requires fresh account-holder security validation, such as biometric, passkey, hardware-backed credential, or equivalent authentication.

```text
REQUEST_MODE_CHANGE
-> fresh account-holder reauthentication
-> biometric / passkey / device credential
-> policy evaluation
-> ALLOW or DENY
-> mode-transition receipt
```

A child-visible switch alone cannot disable the boundary.

### Enforcement precedence

Mandatory legal or age-based restrictions cannot be weakened by an optional guardian toggle.

```text
LAW / JURISDICTION FLOOR
+ verified age eligibility
+ device policy
+ account policy
+ guardian-selected stricter controls
-> EFFECTIVE_CAPABILITY_BOUNDARY
```

A guardian may impose stricter protections on an otherwise eligible device/account, but cannot use the optional mode control to grant an ineligible child unrestricted Normal Mode.

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

For the same verified age state, jurisdiction, guardian state, device/account state, policy version, and capability request, the governed system should produce the same decision until a recorded policy revision changes the boundary.

A regulator or lawmaker should be able to test the service and confirm that unavailable authority remains unavailable even when the user requests it.

## Regulatory evidence chain target

```text
privacy-preserving age assurance
-> jurisdiction + age-band eligibility assertion
-> device/account policy resolution
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
Public newest-first boundary history: IMPLEMENTED
Delivery/operation models: IMPLEMENTED; machine observation pending SITE-0006
Authoritative production mode switching: NOT YET ESTABLISHED
Production age assurance: NOT YET ESTABLISHED
Production parental authorization: NOT YET ESTABLISHED
Production device/account binding: NOT YET ESTABLISHED
Production identity/contact verification: NOT YET ESTABLISHED
Production abuse escalation: NOT YET ESTABLISHED
Production cryptographic receipts/custody: NOT YET ESTABLISHED
```

## Cross-repository propagation rule

This Site work remains an implementation/communications projection. Once the production mode/eligibility contract becomes normative, pertinent semantics should be evaluated for propagation to the canonical Publisher, admissibility, guardian, and other consumers identified by live handoffs. Do not claim propagation until directly applied and verified.

## Next integration goal

After repository-native completion of SITE-0005 and SITE-0006, the next directly related integration goal remains:

```text
CHILD-MODE-AUTHORITY-RUNTIME
privacy-preserving age assertion
+ non-bypassable mode authority
+ device/account binding
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
SITE-0005 boundary-history surface: implemented; repository-native validation active/pending
SITE-0006 delivery/operation surface: implemented; repository-native validation pending
Public demo slice scaffolding/stubs: 0
Next production runtime goal: not yet implemented
```
