# Site Homepage Chat Mirror Handoff

Repository: `StegVerse-Labs/Site`  
Issue: `#569`  
Claim: `SITE-HOMEPAGE-CHAT-569-20260828`  
Branch: `claim/site-homepage-chat-569`  
State: IMPLEMENTED / VALIDATION_PENDING  
Authority effect: NONE  
Activation effect: false

## Goal

Make `index.html` the primary StegVerse conversational surface instead of a directory of internal/public transition pages.

Required visible homepage hierarchy:

```text
StegVerse
                                      My KV | Organizational KV

How can I help?

[ How do I use this chat? ]
[ What is StegVerse? ]
[ What is My KV? ]

[ conversation log ]

[ Type your question...                         Send ]
```

## Canonical runtime reuse

The homepage must reuse the existing Ecosystem Chat runtime assets rather than create a second chat implementation:

- `assets/semantic-command-router.js`
- `assets/ecosystem-chat-semantic-commands.js`
- `assets/ecosystem-chat-va-runtime.js`
- `assets/ecosystem-chat-simple.js`
- `assets/ecosystem-node-views.js`

This lane does not modify those files.

## Simplification requirement

Remove homepage-first exposure of:
- Version & Status
- HeartBeat
- StegWallet
- Governed Ecosystem
- Admissibility Wiki
- Papers
- Thought Experiments
- transition-grid directory
- proof-status blocks
- transition-path explanation

Those destinations may continue to exist and may be reached through conversational routing or direct URLs; they are not homepage navigation competitors.

## KV navigation

- `My KV` -> `my-kv.html`
- `Organizational KV` -> `organizational-kv.html`

The Organizational KV page is a bounded entry surface only. It must not claim that an organization KV is installed, connected, authorized, or activated.

## Starter questions

Exactly these three primary starter prompts are required:

- `How do I use this chat?`
- `What is StegVerse?`
- `What is My KV?`

## Completion gates

- pre-work claim admitted;
- homepage uses canonical chat element IDs required by the existing chat runtime;
- isolated deterministic/static validation PASS;
- Site orchestration/bootstrap gates PASS;
- PR merged;
- public Pages deployment separately verified.

No runtime/provider/KV/organizational authority is created by this UI change.


## Implemented source

- `index.html` — simplified StegVerse homepage using the canonical Ecosystem Chat DOM/runtime contract
- `organizational-kv.html` — bounded non-authorizing Organizational KV entry page
- `scripts/check_site_homepage_chat.py` — static simplification/runtime/KV-navigation validator
- `tests/test_site_homepage_chat.py` — deterministic homepage regression tests
- `.github/workflows/site-homepage-chat.yml` — isolated source validation

The homepage now contains exactly three starter prompts:

1. `How do I use this chat?`
2. `What is StegVerse?`
3. `What is My KV?`

The large transition directory, proof-status blocks, and competing homepage navigation are removed from `index.html`. Existing specialty/evidence pages remain in the repository and are not deleted.
