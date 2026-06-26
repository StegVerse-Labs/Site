# Site Chain Status Validation

## Assumption

This document is a companion validation surface for `docs/SITE_CHAIN_STATUS.md`. It avoids changing Site mirror activation state and does not replace `docs/SITE_MIRROR_HANDOFF.md`.

## Done Criteria

The chain status page is valid when it preserves these fields:

```text
source repo: master-records/core-lite
verification repo: StegVerse-Labs/Standing-Proof-Engine
source payload: samples/spe_mapped_receipt_chain_001.json
SPE fixture: samples/external_master_records_receipt_chain_001.json
SPE expected fixture: expected_results/external_master_records_receipt_chain_001.expected.json
verification command: python -m spe.verify_expected_result expected_results/external_master_records_receipt_chain_001.expected.json
boundary: no adoption claim, no endorsement claim, no Site mirror activation claim, no Publisher closure claim, no consequence-binding standing claim from Site placement
```

## Manual Validation Command

```bash
grep -E "master-records/core-lite|StegVerse-Labs/Standing-Proof-Engine|spe_mapped_receipt_chain_001|external_master_records_receipt_chain_001|verify_expected_result|Site mirror activation|Publisher closure|consequence-binding standing" docs/SITE_CHAIN_STATUS.md
```

## Boundary

This validation document is Site-local documentation only. It does not advance activation and does not make Site the source of truth for SPE or master-records artifacts.

## Next Target

```text
GCAT-BCAT-Engine/Publisher -> publication propagation status surface after SPE/master-records chain evidence remains boundary-preserving
```
