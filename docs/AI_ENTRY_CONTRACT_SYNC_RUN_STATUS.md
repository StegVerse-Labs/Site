# AI Entry Contract Sync Run Status

## Current state

The Site-side AI Entry contract sync is installed and handoff-current.

## Checked commit

```text
de3efe6688192132d3b88eba090f77fd548dc120
```

## GitHub status check result

```text
workflow_runs: []
combined_status.statuses: []
```

No completed workflow run or status check was exposed for this commit through the available GitHub status tools.

## Canonical local/CI command

```bash
python scripts/check_ecosystem_chat_ai_entry.py
```

Expected terminal output includes:

```text
ECOSYSTEM_CHAT_ROUTES_PASS
ECOSYSTEM_CHAT_BACKEND_PASS
ECOSYSTEM_CHAT_API_WRAPPER_PASS
ECOSYSTEM_CHAT_PROVIDER_ADAPTERS_PASS
ECOSYSTEM_CHAT_SDK_ACCESS_PASS
ECOSYSTEM_CHAT_RECEIPT_PREVIEW_PASS
ECOSYSTEM_CHAT_READINESS_PASS
ECOSYSTEM_CHAT_ADAPTER_EXTENSION_PASS
ECOSYSTEM_CHAT_AI_ENTRY_PASS
```

## Interpretation

```text
installation_complete == true
workflow_run_confirmed == false
status_unavailable == true
```

## Next target

Use the canonical validation command in an available runner or wait for the next workflow-dispatched run to confirm the Site-side AI Entry contract sync.
