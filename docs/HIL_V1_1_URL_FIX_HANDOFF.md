# HIL v1.1 URL Fix Handoff

Status: OPERATOR SUBMISSION LAYER ACTIVE — RECEIVER-RECEIPT GATEWAY PENDING

## Source of truth

This file records the active correction and operator activation of the public Humans as the Interoperability Layer experiment path.

## Required public path

The existing public URL `humans-as-interoperability-layer.html` serves the HIL v1.1 experiment directly. Participants are not required to discover or navigate to a version-suffixed page.

Public URL:

`https://stegverse-labs.github.io/Site/humans-as-interoperability-layer.html`

## Canonical v1.1 identity

- Filename: `HIL_Canonical_Paper_v1_1.pdf`
- Repository path: `data/HIL_Canonical_Paper_v1_1.pdf`
- Public artifact path: `data/HIL_Canonical_Paper_v1_1.pdf`
- Size: `87271` bytes
- SHA-256: `a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462`
- Protocol: `HIL-PROTOCOL-v1.1`
- Prompt: `HIL-PROMPT-v1.1`
- Prompt SHA-256: `cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c`

## Layer determination

The participant-facing single-artifact layer is BUILT and is now ACTIVE for the controlled operator cycle.

Activated capabilities:

1. canonical v1.1 PDF download path;
2. exact canonical prompt presentation and copy action;
3. visible-chat summary requirement for participant validation;
4. exactly one downloadable response PDF requirement;
5. no participant copy, conversion, combination, reformatting, or re-export requirement;
6. Site response-PDF selection and local validation;
7. response hashing and provenance-manifest generation;
8. fail-closed gateway readiness and receiver-receipt boundary;
9. alternate unchanged return by LinkedIn DM when governed Site receipt transport is not ready.

The operator may now resubmit the canonical document and obtain the response packet. Site receipt completion remains conditional on a conforming v1.1 gateway.

## Correction completed

The canonical PDF was uploaded at `data/HIL_Canonical_Paper_v1_1.pdf` in commit `382aae8ece779a6e23675d46365f64c909a3b26a`.

The browser client previously requested the missing repository-root path `HIL_Canonical_Paper_v1_1.pdf`. It now requests the installed path `data/HIL_Canonical_Paper_v1_1.pdf`, validates the exact 87,271-byte length, PDF signature, and declared SHA-256 before downloading, and remains fail-closed on any mismatch.

The client discovers a same-origin conforming gateway first and retains the historical external gateway only as a compatibility candidate. Failure of one candidate does not prevent discovery of another conforming endpoint.

Implemented commits:

- canonical binary upload: `382aae8ece779a6e23675d46365f64c909a3b26a`
- corrected download and gateway client: `5da297536b42a187bf330395755dc783fe74af58`
- corrected experiment manifest: `45d222da5e67ecc301e3f851f650db9c5bad19d6`
- exact release verifier: `e4a2eef2144fbe77254218996192508716afc6d3`
- release verification workflow: `07f0b501012a82c73631a8ceca2e6f6d985050ad`

## Automated verification

`scripts/check_hil_v1_1_release.py` verifies as one chain:

1. exact PDF presence;
2. PDF signature;
3. exact byte length;
4. exact SHA-256;
5. public page version and identity markers;
6. client artifact path, hashing, and gateway discovery;
7. experiment-manifest identity and fail-closed authority.

`.github/workflows/check-hil-v1-1-release.yml` executes the verifier whenever the canonical PDF, page, client, manifest, verifier, or workflow changes.

Repository-hosted workflow execution remains separate from committed implementation and must be observed before claiming CI verification.

## Participant return contract

The model must produce one downloadable PDF response packet. The visible chat reply must summarize the artifact sufficiently for participant validation and then direct return of the unchanged PDF through Site intake or LinkedIn DM. No copying, conversion, assembly, or re-export is required.

## Active operator sequence

1. Upload the unchanged `HIL_Canonical_Paper_v1_1.pdf` to the selected model.
2. Submit the exact `HIL-PROMPT-v1.1` text.
3. Validate the visible summary against the requested scope.
4. Download the single complete response PDF without editing or conversion.
5. Upload the unchanged PDF at the public Site intake.
6. If the Site reports that no exact-ready gateway is available, preserve the locally generated provenance record and return the unchanged PDF by LinkedIn DM.
7. When a receiver receipt is issued, retain it as the authoritative submission transition record.

## Remaining activation gates

The participant-facing generation and local-provenance layer is active. The following downstream layers remain pending:

- observe GitHub Pages serving the corrected client and exact PDF;
- confirm the download button returns the exact v1.1 PDF on iPhone/Safari;
- observe the exact-release workflow passing;
- deploy a gateway advertising the exact v1.1 Primary and prompt hashes;
- complete one response submission and retain its receiver receipt;
- verify restart persistence, private review, append-only publication, Site import, and first Master Record release.

## Unknown-value handling

Unknown values must be classified as analytical, execution, custody, governance, or future-stage unknowns. Future-stage identifiers do not reduce analytical quality merely because they have not yet been assigned.

## Activation boundary

Participant-facing activation does not imply receiver-gateway, custody, review, publication, or Master Record activation.

The public URL, canonical PDF bytes, Site metadata, prompt text and hash, and local provenance path are aligned for the controlled operator cycle. A receiver receipt may be claimed only after the gateway advertises and validates the exact v1.1 chain.

Download availability does not grant publication, acceptance, execution, custody, or Master Record authority.
