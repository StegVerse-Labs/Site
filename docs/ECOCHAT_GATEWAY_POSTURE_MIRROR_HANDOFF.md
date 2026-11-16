# ECOCHAT GATEWAY POSTURE — MIRROR HANDOFF

Claim: SITE-ECOCHAT-GATEWAY-POSTURE-20261115
Repository: StegVerse-Labs/Site
Date: 2026-11-15 (America/Chicago)

## Purpose

Carry the gateway binding record (data/ecochat/gateway-binding.json) to
its current truth, and give the public page client the binding-driven
gateway mechanism. Since the conversion claim
(SITE-ECOCHAT-CONVERSION-20261115) filed the binding, EOS was built
behind the gateway on the proving instance:

- the EOS conversational service runs behind the intake gateway, which
  fronts it at /api/eos/{open,turn,close,replay} and receipts every
  crossing (EOS__BUILD__RECORD__03);
- the corpus stands at GEN 02 (11 starters / 7 products / 10 aliases,
  every entry sourced from a filed record) and the engine at grammar
  v3 with classifier v2 and governed analysis (EOS__BUILD__RECORD__02
  and EOS__BUILD__RECORD__04).

The binding JSON still describes the conversion-era surface (SDK
contract endpoints only). This claim corrects the record and adds the
client mechanism. It changes no filed answer text and no live page
behavior: the posture stays PROVING_INSTANCE, publicly_reachable stays
false, and the client gateway flag ships disabled.

## The posture after this claim

data/ecochat/gateway-binding.json:

- gateway endpoints list gains the EOS routes
  (/api/eos/open, /api/eos/turn, /api/eos/close, /api/eos/replay);
- a new eos block records the bound service: front door at the gateway,
  classes RECORD_FACT / CONVERSATION / ANALYSIS, corpus generation 2,
  grammar eos-turn-grammar/v3, segment lifecycle
  open → turns → close (sealed) → replay;
- proving_instance records the three services (seat, intake gateway,
  EOS) on the coordinator VM, localhost only;
- production_binding remains NOT_YET under ECOCHAT-BIND-001 (node in
  the principal's custody), unchanged;
- a client block records the page mechanism: binding-driven, flag
  client_gateway_enabled false, endpoint null.

assets/ecochat-simple-page.js:

- at load, the page fetches data/ecochat/gateway-binding.json;
- on submit, only when the binding's client block enables the gateway
  AND names an endpoint does the page POST the turn to the gateway's
  /api/eos/turn and render the returned answer with its class;
- any failure, absence, or disabled flag falls through to the existing
  device-local behavior, unchanged in every string and path.

## What does not change

- No filed starter answer or product definition text changes.
- index.html and ecosystem-chat.html do not change; the EOS brand
  contract of SITE-ECOCHAT-EOS-NAME-20261115 stands untouched.
- docs/ECOCHAT_SIMPLE_PAGE_MIRROR_HANDOFF.md is not edited; its
  handoff revision is protected.
- The canonical claim registry file is not edited; this claim enters
  as an append-only fragment.
- Production binding (ECOCHAT-BIND-001) and Q3 node transport remain
  the principal's custody items; this claim prepares their Site side
  only — flipping the client flag and naming the endpoint become a
  posture change, not a code change.

Authority effect: NONE.
