# StegVerse.me Personal Origin Bundle Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#739`
Goal: `SITE-STEGVERSE-ME-PERSONAL-ORIGIN-BUNDLE-739`
Branch: `feature/stegverse-me-origin-bundle-739-r1`
State: SOURCE_MERGED_PENDING_CLAIM_RELEASE
Authority effect: NONE
Activation effect: false

## Source of truth

This handoff governs deterministic materialization and later observation of the public `stegverse.me` personal-origin bundle.

Predecessors:
- Site #581 / `docs/STEGVERSE_ME_SITE_ORIGIN_MIRROR_HANDOFF.md`
- Site #680 / `docs/STEGVERSE_ME_OPAQUE_NODE_RESOLVER_MIRROR_HANDOFF.md`

Gateway consumer:
- `StegVerse-org/LLM-adapter#233`
- `docs/STEGVERSE_ME_PERSONAL_ORIGIN_SERVICE_GATEWAY_MIRROR_HANDOFF.md`

## Goal

Materialize only the public files required for the dedicated `stegverse.me` virtual origin, with exact SHA-256 identities, while preserving local browser continuity as the admission boundary.

## Owned files

- `docs/STEGVERSE_ME_PERSONAL_ORIGIN_BUNDLE_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-stegverse-me-origin-bundle-739.json`
- `data/stegverse-me-origin-observation-contract.json`
- `stegos-node/stegverse-me-origin-root.html`
- `stegos-node/stegverse-me-services-origin.html`
- `scripts/build_stegverse_me_origin_bundle.py`
- `scripts/observe_stegverse_me_origin.py`
- `tests/test_stegverse_me_origin_bundle.py`
- `.github/workflows/stegverse-me-origin-bundle.yml`

## Bundle contract

The builder must emit:
- `index.html`
- `node.html`
- `services.html`
- `stegverse-me-opaque-resolver.js`
- `services-state.js`
- `services.js`
- `kv-readiness-snapshot.json`
- `stegverse-me-origin-manifest.json`

The manifest schema is `stegverse.personal-origin.public-bundle/v1` and must:
- contain only public files;
- contain exact SHA-256 values;
- declare `private_kv_included=false`;
- declare `authority_effect=NONE`;
- contain no DNS target or credential material.

## Observation boundary

A future observation may become `VERIFIED` only from direct HTTPS evidence for the dedicated origin and exact authority headers. Source, CI, merge, publication, configured hostname, or DNS intent cannot satisfy that gate.

## Explicit non-claims

This lane does not:
- select a live IP/address;
- mutate DNS;
- issue/adopt TLS material;
- create server-side identity;
- read private KV;
- perform authentic Interlock admission;
- activate `stegverse.me`.

## Remaining runtime destinations

`StegVerse-org/LLM-adapter`
- shared Gateway personal-origin adapter.

`StegVerse-Labs/TVC`
- TV/TVC WebPKI materialization/adoption for the admitted hostname.

`StegVerse-Labs/.github`
- host-native resident Service Gateway execution.

Runtime/DNS owner
- public HTTPS observation, controlled DNS cutover, outage/recovery evidence.


## Merge and validation evidence

- Source PR: #742
- Source merge: `53b975f31ab7007a95baacbe82c6a46f3c7fbbc9`
- Exact validated head: `18d74b02693193a907b22fe807642aa9e095f391`
- StegVerse.me Personal Origin Bundle Validation: PASS
- Site Bootstrap Validate - No Non-TV/TVC Credential Authority: PASS
- Site Handoff Orchestrator: PASS
- Ecosystem Heartbeat Orchestration: PASS
- StegOS Node Public Observation: PASS
- shared Gateway source consumer: StegVerse-org/LLM-adapter#234 merged as `f23638072f950691a1cee26cbfcd6e1e1ed99ae3`
- DNS mutation performed: false
- private KV readback performed: false
- authority effect: NONE
- activation effect: false

Source merge does not establish TV/TVC WebPKI materialization, resident Gateway execution, public HTTPS, DNS cutover, authentic Interlock/InTr admission, private-KV readback, outage/recovery observation, or production activation.
