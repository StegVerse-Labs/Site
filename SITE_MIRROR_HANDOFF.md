# Site Mirror Handoff

## Status

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current Priority

Standing-Proof-Engine v0.5.0 status has been received and recorded for Site propagation.

## Source Artifacts

Destination source: `StegVerse-Labs/Standing-Proof-Engine`

- `SPE_MIRROR_HANDOFF.md`
- `docs/release_snapshot_v0_5_0.md`
- `samples/destination_receipt_chain_001.json`
- `spe/verify_receipt_chain.py`

## Master Records Emission

Destination source: `master-records/core-lite`

- `MASTER_RECORDS_MIRROR_HANDOFF.md`
- `records/spe_destination_receipt_chain_001.json`
- `docs/spe_v0_5_0_status.md`

## Site Record

Destination: `StegVerse-Labs/Site`

- `data/spe-v0-5-0-status.json`

## Downstream Propagation Targets

Destination: `GCAT-BCAT-Engine/Publisher`

- `PUBLISHER_MIRROR_HANDOFF.md`
- `data/spe-v0-5-0-status.json`

Destination: `StegVerse-Labs/admissibility-wiki`

- `ADMISSIBILITY_MIRROR_HANDOFF.md`
- `pages/spe-v0-5-0-standing-boundary.md`

Destination: `StegVerse-002/stegguardian-wiki`

- `STEGGUARDIAN_WIKI_MIRROR_HANDOFF.md`
- `pages/spe-v0-5-0-guardian-boundary.md`

## Build Rule

Before continuing any Site mirror task, check this file first and treat it as the current handoff and task source of truth.

## Boundary

SPE v0.5.0 is a local SPE receipt-chain package with master-records emission recorded. Do not claim external production deployment beyond the recorded targets.

## Next Integration Candidate

Publisher/wiki propagation verification.
