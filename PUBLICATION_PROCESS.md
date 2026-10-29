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

## Downloadable PDF Procedure

Applies to any PDF (or other binary) offered for download from the Site. First user: the real governance assessment sample (`docs/SITE_PUBLIC_PATHS.md`, "Real Governance Assessment Sample Path"; `StegVerse-Labs/.github#3398`).

SKAP Vault invariant (existing source, quoted):

> "SKAP Vault inside KV is the only PII and credential store for every user, the ecosystem's own included; the ecosystem holds none (HST citation pending P1 #163). (`docs/FEDERATION_DIRECTORY.md:3`)"
>
> Quoted from its existing source in `StegVerse-Labs/.github`; not restated as new. This Site holds no PII or credential, and no assessment page or download stores one.

### Default: pointer plus digest only

Until the owner rules on public-use licensing, the default is the `StegVerse-Labs/.github#3394` default: **pointer-and-digest only, no redistribution, no public use.**

- The page shows a pointer to the source (repository, issue or comment URL) and the sha256 of the exact bytes. No file is hosted on the Site and no download link is rendered.
- Public-use licensing is an owner-only ruling (`SOURCE_PUBLIC_REUSE_LICENSING_OWNER_ONLY`). A bot, reviewer or Site owner cannot supply it. Absent a recorded ruling, the default stands.

### Pinning by sha256

- Every PDF is pinned by the sha256 of its exact bytes, computed from the file itself (`sha256sum`), never copied from prose.
- The digest appears on the page, in the pointer, and in the `public-registry.json` claim that covers it, together with the edition.
- A changed byte is a new digest and a new edition. The old edition's entry becomes `DEPRECATED` and its digest must not be served as current.
- A digest that has been recorded but whose bytes have not been located is labelled "recorded digest, bytes unverified" and cannot back a download.

### Hosting the file (only after the owner's ruling)

All of these must be evidenced first, each from its source, not asserted here:

```text
[ ] owner ruling on public-use licensing is recorded (not the default)
[ ] source-use disposition and independent review acceptance are recorded
[ ] Site publication authority is recorded
[ ] the PDF bytes are in hand and their sha256 matches the pinned digest
[ ] the page posture is assigned (MIRROR, or RECEIPT_BACKED for a receipt-tied claim)
[ ] public-registry.json entry added for the claim
```

### Readback after publication

- Live URL returns the page; the download URL (if hosted) returns the file and its bytes re-hash to the pinned sha256.
- Mobile and desktop readback at 390px and 1280px: no horizontal overflow, document landmarks, keyboard skip-link, every local download target non-empty (the existing `check_html.cjs` handoff, `StegVerse-Labs/.github#3393` comment 6506838353).
- Readback results are recorded as their own receipts, kept separate from test and build receipts. A passing CI run is not a live readback.

### What this procedure does not do

It grants no publication authority, no licence, and no endorsement; it does not advance any coordination state; and it adds no workflow, secret, schedule or dependency.

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
