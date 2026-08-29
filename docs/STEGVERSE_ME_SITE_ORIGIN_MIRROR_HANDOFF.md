# StegVerse.me Site Origin Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#581`
Goal: `SITE-STEGVERSE-ME-ORIGIN-581`
Branch: `feature/stegverse-me-origin-581`
State: IMPLEMENTED_LOCAL_VALIDATED / HOSTED_VALIDATION_PENDING
Authority effect: NONE
Activation effect: false

## Purpose

Implement the Site-owned, node-scoped `My StegVerse` projection required by the canonical
`StegVerse-Labs/continuity-vault-kit/KV_PERSONAL_DOMAIN_MIRROR_HANDOFF.md`.

Canonical routes:

```text
https://stegverse.me/
https://stegverse.me/n/<opaque-node>/
https://stegverse.me/n/<opaque-node>/services.html
```

This lane provides reusable source and an origin/routing contract. It does not mutate DNS,
create provider custody, activate a production origin, or claim TLS/public observation.

## Existing sources reused

- `my-kv.html`
- `stegos-node/index.html`
- `stegos-node/stegos-node.js`
- `stegos-node/kv-readiness-snapshot.json`
- IndexedDB `stegos-node-v1` / `meta.registration`
- canonical Receipt #1 registration chain

No alternate node identity, browser fingerprint, user registry, KV registry, or activation
registry may be created by this lane.

## Bounded implementation

- `data/stegverse-me-origin-contract.json` — transport-neutral route and authority contract.
- `stegos-node/services.html` — mobile-first services governance projection.
- `stegos-node/services-state.js` — deterministic lifecycle-state classifier.
- `stegos-node/services.js` — read-only Receipt #1 and KV readiness projection.
- `scripts/check_stegverse_me_origin.py` — static fail-closed validator.
- `tests/stegverse-me-services.test.cjs` — deterministic state and negative tests.
- `.github/workflows/stegverse-me-origin.yml` — validation-only workflow.
- `data/session-work-claims.d/site-stegverse-me-origin-581.json` — exclusive claim.
- `docs/STEGVERSE_ME_SITE_ORIGIN_MIRROR_HANDOFF.md` — this continuation record.

## Lifecycle and governance states

Service lifecycle state is one of:

```text
ACTIVE
INACTIVE
UNAVAILABLE
REVIEW
```

Color mapping:

```text
ACTIVE      -> GREEN
REVIEW      -> YELLOW
UNAVAILABLE -> RED
INACTIVE    -> GRAY
```

Color is never the sole state signal.

A lifecycle state is not a governance verdict. The UI may display the latest verdict and
required action separately but must not merge those values into the lifecycle field.

## Fail-closed rules

1. Missing or invalid Receipt #1 produces `REVIEW`; it never produces `ACTIVE`.
2. Missing, malformed, or stale readiness source produces a visible fail-closed state.
3. `governed_control.enabled=true` is required for `ACTIVE`.
4. Client-side HTML, CSS, JavaScript, cookies, or local state cannot activate a service.
5. The services page has no activation control.
6. No credentials, tokens, passwords, private keys, raw KV identifiers, or provider sessions are accepted.
7. An opaque route is routing input only and cannot grant identity, node, KV, SKAP, Interlock, or execution authority.
8. No production DNS target is emitted until a dedicated origin is selected and verified.
9. Existing `stegverse.org` GitHub Pages binding is not repointed by this lane.
10. Source validation or publication cannot be reported as runtime activation.

## Source completion gates

- claim admitted without collision;
- deterministic service-state tests pass;
- static contract validator passes;
- Receipt #1 absence fails closed to REVIEW;
- invalid readiness projection fails closed;
- ACTIVE requires exact governed enablement;
- explicit state text and accessible labels are present;
- exact-head hosted validation passes;
- PR merged;
- claim terminalized.

## Separate activation gates

- dedicated origin selected;
- authenticated opaque-node resolver implemented;
- production TLS observed;
- exact DNS A/AAAA/CNAME values verified;
- DNS cutover performed;
- root and `www` behavior observed;
- node/KV binding observed through authentic runtime;
- fail-closed runtime outage behavior observed;
- domain migration/recovery test observed;
- durable DNS/origin observation receipt published.

## Current boundary

This lane may complete source implementation and validation without credentials. Production
origin selection, DNS mutation, TLS, authenticated node resolution, private-KV readback, and
runtime activation remain separately unproven.

## Local validation evidence — 2026-08-29

Validated branch head before this reconciliation: `316760c7162c9c7829356a61d60517bc0c0c5115`.

```text
python3 scripts/check_stegverse_me_origin.py
  STEGVERSE_ME_ORIGIN_SOURCE_PASS
  DNS_MUTATION_PERFORMED=false
  AUTHORITY_EFFECT=NONE
  ACTIVATION_EFFECT=false

node tests/stegverse-me-services.test.cjs
  STEGVERSE_ME_SERVICES_STATE_TEST_PASS
  AUTHORITY_EFFECT=NONE
  ACTIVATION_EFFECT=false

python3 scripts/check_session_work_claims.py
  SESSION_WORK_CLAIMS_PASS

python3 scripts/check_stegos_node_projection.py
  STEGOS_NODE_PROJECTION_PASS
  STEGOS_NODE_ONE_ACTION_PEER_SOURCE_PASS
  STEGOS_NODE_OFFLINE_PROOF_SOURCE_PASS
  STEGOS_NODE_KV_CAPABILITY_SHELL_SOURCE_PASS
  STEGOS_NODE_KV_READINESS_BROWSER_STATE_SOURCE_PASS
  STEGOS_NODE_KV_INTR_BROWSER_APPLY_SOURCE_PASS
```

This proves source behavior only. Dedicated origin selection, authenticated route resolution,
DNS, TLS, public observation, and private-KV/runtime activation remain unobserved.
