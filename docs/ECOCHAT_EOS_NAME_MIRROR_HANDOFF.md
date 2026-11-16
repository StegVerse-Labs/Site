# ECOCHAT EOS NAME — MIRROR HANDOFF

Claim: SITE-ECOCHAT-EOS-NAME-20261115
Repository: StegVerse-Labs/Site
Date: 2026-11-15 (America/Chicago)

## Naming authority

Rigel, 2026-11-15 19:22 CST: "Let's name this EOS for EcOSystem Chat."
Carriage onto the page approved by Rigel, 2026-11-15 19:48 CST.

The EcOSystem Chat's name is **EOS**. This claim carries the name onto the
chat's two public pages. Nothing else changes: no behavior, no runtime
asset, no filed answer text.

## The brand contract after this claim

index.html:

- meta description: "EOS — the StegVerse EcOSystem Chat. Ask about the
  StegVerse ecosystem, or submit work for governed analysis."
- a visible brand line in the intro section, above the greeting:
  "EOS — the EcOSystem Chat"
- the scope details summary reads: "What EOS does"
- the chat panel aria-label reads: "EOS — the EcOSystem Chat"

ecosystem-chat.html:

- the document title reads: "EOS — StegVerse EcOSystem Chat"
- the nav's active link text reads: "EOS"

The homepage checker pins the brand line: `EOS — the EcOSystem Chat`
joins REQUIRED_INDEX in scripts/check_site_homepage_chat.py, so the name
cannot silently leave the page.

docs/SITE_HOMEPAGE_CHAT_MIRROR_HANDOFF.md gains one additive line
recording the name; no existing line is altered.

## Explicitly unchanged

- The greeting "How can I help?" and the site title "StegVerse".
- The filed starter answers and product definitions, byte for byte, in
  both assets/ecochat-simple-page.js and the shared runtime.
- Every runtime asset, the governed KV entry chain, the gateway binding,
  and all page behavior.
- docs/ECOCHAT_SIMPLE_PAGE_MIRROR_HANDOFF.md — the released simple-page
  claim's handoff; its revision is protected and it is not edited.

## Release predicate

Release only after the implementation PR merges, hosted validation
passes with no new failures against the pristine-main failure baseline
(the pre-existing python3.9 cluster), and public observation of
https://stegverse.org/ shows the EOS brand line on the page with the
three starter questions still answering with the filed deterministic
texts.

## Boundaries

- Do not modify my-kv.html, the VA pages, HIL live-execution, heartbeat
  orchestration, SV001/SV002 custody, InTr transport, TV/TVC, Master
  Records, node registration, or the claim registry's machine-owned
  surfaces.
- Do not edit the canonical claim registry file; this claim enters as an
  append-only fragment.
- Do not rename the chat in filed historical records; corrections and
  namings are new records.
