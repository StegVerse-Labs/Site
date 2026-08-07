# Child-Safe Networking Mirror Handoff

This file is the current task source of truth for the governed child-safe networking projection in `StegVerse-Labs/Site`.

## Active goal and goal ID

```text
Goal ID: SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT
Goal: make the validated child-safety governance sandbox publicly reachable and continuously verify that the canonical deployed route serves the intended governed behavior.
Originating adjacent goal: demonstrate in a public-facing and publicly usable interface how governance can protect children from the classes of social-network harm driving under-13 and under-16 regulation while preserving safe connection, learning, creativity, play, music, and known-person communication.
Repository: StegVerse-Labs/Site
Branch: main
```

## Authoritative files

```text
child-safety-demo.html
children-safe-networking.html
data/tasks/SITE-0002-CHILD-SAFETY-DEMO.json
data/tasks/SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT.json
scripts/check_child_safety_demo.py
scripts/check_child_safety_public_deployment.py
.github/workflows/verify-child-safety-public-deployment.yml
docs/CHILD_SAFE_NETWORKING_MIRROR_HANDOFF.md
repository-task-observation.report.json
data/site-orchestration-state.json
child-safety-public-deployment.report.json (workflow artifact/output when executed)
```

Previous goal `SITE-0001-CHILD-SAFE-NETWORKING` is complete for the public communications contract and 30-second transcript. `SITE-0002-CHILD-SAFETY-DEMO` is complete for deterministic interactive browser behavior. The current goal is deployment verification only.

## Age-policy grounding — checked 2026-08-07

```text
United States: COPPA special privacy/parental-consent regime applies to children under 13; it is not a general US social-media ban.
Australia: since 2025-12-10, covered age-restricted social-media platforms must take reasonable steps to prevent Australians under 16 from creating or keeping accounts.
United Kingdom: government announced an under-16 social-media ban on 2026-06-15, expected in spring 2027; existing Online Safety Act child-protection duties already apply to services likely accessed by children, with announced restrictions also targeting harmful features such as livestreaming and stranger contact for minors.
```

The implementation does not encode a false universal `13 and under` rule. It separates jurisdictional law from the StegVerse protective baseline.

## Harm model represented by the interface

The public demonstrator addresses the capability classes identified in current child-safety policy debates and regulator guidance rather than merely filtering words after harm occurs:

```text
unknown-person direct contact / grooming opportunity
public exposure and unwanted discoverability
public self-livestreaming
precise-location disclosure
behavioral advertising and cross-service profiling
persuasive engagement design and infinite recommendation
algorithmic exposure to upsetting, manipulative, sexual, or violent material
cyberbullying / abuse with no effective report-block path
```

The design preserves positive networking by separating private/known-contact communication and approved collaboration from public social-media capabilities.

## Protective baseline demonstrated

For users under 16, the sandbox demonstrates:

- known friend/family messaging and approved-friend collaboration may remain available where the guardian/known-contact boundary is established;
- stranger direct contact is blocked;
- public social exposure is restricted;
- engagement-optimized infinite recommendation is disabled;
- precise location disclosure is blocked by default;
- behavioral advertising profiling is blocked;
- reporting and blocking remain available.

For all minors, the sandbox additionally disables public self-livestreaming under the StegVerse protective baseline. The baseline is deliberately stricter than any single jurisdictional minimum and is presented as StegVerse policy, not as a claim that every jurisdiction legally requires each restriction.

## Data-minimization behavior

```text
Age input: age band only in demo
Full birthdate retained: no
Identity retained: no
Location retained: no
Contact list retained: no
Advertising profile retained: no
Network requests from demo: none
Receipt retention: browser display only
```

A production implementation should obtain a privacy-preserving age/eligibility assertion from an authorized age-assurance boundary and should not expose a full birthdate to each relying service merely to decide an age band.

## Public interaction contract

The visitor selects jurisdiction, age band, guardian state, and requested action. The sandbox returns exactly one of:

```text
ALLOW
DENY
REVIEW_REQUIRED
```

Every evaluated transition produces a local machine-readable receipt containing jurisdiction, age band, requested action, guardian boundary, decision, reason, retained-personal-data declaration, demo authority boundary, and production-activation=false.

The sandbox refuses unsafe/unnecessary transitions for protected age bands while preserving bounded positive capabilities. This is capability governance, not a cosmetic parental-control overlay.

## Completed implementation evidence

```text
SITE-0001-CHILD-SAFE-NETWORKING: COMPLETE
  validator: CHILD_SAFE_NETWORKING=PASS
  machine state advancement: e0d6fbf8c587b141d4518db50b5241f5cb0d2214

SITE-0001-PERSONAL-DATA-CONTROL: COMPLETE
  validator: PERSONAL_DATA_CONTROL_RUNTIME=PASS

SITE-0002-CHILD-SAFETY-DEMO: COMPLETE
  validator: CHILD_SAFETY_DEMO=PASS
  AGE_POLICY=JURISDICTION_AWARE
  NETWORK_REQUESTS=NONE
  PERSONAL_DATA_RETENTION=NONE
  AUTHORITY_GRANTED=false
  ACTIVATION_EFFECT=PUBLIC_INTERACTIVE_DEMO_ONLY
  evidence: repository-task-observation.report.json
```

## Current deployment claim and blocker

```text
Task: SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT
Task record: data/tasks/SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT.json
Owner: .github/workflows/verify-child-safety-public-deployment.yml
Verifier: scripts/check_child_safety_public_deployment.py
Canonical target: https://stegverse.org/child-safety-demo.html
Observed GitHub Pages repository status: errored
Latest observed Pages build for demo-era commit: building
Public route HTTP 200 with canonical markers: NOT YET VERIFIED
```

Release condition is machine-observable and fail-closed:

```text
HTTPS certificate verifies
AND final public route is HTTPS
AND HTTP status = 200
AND response contains all canonical demo markers
=> CHILD_SAFETY_PUBLIC_DEPLOYMENT=PASS
```

The verification workflow runs after relevant repository changes, on manual dispatch, and hourly. It preserves `child-safety-public-deployment.report.json` as a workflow artifact and fails until the exact public-route evidence exists. No external session ownership or routine user action is required.

## Required distinction: demonstrator vs production child-safety enforcement

```text
Browser decision enforcement in child-safety-demo.html: REAL WITHIN DEMO
Public accessibility: PENDING SITE-0003 VERIFICATION
Production age assurance: NOT ESTABLISHED BY DEMO
Production parental authorization: NOT ESTABLISHED BY DEMO
Production identity/contact verification: NOT ESTABLISHED BY DEMO
Production moderation/grooming detection: NOT ESTABLISHED BY DEMO
Production abuse-report escalation: NOT ESTABLISHED BY DEMO
Production cryptographic receipts/custody: NOT ESTABLISHED BY DEMO
Legal-compliance certification: NOT CLAIMED
```

This distinction prevents a working public simulator from being falsely represented as a complete production child-safety service.

## Production integration sequence after public demo activation

```text
privacy-preserving age assurance
-> age-band / jurisdiction eligibility assertion
-> parent/guardian authority where required
-> verified known-contact graph
-> service capability request
-> child-safety policy evaluation
-> ALLOW / DENY / REVIEW_REQUIRED
-> execution only after ALLOW
-> immutable decision receipt
-> abuse reporting / emergency escalation boundary
-> custody / reconstruction
-> public transparency projection with sensitive fields redacted
```

Each step requires its own evidence before production activation is claimed. This is the next integration candidate after the public demo is verified; it must not be started as a competing implementation while a canonical runtime owner already exists for an overlapping capability.

## Cross-repository boundaries

This demo remains a Site implementation and communications projection. It does not create new canonical legal or admissibility authority. Any later normative policy contract should propagate to `StegVerse-Labs/admissibility-wiki` only when the production integration contract requires it; publication projection belongs to `GCAT-BCAT-Engine/Publisher`, and guardian-specific normative semantics belong to the canonical guardian repository identified by the Site handoff. No downstream propagation is claimed from the browser demo alone.

## Session consolidation and archive condition

All substantive policy reasoning, age-boundary findings, harm classes, demo behavior, completed validation evidence, current deployment blocker, machine observer, release condition, and next integration sequence are durable in this handoff and repository task records.

The session no longer needs to retain undocumented project knowledge. However, the current public-facing usability goal is not complete until `SITE-0003-CHILD-SAFETY-PUBLIC-DEPLOYMENT` records PASS. The repository-native workflow owns that observation, so this chat does not need to remain the observer; archival readiness depends on whether the user defines the current session goal as the implemented/validated demo or the verified public deployment. Under the current stated goal, public deployment remains incomplete.

## Completeness

```text
SITE-0002 demo developed-files percentage: 100%
SITE-0002 validation percentage: 100%
SITE-0002 integration percentage: 100%
SITE-0002 goal activation: 100% PUBLIC_INTERACTIVE_DEMO_ONLY within repository
SITE-0003 public deployment developed verifier files: 100%
SITE-0003 public route verification: 0% until PASS
SITE-0003 goal activation: 0% until PASS
```
