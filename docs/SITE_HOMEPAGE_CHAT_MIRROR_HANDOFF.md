# Site Homepage Chat Mirror Handoff

Repository: `StegVerse-Labs/Site`  
Issue: `#569`  
Claim: `SITE-HOMEPAGE-CHAT-569-20260828`  
Branch: `claim/site-homepage-chat-569`  
State: IMPLEMENTED_VALIDATED_MERGED / PUBLICATION_VERIFICATION_PENDING  
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


## Validation evidence

Validated implementation head before handoff reconciliation:

`947903adcb34ad53ad3b6f952498ef6676bfbc1a`

Hosted results:

- Site Homepage Chat run `33170347076`: PASS
  - simplified homepage static contract: PASS
  - homepage regression tests: PASS
  - exclusive pre-work claims: PASS
- Ecosystem Heartbeat Orchestration run `33170347114`: PASS
- Site Handoff Orchestrator run `33170347112`: PASS
- Site Bootstrap Validate run `33170347151`: PASS

The first homepage regression run exposed an overly broad test assertion that matched `CONNECTED` inside the correct `NOT CONNECTED` Organizational KV badge. Production behavior was correct; the test was narrowed to reject only an affirmative connected-state badge, and the complete exact-head validation set passed.

This validates source behavior only. Public Pages deployment remains a separate observation gate.


## Merge evidence

- PR: `#571`
- final validated head: `6a114d7f63aea54ccdf16f91d2b6bd2d43e54fdb`
- merge: `78cf6baa9ba23716d623e56fc84b26c7f29b9fac`
- claim release commit: `21e3235db337c69ab15a2aa1f42fdbf34794d26b`

Final exact-head validation:
- Site Homepage Chat run `33170391835`: PASS
- Ecosystem Heartbeat Orchestration run `33170391842`: PASS
- Site Handoff Orchestrator run `33170392033`: PASS
- Site Bootstrap Validate run `33170391843`: PASS

Public Pages deployment remains separately verified; merge does not itself prove that the new homepage is live.


## Public iPhone regression observation — 2026-08-30

Public screenshots from `stegverse.org` exposed two presentation defects after the original homepage merge:

```text
literal "\\n\\n" rendered between Node status and chat
literal "\\n" rendered near the bottom of the page
unregistered Node status instructed registration without an inline registration action
```

Source inspection confirmed the newline defects were checked-in literal escape text in both `index.html` and `ecosystem-chat.html`, not an iOS rendering anomaly.

Repair owner: Site issue `#763` / branch `fix/chat-newline-node-registration`.

Repair contract:

- remove literal escaped-newline text from both chat surfaces;
- expose a user-initiated inline `Register this device` action only while Node status is unregistered;
- reuse `StegVerseNodeContinuity.registerDevice()`;
- preserve existing Receipt #1 validation, 10-question unregistered allowance, and TV/TVC authority boundary;
- hide the registration action once a valid existing Node is observed;
- fail closed on unavailable Node status or registration failure;
- add deterministic regression coverage.

This repair may modify the shared `assets/ecosystem-chat-simple.js` only for the bounded Node-registration UI binding. It does not alter provider routing, model authority, KV authority, or canonical Node receipt semantics.

Public screenshot evidence proves the defect existed. Source merge/CI will prove only repair implementation; a later public browser observation is still required to prove the deployed regression is gone.


### Repair merge and validation

Repair PR `#764` merged as `9d06862e3f1491997df73331acf54e143b9cac35`.

Exact-head validation passed:

- Site Homepage Chat: run `33350171313` — PASS
- Site Node Continuity: run `33350171373` — PASS
- Ecosystem Heartbeat Orchestration: run `33350171329` — PASS
- Site Handoff Orchestrator: run `33350171297` — PASS
- Site Bootstrap Validate: run `33350171309` — PASS
- Observe and Complete Canonical Gateway Tasks: run `33350171306` — PASS

The checked-in literal escape regression is repaired in source, and inline Node registration is wired to the existing continuity API. Public deployment/browser observation remains the final evidence gate for this specific regression.
