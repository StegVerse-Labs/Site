# Site Transition Table Display Copy Hardening

## Purpose

This document records the optional display-copy hardening path for `transition-table-visual.html` without changing mirror activation state or Publisher authority.

## Current Source Text

The transition table visual currently separates the public claim text from the adjacent badge text:

```html
The periodic table analogy holds — and is structurally rigorous
<span class="badge" style="color:#67e8f9;border-color:#67e8f9">structure</span>
```

Some public text extractors may concatenate adjacent visible nodes and render the phrase as:

```text
structurally rigorous structure
```

That extractor output is a display-copy artifact, not a governance claim and not a mirror activation issue.

## Hardening Goal

Prevent public text extractors, previews, crawlers, screen-reader summaries, or copied text from implying that the page claims `structurally rigorous structure` as a phrase.

## Recommended Minimal Change

Change only the badge text from:

```text
structure
```

to:

```text
block map
```

This preserves the intended badge meaning while avoiding accidental phrase concatenation with the preceding public claim.

## Drop-In HTML Replacement Snippet

Replace the current title block snippet with this exact snippet:

```html
<div class="insight-title">
  The periodic table analogy holds — and is structurally rigorous
  <span class="badge" style="color:#67e8f9;border-color:#67e8f9">block map</span>
</div>
```

## Non-Goals

This hardening does not:

- activate the Publisher-to-Site mirror;
- change paper source of truth;
- change manifest metadata;
- change public path semantics;
- change ingestion-surface semantics;
- change Site evidence packet requirements;
- change `docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json`.

## Verification

After applying the snippet, verify that:

```text
structurally rigorous structure
```

no longer appears in plain-text extraction, preview text, or copied visible text.

Acceptable extracted text should read as either:

```text
The periodic table analogy holds — and is structurally rigorous block map
```

or as separate fields:

```text
The periodic table analogy holds — and is structurally rigorous
block map
```

## Status

```text
Status: recommended_patch_documented
Mirror activation impact: none
Publisher authority impact: none
Site activation evidence impact: none
Next action: apply snippet to transition-table-visual.html if display-copy hardening is still desired
```

## Archive Readiness

This document contains the complete optional display-copy hardening rationale, exact replacement snippet, non-goals, and verification target. No prior chat context is required to apply this hardening.
