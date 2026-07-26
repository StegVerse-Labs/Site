# HIL v1 Upload Mirror Handoff

Status: RELEASE-CRITICAL — CANONICAL SITE UPLOAD FLOW BUILT; DEPLOYED GATEWAY OBSERVATION PENDING
Repository: StegVerse-Labs/Site
Date: 2026-07-26
Goal: Make the public HIL response upload path seamless and ready for the LinkedIn launch while preserving exact-byte provenance and fail-closed authority boundaries.

## Source-of-truth relationship

This handoff governs the canonical v1 upload-surface tranche. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide Site authority and to `docs/HIL_SITE_MIRROR_HANDOFF.md` for the full HIL review, publication, and Master Record lifecycle.

## Release-critical defects corrected

1. `data/hil-experiment.json` previously described the obsolete v0.5 Primary while the public page and browser client described canonical v1.0.
2. The public browser client previously depended on one hardcoded historical Render endpoint.
3. The upload surface lacked explicit gateway discovery, timeout handling, drag-and-drop, and a canonical-v1-specific CI contract.
4. A gateway timeout could not be distinguished clearly from a completed receiver-receipt transition.

## Implemented canonical v1 chain

- Primary file: `HIL_Canonical_Paper_v1_0.pdf`
- Primary SHA-256: `e7a86cf05323d8352cfa188e0bff1c35fdb15f9fac6af91ca62b6a126ac4e68f`
- Prompt version: `HIL-PROMPT-v1.0`
- Prompt SHA-256: `bbb2db652a10ef404d565e561bb0a2f7b078bbe95105400faec14be9a6d5642a`
- Provenance schema: `HIL-RESPONSE-PROVENANCE-v1`

## Seamless upload behavior

The participant now:

1. drops or selects one response-only PDF;
2. enters model, provider, consent, and confirmations;
3. presses `Submit response PDF` once;
4. receives local PDF validation and SHA-256 hashing;
5. receives automatic provenance-manifest construction;
6. receives exact PDF plus manifest upload to the first exact-ready gateway;
7. receives the receiver receipt in the same surface;
8. may download provenance and receipt records without rebuilding either artifact.

The client discovers gateway candidates from `data/hil-gateway-config.json` using `first_exact_ready_chain`. Same-origin is attempted first. The historical ecosystem-chat gateway remains only a compatibility fallback and is not an architectural dependency.

## Fail-closed behavior

- No exact-ready gateway: provenance may be prepared locally, but submission is not claimed.
- Timeout before receipt: no successful submission is claimed.
- Primary or prompt mismatch: candidate gateway is rejected.
- Missing consent or confirmations: upload is rejected locally.
- Invalid, empty, oversized, non-PDF, or signature-mismatched file: upload is rejected locally.
- Receiver receipt does not grant review, publication, endorsement, custody, execution, admissibility, or Master Record authority.

## Files and commits

- `data/hil-experiment.json` — canonical v1 manifest — `55885c740a9344a1ff2f01ae90547dcb297cdf9a`
- `data/hil-gateway-config.json` — gateway discovery — `87d0a53ba3b9c114e60890f6051d968550904bc2`
- `assets/hil-experiment-v1.js` — resilient one-action upload — `35421c6a656ab9ba5d21a1c4ea11b7e3f8ce2f18`
- `humans-as-interoperability-layer.html` — polished drop/select surface — `27fc2eac8cc48e7491e5c9d0b1a0c12f6ce3cabc`
- `scripts/check_hil_v1_upload_surface.py` — canonical verifier — `7766ad88758c3a9a02cd663fc53dd29823594e66`
- `.github/workflows/check-hil-v1-upload-surface.yml` — CI binding — `2565fa301db76dc723ccd8948dd65b78b4ef3248`

## Remaining release-critical work

1. Observe the new HIL v1 upload workflow in hosted CI.
2. Observe the public Site deployment serving the new manifest, config, page, and client.
3. Observe one gateway candidate return exact canonical v1 readiness.
4. Execute one deployed controlled PDF submission and retain the receiver receipt.
5. Restart or replace the gateway and verify exact PDF and provenance persistence.
6. Complete authenticated private review and append-only publication for the first response.
7. Import the first public response into the Site index.
8. Build and validate the first chained HIL Master Record release.
9. Verify release projections in Publisher, admissibility-wiki, and stegguardian-wiki.

## LinkedIn launch gate

The research post may link to the public experiment only after the deployed page is observed with:

- canonical v1 Primary download;
- exact published Primary and prompt hashes;
- one-action upload UI;
- gateway readiness status that does not falsely claim intake;
- local provenance fallback when no gateway is ready.

Public acquisition should be described as live only after one deployed receiver receipt has been observed and persisted. Before that point, the page may be described as the canonical paper and governed replication surface with intake activation pending.

## Authority

```text
Site code merged != deployed Site
configured candidate != reachable gateway
readiness response != submission
local provenance != receiver receipt
receiver receipt != private acceptance
private acceptance != public publication
publication != endorsement
Site projection != original-byte custody
Master Record release != scientific proof
```

## Archival continuity

All release-critical Site upload changes, exact hashes, commits, remaining runtime observations, launch wording boundaries, and downstream obligations are represented here. Complete thread is ready for archiving without any additional part of the thread needed to continue.
