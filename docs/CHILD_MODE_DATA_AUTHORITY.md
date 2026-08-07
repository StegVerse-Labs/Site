# Child Mode Data Authority Contract

Status: public engineering boundary and law-comparison record.
Checked: 2026-08-07.

## Governing rule

Child Mode protects not only interaction capabilities but the device data plane itself.

```text
CHILD_MODE
-> OPTIONAL_DATA_HARVESTING = DENY_BY_DEFAULT
-> consent-dependent collection requires a legally authorized consent path
-> guardian/authorized-adult approval is purpose-scoped
-> approval for one purpose does not authorize unrelated collection
-> every collection decision should be receipted
```

A child-visible click, tap, toggle, or acceptance flow is never by itself treated as sufficient authority for optional device-data harvesting in Child Mode.

This is a product-governance rule. It can be stricter than a jurisdiction's minimum legal threshold.

## Protected data classes

The default protected set includes:

- contacts and address book;
- photos, videos and files;
- precise and background location;
- microphone and camera-derived data outside bounded foreground function;
- clipboard contents;
- browsing and application activity;
- advertising identifiers;
- cross-app and cross-service identifiers;
- behavioral profiles and inferred interests;
- telemetry not required for core operation, security, safety, or another documented lawful purpose.

The boundary distinguishes necessary, purpose-bound operation from optional harvesting.

## Consent authority

Do not encode the universal proposition that every person under 18 lacks legal capacity to consent in every jurisdiction.

Instead:

```text
protected-age account
-> identify jurisdiction and age/capacity rule
-> identify lawful basis and whether consent is available
-> identify who has authority to provide that consent
-> if guardian/parent authorization is required, child action cannot substitute
-> bind any authorization to exact data + purpose + recipient + retention period
-> deny unrelated collection/use/disclosure
```

### United States

For covered operators, COPPA generally requires verifiable parental consent before collecting, using, or disclosing personal information from children under 13, subject to specific exceptions. The FTC also recognizes device identifiers and similar persistent identifiers as personal information under COPPA.

Engineering posture: an under-13 child cannot create the required parental authority by tapping an in-app consent control.

### United Kingdom

When an information-society service relies on consent as its lawful basis, children 13 or older can generally give their own consent; below 13, consent generally must come from a person with parental responsibility, subject to limited exceptions. Other lawful bases may sometimes apply.

Engineering posture: Child Mode may impose a stricter rule and refuse optional harvesting even where the child could legally consent.

### Australia

The Privacy Act does not define one universal age of privacy consent. Capacity depends on whether the individual can understand what is proposed; maturity and circumstances matter. OAIC guidance says an organisation may often assume a person over 15 has capacity where individual assessment is impractical, unless there is reason for doubt.

Engineering posture: optional harvesting remains unavailable in Child Mode unless a valid policy path establishes sufficient authority.

## Purpose-bound guardian authorization

Guardian authorization must not become blanket permission.

Example:

```text
parent authenticates
-> approves microphone
-> purpose = live music lesson
-> recipient = lesson service
-> retention = session only
-> ALLOW microphone for that bounded session

contacts = DENY
location = DENY
advertising profile = DENY
cross-service tracking = DENY
```

## Device and account enforcement

### Child-dedicated device

The protected data policy can be hard-bound through device management, OS policy, secure storage, trusted execution, application entitlements, or equivalent controls.

### Shared device

The active authenticated child account automatically invokes the protected data boundary. Apps must not inherit an adult account's broader data authority merely because the physical device is shared.

### Guardian-controlled temporary Child Mode

Fresh account-holder reauthentication is required to enter or leave the guardian-controlled protected state. Leaving Child Mode does not retroactively authorize collection that was denied while Child Mode was active.

## Determinacy tests

```text
child app requests contacts for advertising
-> DENY

child taps allow tracking
-> DENY as harvesting authority

parent approves microphone for bounded live lesson
-> ALLOW microphone for that purpose/session only
-> unrelated reuse remains DENY

service requests persistent device identifier for cross-service profiling
-> DENY
```

## Policy objective

The child should be able to use a network or device without the act of participation turning the device itself into a harvestable data source.

This strengthens the policy alternative to blanket bans: safety is enforced through a deterministic authority boundary on both activity and data, rather than by excluding the child from digital participation.

## Boundary change record

Newest-first descending chronology.

### 2026-08-07 — Device-data harvesting boundary

Change: Child Mode now explicitly denies optional device-data harvesting by default and rejects child interaction as sufficient authority for consent-dependent harvesting.

Rationale: a child-safety boundary must protect the device data plane as well as communication and social capability. Device use is not blanket data-harvesting consent.
