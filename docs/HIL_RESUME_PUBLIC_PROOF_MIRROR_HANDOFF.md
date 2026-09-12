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
- Verify public HTTPS reachability and exact source-contract markers only.
- Record public URL, HTTP status, and observed page SHA-256 in the existing proof receipt.
- Do not interpret public propagation as current-iPhone local state, receiver custody, restart proof, TVC lifecycle admission, governance authority, credential authority, publication authorization, or parent completion.
- TV/TVC remains credential authority; GitHub runtime authority remains `NONE` for the HIL runtime.

## Expected proof

The workflow must retry the canonical resume URL with cache-busting query parameters until a 200 response serves the durable-resume contract or the bounded retry window fails. The served page must contain markers for the canonical same-device continuation surface, the automatic ESRL route, the automatic custody route, device-continuity fail-closed semantics, and `HIL-RECEIVER-RECEIPT-v2` validation/display support.

## Next step

After a merged workflow change produces a passing public proof receipt for the resume page, public propagation may be considered proven. Authentic HIL receiver/custody evidence still requires execution on the current iPhone and remains separate from deployment proof.
