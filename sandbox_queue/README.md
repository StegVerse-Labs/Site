# sandbox_queue

Bundles routed here require sandbox review before they may re-enter ingestion.

The ephemeral sandbox runner reviews ZIPs here, writes reports, and may emit repaired candidate ZIPs into `incoming/`.

The sandbox does not install files directly.
