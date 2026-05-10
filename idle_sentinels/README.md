# incoming

Place upload-safe ZIP bundles in this folder.

When no explicit bundle is supplied, the ingestor processes `incoming/*.zip` as one bounded queue pass.

Structural marker files are preserved and are not treated as queue items:

```text
.gitkeep
README.md
```

Queue behavior:

```text
incoming/*.zip
→ installed_bundles/      when accepted and applied
→ failed_bundles/         when stale, already seen, invalid, or failed
→ sandbox_queue/          when sandbox review or repair is required
→ privileged_queue/       when privileged workflow/authority handling is required
```

Upload-safe bundles may use dotless workflow paths:

```text
github/workflows/example.yml
```

The ingestor maps those to the repository workflow directory when privileged handling is allowed.

Queue mode must not automatically apply bundles that mutate the ingestion engine itself. Those bundles are routed to `sandbox_queue/` for review.

Ingestion applies only changed or missing files. It archives or routes source ZIPs out of `incoming/` and writes JSON/Markdown receipts.
