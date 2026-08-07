# Child Mode Regulatory Governance Matrix

Status: live engineering/policy boundary record and law-comparison surface.
Checked: 2026-08-07.

## Purpose

This record is not a liability waiver. It states the child-safety boundaries as presently configured, compares those boundaries with current and proposed law, and preserves the rationale for later adjustments.

Its public purpose is to demonstrate that child-safety controls can be deterministic at the activity/capability boundary and therefore deserve serious consideration as an alternative to blanket exclusion from social networking.

The governing question is not only whether a child may enter a service. It is also which capabilities the service may exercise for that child.

## Core product rule

The visible `NORMAL MODE / CHILD MODE` toggle is a user-facing declaration of service state. It is not the source of legal authority.

Production mode selection must be derived from an authoritative eligibility state such as privacy-preserving age assurance, jurisdiction, parental/guardian authority where required, and service policy. A protected child must not be able to acquire adult capabilities by changing a client-side toggle, editing local state, changing a birthdate field, using a VPN, or otherwise bypassing policy.

The UI may allow a user to request a mode transition. The runtime decides whether that transition is admissible.

## Regulatory design objective

The objective is to make the child-facing service materially different from the risk-bearing service class that regulators are restricting, and to make those differences inspectable, testable, enforceable, and publicly revisable.

This creates a technically inspectable third option between unrestricted social media and complete exclusion from networking:

```text
GENERAL / ADULT-CAPABLE SOCIAL SERVICE
or
AGE-GOVERNED CHILD COMMUNICATIONS + COLLABORATION SERVICE
```

The proposition to test publicly is straightforward: if the risk-bearing capabilities can be made deterministically unavailable while socially valuable communication remains available, that governed boundary is a plausible policy solution that should be evaluated alongside or in lieu of complete bans.

## Mode architecture

### Normal Mode

Represents the general/adult-capable service experience. Eligibility for Normal Mode is an authority decision, not a preference when the user is legally protected by an age restriction.

### Child Mode

Child Mode is a separate capability profile, not a visual theme. Its default authority should be restricted to purpose-bound, known-contact, safety-preserving functions.

Minimum baseline:

- verified or otherwise legally sufficient age/eligibility state;
- jurisdiction-aware policy;
- known-contact or guardian-approved relationship graph for direct interpersonal communication;
- no unsolicited stranger direct contact for protected age bands;
- no public social graph or public discoverability for protected age bands;
- no engagement-optimized infinite recommender for protected age bands;
- no behavioral advertising or child profiling;
- no precise-location disclosure by default;
- no public self-livestreaming for minors under the StegVerse protective baseline;
- safety reporting and blocking always available;
- clear appeal/review path for incorrect age or mode classification;
- anti-bypass controls;
- data minimization and purpose limitation for age-assurance evidence;
- auditable receipts for mode changes and sensitive capability decisions.

## Australia — operative law

As of 10 December 2025, covered age-restricted social-media platforms must take reasonable steps to prevent Australians under 16 from creating or keeping accounts.

Current eSafety guidance indicates covered-service characteristics include a significant purpose of online social interaction, user linking/interactions, user posting, and a recommender and/or logged-in feature. Standalone messaging and online gaming are among excluded service types, but a messaging service can become covered if social-media-style features change its nature.

Engineering implications:

1. A `Child Mode` toggle alone does not satisfy the obligation if the underlying product remains a covered age-restricted social-media account.
2. Self-declared birthdate alone is not a sufficient age-assurance strategy.
3. The system should detect/prevent common workarounds and provide review/appeal for errors.
4. Under-16 users in Australia should not receive an account that is functionally the same covered social-media service with cosmetic restrictions.
5. The strongest architecture is a genuinely bounded child communications/collaboration service profile whose significant purpose and enabled features remain outside the risk-bearing social-media pattern where the law and regulator permit that classification.
6. Product evolution must be continuously reassessed because adding public posting, broad social discovery, recommender feeds, or other social-media-style capabilities can change classification.

## United States — COPPA baseline

COPPA applies to operators of child-directed services under 13 and general-audience services with actual knowledge that they collect personal information from a child under 13.

Production implications for a known under-13 user include notice, verifiable parental consent where required before collection/use/disclosure, data minimization, security, deletion/retention controls, and the updated COPPA requirements concerning third-party disclosure/targeted advertising.

The FTC's 2026 age-verification enforcement policy supports age-verification processing without prior parental consent in specified circumstances when the information is used solely for age determination, retained only as necessary, protected, appropriately disclosed, and handled by suitable providers.

Engineering implications:

- age-assurance evidence should be isolated from advertising and general product analytics;
- age-verification data should be deleted promptly when no longer necessary;
- a child-mode decision should consume an eligibility assertion rather than broadly expose raw identity evidence;
- targeted advertising and unrelated third-party disclosure should not be part of the Child Mode business model;
- parental consent must not be treated as a blanket grant of unrelated capabilities.

## United Kingdom — announced under-16 direction plus existing Online Safety duties

The UK government announced an under-16 social-media ban on 15 June 2026. Its public fact sheet also states that harmful features such as livestreaming and strangers contacting children will be restricted for under-18s.

The final implementing law/rules must be tracked as they change.

Engineering implications now:

- maintain reliable age/eligibility state;
- prevent protected users from obtaining prohibited social-media capability through client-side switching;
- disable stranger contact and public self-livestreaming where the applicable rule requires it;
- preserve bounded communication/collaboration surfaces separately from public social-media behavior;
- retain evidence showing what capability existed for which age state and why.

## Determinacy standard

A regulator, policymaker, parent, or user should be able to test the same protected account repeatedly and obtain the same policy result from the same inputs.

Expected evidence:

```text
verified eligibility assertion
-> CHILD_MODE authority state
-> capability manifest
-> known-contact boundary
-> no public discovery authority
-> no stranger-DM authority
-> no child behavioral-advertising authority
-> no engagement-recommender authority
-> no precise-location disclosure authority
-> age-appropriate livestream restriction
-> report/block authority retained
-> transition receipt
```

Attempting to switch a protected child to Normal Mode should produce:

```text
REQUEST_NORMAL_MODE
-> verify eligibility
-> if legal/policy threshold not met: DENY
-> retain reason + policy version + evidence reference in receipt
```

The control therefore has three conceptual states even if the visual UI remains a simple two-position switch:

```text
NORMAL_MODE_ACTIVE
CHILD_MODE_ACTIVE
NORMAL_MODE_REQUEST_DENIED_BY_POLICY
```

## Measures that would make the boundary non-determinant

The following would undermine the proposition that Child Mode is a substantive governance alternative:

- child chooses their own unverified age and immediately unlocks Normal Mode;
- parent can universally override statutory restrictions;
- same public feed remains available with only content filtering changed;
- same public follower/discovery graph remains enabled;
- stranger messaging remains available after a warning;
- targeted advertising remains active;
- engagement recommender remains active but is labeled `safer`;
- precise location remains collected despite not being needed;
- hidden product features contradict the public Child Mode claims;
- no evidence of anti-bypass controls;
- no review path for erroneous age classification;
- no capability/version receipts for audits.

## Public comparison posture

The public page should show, for each material boundary:

```text
CURRENT BOUNDARY
LEGAL / POLICY RELEVANCE
DETERMINISTIC TEST
LATEST CHANGE + RATIONALE
```

This is a living comparison record. When laws, proposed laws, regulator guidance, or StegVerse policy change, the operative boundary may change as well. Those changes should be appended rather than silently replacing prior rationale.

## Boundary change record

Append-only. New entries go below prior entries.

### 2026-08-07 — Initial bounded-networking profile

Change: established Normal Mode / Child Mode distinction and a protected capability profile that removes stranger contact, public exposure, behavioral profiling, unnecessary precise-location disclosure, public self-livestreaming under the protective minor policy, and engagement-optimized recommendation while preserving bounded communication and collaboration.

Rationale: demonstrate that activity boundaries can be deterministic and testable and therefore constitute a plausible governance alternative that lawmakers should consider alongside or in lieu of complete bans.

### 2026-08-07 — Boundary transparency rule

Change: established an append-only public record of subsequent boundary adjustments and their rationale; reframed the public language as boundary-state disclosure and legal comparison rather than waiver-oriented language.

Rationale: preserve a visible history of what changed, why it changed, and how the governing boundary evolved.