# ECOCHAT SIMPLE PAGE — MIRROR HANDOFF

Claim: SITE-ECOCHAT-SIMPLE-PAGE-20261115
Worker: claude-coordinator (Muse lane, coordinator surface)
Repository: StegVerse-Labs/Site
Branch: ecochat/simple-page-20261115

## Origin

Principal direction, 2026-11-15 18:13 CST: the front page is to be reduced
to the very simple page of the Ecosystem Chat design (Install Amendment 01:
as simple as any LLM page, depth one layer down).

Defect of record, reproduced 2026-11-15 by three independent observations
(the principal's device screenshots, a signed-out desktop browser run, and
a Node harness executing the served code): `assets/ecosystem-chat-runtime.js`
builds its export table with a reference to `isMath`, a function defined
nowhere in the Site's assets. Evaluating the table throws a ReferenceError,
`window.EcosystemRuntime` is never assigned, and every Ecosystem Chat
submission on every page loading that runtime ends in the catch-all text
"I could not complete that conversation locally just now. Please try again."
The deterministic starter answers inside the runtime are intact but
unreachable. Static checkers pass because they verify text presence, not
execution.

## Scope of this claim

1. `index.html` reduced to the simple page: the chat (heading, log, three
   starter prompts, input, send), the governed My KV launcher, and the
   Organizational KV link, with what the chat does stated in one layer
   down. Driven by one self-contained script,
   `assets/ecochat-simple-page.js`: record-bound questions are answered
   deterministically from the filed starter/product-definition texts;
   everything else receives the filed gateway state (proving instance,
   not publicly reachable) — never an invented answer, never "try again".
   All storage and hashing in the script is guarded so no browser context
   can kill the ask path.
2. `assets/ecosystem-chat-runtime.js`: the missing `isMath` is defined,
   consistent with the file's own governed arithmetic path. This revives
   the shared runtime for `ecosystem-chat.html`, whose stack is otherwise
   untouched. No token the contract checker pins is removed.
3. Homepage contract checkers amended to the simple-page contract, in the
   open, inside this claim: `scripts/check_site_homepage_chat.py`
   (REQUIRED_INDEX becomes the simple page's markers; runtime-ownership
   lines move to the simple page script) and
   `scripts/check_site_node_continuity.py` (the node client/status
   requirement is dropped for the home surface only; the
   ecosystem-chat.html surface requirement is unchanged).
   `docs/SITE_HOMEPAGE_CHAT_MIRROR_HANDOFF.md` ownership lines updated to
   match.

## Release predicate (claim_expires_when)

Release only after the implementation PR merges, hosted validation passes
with no new failures against the pristine-main failure baseline beyond the
two amended contract checkers (which must PASS in amended form), and
public observation of https://stegverse.org/ shows the simple page
answering the three starter questions with the filed deterministic texts.

## Collision boundaries

- Do not modify ecosystem-chat.html, my-kv.html, the VA pages, HIL
  live-execution, heartbeat orchestration, SV001/SV002 custody, InTr
  transport, TV/TVC, Master Records, or node registration surfaces.
- Checker amendments are confined to the index/homepage-surface pins
  named above; every other surface's pins stand.
- Do not introduce third-party runtime endpoints, provider credentials,
  or GitHub-token runtime authority.
- Do not edit the canonical claim registry file; this claim enters as an
  append-only fragment.
- Do not claim gateway activation or live behavior from source, CI,
  merge, or deployment alone.
