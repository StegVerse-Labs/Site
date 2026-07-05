# LLM Free Tier Trust Status

## Purpose

This Site status surface mirrors the public-facing free-tier trust boundary from `StegVerse-org/LLM-adapter` for the StegVerse Ecosystem Chat / governed LLM entry point.

The Site page is display-only. It does not call live model providers, issue receipts, persist records, export audit packets, or grant execution authority.

## Source Contract

```text
Repository: StegVerse-org/LLM-adapter
Capability manifest: adapter.capabilities.json
Response field: free_tier_trust
Policy doc: docs/FREE_TIER_TRUST_POLICY.md
Policy manifest: examples/free_tier_trust_policy.json
```

## Site Display Contract

```text
public user inquiry
  -> bounded free-tier quota envelope
  -> governed LLM adapter request
  -> Site-visible free-tier trust metadata
  -> transition receipt inspection
  -> bounded receipt export / replay / reconstruction limits
  -> upgrade only for scale, retention, connectors, premium models, or API depth
```

## Display Values

```text
Governed inquiries per day: 5
Trial governed inquiries total: 25
Receipt exports per day: 1
Replays per day: 1
Reconstruction scope: recent-session limited
Private connectors: paid or governed upgrade path
Premium models: paid or governed upgrade path
Static demo only: false
Bounded live use: true
```

## Explicit Non-Claims

```text
Quota availability is not admissibility.
Quota availability is not execution authority.
Receipt export is not permanent retention.
Replay does not grant commit-time standing.
Reconstruction does not grant commit-time standing.
Upgrading does not change admissibility requirements.
```

## Remaining Activation Work

```text
StegVerse-Labs/Site:
  - keep this display synchronized with LLM-adapter capability manifest
  - add checker coverage for ecosystem-chat.html free-tier display

StegVerse-org/StegVerse-SDK:
  - ingest quota/receipt/replay metadata contract
```
