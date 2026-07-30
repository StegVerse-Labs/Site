# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public HIL experiment surface in `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide activation authority.

## Current goal

Activate and publicly announce the complete v1.1 provenance-bound participant path from the verified Primary and exact prompt through unchanged response bytes, receiver readiness, verified submission receipt, participant review, append-only publication, Site projection, Master Record release, and machine-observed deployed evidence.

```text
Primary surface: humans-as-interoperability-layer.html
Canonical service: https://stegverse.org/hil/upload/
Operational receiver: https://stegverse.org
Receiver discovery: data/hil-receiver-config.json
Receiver runtime: src/worker.js
Custody backend: portable-sqlite-chunks-v1 through HIL_REGISTRY
Announcement packet: docs/HIL_START_ANNOUNCEMENT.md
Announcement receipt template: data/hil-start-announcement-receipt.template.json
Experiment manifest: data/hil-experiment.json
Public response index: data/hil-responses.json
Master Record index: data/hil-master-records.json
Observer formalization: docs/HIL_OBSERVER_MODEL.md
Site contract guard: scripts/verify_hil_site_contract.py
Readiness guard: scripts/verify_hil_readiness_record.py
Controlled-cycle guard: scripts/verify_hil_controlled_cycle.py
Controlled-cycle tests: tests/test_verify_hil_controlled_cycle.py
Restart-persistence guard: scripts/verify_hil_restart_persistence.py
Restart-persistence tests: tests/test_verify_hil_restart_persistence.py
Site contract workflow: .github/workflows/hil-site-contract.yml
Live probe workflow: .github/workflows/hil-live-probe.yml
Manual custody-cycle workflow: .github/workflows/hil-controlled-cycle.yml
Manual restart-persistence workflow: .github/workflows/hil-restart-persistence.yml
Result: RECEIVER_IMPLEMENTED_CONTROLLED_AND_RESTART_GATES_AUTOMATED_PENDING_LIVE_EVIDENCE
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
Controlled evidence manifest: HIL-CONTROLLED-CYCLE-EVIDENCE-MANIFEST-v1
Restart evidence manifest: HIL-RESTART-PERSISTENCE-EVIDENCE-MANIFEST-v1
```

## Current implementation state

The canonical participant-facing service is published under `https://stegverse.org/hil/upload/`. Receiver discovery resolves to the same-origin receiver at `https://stegverse.org`.

The browser remains fail-closed. It enables submission only after `/api/hil/readiness` returns a conforming HTTP 200 `READY` record bound to the exact v1.1 protocol, Primary hash, prompt hash, provenance schema, and participant-metadata contract.

The receiver stores exact PDF bytes as ordered, individually hashed chunks through the `HIL_REGISTRY` D1 binding. A receipt is issued only after reconstruction confirms byte length and SHA-256. The provider-specific D1 UUID remains deployment-managed and is not committed to the portable repository.

The live probe preserves DNS state, endpoint status, final URL, response headers, capped response bytes, readiness JSON, and independent validation output. A fixture or configured binding is not a live readiness observation.

The controlled-cycle verifier consumes the original PDF, provenance manifest, receiver receipt, later status response, and retrieved PDF. It verifies original and retrieved PDF signatures, exact-byte equality, SHA-256 continuity, provenance hashes, canonical receipt integrity, custody and registry states, review and publication boundaries, status consistency, accepted state, byte count, chunk count, and custody backend.

`.github/workflows/hil-controlled-cycle.yml` automates one manual synthetic infrastructure cycle. It requires the exact dispatch phrase `RUN CONTROLLED HIL CYCLE`, validates live readiness before transmission, generates a labeled synthetic PDF that is not research data, submits only through the durable endpoint, retrieves status and exact bytes, runs the controlled-cycle verifier, and preserves a hashed 90-day evidence artifact.

The restart-persistence verifier consumes the original receipt, status observed after a real hosted redeployment or replacement, and the PDF retrieved after that transition. It independently validates receipt integrity, submission identity, accepted state, custody backend, chunk presence, response hash, byte length, exact reconstructed bytes, and continuing `PENDING` review / `NOT_AUTHORIZED` publication boundaries.

`.github/workflows/hil-restart-persistence.yml` makes that durability gate executable. It requires the exact dispatch phrase `VERIFY HIL RESTART PERSISTENCE`, the original synthetic submission ID, expected response SHA-256, and original receipt JSON. It revalidates receiver readiness, fetches the same status and bytes after redeployment, runs the restart verifier, and preserves `HIL-RESTART-PERSISTENCE-EVIDENCE-MANIFEST-v1` for 90 days.

```text
service_page_published: true
receiver_discoverable: true
receiver_runtime_implemented: true
custody_backend_implemented: true
receiver_ready_observed: false
live_probe_installed: true
independent_readiness_validator_installed: true
controlled_cycle_validator_installed: true
controlled_cycle_tests_ci_bound: true
manual_controlled_cycle_workflow_installed: true
manual_controlled_cycle_executed: false
restart_persistence_validator_installed: true
restart_persistence_tests_ci_bound: true
manual_restart_persistence_workflow_installed: true
restart_persistence_observed: false
upload_enabled_without_ready: false
announcement_packet_installed: true
announcement_published: false
first_participant_submission_observed: false
```

## Required next vertical slice

1. Retrieve the next `hil-live-probe-*` artifact.
2. Accept readiness only when the response is HTTP 200, the body reports `READY`, and independent validation reports `HIL_READINESS_RECORD=PASS`.
3. Manually dispatch `HIL Controlled Custody Cycle` with `RUN CONTROLLED HIL CYCLE`.
4. Preserve the resulting `hil-controlled-cycle-*` artifact.
5. Require `HIL_CONTROLLED_CYCLE=PASS` and verify `evidence-manifest.json`.
6. Treat the synthetic cycle as infrastructure evidence only; it is not a participant response or experimental result.
7. Cause or independently observe an actual hosted restart, redeployment, or receiver replacement after the accepted synthetic submission.
8. Manually dispatch `HIL Restart Persistence Verification` using the original submission ID, response SHA-256, and original receipt JSON.
9. Require `HIL_RESTART_PERSISTENCE=PASS` and verify the restart evidence manifest before claiming durable custody across deployment transition.
10. Perform the first genuine participant response submission only after both infrastructure gates pass.
11. Record one authenticated private-review disposition.
12. Record one separately authenticated append-only publication.
13. Import the first authorized public record into `data/hil-responses.json`.
14. Build and validate the first `HIL-MASTER-RECORD-RELEASE-v1` chain.
15. Submit to `master-records/orchestration` only under separate authorization.
16. Propagate release verification to Publisher and public wikis only after the release gate passes.
17. Publish the public announcement only when live evidence supports every announcement claim.

## Known remaining files and destinations

```text
StegVerse-Labs/Site
- live readiness observation record: pending workflow artifact capture
- synthetic controlled-cycle evidence package: workflow installed; execution pending
- restart/replacement durability evidence: verifier and workflow installed; real deployment transition and execution pending
- first participant response evidence: pending after both infrastructure gates
- docs/HIL_START_ANNOUNCEMENT.md: installed; publication pending activation evidence
- data/hil-start-announcement-receipt.template.json: installed; public reference and timestamp pending
- data/hil-responses.json: first authorized publication pending
- data/hil-master-records.json: first release pending
- data/hil-experiment.json: observer-mode schema extension pending review
- observer ambiguity and UNRESOLVED fixtures: pending

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
service page published != receiver ready
configured receiver != conforming readiness
configured D1 binding != live D1 query evidence
conforming fixture != live readiness observation
receiver readiness != durable-state proof
synthetic controlled cycle != participant experiment
receiver receipt != controlled-cycle verification
controlled-cycle verification != restart persistence
restart persistence != private acceptance
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

This handoff, the canonical service route, same-origin receiver, D1 custody implementation, live probe, controlled-cycle and restart-persistence workflows, validators, tests, CI workflow, and repository history preserve the complete continuation state without requiring this conversation thread.
