# Marketplace–Coinbase Accessibility Mirror Handoff

## Scope

This file is the current handoff for the StegVerse Site projection of the governed Marketplace–Coinbase paper-trading accessibility chain.

The Site projection is display and continuity evidence only. It does not grant Coinbase credentials, funded-order authority, custody, withdrawal, publication, release, execution, or live financial authority.

## Upstream chain

```text
StegVerse-Labs/crypto-bot first-accessibility PASS
-> GCAT-BCAT-Engine/Marketplace governed artifact collection and acknowledgement
-> GCAT-BCAT-Engine/Publisher bounded reconstruction status
-> StegVerse-Labs/Site public accessibility projection
```

## Layer determination

```text
prior_state: NOT_BUILT_IN_STEGVERSE_SITE
current_state: BOUNDED_SITE_PROJECTION_IMPLEMENTATION_INSTALLED_ACTIVATION_PENDING_UPSTREAM_VERIFIED_STATUS
execution_class: PARALLEL_SAFE
claimed_paths:
  - docs/MARKETPLACE_COINBASE_ACCESSIBILITY_MIRROR_HANDOFF.md
  - scripts/import_marketplace_coinbase_accessibility.py
  - data/marketplace-coinbase-accessibility-status.json
  - .github/workflows/import-marketplace-coinbase-accessibility.yml
```

These paths do not overlap the active HIL upload owner recorded in `data/ecosystem-heartbeat-state.json`.

## Acceptance states

The importer records exactly one bounded state:

- `PENDING_UPSTREAM`: Publisher has not yet produced a usable public status.
- `REJECTED_UPSTREAM`: the Publisher record is malformed, digest-invalid, authority-escalating, or internally inconsistent.
- `PAPER_ACCESSIBLE`: Publisher reports `VERIFIED`, `paper_release_verified: true`, complete source identities and evidence bindings, and all authority fields remain false.

## Required Publisher conditions

```text
schema = stegverse.publisher.marketplace_coinbase_release_evidence.v2
status_digest = valid canonical sha256 digest
status = VERIFIED
paper_release_verified = true
publication_authorized = false
release_authorized = false
execution_authorized = false
live_authority_granted = false
```

The Site projection additionally requires non-empty upstream source identities and evidence bindings. It persists only the bounded public Publisher status and derived Site projection; it never stores raw private crypto-bot or Marketplace artifacts.

## Output

```text
data/marketplace-coinbase-accessibility-status.json
```

The Site output always preserves:

```text
paper_trading_accessible = true only after Publisher VERIFIED
live_trading_accessible = false
publication_authority = NOT_GRANTED
release_authority = NOT_GRANTED
execution_authority = NOT_GRANTED
live_authority = NOT_GRANTED
```

## Activation owner and stop condition

The repository workflow `.github/workflows/import-marketplace-coinbase-accessibility.yml` owns activation. It runs hourly, on dispatch, and when its bounded implementation changes.

Completion evidence requires a committed Site status with:

```text
state = PAPER_ACCESSIBLE
publisher_status = VERIFIED
publisher_status_digest = exact validated digest
paper_trading_accessible = true
live_trading_accessible = false
all authority fields = NOT_GRANTED
```

Until Publisher produces `VERIFIED`, the correct Site state is `PENDING_UPSTREAM`; absence of upstream completion is not interpreted as failure or authority.

## Remaining upstream coordination

1. Marketplace issue `GCAT-BCAT-Engine/Marketplace#1` must produce `COLLECTED`, acknowledgement `ACCEPTED` or `DUPLICATE`, sequence-2 transport, and the named Marketplace artifact.
2. Publisher issue `GCAT-BCAT-Engine/Publisher#19` must reconstruct the exact chain and persist bounded `VERIFIED` status.
3. Site then imports the public status automatically and records `PAPER_ACCESSIBLE`.
4. Live Coinbase authority remains outside this program and denied.

## Archive readiness

This handoff and its named implementation files preserve all StegVerse Site continuation context for this layer without prior chat history.
