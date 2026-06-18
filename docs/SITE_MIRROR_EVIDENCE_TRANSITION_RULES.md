# Site Mirror Evidence Transition Rules

## Purpose

This packet defines how Site mirror activation evidence may transition from `pending` to real evidence values.

The transition rule prevents accidental or premature activation claims when evidence fields are updated.

## Source Of Truth

```text
Ledger: docs/SITE_MIRROR_ACTIVATION_LEDGER.json
Evidence requirements: docs/SITE_MIRROR_EVIDENCE_REQUIREMENTS.md
Activation status: docs/SITE_MIRROR_ACTIVATION_STATUS.md
Handoff: docs/SITE_MIRROR_HANDOFF.md
```

## Non-Activation Rule

Site-side evidence alone does not activate the mirror. Publisher closure remains required before activation can be claimed.

## Allowed Evidence States

```text
pending
observed
verified
activated
```

## Current Required State

Before Publisher closure evidence exists, every activation evidence key must remain:

```text
pending
```

## Transition Rule

Evidence may only advance from `pending` when the corresponding real artifact or commit exists and can be referenced by the ledger.

Activation may only advance to `activated` when all Publisher closure requirements have been satisfied:

```text
Publisher verification receipt artifact
Site evidence artifact
Publisher closure receipt
Publisher verification tracker activation commit
Publisher activation-status update commit
```

## Forbidden Transition

The Site repository must not transition directly from `pending` to `activated` using Site-local evidence alone.

## Required Checks

```text
python scripts/check_site_mirror_evidence_requirements.py
python scripts/check_site_mirror_activation_ledger.py
python scripts/check_site_mirror_activation_status.py
python scripts/check_site_mirror_evidence_transition_rules.py
```

## Completion Condition

This packet is valid when:

```text
python scripts/check_site_mirror_evidence_transition_rules.py
```

passes.

## Archive Readiness

This packet lets a future session update evidence values without guessing whether an evidence transition is allowed.
