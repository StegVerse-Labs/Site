# StegVerse.me Dedicated My KV Origin Mirror Handoff

Status: ACTIVE / ORIGIN_ARCHITECTURE_SELECTION
Repository: StegVerse-Labs/Site
Issue: #581
Branch: claim/site-stegverse-me-origin-581
Goal ID: SITE-STEGVERSE-ME-MY-KV-ORIGIN-581
Created: 2026-08-28

## Goal

Establish a dedicated public origin for `stegverse.me` that serves the personal My KV / node-scoped experience without changing the existing `stegverse.org` GitHub Pages custom-domain binding.

Canonical user routes:

```text
https://stegverse.me/n/<opaque-node>/
https://stegverse.me/n/<opaque-node>/services.html
```

## Current live facts

- `StegVerse-Labs/Site/CNAME` currently contains `stegverse.org`.
- Existing Site GitHub Pages deployment is bound to `stegverse.org`.
- `stegverse.me` is present in Cloudflare DNS management and currently has no production routing records.
- Existing Node continuity / Receipt #1 implementation is already present in Site.
- Existing My KV onboarding is already present in `my-kv.html`.
- Existing StegOS/KV capability projection is already deployed on the current Site surface.
- `stegverse.me` must remain a projection/entrance, not KV/SKAP/identity/Interlock/execution authority.

## Non-negotiable authority boundary

The dedicated origin MAY:

- serve HTML/CSS/JS/static assets;
- resolve opaque node routes;
- present authenticated My KV projections;
- display service governance states;
- transport bounded requests to canonical governed interfaces.

The dedicated origin MUST NOT become:

- KnowledgeVault custody authority;
- SKAP credential authority;
- TV/TVC credential authority;
- node/device authority;
- identity authority;
- Interlock/InTr authority;
- service activation authority;
- receipt authority;
- recovery authority.

## Origin architecture decision

Do not repoint `stegverse.org` or reuse its single GitHub Pages custom-domain binding.

Preferred architecture:

```text
stegverse.me
   |
   v
dedicated static origin for My KV
   |
   +--> Site-derived My KV / Node shell assets
   |
   +--> canonical governed runtime interfaces
```

The preferred implementation is a separate static publication target with its own custom-domain/TLS binding. A separate GitHub Pages repository/site is acceptable as an interim publication carrier because it does not become application authority, but the deployment must remain portable and reconstructable outside GitHub.

A Cloudflare-only rewrite/proxy to `stegverse.org` is not the preferred end state because it would make the `stegverse.me` route depend on that edge mapping rather than on a dedicated independently addressable origin.

## Dedicated origin package

The origin should contain only the bounded user-facing My KV shell and shared assets required by it.

Minimum surface:

```text
/
  index.html
/n/<opaque-node>/
  index.html
  services.html
/assets/
  shared UI assets
  node-continuity client
  My KV projection client
  service-governance projection client
```

The source package should reuse canonical Site implementations rather than minting a second Node identity or alternate Receipt #1 chain.

## Node routing contract

`<opaque-node>` is a routing handle only.

On open:

```text
inspect bounded local continuity
-> reconcile node/KV binding when online
-> validate admitted continuity evidence
-> render Established Node or Register Device
-> resolve My KV projection
```

Possession of the route alone grants no authority.

## Services governance projection

```text
ACTIVE      -> GREEN
REVIEW      -> YELLOW
UNAVAILABLE -> RED
INACTIVE    -> GRAY
```

Every card must show the text state in addition to color.

`REVIEW` means a governed human decision/action is required before proceeding. `RE-REGISTER DEVICE` is one possible REVIEW resolution.

`UNAVAILABLE` includes a service that simply is not available yet.

## DNS/TLS activation sequence

No DNS cutover until the dedicated origin is observed independently.

Required order:

1. materialize dedicated origin package;
2. deploy to a dedicated publication target;
3. obtain the exact origin hostname;
4. configure `stegverse.me` as that publication target's custom domain;
5. confirm the target recognizes the hostname before public cutover;
6. add apex DNS records for the exact target;
7. add `www` alias/redirect only if desired;
8. wait for certificate issuance;
9. verify HTTPS directly;
10. verify `/n/<opaque-node>/` and `/services.html`;
11. publish durable observation receipt;
12. test origin/domain migration recovery.

## DNS rule

Do not hard-code GitHub Pages A records until the chosen dedicated publication target is established.

If the dedicated target is GitHub Pages, use GitHub's then-current documented apex records and the dedicated site's generated `*.github.io` hostname.

If the dedicated target exposes a stable hostname and supports apex CNAME flattening, the apex may instead use the appropriate flattened CNAME form.

The exact DNS values are therefore an output of the origin deployment, not an input guessed in advance.

## Remaining machine-executable work

- build the bounded My KV origin package from current Site source;
- add deterministic route generation/fallback for `/n/<opaque-node>/`;
- implement `services.html` governance cards;
- add exact tests for Established Node / Register Device behavior;
- add negative tests proving route knowledge/client mutation does not grant authority;
- add deploy-target portability manifest;
- add origin observation receipt schema/validator;
- prepare DNS/TLS verification checklist;
- deploy to a dedicated publication target;
- record exact DNS values after target creation;
- perform post-cutover direct observation.

## External/manual gates

- creation/selection of any new external publication target that cannot be created through the connected repository/runtime tools;
- Cloudflare DNS mutation if no connected DNS write authority is available;
- final certificate observation after DNS propagation.

## Completion states

```text
handoff: COMPLETE
origin package: NOT YET IMPLEMENTED
dedicated publication target: NOT YET ESTABLISHED
custom-domain binding: NOT CONFIGURED
DNS: INTENTIONALLY EMPTY
TLS: NOT OBSERVED
node route: NOT OBSERVED ON STEGVERSE.ME
services route: NOT OBSERVED ON STEGVERSE.ME
authority effect: NONE
activation effect: false
```
