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

The checked-in task state is the durable terminal evidence. It records:

```text
activation_ready: true
status: ACCESSIBLE
SITE-MCFA-001: COMPLETED
SITE-MCFA-002: COMPLETED
SITE-MCFA-003: COMPLETED
SITE-MCFA-004: COMPLETED
external_tasks: []
publication_authority: NOT_GRANTED
release_authority: NOT_GRANTED
execution_authority: NOT_GRANTED
live_authority: NOT_GRANTED
custody_authority: NOT_GRANTED
withdrawal_authority: NOT_GRANTED
```

Issue `Site#130` is closed completed. Those durable facts supersede the earlier pre-activation wording in this handoff.

## Retained implementation

The following bounded source/evidence remains retained:

```text
scripts/import_marketplace_coinbase_first_accessibility.py
scripts/continue_marketplace_coinbase_first_accessibility.py
data/marketplace-coinbase-first-accessibility-status.json
data/marketplace-coinbase-first-accessibility-task-state.json
data/marketplace-coinbase-first-accessibility-source-observation.json
```

Retaining a deterministic controller/importer does not authorize recurring execution. It remains available for StegVerse-local inspection/reconstruction if another canonical owner explicitly consumes it.

## Hosted continuation retirement

The former `.github/workflows/continue-marketplace-coinbase-first-accessibility.yml` loop is superseded and removed under Site workflow-minimization batch 13.

Why retirement is safe:

1. the bounded projection is already `ACCESSIBLE`;
2. `activation_ready` is true;
3. all four repository tasks are completed;
4. the coordination issue is already closed completed;
5. there are no unnamed external tasks;
6. the former hourly workflow continued to use GitHub-hosted schedule, repository write permission, persisted checkout credentials, `github.token`, issue mutation, commit/push writeback, and artifact upload after terminal completion;
7. none of that hosted authority is necessary to preserve the completed bounded projection.

No replacement hosted schedule, writeback loop, GitHub token, or NON-TV/TVC credential path is created. No TV/TVC protected value is exported into GitHub Actions.

## Continuation semantics

The completed projection is now **state-retained rather than clock-driven**. A future source change that genuinely requires new work must enter through a fresh admitted Site/StegVerse task and claim; it may not silently reactivate the retired GitHub-hosted loop.

Any such future task must preserve:

```text
credential_authority: TV/TVC
github_token_production_authority: NONE
live_authority: NOT_GRANTED unless separately governed
wallet_signing_broadcast: outside this Site projection
```

## Validation and release condition for batch 13

Batch 13 is complete only when:

- the terminal task state remains unchanged in substance;
- `Site#130` remains closed completed;
- the former hosted continuation workflow is absent;
- Site workflow inventory decreases by exactly one;
- Site pre-work claims pass;
- Site Handoff Orchestrator passes;
- Ecosystem Heartbeat Orchestration passes;
- Site Bootstrap Validate passes;
- Check StegFin Phone Projection passes;
- no hosted validation result is interpreted as live financial or product activation.

## Canonical continuation

Workflow/token minimization continues under:

- `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`
- `data/session-work-claims.json`
- `StegVerse-Labs/Site#268`

The Marketplace first-accessibility projection itself has no recurring execution requirement at this terminal state.
