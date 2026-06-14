# StegVerse Site Publication Process

Generated: `2026-06-14`

## Purpose

This document defines how new information becomes public-facing on `StegVerse-Labs/Site`.

The Site is a public mirror. It is not proof authority. It does not convert an idea, screenshot, conversation, repo status, receipt, or research note into truth merely by publishing it.

## Done Definition

A public Site update is done only when:

- the public claim has a posture;
- the authority source is named or the claim is explicitly marked as research/non-proof;
- the page uses the shared public Site shell when practical;
- stale or superseded information is deprecated instead of silently treated as current;
- proof-heavy language points back to the authority repo, receipt, stage, commit, or source file;
- the Site remains a public mirror rather than becoming the source of proof.

## Public Postures

### DRAFT

Not public-facing yet. Raw screenshots, notes, conversations, tests, and ideas begin here.

### RESEARCH_NOTE

Useful public-facing material that may guide future work, but is not proof authority.

### MIRROR

A Site page reflects another repo, artifact, stage, or receipt. The Site is reporting state; it is not creating authority.

### RECEIPT_BACKED

A claim is tied to a receipt, formalism test, stage result, commit, hash, or other evidence object.

### CANONICAL_CLAIM

Stable public doctrine. Canonical claims still point back to the authority structure that supports them.

### DEPRECATED

Retained for historical continuity only. Deprecated material must not be treated as current public posture.

## Intake Flow

```text
raw input
→ classify
→ identify authority source
→ assign public posture
→ select public page category
→ publish or hold
→ update public-registry.json
```

## Page Categories

### Public Explanation Pages

Examples:

- `index.html`
- `about.html`
- `methodology.html`
- `product.html`

These pages explain StegVerse to outside readers.

### Proof Mirror Pages

Examples:

- `formalism-tests-stage-1-to-31.html`
- `transition-table-visual.html`
- `stegverse-002.html`

These pages mirror proof posture, test posture, receipt posture, and work-entity posture. They must avoid implying that the Site itself is proof authority.

### Commercial / Support Pages

Examples:

- `pricing.html`
- `support.html`
- `stegfinco.html`

These pages may describe services, support paths, and payment posture. Payment evidence is not authority.

## Publication Gate

Before updating a public page, answer:

```text
[ ] What is the claim?
[ ] What is the public posture?
[ ] What authority source supports it?
[ ] Is this a proof claim, research note, mirror, or commercial/service claim?
[ ] Which public page category should carry it?
[ ] Does it require an entry in public-registry.json?
[ ] Does the page preserve the Site boundary doctrine?
```

## Boundary Doctrine

```text
formalism-tests  =  proof/test authority
Site             =  public mirror
StegVerse-002    =  governed work-entity
Transition Table =  public posture map
production       =  accredited participation, not sovereign authority

Site is a public mirror, not proof authority.
```

## Operating Rule

Do not publish unprocessed new information as a public claim.

Process it first.

Then publish the posture, not the assumption.
