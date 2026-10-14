# HIL Resume Public Proof Mirror Handoff

Updated: 2026-09-11
Repository: `StegVerse-Labs/Site`
Issue: `#1260`
Parent goal: `SHWP-HIL-SOVEREIGN-RECEIVER-001`
Parent COSV: `50000000102000`

## Purpose

Extend the existing HIL public deployment proof so it independently verifies the canonical same-device HIL resume surface at `https://stegverse.org/stegos-bootstrap/hil-resume.html` after source merge/deployment.

## Boundaries

- Reuse the existing `HIL Public Page Proof` workflow; do not create a second deployment/proof runtime.
- Verify that the public page is served byte-identical to its source at the deployed commit.
- Record the deployed commit, the source and served SHA-256 of each surface, and the HTTP status in the existing proof receipt.
- Do not interpret public propagation as current-iPhone local state, receiver custody, restart proof, TVC lifecycle admission, governance authority, credential authority, publication authorization, or parent completion.
- TV/TVC remains credential authority; GitHub runtime authority remains `NONE` for the HIL runtime.

## Expected proof

Superseded 2026-10-14 (owner direction on StegVerse-Labs/.github#3106: no external machine is awaited; every action is bound to a state transition). The workflow no longer retries a URL until it answers. It runs once when a GitHub Pages deployment completes, makes one request per HIL surface (`humans-as-interoperability-layer.html`, `stegos-bootstrap/hil-resume.html`), and requires the served bytes to equal the bytes of the same file at the deployed commit (`scripts/hil_public_page_proof.py`; the Site publishes with `.nojekyll`). The fixed marker list it replaced had drifted from the resume page and kept the proof red from 2026-10-12.

Each attempt ends in one disposition:

- `PASS`: every surface is served byte-identical to its source.
- `NO_TRANSITION`: the surfaces are unchanged since a recorded `PASS`; nothing is fetched or rewritten.
- `FAIL_CLOSED`: the record carries `failure_code`, `failed_predicate`, `required_evidence_or_repair`, `retry_entrypoint` (this workflow), `owning_existing_goal` (`SHWP-HIL-SOVEREIGN-RECEIVER-001`) and `next_attempt` (the next completed Pages deployment, or a manual dispatch).

## Next step

After a merged workflow change produces a passing public proof receipt for the resume page, public propagation may be considered proven. Authentic HIL receiver/custody evidence still requires execution on the current iPhone and remains separate from deployment proof.
