# incoming

Place upload-safe ZIP bundles in this folder.

When no explicit bundle is supplied, the ingestor processes `incoming/*.zip` as one bounded queue pass.

The ephemeral sandbox may emit repaired candidate ZIPs into this folder. Those candidates must still pass through normal ingestion before any live repo change is installed.
