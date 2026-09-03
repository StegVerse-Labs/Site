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


### Deployment evidence for repair

Cloudflare reported a successful Site deployment for repair head `91017bb80a993b60b46bf61cb8a5baee5075a178` at 2026-08-31 02:17 UTC.

Deployment success proves the repair source was accepted by the configured Site deployment path. It does not by itself prove that every edge/cache path or the user's browser is serving the repaired bytes.

A public text crawl performed immediately afterward still returned the pre-repair literal `\\n\\n` / `\\n` content, so the deployed-browser state remains `PROPAGATION_OR_CACHE_REVALIDATION_PENDING` until a fresh public browser fetch shows:
- no visible literal newline escapes;
- inline `Register this device` action when unregistered;
- normal chat layout.

No further source repair is presently indicated by repository evidence.


## Registration recheck UX hardening — 2026-08-30

Issue `#765` tightens the presentation behavior for previously registered devices/browser contexts.

Required behavior:

```text
valid current Receipt #1 / registration observed
-> display registered status
-> expose no registration action

registration not immediately visible
-> expose Check current registration
-> canonical StegVerseNodeContinuity.status() recheck

recheck finds registered
-> hide action

recheck still finds unregistered
-> only then expose Register this device

register action
-> canonical status() recheck again
-> existing registerDevice() final recheck
-> create Receipt #1 only if still unregistered
```

The current browser implementation can inspect only the current `stegverse.org` origin/browser storage context. It must not claim that absence there proves the physical device has never been registered in another isolated browser/webview storage partition. This is why the UI now distinguishes **registration not visible** from **confirmed unregistered in this browser context**.

This change does not alter Node identity, Receipt #1 generation/validation, provider authority, KV authority, or the 10-question unregistered allowance.


### Registration recheck merge and validation

Issue `#765` / PR `#766` merged as `7f4edb91ddd5ebb035ef569ca68ccf48b1012f21`.

Validated head `594a00fa319d74806f1cc5d8fc3a319226ea8e5d` passed:

- Site Homepage Chat: `33351213405`
- Site Node Continuity: `33351213400`
- Ecosystem Heartbeat Orchestration: `33351213408`
- Site Handoff Orchestrator: `33351213456`
- Site Bootstrap Validate: `33351213393`

Current registration UX contract:

```text
registered -> no registration action
not visible -> Check current registration
confirmed unregistered in current browser context -> Register this device
pre-registration -> status() recheck
registerDevice() -> final duplicate-prevention status() recheck
```

Cross-browser/webview registration discovery remains a separate continuity capability; the browser page does not claim physical-device-global knowledge from one storage partition.


## Public starter-semantic failure and repair — 2026-08-30

Real iPhone observation showed that all three homepage starter prompts fell through to the bounded `stegverse-reference-lm-v1` path and produced substantially the same governance-oriented output. The same observation showed the unregistered model allowance decrementing from 10 to 9 to 8 and responses ending mid-sentence.

Root cause is explicit in source:

```text
reference model role: bounded second-order reference model
reference corpus: StegVerse governance-oriented material
production conversational equivalence: false
admitted completion ceiling: 64 tokens
starter prompts: previously fell through to model path
```

Issue `#767` repairs the public starter surface by treating the exact three homepage starter prompts as source-grounded deterministic capabilities:

- `How do I use this chat?` -> usage/capability explanation;
- `What is StegVerse?` -> ecosystem overview;
- `What is My KV?` -> KnowledgeVault overview.

Each emits a deterministic same-execution reconstruction receipt with `model_execution:false`, so the existing client must not decrement the 10-question unregistered **model** allowance for these starter interactions.

The admitted reference-model completion ceiling is raised from 64 to 256 tokens. This remains bounded and does not change model identity, corpus, provider authority, or its non-production-equivalent status.

Public screenshot evidence establishes the pre-repair semantic failure. Merge/CI establishes source repair only; fresh iPhone re-observation remains required.


### Canonical StegOS projection correction

The initial Site branch modification to `stegos-bootstrap/admitted-inference.js` correctly changed the desired bound but caused the exact StegOS projection validator to fail. That failure was preserved rather than bypassed.

Canonical correction:
- StegOS issue `#125`;
- StegOS PR `#126`;
- StegOS CI run `33351654603`: PASS;
- canonical StegOS merge `145fe88376f28eab26cdcd60df45a7e74ed0b9c1`;
- canonical `mobile/web-bootstrap/admitted-inference.js` Git blob `493cf77a64479efe816cb2d89e38e4255bca121b`;
- Site projected `stegos-bootstrap/admitted-inference.js` is exact-byte equivalent to that canonical blob;
- Site projection validator is rebound to the new upstream commit/blob.

This preserves StegOS as the source owner and Site as an exact public projection consumer.


### Starter semantic repair merge and validation

Issue `#767` / Site PR `#769` merged as `b8a3491c9792ec422f0a703584e5dacf8cc6304f`.

Final validated Site head `f153c7d3469ac50c8f3aecddec761cdfb4225a3a` passed:
- Site Homepage Chat: `33351717569`
- Site Node Continuity: `33351717549`
- Ecosystem Heartbeat Orchestration: `33351717558`
- Site Handoff Orchestrator: `33351717550`
- Site Bootstrap Validate: `33351717570`

Canonical StegOS upstream completion-bound repair:
- StegOS PR `#126`
- StegOS CI `33351654603`: PASS
- merge `145fe88376f28eab26cdcd60df45a7e74ed0b9c1`

Current source truth:
```text
starter semantic routing: MERGED / VALIDATED
starter model allowance consumption: PREVENTED BY model_execution=false
starter deterministic receipt: IMPLEMENTED
reference-model max_tokens: 256 / CANONICAL STEGOS PROJECTION
public iPhone re-observation: PENDING
```


## Registered-status hidden-control live repair — 2026-09-02

A current-iPhone public screenshot established a precise presentation contradiction on Ecosystem Chat:

```text
Node status text: Registered StegVerse Node
visible action: Check current registration
```

The Node continuity JavaScript was already setting `nodeRegister.hidden=true` for a registered Node. Source inspection identified the rendering defect in the shared design system instead: `.sv-btn { display: inline-block; }` overrides the browser's default rendering of the HTML `hidden` attribute in the author cascade.

Bounded repair:

```css
[hidden] { display: none !important; }
```

This restores the platform `hidden` contract for all Site components while leaving the existing Node status/recheck state machine unchanged. When JavaScript intentionally sets `hidden=false` for unresolved or confirmed-unregistered state, the control remains available normally.

Branch: `fix/hidden-node-registration-control-20260902`
Claim: `SITE-HIDDEN-NODE-REGISTRATION-CONTROL-20260902`
State: IMPLEMENTED_SOURCE_PENDING_VALIDATION_MERGE

No Node identity, Receipt #1, KV, HIL/InTr transport, Interlock, provider, credential, execution, activation, custody, publication, or release authority semantics are changed by this presentation repair.
