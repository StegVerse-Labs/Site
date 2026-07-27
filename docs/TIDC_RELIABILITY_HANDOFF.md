# TIDC Reliability Workflow Handoff

## Parent handoff

```text
parent: docs/TIDC_OPEN_RESEARCH_HANDOFF.md
posture: RELIABILITY_WORKFLOW
research_state: PILOT_NOT_CONFIRMATORY
release_target: Release 2 — independent coding and disagreement
manual_user_action_required: independent coder execution only
```

This file governs the reliability workflow subordinate to the open-research handoff. It does not replace the parent research handoff or alter the ten-event pilot ledger.

## Installed workflow assets

```text
candidate packet: data/tidc/second-coding-packet-v0.1.json
coder response template: data/tidc/coder-response.template.v0.1.json
disagreement template: data/tidc/disagreement-ledger.template.v0.1.json
agreement calculator: scripts/calculate_tidc_agreement.py
publication validator: scripts/check_tidc_publication.py
```

## Required execution sequence

```text
1. Freeze the candidate packet version.
2. Give the packet and cited source material to an independent coder.
3. Require an explicit independence attestation.
4. Preserve null and Unresolved values rather than infer missing evidence.
5. Validate the completed coder response.
6. Compare first-pass and independent coding with calculate_tidc_agreement.py.
7. Publish exact agreement, field-level metrics, and every disagreement.
8. Resolve disagreements only through recorded source-based rationale.
9. Record codebook revisions and superseded classifications.
10. Re-run scripts/check_tidc_publication.py before release-state changes.
```

## Agreement command

```text
python scripts/calculate_tidc_agreement.py \
  data/tidc/coder-response.first-pass.v0.1.json \
  data/tidc/coder-response.independent-01.v0.1.json \
  --output data/tidc/disagreement-ledger.v0.1.json
```

The calculator requires both inputs to use the coder-response schema and to contain explicit independence attestations. It compares shared record IDs and emits field-level exact agreement plus an unresolved disagreement ledger.

## Reliability boundary

```text
high agreement != hypothesis confirmation
low agreement != hypothesis rejection
coder consensus != historical truth
disagreement != error to conceal
resolution != silent overwrite
independent coding != independent replication
```

Agreement measures whether the codebook and evidence packet can be applied reproducibly. It does not establish that technology-induced discovery clustering exists.

## Release gate

Release 2 remains blocked until all of the following are present:

- one completed independent coder response covering all candidate records or explicitly documenting exclusions;
- explicit independence attestation;
- machine-generated agreement output;
- retained disagreement records;
- source-based resolution notes or unresolved status;
- codebook revision record where disagreements expose ambiguous definitions;
- validator success after all public-surface updates.

## Current completion state

```text
second-coding packet: COMPLETE
coder-response schema/template: COMPLETE
disagreement-ledger schema/template: COMPLETE
agreement calculator: COMPLETE
validator integration: COMPLETE
independent coder response: PENDING
agreement output: PENDING
disagreement adjudication: PENDING
codebook revision record: PENDING
Release 2 activation: BLOCKED
```

## Next files

```text
data/tidc/coder-response.first-pass.v0.1.json
data/tidc/coder-response.independent-01.v0.1.json
data/tidc/disagreement-ledger.v0.1.json
docs/TIDC_CODEBOOK_REVISIONS.md
docs/TIDC_SOURCE_PACKET_INDEX.md
```

The first-pass response may be generated mechanically from the pilot ledger only as a comparison artifact. It must be labeled as first-pass coding and must not be presented as independent.

## Latest change

```text
date: 2026-07-27
change: completed reliability workflow scaffolding and fail-closed validation
release_state_changed: false
reason: independent coding has not yet occurred
```
