# TIDC Reliability Execution Status

```text
updated: 2026-07-27
posture: PILOT_NOT_CONFIRMATORY
release_target: Release 2 — independent coding and disagreement
```

## Completed infrastructure

- discovery-event pilot ledger;
- separate access-precursor ledger;
- blinded second-coding packet;
- coder-response template;
- governed first-pass snapshot;
- disagreement-ledger template;
- agreement calculator;
- synthetic calculator tests;
- codebook revision record;
- source packet index;
- fail-closed publication validator;
- reliability and open-research handoffs.

## First-pass boundary

`data/tidc/coder-response.first-pass.v0.1.json` is a structured snapshot reconstructed from the published pilot and precursor ledgers. It deliberately sets:

```text
coding_role: FIRST_PASS_SNAPSHOT
independence_attestation: false
```

The snapshot is suitable as the comparison baseline. It is not an independent coding result and must never be counted as the required second pass.

## Calculator execution boundary

`scripts/calculate_tidc_agreement.py` accepts either an independently attested first response or the governed first-pass snapshot as its first argument. Its second argument must always carry a true independence attestation.

Synthetic test data may exercise the calculator but must not be copied into the research outputs or treated as reliability evidence.

## Current release blockers

1. A genuinely independent coder must review the allowed source packet without consulting first-pass classifications.
2. The completed response must preserve inaccessible evidence, null dates, uncertainty, and exclusion recommendations.
3. The agreement calculator must produce the first real disagreement ledger.
4. Every disagreement must remain unresolved, be source-adjudicated, or trigger a versioned codebook revision.
5. Agreement and disagreement results must be published without representing coding consistency as support for the clustering hypothesis.
6. Archival source gaps identified in `docs/TIDC_SOURCE_PACKET_INDEX.md` remain open.

## Next integration sequence

```text
independent coder response
-> schema and attestation validation
-> agreement calculation
-> disagreement preservation
-> source adjudication
-> codebook revision where required
-> public reliability report
-> Release 2 gate review
```

## Authority boundary

```text
first-pass snapshot != independent coding
synthetic test != reliability evidence
percent agreement != hypothesis confirmation
resolved disagreement != erased disagreement
public report != proof authority
```
