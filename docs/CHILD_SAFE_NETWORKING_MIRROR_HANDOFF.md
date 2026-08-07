# Child-Safe Networking Mirror Handoff

This file is the canonical task source of truth for governed child-safe networking in `StegVerse-Labs/Site`.

Repository: `StegVerse-Labs/Site`  
Branch: `main`

## Active goals

```text
SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT
State: COMPLETE — GitHub Pages built and canonical public-route verifier passed.

SITE-0004-CHILD-MODE-GOVERNANCE-TOGGLE
State: COMPLETE — repository-native validator recorded MODE_TOGGLE=NORMAL_MODE_CHILD_MODE.

SITE-0005-CHILD-SAFETY-BOUNDARY-HISTORY
Goal: current boundary/law comparison with preserved newest-first chronology.
State: repository-native completion observation pending/active.

SITE-0006-CHILD-MODE-DELIVERY-OPERATION
Goal: child-dedicated devices, shared age-governed accounts, guardian-controlled temporary use.
State: repository-native validation pending/active.

SITE-0007-CHILD-MODE-DATA-AUTHORITY
Goal: protect device/account data from optional harvesting unless a legally authorized, purpose-scoped path exists.
State: repository-native validation pending/active.

SITE-0008-CHILD-SAFETY-REGULATORY-PILOT
Goal: provide a regulator-testable temporary pilot model comparing blanket account restrictions with deterministic Child Mode capability and zero-optional-data-harvesting enforcement.
State: READY_FOR_MACHINE_COMPLETION_CHECK.
```

## Authoritative files

```text
child-safety-demo.html
child-mode-data-protection.html
child-safety-regulatory-pilot.html
children-safe-networking.html
docs/CHILD_MODE_REGULATORY_GOVERNANCE.md
docs/CHILD_MODE_DATA_AUTHORITY.md
docs/CHILD_SAFETY_REGULATORY_PILOT.md
data/tasks/SITE-0002-CHILD-SAFETY-DEMO.json
data/tasks/SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT.json
data/tasks/SITE-0004-CHILD-MODE-GOVERNANCE-TOGGLE.json
data/tasks/SITE-0005-CHILD-SAFETY-BOUNDARY-HISTORY.json
data/tasks/SITE-0006-CHILD-MODE-DELIVERY-OPERATION.json
data/tasks/SITE-0007-CHILD-MODE-DATA-AUTHORITY.json
data/tasks/SITE-0008-CHILD-SAFETY-REGULATORY-PILOT.json
scripts/check_child_safety_demo.py
scripts/check_child_mode_data_authority.py
scripts/check_child_safety_regulatory_pilot.py
scripts/check_child_safety_public_deployment.py
.github/workflows/verify-child-safety-public-deployment.yml
repository-task-observation.report.json
data/site-orchestration-state.json
```

## Completed predecessor evidence

```text
SITE-0001-PERSONAL-DATA-CONTROL: COMPLETE
SITE-0002-CHILD-SAFETY-DEMO: COMPLETE
SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT: COMPLETE
  Canonical target: https://stegverse.org/child-safety-demo.html
  Verification workflow run: 31188562057
  Verification conclusion: success
SITE-0004-CHILD-MODE-GOVERNANCE-TOGGLE: COMPLETE
  CHILD_SAFETY_DEMO=PASS
  MODE_TOGGLE=NORMAL_MODE_CHILD_MODE
  MODE_AUTHORITY=VERIFIED_POLICY_STATE_REQUIRED_IN_PRODUCTION
```

## Governing public purpose

These public child-safety surfaces are boundary specifications, law-comparison records, and testable evidence models; they are not liability waivers.

```text
If risk-bearing activity can be deterministically refused,
optional child-data harvesting can be zero by default,
and positive bounded communication remains available,
then capability governance is a falsifiable alternative that lawmakers
can test alongside or in lieu of complete social-network exclusion.
```

## Current regulatory semantics — checked 2026-08-07

### Australia

Australia's under-16 minimum-age account restriction is operative. Covered age-restricted social-media platforms must take reasonable steps to prevent under-16 Australians from creating or keeping accounts. eSafety monitors compliance, expects existing-account detection, new-account prevention, bypass resistance, review/error correction, and can move from monitoring to enforcement where evidence supports systemic breach findings.

### United Kingdom

The UK government has announced an under-16 social-media ban, with implementation expected in 2027. Ofcom is assessing how highly effective age assurance should work in practice. This is materially different from Australia's already-operative account restriction. Protected-user admission to a UK pilot would require an explicit lawful pilot/sandbox/authorization mechanism rather than unilateral platform self-exemption.

### United States

COPPA is not a general nationwide social-media account ban. It regulates covered collection/use/disclosure of personal information from children under 13 and generally requires verifiable parental consent before that processing, subject to exceptions. StegVerse Child Mode is deliberately stricter for optional harvesting.

## Mode and authority contract

```text
NORMAL MODE
<->
CHILD MODE
```

Child Mode is a materially different capability and data-authority profile.

```text
VISIBLE TOGGLE != AGE AUTHORITY
VISIBLE TOGGLE != LEGAL ELIGIBILITY
VISIBLE TOGGLE != PARENTAL CONSENT
VISIBLE TOGGLE != DATA-HARVESTING AUTHORITY
```

Effective runtime authority is determined by verified eligibility, jurisdiction, device/account state, guardian authority where applicable, policy version, and law.

## Delivery and operation

### Child-dedicated device

```text
DEVICE_BOOT
-> DEVICE_CLASS=CHILD_DEDICATED
-> CHILD_MODE_REQUIRED
-> protected capability + data-authority manifest
-> prohibited capabilities and optional harvesting unavailable
```

### Shared managed device

```text
ACCOUNT_LOGIN
-> verified account identity
-> age/eligibility state
-> jurisdiction + policy
-> effective service mode
-> account-scoped capability + data-authority manifest
```

### Guardian-controlled temporary Child Mode

```text
REQUEST_MODE_CHANGE
-> fresh account-holder reauthentication
-> biometric/passkey/hardware-backed credential
-> policy evaluation
-> ALLOW or DENY
-> mode-transition receipt
```

Mandatory legal/age restrictions cannot be weakened by an optional guardian toggle.

## Data-authority boundary

```text
CHILD_MODE
-> OPTIONAL_DATA_HARVESTING = DENY_BY_DEFAULT
-> child-visible click/tap/toggle is not sufficient harvesting authority
-> consent-dependent collection requires legally authorized authority
-> guardian/authorized-adult approval is purpose-scoped
-> approval for one purpose does not authorize unrelated collection
-> collection/use/disclosure decisions produce receipts
```

Protected classes include contacts/address book, photos/videos/files, precise/background location, microphone/camera-derived data outside a bounded foreground function, clipboard, browsing/application activity, advertising identifiers, cross-app/cross-service identifiers, behavioral profiles/inferred interests, and nonessential telemetry.

StegVerse deliberately does not encode the universal legal proposition that every minor lacks consent capacity in every jurisdiction. Instead, Child Mode adopts the stricter product rule that optional harvesting remains denied unless an authorized policy path establishes sufficient authority for the exact data, purpose, recipient, and retention window.

## Regulator-verifiable temporary pilot

The pilot is not a self-exemption from a ban.

```text
REGULATOR / LAWFUL PILOT AUTHORITY
+ defined jurisdiction
+ defined protected age cohort
+ defined service/capability perimeter
+ defined duration / termination condition
+ approved age-assurance method
+ approved evidence/reporting schedule
=> PILOT_ADMISSIBLE
```

Without that authority, ordinary applicable minimum-age restrictions continue to govern.

### Five-layer evidence package

```text
1. ELIGIBILITY EVIDENCE
   age assurance + jurisdiction + age band + policy version + appeal state

2. CAPABILITY EVIDENCE
   regulator-testable prohibited and positive transitions

3. DATA-EGRESS EVIDENCE
   data class + requester + purpose + recipient + authority + decision + released amount + retention + receipt hash

4. BOUNDARY-CHANGE EVIDENCE
   newest-first public policy history with rationale + version/commit + validation evidence

5. OUTCOME / INCIDENT EVIDENCE
   privacy-preserving aggregate bypass, appeal, denial, positive-use, data-request, incident and suspension metrics
```

The pilot should verify the boundary without surveilling the child.

### Expected prohibited-transition tests

```text
UNKNOWN_PERSON_DM -> DENY
PUBLIC_DISCOVERY -> DENY
PUBLIC_SELF_LIVESTREAM -> DENY where policy requires
ENGAGEMENT_RECOMMENDER -> DENY
BEHAVIORAL_AD_PROFILE -> DENY
PRECISE_LOCATION_DISCLOSURE -> DENY
NORMAL_MODE_REQUEST_BY_PROTECTED_USER -> DENY
```

Positive controls:

```text
KNOWN_CONTACT_MESSAGE -> ALLOW when boundary established
APPROVED_COLLABORATION -> ALLOW
REPORT_BLOCK -> ALLOW
```

### Zero-harvesting pilot rule

```text
OPTIONAL_DATA_HARVESTING = ZERO_BY_DEFAULT
UNDECLARED_DATA_EGRESS = NONE
```

Necessary operational/security processing must be separately classified, minimized, purpose-bound, retention-limited and auditable. It cannot become a hidden behavioral-profiling or advertising channel.

### Fail-closed pilot behavior

```text
age assurance unavailable -> no new protected-user admission
policy/receipt chain broken -> sensitive transition DENY
unknown data egress detected -> affected data class DENY + incident
mandatory boundary test fails -> affected pilot access SUSPENDED
regulator termination condition -> pilot disabled
```

### Proposed pilot success criteria

```text
AGE_STATE_ENFORCEMENT = PASS
PROHIBITED_CAPABILITY_TESTS = PASS
NORMAL_MODE_BYPASS = DENY
OPTIONAL_DATA_HARVESTING = ZERO_BY_DEFAULT
UNDECLARED_DATA_EGRESS = NONE
APPEAL_PATH = OPERATIONAL
BOUNDARY_HISTORY = COMPLETE
RECEIPT_RECONSTRUCTION = PASS
FAIL_CLOSED_BEHAVIOR = PASS
```

No marketing claim substitutes for these results.

## Strategic transparency advantage

The current minimum-age model puts responsibility on the platform to keep protected users out of a covered service. The governed pilot asks the platform to prove, continuously, that specified dangerous interaction authorities and data authorities do not exist for the protected user.

This does not shift responsibility away from the platform. It makes responsibility more granular and observable:

```text
prove what the system cannot do
+ prove what data it cannot take
+ prove every allowed exception
+ prove what happens when evidence fails
```

That aligns interests in both directions: government gets inspectable enforcement evidence, families preserve bounded positive participation, the platform cannot monetize optional child data while claiming safety, and bad actors lose specific interaction authorities instead of the child losing every network benefit.

## Boundary-history rule

All public histories preserve prior entries and render newest-first in descending chronological order. Every later threshold, capability, data, assurance, or pilot-scope change records its rationale and implementation/validation evidence.

## Required distinction

```text
Normal/Child visible toggle: IMPLEMENTED AND VALIDATED IN DEMO
Public canonical Child Mode route: VERIFIED
Public boundary/law comparison: IMPLEMENTED
Public newest-first boundary history: IMPLEMENTED
Delivery/operation models: IMPLEMENTED; machine observation pending/active
Public data-authority boundary: IMPLEMENTED; machine observation pending/active
Public regulatory pilot model: IMPLEMENTED; machine observation pending SITE-0008
Production device-level enforcement: NOT YET ESTABLISHED
Production regulator-authorized pilot: NOT ACTIVATED
Production age assurance: NOT YET ESTABLISHED
Production cryptographic data/capability receipts and custody: NOT YET ESTABLISHED
```

## Cross-repository propagation

This Site work is currently implementation/communications and pilot-evidence projection. Once the runtime contract becomes normative, semantics must be evaluated for propagation to canonical Publisher, admissibility, guardian, master-records, and other consumers identified by live handoffs. Do not claim propagation until directly applied and verified.

## Next integration goal

After repository-native completion of SITE-0005 through SITE-0008, the next runtime goal remains:

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
+ regulator-verifiable pilot evidence export
```

Before implementation, locate the canonical runtime owner and applicable mirror handoff; do not create a competing runtime implementation.

## Completeness

```text
SITE-0002 demo: 100% implemented and validated
SITE-0003 public deployment: 100% verified
SITE-0004 governed mode toggle: 100% implemented and machine-validated
SITE-0005 boundary history: implemented; observation active/pending
SITE-0006 delivery/operation: implemented; observation active/pending
SITE-0007 data authority: implemented; observation active/pending
SITE-0008 regulatory pilot: implemented; observation pending
Public child-safety/pilot slice scaffolding or stubs: 0 known
Production enforcement/pilot activation: not yet implemented/authorized
```
