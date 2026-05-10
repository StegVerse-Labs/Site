# Site Bundle Ingestion Engine v1

Upload-safe bundle. No leading-dot paths are included.

## Files

| File | Version | Purpose |
|---|---:|---|
| `tools/bundle_ingest.py` | v1 | Reads a ZIP bundle, maps paths, compares hashes, applies changed files, writes reports. |
| `data/bundle-ingestion-policy-v1.json` | v1 | Defines ingestion policy, protected paths, and dotless workflow path mapping. |
| `github/workflows/ingest-bundle.yml` | v1 | GitHub Actions workflow for ingesting bundles. |
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

The ingestion engine itself maps future bundle paths from:

```text
github/workflows/
```

to:

```text
.github/workflows/
```

## What this solves

Instead of manually comparing bundle contents, you upload a ZIP bundle to:

```text
incoming/
```

Then run:

```text
Actions → Ingest Bundle
```

The workflow:

```text
1. Finds the newest incoming/*.zip bundle, unless a specific path is supplied.
2. Reads all files in the bundle.
3. Skips unsafe paths.
4. Maps dotless workflow paths to .github/workflows paths.
5. Compares target files by SHA-256.
6. Applies only missing or changed files.
7. Writes bundle-ingestion-report.json and bundle-ingestion-report.md.
8. Commits the ingested changes.
```

## Done check

```text
1. Upload these ingestion-engine files.
2. Ensure github/workflows/ingest-bundle.yml is placed in GitHub at .github/workflows/ingest-bundle.yml.
3. Commit.
4. Confirm Actions shows Ingest Bundle.
5. Place any future bundle under incoming/.
6. Run Actions → Ingest Bundle.
7. Download bundle-ingestion-report.
```

## Safety

```text
No files are deleted.
Root README.md inside an uploaded bundle is treated as bundle documentation and is not applied to repo root.
Unsafe absolute paths and parent traversal paths are skipped.
Protected workflow path for the ingestor itself is skipped.
```
