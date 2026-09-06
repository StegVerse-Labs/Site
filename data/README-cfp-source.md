# CFP data ingestion — source and freshness contract

`data/cfp-data.json` is the current-season CFP/NCAAF projection consumed by the public Site surface. Its canonical schema is `schema_version: 2.0.0`.

## Canonical path

```text
public college-football sources
        ↓
scripts/fetch_cfp_data.py
        ↓
scripts/check_cfp_data_freshness.py
        ↓
data/cfp-data.json
        ↓
cfp/cfp.js
```

`.github/workflows/cfp_ingest.yml` is the scheduled/manual carrier for this same path. No `CFP_SOURCE_URL` secret, provider API key, or alternate JSON authority is required.

## Fail-closed freshness rule

Historical rankings must never be carried forward into the current data file merely because a fetch fails. A new `last_updated` value does not make old data current.

The required invariants are:

- `season` equals the current UTC season year;
- `freshness.current_season_only` is `true`;
- `freshness.historical_rankings_carried_forward` is `false`;
- `PRE_CFP_RANKINGS` has an empty `rankings` array;
- CFP rankings appear only after a current-season CFP committee ranking is actually observed;
- other polls remain labeled as their own polls and are not promoted to CFP rankings;
- source failures are represented in `freshness.source_errors` and `availability`.

The retained 2025 material is historical reference only. `historical_reference.included_in_current_rankings` must remain `false`.

## Validation

```bash
python scripts/check_cfp_data_freshness.py
```

This validation checks the season/phase contract, historical-ranking exclusion, current-source URLs, and README completeness predicates.

## Authority boundary

This data plane is a public sports-information projection. It grants no sports-officiating, wagering, ticketing, governance, credential, runtime, or publication authority. Source, CI, merge, workflow success, or a generated timestamp is not proof that public deployment or a specific upstream observation occurred.
