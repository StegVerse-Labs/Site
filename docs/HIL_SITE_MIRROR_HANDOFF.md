# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public HIL experiment surface in `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide activation authority.

## Current goal

Activate and publicly announce the complete v1.1 provenance-bound participant path from the verified Primary and exact prompt through unchanged response bytes, receiver readiness, verified submission receipt, participant review, append-only publication, Site projection, Master Record release, and machine-observed deployed evidence.

```text
Primary surface: humans-as-interoperability-layer.html
Canonical service: https://stegverse.org/hil/upload/
Client: assets/hil-experiment-v1.1.js
Receiver discovery: data/hil-receiver-config.json
Operational receiver: https://stegverse.org
Announcement packet: docs/HIL_START_ANNOUNCEMENT.md
Announcement receipt template: data/hil-start-announcement-receipt.template.json
Experiment manifest: data/hil-experiment.json
Public response index: data/hil-responses.json
Master Record index: data/hil-master-records.json
Observer formalization: docs/HIL_OBSERVER_MODEL.md
Receiver runtime: src/worker.js
Custody backend: portable-sqlite-chunks-v1 through HIL_REGISTRY
D1 binding posture: dashboard-managed existing binding; no provider UUID committed to the portable repository
Site contract guard: scripts/verify_hil_site_contract.py
Readiness record guard: scripts/verify_hil_readiness_record.py
Conforming readiness fixture: tests/fixtures/hil-readiness-ready-v1.1.json
Site contract workflow: .github/workflows/hil-site-contract.yml
Live probe workflow: .github/workflows/hil-live-probe.yml
Live probe evidence hardening commit: cba0a104fb7e08622450b664d4461334cea72830
Result: RECEIVER_IMPLEMENTED_FAIL_CLOSED_PENDING_LIVE_READY_AND_CONTROLLED_RECEIPT
Authority: NONE
```

## Canonical v1.1 chain

```text
Primary version: v1.1
Primary SHA-256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Protocol: HIL-PROTOCOL-v1.1
Prompt: HIL-PROMPT-v1.1
Prompt SHA-256: cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
Provenance schema: HIL-RESPONSE-PROVENANCE-v1.1
Receipt schema: HIL-RECEIVER-RECEIPT-v2
Announcement receipt schema: HIL-START-ANNOUNCEMENT-RECEIPT-v1
Observer model: HIL-OBSERVER-MODEL-v0.1
```

## Current public service state

The canonical participant-facing service is published under `https://stegverse.org/hil/upload/`, and receiver discovery resolves to the same-origin receiver at `https://stegverse.org`.

The browser remains fail-closed. It validates the configured HTTPS receiver and enables submission only after the receiver returns a conforming readiness record bound to the exact v1.1 protocol, Primary hash, prompt hash, provenance schema, and participant-metadata contract.

The receiver no longer requires Cloudflare R2. Exact PDF bytes are split into ordered, individually hashed chunks and persisted through the existing `HIL_REGISTRY` D1 binding. The receipt is issued only after reconstruction verifies byte length and SHA-256. The repository intentionally does not commit the account-specific D1 UUID because the existing production binding is managed in the deployment environment; portability is preserved by the binding contract rather than a provider account identifier.

The repository also contains an offline independent validator for a preserved readiness response. `scripts/verify_hil_readiness_record.py` validates the readiness contract without granting custody, publication, or execution authority. CI evaluates it against `tests/fixtures/hil-readiness-ready-v1.1.json`.

The live probe now checks out the repository, disables redirect following, caps preserved response bodies at 65,536 bytes, records DNS addresses, headers, status, final URL, TLS posture, and exact readiness bytes, then runs the offline readiness validator against the preserved body. The probe remains evidence-only and does not fail closed merely because the public receiver is not yet READY; it records `PASS`, `FAIL`, or `NOT_OBSERVED` as an artifact for review.

```text
service_page_published: true
receiver_discoverable: true
receiver_runtime_implemented: true
r2_required: false
d1_binding_reported_configured: true
receiver_ready_observed: false
independent_readiness_validator_installed: true
conforming_readiness_fixture_ci_bound: true
live_readiness_transport_capture_installed: true
live_readiness_independent_validation_installed: true
upload_enabled_without_ready: false
announcement_packet_installed: true
announcement_published: false
first_controlled_submission_observed: false
```

A configured receiver address is not a readiness receipt. A configured binding is not a live readiness observation. A conforming fixture is not a live receiver observation. A published service page is not evidence of durable custody, review approval, publication, Master Records reconstruction, or Site activation.

## Announcement state

`docs/HIL_START_ANNOUNCEMENT.md` is the canonical announcement packet. It contains the public launch statement, compact LinkedIn version, first-comment explanation, required claim boundaries, announcement receipt template, and next governed transition sequence.

The machine-usable receipt template is installed at `data/hil-start-announcement-receipt.template.json`. It remains incomplete until the public post supplies an RFC3339 timestamp, channel, and public reference.

Do not claim that the receiver is currently READY until a live conforming readiness response has been independently observed and preserved.

## Participant path

```text
1. Open https://stegverse.org/hil/upload/
2. Download the canonical v1.1 Primary PDF.
3. Provide the unchanged Primary and exact prompt to an AI system.
4. Preserve the one complete response PDF unchanged.
5. Select the response PDF on the HIL service page.
6. Upload only when the governed receiver reports READY.
7. Verify the receiver receipt and accepted-submission review transition.
8. Preserve participant publication preference separately from final disposition.
```

## Observer formalization state

`docs/HIL_OBSERVER_MODEL.md` separates proposer, committer, and observer as functional roles; formalizes the asymmetry between a long-window context that accumulates commitment and a context repeatedly required to propose; distinguishes structure, interpretation, significance, commitment, and observation; and requires `UNRESOLVED` when evidence cannot establish whether a proposal entered shared reality.

This work grants no intake, review, publication, custody, execution, or Master Record authority. Exact-byte continuity does not by itself establish that participant meaning changed or that a proposal became a committed shared state.

## Required next vertical slice

1. Allow the current Site deployment to publish the provider-neutral D1 receiver build and hardened live-probe workflow.
2. Retrieve the next `hil-live-probe-*` artifact and inspect `live-probe.json`, `readiness-body.json`, `readiness-headers.json`, and `readiness-validation.txt`.
3. Accept receiver readiness only when the public response is HTTP 200, the body reports `READY`, and the independent validator reports `HIL_READINESS_RECORD=PASS`.
4. Perform one controlled response-PDF upload through `https://stegverse.org/hil/upload/`.
5. Preserve the verified receiver receipt and exact-byte retrieval result.
6. Prove receiver storage persistence through an actual hosted restart or replacement.
7. Record one authenticated private-review disposition.
8. Record one separately authenticated append-only publication.
9. Import the first public record into `data/hil-responses.json`.
10. Build and validate the first `HIL-MASTER-RECORD-RELEASE-v1` chain.
11. Submit to `master-records/orchestration` only under separate authorization.
12. Propagate release verification to Publisher and the public wikis only after the release gate passes.
13. Publish the public announcement only after the live receiver and controlled cycle evidence support the announcement claims.

## Known remaining files and destinations

```text
StegVerse-Labs/Site
- live readiness observation record: pending capture from hil-live-probe artifact
- controlled upload receipt fixture/evidence: pending capture
- restart/replacement durability record: pending capture
- docs/HIL_START_ANNOUNCEMENT.md: installed; publication pending activation evidence
- data/hil-start-announcement-receipt.template.json: installed; public reference and timestamp pending
- data/hil-responses.json: first publication pending
- data/hil-master-records.json: first release pending
- data/hil-experiment.json: observer-mode schema extension pending review
- tests/fixtures or equivalent: observer ambiguity and UNRESOLVED cases pending

master-records/orchestration
- exact-byte custody import: pending
- transition and publication reconstruction: pending
- first HIL Master Record release validation: pending

GCAT-BCAT-Engine/Publisher
- release verification task: create at authorized release/tag stage

StegVerse-Labs/admissibility-wiki
- release verification task: create at authorized release/tag stage

StegVerse-002/stegguardian-wiki
- release verification task: create at authorized release/tag stage
```

## Authority boundaries

```text
announcement ready != announcement published
announcement receipt template != completed announcement receipt
service page published != receiver ready
configured receiver != conforming readiness
configured D1 binding != live D1 query evidence
conforming fixture != live readiness observation
receiver readiness != durable-state proof
receiver receipt != private acceptance
private acceptance != publication
publication record != original-byte custody
Site projection != endorsement
Master Record release != custody
proposal generated != committed transition
observer visibility != commit authority
structure preserved != meaning reconstructed
interpretation recorded != significance established
```

## Release posture

No release tag or unrestricted public data-acquisition activation is authorized until one deployed controlled cycle produces a verified receipt, survives an actual hosted restart or replacement, completes authenticated private review and append-only publication, updates the Site projection, and produces a validated Master Record release.

## Archive readiness

This handoff, the canonical service route, same-origin receiver discovery contract, provider-neutral D1 custody implementation, validators, fixtures, CI workflows, and repository history preserve the complete continuation state without requiring this conversation thread.
