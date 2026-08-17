# Marketplace–Coinbase First-Accessibility — StegVerse Site Handoff

## Authority and current state

- Goal: `MARKETPLACE-COINBASE-FIRST-ACCESSIBILITY-001`
- Repository: `StegVerse-Labs/Site`
- Canonical issue: `StegVerse-Labs/Site#130`
- Credential authority: `TV/TVC`
- GitHub token production authority: `NONE`
- Financial/live execution authority: `NOT_GRANTED`
- Wallet/custody/withdrawal authority: `NOT_GRANTED`
- Current bounded Site projection: `ACCESSIBLE`
- Current task state: terminal repository work complete; no recurring hosted continuation or importer is required.

This handoff governs the bounded public Site projection only. It does not grant funded Coinbase, live-order, custody, withdrawal, settlement, publication, release, or wallet authority.

## Authoritative retained evidence

```text
source repository: StegVerse-Labs/crypto-bot
verified source commit: 73a0543ddb27a88fd4913e7dcfa2127132299baa
verified source workflow run: 30681165495
verified source receipt digest: sha256:5f6cc484c74f5795973cd2e6c52cc349e1cc464064841a29c3d28ed863e98758
verified outbound manifest digest: sha256:854bd485bb93a50a086778d21a33da33299ef3abc36552547a5bf41d9e797333
Site status: data/marketplace-coinbase-first-accessibility-status.json
Site task state: data/marketplace-coinbase-first-accessibility-task-state.json
```

The checked-in task state is durable terminal evidence: `activation_ready: true`, `status: ACCESSIBLE`, `SITE-MCFA-001` through `SITE-MCFA-004` all `COMPLETED`, and no external tasks. Publication, release, execution, live, custody, and withdrawal authority remain `NOT_GRANTED`. `Site#130` is closed completed.

## Retained deterministic implementation

```text
scripts/import_marketplace_coinbase_first_accessibility.py
scripts/continue_marketplace_coinbase_first_accessibility.py
data/marketplace-coinbase-first-accessibility-status.json
data/marketplace-coinbase-first-accessibility-task-state.json
data/marketplace-coinbase-first-accessibility-source-observation.json
```

Retaining deterministic source does not authorize recurring execution. It is available for StegVerse-local inspection/reconstruction only if a fresh canonical task explicitly consumes it.

## Hosted execution retirement

Two obsolete GitHub-hosted loops are superseded:

1. batch 13 removed `.github/workflows/continue-marketplace-coinbase-first-accessibility.yml`;
2. batch 14 removes `.github/workflows/import-marketplace-coinbase-first-accessibility.yml`.

Both removals are bounded by the already-terminal checked-in state. The batch-13 continuation loop was hourly and retained repository/issue writeback plus `github.token`. The batch-14 importer was also hourly, used `contents: write`, GitHub checkout credentials, repository commit/push writeback, setup action, and artifact upload after the projection was already terminal.

No replacement hosted schedule, writeback loop, GitHub token, or NON-TV/TVC credential path is created. No TV/TVC protected value is exported into GitHub Actions.

## Continuation semantics

The completed projection is state-retained rather than clock-driven. A future upstream source change that genuinely requires renewed projection work must create a fresh admitted Site/StegVerse task and claim. It may not silently reactivate either retired hosted workflow.

Any future task must preserve:

```text
credential_authority: TV/TVC
github_token_production_authority: NONE
live_authority: NOT_GRANTED unless separately governed
wallet_signing_broadcast: outside this Site projection
```

## Batch-14 release gate

Batch 14 is complete only when the terminal evidence remains intact; `Site#130` remains closed; both retired first-accessibility hosted workflows are absent; deterministic importer/controller source remains; workflow inventory decreases exactly from 111 to 110; Site pre-work claims, Site Handoff Orchestrator, Ecosystem Heartbeat Orchestration, Site Bootstrap Validate, and Check StegFin Phone Projection pass; and hosted validation is not treated as live financial/product activation.

## Canonical continuation

Workflow/token minimization continues under:

- `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`
- `data/session-work-claims.json`
- `StegVerse-Labs/Site#268`

The Marketplace first-accessibility projection itself has no recurring execution requirement at this terminal state.
