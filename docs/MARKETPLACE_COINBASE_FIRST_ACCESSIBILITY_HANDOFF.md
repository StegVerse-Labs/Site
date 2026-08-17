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
- Current task state: terminal repository work complete; no recurring hosted continuation is required.

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

The checked-in task state is the durable terminal evidence. It records `activation_ready: true`, `status: ACCESSIBLE`, `SITE-MCFA-001` through `SITE-MCFA-004` all `COMPLETED`, and no external tasks. Publication, release, execution, live, custody, and withdrawal authority remain `NOT_GRANTED`. Issue `Site#130` is closed completed. Those durable facts supersede the earlier pre-activation wording in this handoff.

## Retained implementation

```text
scripts/import_marketplace_coinbase_first_accessibility.py
scripts/continue_marketplace_coinbase_first_accessibility.py
data/marketplace-coinbase-first-accessibility-status.json
data/marketplace-coinbase-first-accessibility-task-state.json
data/marketplace-coinbase-first-accessibility-source-observation.json
```

Retaining deterministic source does not authorize recurring execution. It remains available for StegVerse-local inspection/reconstruction if another canonical owner explicitly consumes it.

## Hosted continuation retirement

The former `.github/workflows/continue-marketplace-coinbase-first-accessibility.yml` loop is superseded and removed under Site workflow-minimization batch 13.

Retirement is bounded because the projection is already terminally `ACCESSIBLE`, all four repository tasks are complete, the coordination issue is closed, and there are no unnamed external tasks. The retired workflow nevertheless continued to run hourly with repository/issue write permission, persisted checkout credentials, `github.token`, issue mutation, commit/push writeback, and artifact upload.

No replacement hosted schedule, writeback loop, GitHub token, or NON-TV/TVC credential path is created. No TV/TVC protected value is exported into GitHub Actions.

## Continuation semantics

The completed projection is state-retained rather than clock-driven. A future source change that genuinely requires new work must enter through a fresh admitted Site/StegVerse task and claim; it may not silently reactivate the retired GitHub-hosted loop.

Any future task must preserve:

```text
credential_authority: TV/TVC
github_token_production_authority: NONE
live_authority: NOT_GRANTED unless separately governed
wallet_signing_broadcast: outside this Site projection
```

## Batch-13 release gate

Batch 13 is complete only when the terminal task state remains intact; `Site#130` remains closed; the former hosted continuation workflow is absent; workflow inventory decreases by exactly one; Site pre-work claims, Site Handoff Orchestrator, Ecosystem Heartbeat Orchestration, Site Bootstrap Validate, and Check StegFin Phone Projection pass; and no hosted validation result is treated as live financial/product activation.

## Canonical continuation

Workflow/token minimization continues under:

- `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`
- `data/session-work-claims.json`
- `StegVerse-Labs/Site#268`

The Marketplace first-accessibility projection itself has no recurring execution requirement at this terminal state.
