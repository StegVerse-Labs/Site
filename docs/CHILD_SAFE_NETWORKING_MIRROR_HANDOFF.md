# Child-Safe Networking Mirror Handoff

This file is the current task source of truth for governed child-safe networking in `StegVerse-Labs/Site`.

## Active goals

```text
SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT
Goal: make the validated child-safety governance sandbox publicly reachable and continuously verify the canonical deployed route.
State: COMPLETE — GitHub Pages built and canonical public-route verifier passed.

SITE-0004-CHILD-MODE-GOVERNANCE-TOGGLE
Goal: expose an obvious NORMAL MODE / CHILD MODE control while ensuring the protected mode is a separately enforced capability profile rather than a cosmetic preference.
State: COMPLETE — repository-native validator recorded MODE_TOGGLE=NORMAL_MODE_CHILD_MODE.
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
scripts/check_child_safety_demo.py
scripts/check_child_safety_public_deployment.py
.github/workflows/verify-child-safety-public-deployment.yml
docs/CHILD_SAFE_NETWORKING_MIRROR_HANDOFF.md
repository-task-observation.report.json
data/site-orchestration-state.json
```

## Completed evidence

```text
SITE-0001-CHILD-SAFE-NETWORKING: predecessor communications contract
SITE-0001-PERSONAL-DATA-CONTROL: COMPLETE
SITE-0002-CHILD-SAFETY-DEMO: COMPLETE
  CHILD_SAFETY_DEMO=PASS
  AGE_POLICY=JURISDICTION_AWARE
  NETWORK_REQUESTS=NONE
  PERSONAL_DATA_RETENTION=NONE
  AUTHORITY_GRANTED=false
  ACTIVATION_EFFECT=PUBLIC_INTERACTIVE_DEMO_ONLY

SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT: COMPLETE
  GitHub Pages repository status: built
  Pages build: 1137699817
  Pages build commit: ab4487bd96e1dbde364ed709f2f6da2f024058ea
  Canonical target: https://stegverse.org/child-safety-demo.html
  Verification workflow run: 31188562057
  Verification job: 92899242614
  Verification conclusion: success
  Verification artifact: 8997779738
  Artifact sha256: 3c9f20070fd2258fde6288aa647484591cbc8fc16ad2c37ba3cc6a2607dc4cd4

SITE-0004-CHILD-MODE-GOVERNANCE-TOGGLE: COMPLETE
  CHILD_SAFETY_DEMO=PASS
  MODE_TOGGLE=NORMAL_MODE_CHILD_MODE
  MODE_AUTHORITY=VERIFIED_POLICY_STATE_REQUIRED_IN_PRODUCTION
```

The red GitHub Pages deployment indicator observed in the user screenshot represented an earlier deployment state. It is superseded by the successful Pages build and canonical route verification above.

## Mode contract

The public interface presents an obvious two-position control:

```text
NORMAL MODE
<->
CHILD MODE
```

`NORMAL MODE` represents the general/adult-capable service experience.

`CHILD MODE` represents a materially different capability profile. It is not a visual theme and is not merely parental-control styling.

Critical authority rule:

```text
VISIBLE TOGGLE != AGE AUTHORITY
VISIBLE TOGGLE != LEGAL ELIGIBILITY
VISIBLE TOGGLE != PARENTAL CONSENT
```

In production, a toggle interaction may request a service-mode transition, but the runtime must evaluate verified eligibility, jurisdiction, guardian authority where required, policy version, and applicable law before changing authority.

A legally protected child must not be able to obtain Normal Mode by changing the visible switch, editing client state, changing a self-declared birthdate, using a VPN to alter apparent jurisdiction, replaying an old eligibility token, or using a parent setting to override a statutory prohibition. A denied attempt should create an inspectable transition receipt.

## Child Mode protective baseline

For protected age bands the child-facing capability graph preserves bounded positive networking while removing social-media risk capabilities.

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

The service must not treat parental approval of one bounded purpose as blanket permission for unrelated capabilities.

## Regulatory grounding — checked 2026-08-07

### United States

COPPA applies special privacy/parental-consent obligations for children under 13 on covered services. Engineering posture: privacy-preserving age assurance -> eligibility assertion -> COPPA child state where applicable -> parental consent for covered collection/use/disclosure where required -> no child behavioral-advertising business model -> minimize/delete age evidence when no longer necessary.

### Australia

Since 2025-12-10, covered age-restricted social-media platforms must take reasonable steps to prevent Australians under 16 from creating or keeping accounts. Self-declared birthdate alone is not the intended assurance model; bypass resistance and error review/appeal matter. Standalone messaging and online gaming are among excluded service categories, but a messaging service can become covered if social-media-style features alter its nature.

Engineering posture: do not present the same covered social-media account to an under-16 user behind a cosmetic switch; maintain a genuinely bounded child communication/collaboration capability profile; continuously reassess classification as features change.

### United Kingdom

The UK government announced an under-16 social-media ban on 2026-06-15 and announced restrictions targeting harmful features including livestreaming and strangers contacting children. Final implementing details must be tracked before any legal-certification claim.

Engineering posture: verified age/eligibility state; protected user cannot self-enable prohibited capability; stranger-contact/livestream restrictions represented in capability authority; auditable policy evidence retained.

## Strategic legal/product objective

The objective is not to evade a ban. No product design can guarantee how a legislature, regulator, or court will classify a future service.

The objective is to establish a technically inspectable third category between unrestricted social media and excluding children from networking:

```text
GENERAL / ADULT-CAPABLE SOCIAL SERVICE
or
AGE-GOVERNED CHILD COMMUNICATIONS + COLLABORATION SERVICE
```

For the second category to be credible, its significant purpose, feature set, incentives, data practices, contact graph, recommendation behavior, and runtime authority must actually differ from the risk-bearing social-media model. A regulator should be able to test a protected account and confirm that the service cannot provide prohibited capability even if the user asks for it.

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

For a protected user requesting Normal Mode:

```text
REQUEST_NORMAL_MODE
-> verify eligibility
-> threshold not met
-> DENY
-> receipt(policy version + reason + evidence reference)
```

## Public claim boundary

Allowed engineering claim:

> Child Mode is a separately governed capability profile designed around current child-safety regulatory principles. It prevents protected users from self-authorizing adult/social-media capabilities and provides inspectable evidence for sensitive capability decisions.

Do not claim:

> Child Mode guarantees exemption from social-media minimum-age laws.

Legal compliance/certification remains jurisdiction- and implementation-specific.

## Required distinction

```text
Normal/Child visible toggle: IMPLEMENTED AND VALIDATED IN DEMO
Child capability enforcement: REAL WITHIN DEMO
Public canonical route: VERIFIED
Authoritative production mode switching: NOT YET ESTABLISHED
Production age assurance: NOT YET ESTABLISHED
Production parental authorization: NOT YET ESTABLISHED
Production identity/contact verification: NOT YET ESTABLISHED
Production moderation/grooming detection: NOT YET ESTABLISHED
Production abuse escalation: NOT YET ESTABLISHED
Production cryptographic receipts/custody: NOT YET ESTABLISHED
Legal-compliance certification: NOT CLAIMED
```

## Cross-repository propagation rule

This Site work remains an implementation/communications projection and does not create canonical legal authority. Once the production mode/eligibility contract becomes normative, pertinent semantics should be evaluated for propagation to:

```text
StegVerse-Labs/Sit
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
stegguardian-wiki / canonical guardian repository
```

Do not claim propagation until directly applied and verified in those destinations.

## Next integration goal

With `SITE-0003` and `SITE-0004` complete, the next directly related integration goal is:

```text
CHILD-MODE-AUTHORITY-RUNTIME
privacy-preserving age assertion
+ non-bypassable mode authority
+ capability manifest
+ guardian/known-contact authority
+ immutable mode-transition receipts
```

Before implementation, locate the canonical runtime owner and applicable mirror handoff; do not create a competing implementation if another repository/session already owns the overlapping runtime.

## Completeness

```text
SITE-0002 demo: 100% implemented and validated
SITE-0003 public deployment: 100% verified
SITE-0004 governed mode toggle: 100% implemented and machine-validated
Public demo slice scaffolding/stubs: 0
Next production runtime goal: not yet implemented
```
