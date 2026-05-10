# MS-012C Ingestion Receipt Boundary v1

Upload-safe bundle. No leading-dot paths are included.

## Files

| File | Version | Purpose |
|---|---:|---|
| `tools/bundle_ingest.py` | v2 | Ingests bundles, fingerprints proposed repo transitions, writes receipts, appends ledger, updates fingerprint index. |
| `data/bundle-ingestion-policy-v1.json` | v2 | Defines ingestion policy, protected paths, dotless workflow mapping, and receipt outputs. |
| `data/latest-bundle-ingestion-receipt-v1.json` | v1 | Latest ingestion receipt placeholder until first run. |
| `data/bundle-ingestion-ledger-v1.jsonl` | v1 | Append-only ingestion ledger. |
| `data/bundle-fingerprint-index-v1.json` | v1 | Bundle fingerprint index. |
| `github/workflows/ingest-bundle.yml` | v2 | Runs the ingestion boundary and commits receipt-backed ingested changes. |
| `incoming/README.md` | v1 | Explains where upload bundles go. |

## Important workflow path note

This bundle intentionally stores the workflow without a leading dot:

```text
github/workflows/ingest-bundle.yml
```

For GitHub Actions to recognize it, the file must ultimately live at:

```text
.github/workflows/ingest-bundle.yml
```

## What this creates

This is the first ingestion/fingerprinting boundary for autonomous StegVerse construction.

A future bundle becomes a proposed repo-state transition:

```text
bundle enters
paths normalized
workflow paths mapped
bundle hash computed
file hashes compared
changed files applied
receipt produced
ledger appended
fingerprint index updated
commit made
```

## Done check

```text
1. Upload these ingestion-engine files.
2. Put github/workflows/ingest-bundle.yml at .github/workflows/ingest-bundle.yml.
3. Commit.
4. Confirm Actions shows Ingest Bundle.
5. Place a future bundle under incoming/.
6. Run Actions → Ingest Bundle.
7. Download bundle-ingestion-report.
```
