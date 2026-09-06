# Single-Lane Manifold Matrix Paper Mirror Handoff

Repository: `StegVerse-Labs/Site`
Parent authority: `docs/SITE_MIRROR_HANDOFF.md`
Canonical research source: `GCAT-BCAT-Engine/Publisher/papers/single-lane-manifold-matrix-governance.md`
Public surface: `papers/single-lane-manifold-matrix-governance.html`
Index surface: `Papers.html`

## Goal

Render the mathematical candidate as a polished public paper instead of exposing raw Markdown/source notation, and use the resulting presentation contract as the standard for public StegVerse paper readers.

## Resolved defects

- Raw Markdown/source text was previously exposed through a `<pre>` reader.
- Markdown headings, emphasis markers, and fenced code were visible to readers.
- Mathematical blocks were not typeset.
- The first MathJax conversion pass left control-word adjacency defects when symbols such as `∇` or `∂` touched an adjacent variable; e.g. `∇b` became the invalid TeX control word `\nablab`.
- Natural-language connective phrases inside display equations were rendered as concatenated italic math variables.

## Implemented behavior

- Preserve the canonical Publisher source unchanged.
- Render Markdown into semantic HTML.
- Typeset inline and display mathematics using MathJax.
- Preserve tables, ordered test lists, theorem/definition prose, and publication-status language.
- Keep Site as a bounded display surface; do not strengthen candidate status.
- Keep a visible canonical Publisher-source link.
- Fail visibly if the canonical source or rendering dependency cannot be fetched.
- Delimit generated TeX control words so adjacent variables cannot merge into a control sequence.
- Render known natural-language connective phrases inside mathematical blocks as `\text{...}`.
- Preserve mobile equation overflow containment.
- Promote the same requirements into `docs/SITE_PAPER_DISPLAY_POLICY.md` as the default public-paper presentation standard.

## Current commits

```text
initial polished reader: d57fb8ffcdf5e7917fedd2a889372ba547b22f31
control-word/prose math repair: 6bf7055d59118ae05eab8dc113c35d9d6813684f
paper display standard: 14dd7c50ca3767e757cbac0999d4b7d8767f52df
```

## README impact preflight

No README change required. This task changes bounded publication presentation and publication-display policy only. It does not alter repository runtime behavior, governance authority, governed interfaces, evidence semantics, prerequisites, runtime dependencies, failure authority, or capability meaning.

## Collision / ownership preflight

This work remains bounded to the existing task-specific publication handoff and public paper display policy. It does not claim HIL, runtime, provider, custody, activation, or other active execution paths.

## Completion predicate

Repository implementation is complete when the public reader converts canonical Markdown to formatted HTML, MathJax typesets the mathematical expressions without unresolved control sequences, raw Markdown markers are not the primary presentation, and the repository policy defines the same presentation contract for future public papers.

Live completion additionally requires observation of the corrected public route after deployment/propagation.

## Remaining destinations

- `StegVerse-Labs/Site`: live verification of the corrected equation rendering and continued adoption of the publication presentation standard by public paper readers.
- `GCAT-BCAT-Engine/Publisher`: no source mutation required for this rendering fix.
- `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, `StegVerse-002/stegguardian-wiki`: no propagation required solely from this visual rendering repair unless their publication contracts explicitly consume Site display policy.

Authority effect: NONE
Activation effect: NONE
