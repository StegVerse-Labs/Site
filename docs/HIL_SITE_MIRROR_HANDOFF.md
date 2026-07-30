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
Operational receiver candidate: https://receiver.stegverse.com
Announcement packet: docs/HIL_START_ANNOUNCEMENT.md
Announcement receipt template: data/hil-start-announcement-receipt.template.json
Experiment manifest: data/hil-experiment.json
Public response index: data/hil-responses.json
Master Record index: data/hil-master-records.json
Observer formalization: docs/HIL_OBSERVER_MODEL.md
Receiver runtime: StegVerse-org/LLM-adapter
Runtime handoff: StegVerse-org/LLM-adapter/docs/HIL_RUNTIME_MIRROR_HANDOFF.md
Site contract guard: scripts/verify_hil_site_contract.py
Readiness record guard: scripts/verify_hil_readiness_record.py
Conforming readiness fixture: tests/fixtures/hil-readiness-ready-v1.1.json
Site contract workflow: .github/workflows/hil-site-contract.yml
Result: ANNOUNCEMENT_READY_RECEIVER_FAIL_CLOSED_PENDING_LIVE_READY
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

Merged Site PR #107 publishes the canonical participant-facing service under `https://stegverse.org/hil/upload/` and configures receiver discovery for `https://receiver.stegverse.com`.

The browser remains fail-closed. It validates the configured HTTPS receiver and enables submission only after the receiver returns a conforming readiness record bound to the exact v1.1 protocol, Primary hash, prompt hash, provenance schema, and participant-metadata contract.

The repository now also contains an offline independent validator for a preserved readiness response. `scripts/verify_hil_readiness_record.py` validates the exact nine-field readiness contract without granting custody, publication, or execution authority. CI evaluates it against `tests/fixtures/hil-readiness-ready-v1.1.json`.

```text
service_page_published: true
receiver_discoverable: true
receiver_ready_observed: false
independent_readiness_validator_installed: true
conforming_readiness_fixture_ci_bound: true
upload_enabled_without_ready: false
announcement_ready: true
announcement_receipt_template_installed: true
announcement_published: false
first_controlled_submission_observed: false
```

A configured receiver address is not a readiness receipt. A conforming fixture is not a live receiver observation. A published service page is not evidence of durable custody, review approval, publication, Master Records reconstruction, or Site activation.

## Announcement state

`docs/HIL_START_ANNOUNCEMENT.md` is the canonical announcement packet. It contains:

- the full public launch statement;
- a compact LinkedIn version;
- a first-comment explanation;
- required claim boundaries;
- an announcement receipt template;
- the next governed transition sequence.

The machine-usable receipt template is installed at `data/hil-start-announcement-receipt.template.json`. It remains incomplete until the public post supplies an RFC3339 timestamp, channel, and public reference.

The announcement may be published now because it truthfully states that the experiment is beginning while preserving the receiver's fail-closed state. It must not claim that the receiver is currently READY unless a live conforming readiness response has been independently observed.

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

1. Publish the public announcement from `docs/HIL_START_ANNOUNCEMENT.md`.
2. Complete and preserve `data/hil-start-announcement-receipt.template.json` as an `HIL-START-ANNOUNCEMENT-RECEIPT-v1` record containing the public post reference.
3. Fetch and preserve the public response body from `https://receiver.stegverse.com/api/hil/readiness` together with observation timestamp, response headers, status code, and transport endpoint.
4. Run `python scripts/verify_hil_readiness_record.py <preserved-readiness-body.json>` and preserve its result as independent readiness evidence.
5. Verify public publication-readiness separately.
6. Perform one controlled response-PDF upload through `https://stegverse.org/hil/upload/`.
7. Preserve the verified receiver receipt and participant review transition.
8. Prove receiver storage persistence through an actual hosted restart or replacement.
9. Record one authenticated private-review disposition.
10. Record one separately authenticated append-only publication.
11. Import the first public record into `data/hil-responses.json`.
12. Build and validate the first `HIL-MASTER-RECORD-RELEASE-v1` chain.
13. Submit to `master-records/orchestration` only under separate authorization.
14. Propagate release verification to Publisher and the public wikis only after the release gate passes.

## Known remaining files and destinations

```text
StegVerse-Labs/Site
- docs/HIL_START_ANNOUNCEMENT.md: installed; public post pending
- data/hil-start-announcement-receipt.template.json: installed; public reference and timestamp pending
- scripts/verify_hil_readiness_record.py: installed
- tests/fixtures/hil-readiness-ready-v1.1.json: installed and CI-bound
- live readiness observation record: pending capture
- data/hil-responses.json: first publication pending
- data/hil-master-records.json: first release pending
- data/hil-experiment.json: observer-mode schema extension pending review
- tests/fixtures or equivalent: observer ambiguity and UNRESOLVED cases pending

StegVerse-org/LLM-adapter
- public receiver readiness evidence: pending
- controlled Site upload and receipt evidence: pending
- hosted restart/replacement persistence evidence: pending
- authenticated private-review evidence: pending
- append-only publication evidence: pending

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

This handoff, `docs/HIL_START_ANNOUNCEMENT.md`, the announcement receipt template, merged PRs #105 through #107, the canonical service route, receiver discovery contract, runtime handoff, validators, fixtures, CI workflow, and repository history preserve the complete continuation state without requiring this conversation thread.
