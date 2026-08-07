# Child Safety Regulatory Pilot — Evidence and Enforcement Model

Status: public engineering/policy proposal for regulator-authorized evaluation.
Checked: 2026-08-07.

## Purpose

This proposal does not ask a platform to ignore, route around, or self-exempt from a minimum-age law.

It defines a regulator-authorized temporary pilot model for testing whether deterministic capability governance can produce child-safety outcomes that are at least as observable and enforceable as a blanket account restriction while preserving bounded communication, learning, creativity, and known-person collaboration.

The central comparison is:

```text
BAN MODEL
prevent protected users from holding/accessing covered accounts
+ monitor whether platforms take required/reasonable steps
+ investigate systemic breaches
+ impose remedies/penalties

GOVERNED PILOT MODEL
verify protected eligibility
+ bind CHILD_MODE
+ deny prohibited interaction capabilities
+ deny optional data harvesting by default
+ record every sensitive decision
+ expose regulator-testable evidence
+ suspend pilot access if evidence fails
```

## Current regulatory semantics

### Australia

Australia's under-16 social-media account restriction is operative. Covered platforms must take reasonable steps to prevent under-16 Australians from creating or keeping accounts. eSafety monitors compliance, expects platforms to identify existing underage accounts, prevent new underage accounts, resist workarounds, provide review/error-correction paths, and can move from compliance monitoring to enforcement when evidence supports systemic breach findings.

This means enforcement is not simply `child seen on platform = violation`. The regulated object is whether the platform has taken the required/reasonable steps and whether those steps operate in practice.

### United Kingdom

The UK government has announced an under-16 social-media ban, with implementation expected in 2027. Ofcom is developing the age-assurance/enforcement approach and is assessing how highly effective age checks can support the restriction.

The important semantic distinction for a pilot is that the UK restriction is announced but not yet fully operative in the same sense as Australia's current account restriction. A pilot would therefore require an explicit lawful basis, authorization, sandbox, exemption, trial mechanism, or other regulator-approved route before protected users are admitted to any covered experience.

### United States / under-13 privacy baseline

COPPA is not a general nationwide social-media account ban. It regulates collection, use, and disclosure of personal information from children under 13 by covered operators and generally requires verifiable parental consent before such collection, subject to limited exceptions. For this pilot, the StegVerse posture is stricter than the minimum: optional harvesting remains denied by default for Child Mode.

## Why enforcement evidence matters

A blanket restriction can appear simple at the policy layer while still creating difficult evidence questions:

- Was the user reliably age-assured?
- Were existing underage accounts actually detected and deactivated?
- Can the user bypass controls with alternate accounts, false documents, VPNs, or device changes?
- What false-positive/false-negative rates occur?
- Can wrongly restricted users appeal?
- Does the platform collect additional child data while performing age assurance?
- How does the regulator prove systemic compliance or noncompliance?

A governed pilot should make those same questions inspectable and add a second class of evidence: whether prohibited capabilities and data access remain technically unavailable after the protected user is admitted to the bounded environment.

## Pilot admission rule

Protected users are not admitted merely because StegVerse believes the model is safer.

```text
REGULATOR / LAWFUL PILOT AUTHORITY
+ defined jurisdiction
+ defined age cohort
+ defined service/capability perimeter
+ defined duration or termination condition
+ approved age-assurance method
+ approved evidence/reporting schedule
=> PILOT_ADMISSIBLE
```

Without that authority, ordinary applicable minimum-age restrictions continue to govern.

## Zero-harvesting default

During the pilot:

```text
OPTIONAL_DATA_HARVESTING = DENY_BY_DEFAULT
```

No optional data extraction is permitted merely because the protected user has been admitted to the pilot.

Protected classes include, at minimum:

- contacts/address book;
- photos, videos and files;
- precise/background location;
- microphone/camera-derived data beyond the bounded foreground function;
- clipboard;
- browsing/application activity;
- advertising identifiers;
- cross-app/cross-service identifiers;
- behavioral profiles and inferred interests;
- nonessential telemetry.

Necessary operational/security processing must be separately classified, minimized, purpose-bound, retention-limited, and auditable. It must not become a hidden substitute for advertising or behavioral profiling.

## Regulator-verifiable evidence package

A pilot should produce evidence at five layers.

### 1. Eligibility evidence

```text
age-assurance event
jurisdiction
age-band / eligibility result
assurance method/class
policy version
appeal/review state
raw identity evidence retained? yes/no + retention rule
```

Regulator verifies that the account entered the correct policy state without requiring the child-facing service to retain unnecessary identity evidence.

### 2. Capability-denial evidence

A regulator receives test accounts or an equivalent controlled test harness and attempts defined prohibited transitions.

Expected examples:

```text
UNKNOWN_PERSON_DM -> DENY
PUBLIC_DISCOVERY -> DENY
PUBLIC_SELF_LIVESTREAM -> DENY where policy requires
ENGAGEMENT_RECOMMENDER -> DENY
BEHAVIORAL_AD_PROFILE -> DENY
PRECISE_LOCATION_DISCLOSURE -> DENY
NORMAL_MODE_REQUEST_BY_PROTECTED_USER -> DENY
```

Positive functions are tested separately:

```text
KNOWN_CONTACT_MESSAGE -> ALLOW when boundary established
APPROVED_COLLABORATION -> ALLOW
REPORT_BLOCK -> ALLOW
```

### 3. Data-egress evidence

The strongest pilot should make zero optional harvesting measurable rather than declarative.

Evidence can include:

```text
requested data class
requesting component/service
purpose
recipient
authority reference
decision
bytes/records released if ALLOW
retention window
receipt hash
```

For optional harvesting during Child Mode the expected default is:

```text
decision = DENY
released = 0
```

Regulator-approved technical instrumentation may verify that no undeclared telemetry/SDK path silently exports protected classes.

### 4. Boundary-change evidence

All changes to age thresholds, capability rules, data rules, assurance methods, or pilot scope are recorded publicly in newest-first descending chronology while preserving prior entries.

Each change records:

```text
change time
previous state
new state
rationale
legal/policy trigger if applicable
implementation commit/version
validation evidence
```

### 5. Outcome and incident evidence

The pilot should report privacy-preserving aggregate outcome metrics such as:

- age-assurance success/failure/review rates;
- false-positive/false-negative findings where measurable;
- attempted bypasses detected;
- denied prohibited transitions;
- allowed positive transitions;
- optional-data requests denied;
- data-authority exceptions granted by lawful authority;
- appeals and reversals;
- abuse reports and response times;
- policy/version changes;
- pilot suspensions or fail-closed events.

The metric system must not require building a behavioral surveillance profile of the children in order to prove safety.

## Fail-closed pilot rules

The pilot should automatically enter `SUSPENDED` or `REVIEW_REQUIRED` when required evidence cannot be produced.

Examples:

```text
age assurance unavailable -> no new protected-user admission
policy receipt chain broken -> sensitive transition DENY
unknown data egress detected -> affected data class DENY + incident
mandatory boundary test fails -> pilot access suspended for affected cohort/capability
regulator termination condition -> pilot disabled
```

## Independent verification

The pilot should support regulator or independent evaluator testing without requiring access to private child content.

Preferred evidence:

- deterministic test accounts;
- signed policy/capability manifests;
- redacted decision receipts;
- hashed data-egress receipts;
- reproducible boundary tests;
- public boundary history;
- aggregate privacy-preserving metrics;
- external test reports;
- incident/suspension receipts.

The goal is to verify the boundary, not surveil the child.

## Comparative policy question

A regulator can compare two models using evidence rather than rhetoric:

```text
BLANKET BAN / ACCOUNT RESTRICTION
How reliably is the protected user kept out?
How is platform compliance proven?
What bypass/appeal/error rates exist?
What child data is collected to enforce the restriction?

GOVERNED PILOT
How reliably are prohibited capabilities kept unavailable?
How is every denial/exception proven?
Does optional harvesting remain zero by default?
Can bounded positive communication remain available?
What happens when the evidence chain fails?
```

This does not presume the governed model should replace a ban. It creates a falsifiable way for government to determine whether it should.

## Pilot success criteria

A regulator-defined pilot can be considered successful only if its predeclared criteria are satisfied. Minimum proposed criteria:

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

No single marketing statement substitutes for these results.

## Strategic transparency advantage

A minimum-age law usually makes the platform responsible for excluding the protected user from a covered service because of harms associated with the service and its use.

This pilot makes a different proposition testable: the service operator can accept responsibility for proving which dangerous capabilities and data authorities do not exist for the protected user, while preserving beneficial participation.

That creates aligned incentives:

- government gains direct, inspectable enforcement evidence;
- families gain a bounded environment instead of an all-or-nothing choice;
- the platform cannot monetize optional child data while claiming safety;
- bad actors lose specific interaction authorities rather than the child losing every network benefit;
- policy changes remain publicly traceable.

The pilot therefore offers a measurable governance alternative without asserting that current minimum-age laws are unnecessary or invalid.