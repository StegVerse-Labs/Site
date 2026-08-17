# Marketplace–Coinbase Accessibility Mirror Handoff

## Authority and goal

- Goal ID: `MARKETPLACE-COINBASE-PAPER-ACCESSIBILITY-001`
- Repository: `StegVerse-Labs/Site`
- Owner issue: `StegVerse-Labs/Site#131`
- Credential authority: `TV/TVC`
- NON-TV/TVC secret/token requirement: `NONE`
- GitHub token production/control-plane authority: `NONE`
- Publication/release/execution/live financial authority: `NOT_GRANTED`

This Site surface is bounded evidence and continuity only. It does not grant funded Coinbase, live-order, custody, withdrawal, settlement, publication, release, execution, or wallet authority.

## Current state

```text
SITE_MARKETPLACE_COINBASE_PAPER_ACCESSIBILITY_TERMINAL_COMPLETE
```

The four controller stop conditions have now been directly reconciled against repository-resident evidence:

1. `StegVerse-Labs/crypto-bot/data/first-accessibility-mark-status.json` — `status=PASS`, `paper_trading_accessible=true`.
2. `GCAT-BCAT-Engine/Marketplace/data/marketplace-coinbase-outbound-collection-status.json` — `status=COLLECTED`, acknowledgement `ACCEPTED`, sequence-2 transport present.
3. `GCAT-BCAT-Engine/Publisher/data/marketplace-coinbase-release-evidence-status.json` — `status=VERIFIED`, `paper_release_verified=true`.
4. `StegVerse-Labs/Site/data/marketplace-coinbase-accessibility-status.json` — `state=PAPER_ACCESSIBLE`, `paper_trading_accessible=true`, `live_trading_accessible=false`.

The earlier `CONTROLLER_ACCESS_REPAIR` state was caused by a token-dependent GitHub API observation path returning blocked/404 observations. It was not evidence that MC-01 or MC-02 were incomplete.

## Canonical retained evidence

```text
data/marketplace-coinbase-activation-tasks.json
scripts/advance_marketplace_coinbase_activation.py
data/marketplace-coinbase-accessibility-status.json
scripts/import_marketplace_coinbase_accessibility.py
tests/test_marketplace_coinbase_accessibility.py
```

`data/marketplace-coinbase-activation-tasks.json` is now schema v3 and records all four tasks `COMPLETE`, all stop conditions satisfied, `credential_used=false`, `non_tv_tvc_token_required=false`, `github_token_authority=NONE`, and `network_reobservation_required=false`.

The retained `scripts/advance_marketplace_coinbase_activation.py` is no longer a network controller. It is a deterministic local validator for the terminal state. It refuses `STEGVERSE_CROSS_REPO_READ_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN`, `GITHUB_PAT`, and `MARKETPLACE_COINBASE_EVIDENCE_TOKEN`; validates the four terminal task records; validates the checked-in Site bounded projection; and grants no authority.

## Hosted controller retirement

The former `.github/workflows/advance-marketplace-coinbase-activation.yml` surface is removed under Site workflow-minimization batch 15.

That workflow previously supplied `secrets.MARKETPLACE_COINBASE_EVIDENCE_TOKEN` and `${{ github.token }}`, granted repository/issue write permissions, performed checkout/setup, committed and pushed controller state, and uploaded artifacts. Those mechanics violate the TV/TVC-only credential direction and are unnecessary after all four stop conditions are directly complete.

The separate hosted importer `.github/workflows/import-marketplace-coinbase-accessibility.yml` was already retired by batch 14 after the bounded Site projection became state-retained. No replacement GitHub-hosted scheduler, token path, issue mutation loop, commit/push loop, or artifact transport is created.

## Continuation semantics

The completed paper-accessibility projection is now state-retained rather than clock-driven. A future upstream change that genuinely creates new work must enter through a fresh admitted StegVerse task/claim and may use only its canonical credential/worker authority. It may not silently reactivate the retired GitHub token paths.

The retained invariant is:

```text
credential_authority: TV/TVC
non_tv_tvc_token_required: false
github_token_authority: NONE
paper_accessibility: retained evidence
live_trading_accessible: false
publication_authority: NOT_GRANTED
release_authority: NOT_GRANTED
execution_authority: NOT_GRANTED
live_authority: NOT_GRANTED
```

## Validation and release gate

Batch 15 may release only after exact-head validation proves:

- `scripts/advance_marketplace_coinbase_activation.py` passes against the v3 terminal task state without credential environment variables;
- Site Bootstrap Validate passes, including workflow inventory, session-claim validation, canonical Site application, ST-017 sandbox and authority-boundary checks;
- Site Handoff Orchestrator passes;
- Ecosystem Heartbeat Orchestration passes;
- Check StegFin Phone Projection passes without wallet authority;
- workflow inventory decreases exactly from 110 to 109, with 3 canonical, 106 migration-required operational and 0 placeholders;
- no product, runtime, financial or wallet activation is inferred from hosted validation.

## Canonical continuation

Workflow/token minimization continues under:

- `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`
- `data/session-work-claims.json`
- `StegVerse-Labs/Site#268`

After B15 release, `Site#131` may close completed because its bounded controller denominator is fully satisfied and no recurring Site controller responsibility remains.
