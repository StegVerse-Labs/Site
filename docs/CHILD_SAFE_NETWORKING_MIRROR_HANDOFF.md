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
Goal: explain and validate delivery on child-dedicated devices, shared managed accounts, and guardian-controlled temporary device use.
State: repository-native validation pending/active.

SITE-0007-CHILD-MODE-DATA-AUTHORITY
Goal: protect device/account data from optional harvesting in Child Mode unless a legally authorized, purpose-scoped consent path exists.
State: READY_FOR_MACHINE_COMPLETION_CHECK.
```

Repository: `StegVerse-Labs/Site`
Branch: `main`

## Authoritative files

```text
child-safety-demo.html
child-mode-data-protection.html
children-safe-networking.html
docs/CHILD_MODE_REGULATORY_GOVERNANCE.md
docs/CHILD_MODE_DATA_AUTHORITY.md
data/tasks/SITE-0002-CHILD-SAFETY-DEMO.json
data/tasks/SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT.json
data/tasks/SITE-0004-CHILD-MODE-GOVERNANCE-TOGGLE.json
data/tasks/SITE-0005-CHILD-SAFETY-BOUNDARY-HISTORY.json
data/tasks/SITE-0006-CHILD-MODE-DELIVERY-OPERATION.json
data/tasks/SITE-0007-CHILD-MODE-DATA-AUTHORITY.json
scripts/check_child_safety_demo.py
scripts/check_child_mode_data_authority.py
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
  Canonical target: https://stegverse.org/child-safety-demo.html
  Verification workflow run: 31188562057
  Verification conclusion: success

SITE-0004-CHILD-MODE-GOVERNANCE-TOGGLE: COMPLETE
  CHILD_SAFETY_DEMO=PASS
  MODE_TOGGLE=NORMAL_MODE_CHILD_MODE
  MODE_AUTHORITY=VERIFIED_POLICY_STATE_REQUIRED_IN_PRODUCTION
```

## Public purpose

The child-safety surfaces are public boundary specifications and law-comparison records, not liability waivers. They demonstrate that risk-bearing activity and data authority can be deterministically constrained while beneficial digital participation remains available.

```text
If risk-bearing activity can be deterministically refused
and optional data harvesting can be denied by default
while bounded communication, learning, creativity, collaboration,
and known-person networking remain available,
then capability governance is a plausible alternative that lawmakers
should evaluate alongside or in lieu of complete bans.
```

## Boundary-history rule

Public history is preserved and rendered newest-first:

```text
new policy/law/technical change
-> retain previous entries
-> insert newest entry at the top
-> state exact boundary change
-> state rationale
-> update law/policy comparison where relevant
-> validate NEWEST_FIRST_DESCENDING_CHRONOLOGY
```

## Mode contract

```text
NORMAL MODE
<->
CHILD MODE
```

`CHILD MODE` is a materially different capability and data-authority profile, not a visual theme.

```text
VISIBLE TOGGLE != AGE AUTHORITY
VISIBLE TOGGLE != LEGAL ELIGIBILITY
VISIBLE TOGGLE != PARENTAL CONSENT
VISIBLE TOGGLE != DATA-HARVESTING AUTHORITY
```

The visible switch may request a transition; effective runtime authority is determined by verified eligibility, jurisdiction, device/account state, guardian authority where applicable, policy version, and law.

## Methods of delivery and operation

### Child-dedicated device

```text
DEVICE_BOOT
-> DEVICE_CLASS=CHILD_DEDICATED
-> CHILD_MODE_REQUIRED
-> protected capability + data-authority manifest
-> prohibited capabilities and optional harvesting unavailable
```

Normal Mode is absent or requires authorized reprovisioning outside the child's authority.

### Shared device with managed accounts

```text
ACCOUNT_LOGIN
-> verified account identity
-> age/eligibility state
-> jurisdiction + policy
-> effective service mode
-> account-scoped capability + data-authority manifest
```

An age-governed child account enters Child Mode automatically. Account switching is an authority transition.

### Guardian-controlled temporary Child Mode

Changing into or out of guardian-controlled Child Mode requires fresh account-holder security validation such as biometric, passkey, hardware-backed credential, or equivalent authentication.

```text
REQUEST_MODE_CHANGE
-> fresh account-holder reauthentication
-> policy evaluation
-> ALLOW or DENY
-> mode-transition receipt
```

Mandatory legal or age-based restrictions cannot be weakened by an optional guardian toggle.

## Child Mode data-authority boundary

Child Mode protects the device data plane itself.

```text
CHILD_MODE
-> OPTIONAL_DATA_HARVESTING = DENY_BY_DEFAULT
-> child-visible click/tap/toggle is not sufficient harvesting authority
-> consent-dependent collection requires legally authorized consent path
-> guardian/authorized-adult approval is purpose-scoped
-> approval for one purpose does not authorize unrelated collection
-> collection/use/disclosure decisions should produce receipts
```

Protected data classes include contacts/address book, photos/videos/files, precise/background location, microphone/camera-derived data outside a bounded foreground function, clipboard, browsing/application activity, advertising identifiers, cross-app/cross-service identifiers, behavioral profiles/inferred interests, and nonessential telemetry.

A guardian approval for one bounded purpose is not blanket permission. Example: approving microphone access for a live music lesson does not authorize contacts, location, advertising profiles, cross-service tracking, or unrelated retention.

## Consent-law nuance — checked 2026-08-07

Do not encode the universal claim that every person under 18 lacks legal capacity to consent in every jurisdiction.

### United States

COPPA generally requires verifiable parental consent before covered operators collect, use, or disclose personal information from children under 13, subject to limited exceptions. An under-13 child cannot create that parental authority by tapping an in-app consent control.

### United Kingdom

Where consent is the lawful basis for an information-society service, children 13+ can generally consent for themselves; below 13, parental-responsibility authorization is generally required, subject to limited exceptions. Other lawful bases can sometimes apply.

### Australia

Privacy law does not specify one universal consent age. Capacity depends on maturity and understanding; OAIC guidance treats capacity contextually.

### StegVerse product posture

Child Mode may be stricter than the legal minimum: optional harvesting remains denied unless an authorized policy path establishes sufficient authority for the exact data, exact purpose, recipient, and retention window.

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
- optional device-data harvesting without authorized purpose-scoped authority
```

## Determinacy target

For the same verified age state, jurisdiction, guardian state, device/account state, policy version, capability request, and data request, the governed system should produce the same decision until a recorded policy revision changes the boundary.

## Regulatory evidence chain target

```text
privacy-preserving age assurance
-> jurisdiction + age-band eligibility assertion
-> device/account policy resolution
-> CHILD_MODE authority state
-> guardian authority where required
-> capability request OR data-access request
-> purpose + recipient + retention scope
-> policy evaluation
-> ALLOW / DENY / REVIEW_REQUIRED
-> execution only after ALLOW
-> immutable decision/mode/data receipt
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
Public data-authority boundary: IMPLEMENTED; machine observation pending SITE-0007
Production device-level data enforcement: NOT YET ESTABLISHED
Production age assurance: NOT YET ESTABLISHED
Production parental/guardian authorization: NOT YET ESTABLISHED
Production cryptographic data-access receipts/custody: NOT YET ESTABLISHED
```

## Cross-repository propagation rule

This Site work remains an implementation/communications projection. Once the production mode/eligibility/data-authority contract becomes normative, pertinent semantics should be evaluated for propagation to canonical Publisher, admissibility, guardian, master-records, and other consumers identified by live handoffs. Do not claim propagation until directly applied and verified.

## Next integration goal

After repository-native completion of SITE-0005, SITE-0006, and SITE-0007, the next directly related integration goal remains:

```text
CHILD-MODE-AUTHORITY-RUNTIME
privacy-preserving age assertion
+ non-bypassable mode authority
+ device/account binding
+ capability manifest
+ data-authority manifest
+ guardian/known-contact authority
+ purpose-scoped consent authority
+ immutable mode/capability/data-access receipts
```

Before implementation, locate the canonical runtime owner and applicable mirror handoff; do not create a competing implementation if another repository/session already owns overlapping runtime work.

## Completeness

```text
SITE-0002 demo: 100% implemented and validated
SITE-0003 public deployment: 100% verified
SITE-0004 governed mode toggle: 100% implemented and machine-validated
SITE-0005 boundary-history surface: implemented; repository-native validation active/pending
SITE-0006 delivery/operation surface: implemented; repository-native validation active/pending
SITE-0007 data-authority surface: implemented; repository-native validation pending
Public demo/data-authority slice scaffolding/stubs: 0 known
Next production runtime goal: not yet implemented
```
