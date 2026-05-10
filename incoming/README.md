# incoming

Place upload-safe ZIP bundles in this folder.

The ingestion workflow reads the newest `incoming/*.zip` bundle by default.

The ingestor maps this bundle path:

```text
github/workflows/example.yml
```

to this repository path:

```text
.github/workflows/example.yml
```

No file is deleted by ingestion. Only changed or missing files are applied.
