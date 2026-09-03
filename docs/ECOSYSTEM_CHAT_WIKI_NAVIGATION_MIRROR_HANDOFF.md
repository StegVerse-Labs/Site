# Ecosystem Chat Wiki Navigation Mirror Handoff

Repository: `StegVerse-Labs/Site`
State: ACTIVE_IMPLEMENTATION
Branch: `fix/ecosystem-chat-wiki-navigation-20260902`
Updated: 2026-09-02
Authority effect: NONE
Activation effect: false

## Observed defect

A current-iPhone Ecosystem Chat request asked:

```text
What is the url for StegTalk wiki?
```

The public chat returned unrelated generic governance prose instead of the requested URL.

## Canonical source

Site already carries the canonical public link in:

- `data/wiki-public-links.json`
- `docs/wiki-links.md`

Canonical StegTalk Wiki URL:

```text
https://stegverse-labs.github.io/stegtalk-wiki/
```

## Goal

Handle plain-language wiki navigation requests before generic conversational/model fallback.

The repair must:

- recognize an explicit StegTalk Wiki URL/navigation question;
- return the canonical URL directly;
- perform no provider/model call;
- preserve ordinary prompts and existing semantic shorthand behavior;
- keep the canonical URL locked to `data/wiki-public-links.json` through regression validation;
- grant no execution, credential, routing-authority, publication-authority, or activation authority.

## Claimed surfaces

- `assets/ecosystem-chat-semantic-commands.js`
- `tests/semantic-command-router.test.cjs`
- `scripts/check_semantic_shorthand_commands.py`
- `docs/ECOSYSTEM_CHAT_WIKI_NAVIGATION_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-ecosystem-chat-wiki-navigation-20260902.json`

## Release boundary

Release after exact-head semantic command validation, Site orchestration/bootstrap/heartbeat gates, merge, and truthful handoff reconciliation. A later public observation may confirm deployment but must not hold source ownership open.
