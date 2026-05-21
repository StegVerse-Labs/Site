# Stage 10 Site Mirror

## Purpose

This document describes the Site mirror for the Stage 10 canonical transition-table release candidate.

The proof authority remains:

```text
formalism-tests
```

The Site role is:

```text
public_mirror
```

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```

## Public Page

```text
stage10-canonical-release.html
```

## Mirrored Data

```text
data/formalism-tests/transition-table-v1-rc1/canonical_transition_table_release.json
data/formalism-tests/transition-table-v1-rc1/canonical_transition_table_release.sha256
data/formalism-tests/transition-table-v1-rc1/replay_packet.json
data/formalism-tests/transition-table-v1-rc1/release_receipt.json
data/formalism-tests/transition-table-v1-rc1/stage10_canonical_release_report.json
data/formalism-tests/transition-table-v1-rc1/index.json
data/formalism-tests/transition-proof-surface.json
```

## Release Candidate

```text
release_id: transition-table-v1-rc1
canonical_status: release_candidate
canonical_elements: 13
coupling_classes: 9
```

## Hash

```text
8330ea16c351226b03bf25e2ad04ef47c0e35a6fbfb1e22a8222122958f8bc2f
```

## Rule

Site may display, link, and explain the proof artifacts.

Site must not alter receipt authority, derive new proof status, or become canonical proof storage.
