# Unified Governed Experience Mirror Handoff

Updated: 2026-08-27
Repository: `StegVerse-Labs/Site`
Canonical issue: `#510`

## Source of truth

This is the bounded continuation record for the Site unified-governed-experience validator reconciliation discovered by Site#501.

Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`.
Shared conversational topology authority is `docs/UNIFIED_CONVERSATIONAL_CAPABILITY_MIRROR_HANDOFF.md`.
Current public UX status is `docs/SITE_UNIFIED_GOVERNED_EXPERIENCE_STATUS.md`.
Machine-readable capability state is `data/unified-conversational-capabilities.json`.

## Current product contract

```text
primary public surface: ecosystem-chat.html
homepage posture: one primary conversational entry plus contextual governed destinations
ordinary language: primary
technical competency assumption: none
internal architecture: hidden by default
contextual links/actions: only when useful
Site execution authority: none
Site receipt authority: none
alternate primary general-chat stack: prohibited
```

Historical phase-specific implementation copy is not a completion predicate for the current user-facing contract.

## Machine-discovered failure

Site Task Runner run `33025351274` passed the semantic, gateway, HIL, and HPS validators, then failed:

```text
scripts/check_site_unified_governed_experience.py
missing status text:
- Primary hero action: Open Ecosystem Chat -> ecosystem-chat.html
- Secondary hero action: View transition menu -> #transition-menu
- Transition Intent Engine phase prose
- Contextual Continuation Panel phase prose
- legacy authority wording
classification: VALIDATOR_DRIFT
```

The current status document intentionally describes the shared conversational-capability topology rather than retaining obsolete phase labels.

## Repair contract

The validator must continue to enforce the homepage's single governed entry and transition-routing semantics.

The status-document validation must bind to stable current invariants:

```text
Goal: unified-governed-experience
Primary operating surface: ecosystem-chat.html
Homepage posture: one primary conversational entry plus contextual governed destinations
Shared capability contract: data/unified-conversational-capabilities.json
Capability handoff: docs/UNIFIED_CONVERSATIONAL_CAPABILITY_MIRROR_HANDOFF.md
technical competency assumption: none
ordinary-language conversation: primary
internal architecture: hidden by default
false authority: prohibited
Execution authority from Site: none
Receipt authority from Site: none
```

No phase label, implementation milestone, or historical local-preview component may be required solely to keep CI green.

## Current state

```text
issue: #510
branch: fix/unified-governed-validator-510-r2
status-contract repair: MERGED previously as PR #511 / 9d6ec7f4afdf9da41317fc2447c5bd601c51bb88
first post-merge Site Task Runner: 33025550407
first post-merge result: FAILED_AT_FORMAT_SENSITIVE_HERO_BOUNDARY
hero-boundary R2 repair: IMPLEMENTED
exact-head hosted validation: PENDING
merge: NOT_MERGED
next Site Task Runner advance: PENDING
authority effect: NONE
activation effect: false
```

## First post-merge execution

PR #511 merged at `9d6ec7f4afdf9da41317fc2447c5bd601c51bb88`. Main Bootstrap run `33025527083` completed SUCCESS and started Site Task Runner `33025550407`.

The worker proved all preceding repaired gates still pass, including semantic routing, gateway/receipt envelopes, HIL v1.1 compatibility, and HPS validation. The unified-governed validator then failed at its HTML extraction boundary:

```text
failure: homepage missing single-entry note after hero
actual page: single-entry-note is present after sv-hero
cause: validator required exact "</div>\n\n  <div class=\"single-entry-note\">" serialization
classification: VALIDATOR_FORMAT_DRIFT
product-contract failure: false
```

R2 keeps the current semantic hero contract and replaces only the whitespace-sensitive boundary lookup with a structural search for the following `single-entry-note` element. It still fails if the note is absent or does not follow the hero.

## Remaining work

1. Validate the R2 formatting-independent hero boundary on exact head through Site claim/orchestration/bootstrap gates.
2. Merge only after required gates pass.
3. Observe a subsequent Bootstrap -> Site Task Runner run advancing beyond this validator.
4. Return control to Site#501 and continue the next exact machine failure.

## Archive posture

This handoff, issue #510, its task/claim, the current status document, unified conversational handoff, and workflow evidence are sufficient to continue without conversation context.
