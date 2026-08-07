# Child-Safe Networking Mirror Handoff

This file is the current task source of truth for the governed child-safe networking projection in `StegVerse-Labs/Site`.

## Active goal and goal ID

```text
Goal ID: SITE-0002-CHILD-SAFETY-DEMO
Goal: expose a public, usable, jurisdiction-aware child-safety governance sandbox that demonstrates useful connection, deterministic refusal, review boundaries, privacy-first age signals, and inspectable receipts without collecting personal data.
Originating adjacent goal: demonstrate in a public-facing interface how governance can protect children from the classes of social-network harm driving under-13 and under-16 regulation while preserving safe connection, learning, creativity, play, music, and known-person communication.
Repository: StegVerse-Labs/Site
Branch: main
```

## Authoritative files

```text
child-safety-demo.html
children-safe-networking.html
data/tasks/SITE-0002-CHILD-SAFETY-DEMO.json
scripts/check_child_safety_demo.py
docs/CHILD_SAFE_NETWORKING_MIRROR_HANDOFF.md
repository-task-observation.report.json
data/site-orchestration-state.json
```

Previous goal `SITE-0001-CHILD-SAFE-NETWORKING` remains complete and canonical for the public communications contract and 30-second transcript.

## Age-policy grounding — checked 2026-08-07

```text
United States: COPPA special privacy/parental-consent regime applies to children under 13; it is not a general US social-media ban.
Australia: since 2025-12-10, covered age-restricted social-media platforms must take reasonable steps to prevent Australians under 16 from creating or keeping accounts.
United Kingdom: government announced an under-16 social-media ban on 2026-06-15, with implementation expected in spring 2027; existing Online Safety Act child-protection duties already apply to services likely accessed by children.
```

The demo therefore does not encode a false universal `13 and under` rule. It separates jurisdictional law from the StegVerse protective baseline.

## Protective baseline demonstrated

For users under 16, the sandbox demonstrates:

- known friend/family messaging and approved-friend collaboration may remain available;
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

## Canonical ownership and claims

```text
Canonical task owner: scripts/observe_and_complete_repository_tasks.py
Implementation claim: repository-local parallel-safe child-safety demo lane
Validation claim: repository task controller executes scripts/check_child_safety_demo.py
Claim creation time: 2026-08-07T14:20:00Z
Claim release condition: validator returns CHILD_SAFETY_DEMO=PASS and machine controller records COMPLETE, or task is explicitly superseded.
Collision boundaries: do not modify humans-as-interoperability-layer.html, assets/hil-*, or scripts/check_hil_*upload*.
```

## Public interaction contract

The user can select jurisdiction, age band, guardian state, and a requested action. The sandbox returns exactly one of:

```text
ALLOW
DENY
REVIEW_REQUIRED
```

Every evaluated transition produces a local machine-readable receipt containing jurisdiction, age band, requested action, guardian boundary, decision, reason, retained-personal-data declaration, demo authority boundary, and production-activation=false.

The sandbox is expected to refuse at least these unsafe/unnecessary transitions for protected age bands:

```text
unknown-person direct contact
public posting to strangers
public self-livestreaming
precise-location disclosure
behavioral advertising profiling
engagement-optimized infinite recommendation
```

It is expected to preserve at least these positive capabilities where their boundary is established:

```text
known friend/family messaging
approved-friends music collaboration
report/block capability
```

## Required distinction: demonstrator vs production child-safety enforcement

```text
Browser decision enforcement in child-safety-demo.html: REAL WITHIN DEMO
Production age assurance: NOT ESTABLISHED BY DEMO
Production parental authorization: NOT ESTABLISHED BY DEMO
Production identity/contact verification: NOT ESTABLISHED BY DEMO
Production moderation/grooming detection: NOT ESTABLISHED BY DEMO
Production abuse-report escalation: NOT ESTABLISHED BY DEMO
Production cryptographic receipts/custody: NOT ESTABLISHED BY DEMO
Legal-compliance certification: NOT CLAIMED
```

This distinction prevents a working public simulator from being falsely represented as a complete production child-safety service.

## Production integration sequence after demo completion

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

Each step requires its own evidence before production activation is claimed.

## Previous completed goal evidence

```text
SITE-0001-CHILD-SAFE-NETWORKING: COMPLETE
Validator: CHILD_SAFE_NETWORKING=PASS
Machine state advancement: e0d6fbf8c587b141d4518db50b5241f5cb0d2214
Personal-data-control overlap: SITE-0001-PERSONAL-DATA-CONTROL COMPLETE
```

## Validation command

```text
python scripts/check_child_safety_demo.py
```

Expected success marker:

```text
CHILD_SAFETY_DEMO=PASS
```

## Cross-repository boundaries

This demo remains a Site implementation and communications projection. It does not create new canonical legal or admissibility authority. Any later normative policy contract should be propagated to `StegVerse-Labs/admissibility-wiki` only when the production integration contract requires it; publication projection belongs to `GCAT-BCAT-Engine/Publisher`, and guardian-specific normative semantics belong to the canonical guardian repository identified by the Site handoff. No such propagation is claimed from the browser demo alone.

## Archive conditions

The current adjacent goal is archive-safe when `SITE-0002-CHILD-SAFETY-DEMO` is machine-observed COMPLETE and this handoff contains that evidence. The repository-native controller then owns future revalidation. Production child-safety runtime remains a distinct next integration goal and must not be inferred from demo completion.

## Completeness

```text
developed-files percentage: 100% for the four-file demo slice once all files are committed
validation percentage: pending repository-native observation
integration percentage: pending repository-native task completion
current goal-activation percentage: pending PUBLIC_INTERACTIVE_DEMO_ONLY completion
```
