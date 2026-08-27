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
branch: fix/unified-governed-validator-510
validator repair: PENDING
exact-head hosted validation: PENDING
merge: NOT_MERGED
next Site Task Runner advance: PENDING
authority effect: NONE
activation effect: false
```

## Remaining work

1. Repair the validator against the current stable contract.
2. Admit the bounded #510 task/claim.
3. Validate exact head through Site claim/orchestration/bootstrap gates.
4. Merge only after required gates pass.
5. Observe a subsequent Bootstrap -> Site Task Runner run advancing beyond this validator.
6. Return control to Site#501 and continue the next exact machine failure.

## Archive posture

This handoff, issue #510, its task/claim, the current status document, unified conversational handoff, and workflow evidence are sufficient to continue without conversation context.
