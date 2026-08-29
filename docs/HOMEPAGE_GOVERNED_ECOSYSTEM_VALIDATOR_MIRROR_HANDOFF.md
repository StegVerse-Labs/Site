# Homepage Governed Ecosystem Validator Mirror Handoff

Updated: 2026-08-26
Repository: `StegVerse-Labs/Site`
Canonical issue: `#521`
Parent continuation: `Site#501`

## Source of truth

Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`.
Current user-facing homepage topology remains governed by `docs/UNIFIED_GOVERNED_EXPERIENCE_MIRROR_HANDOFF.md` and `docs/SITE_UNIFIED_GOVERNED_EXPERIENCE_STATUS.md`.
This handoff owns only the stale homepage governed-ecosystem validator exposed after Site#519 merged.

## Machine-discovered failure

Main Bootstrap `33029312606` completed SUCCESS and Site Task Runner `33029333456` advanced through:

```text
SITE MIRROR ORCHESTRATION: PASS
SITE MIRROR WORKFLOW: PASS
SITE MIRROR READINESS: PASS
SITE MIRROR TASK COMPLETION: PASS
SITE UPSTREAM GATES: PASS
SITE MIRROR FULL READINESS: PASS
```

The next exact failure was:

```text
scripts/check_site_homepage_governed_ecosystem.py
failure: missing:display mirror
classification: VALIDATOR_EXACT_TEXT_DRIFT
product/homepage failure: false
```

Current `index.html` already exposes the governed-ecosystem destination and mirror boundary with current user-facing language:

```text
governed-ecosystem.html
Governed Ecosystem
Admissibility Wiki
StegVerse public mirror status
Site is a public mirror and transition router preview, not proof source.
```

The obsolete phrase `display mirror` is not a product contract and must not be reinserted solely for CI.

## Repair contract

The validator requires the current destination, naming, upstream admissibility route, public-mirror status, and explicit non-proof boundary. It no longer requires historical exact wording.

No homepage content is changed by this repair.

## Machine-readable task vector visibility

Canonical COSV task notation remains visible and explicit:

```text
profile: task.v1
notation: L R U I V G O C M T B E A P
width: 14
canonical profile: StegVerse-Labs/.github/management/COSV_PROFILE_V1.json
```

A concrete 14-digit vector for this task remains unminted unless the canonical COSV control-plane projection emits one. Unknown is retained as unknown rather than guessed.

## Current state

```text
issue: #521
branch: fix/homepage-governed-ecosystem-validator-521
validator repair: IMPLEMENTED
exact-head hosted validation: PENDING
merge: NOT_MERGED
next Site Task Runner advance: PENDING
authority effect: NONE
activation effect: false
```

## Remaining work

1. Admit bounded task/claim.
2. Validate exact head.
3. Merge only after required gates pass.
4. Observe subsequent Bootstrap -> Site Task Runner advance beyond homepage governed-ecosystem validation.
5. Continue Site#501 until Pages deployment and semantic-shorthand live verification are actually reached.

## Archive posture

This handoff plus issue #521, its machine task/claim, and workflow evidence preserve this bounded continuation state.


## 2026-08-28 simplified-homepage refresh

State: CLAIM_PENDING_ADMISSION

The original #521 contract predated Site #569. The current machine-discovered failure is Site Task Runner `33227912525`, where `scripts/check_site_homepage_governed_ecosystem.py` still requires Governed Ecosystem / Admissibility Wiki / mirror-status content in `index.html`.

That requirement is now stale.

Current contract:

```text
index.html = simplified conversational shell
primary navigation = My KV | Organizational KV
governed-ecosystem.html = dedicated direct/contextual destination
admissibility-wiki.html = dedicated direct/contextual destination
homepage requirement to expose those specialty surfaces = false
authority effect = NONE
```

This refreshed lane must not modify `index.html`. It validates the existence and authority boundaries of the dedicated specialty surfaces while ensuring the retired homepage-link requirement does not return.
