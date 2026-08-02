# Marketplace–Coinbase Accessibility Mirror Handoff

## Active goal and goal ID

- Goal ID: `MARKETPLACE-COINBASE-PAPER-ACCESSIBILITY-001`
- Repository: `StegVerse-Labs/Site`
- Branch: `main`
- Owner issue: `StegVerse-Labs/Site#131`
- Goal: project the verified Publisher paper chain into a public StegVerse accessibility state without granting live or financial authority.

## Authoritative files

- `scripts/import_marketplace_coinbase_accessibility.py`
- `tests/test_marketplace_coinbase_accessibility.py`
- `data/marketplace-coinbase-accessibility-status.json`
- `.github/workflows/import-marketplace-coinbase-accessibility.yml`
- this handoff

## Current state

```text
SITE_MARKETPLACE_COINBASE_PAPER_ACCESSIBILITY_ACTIVATED_AND_MACHINE_PERSISTED
```

The Site projection is display and continuity evidence only. It does not grant Coinbase credentials, funded-order authority, custody, withdrawal, publication, release, execution, or live financial authority.

## Verified upstream

- Publisher repository: `GCAT-BCAT-Engine/Publisher`
- Publisher status path: `data/marketplace-coinbase-release-evidence-status.json`
- Publisher status: `VERIFIED`
- Publisher status digest: `sha256:36a2f6da4b5af18375fd798ef954ec703ea719beefbab2d5949954b79ca1e477`
- Publisher machine persistence commit: `913a89d0ec867c3c9b570ec8352be554790a45f0`

## Completed work and evidence

- initial Site projection activation commit: `338abd5e008cda4af83a74ab3d1ac08e8e1c6103`
- machine-owned importer persistence commit: `99eeb59f757e4bdbaf020817b6ece5267349e93b`
- projection tests: commit `f0efc721b217d243d0d4569fcc7f9ccc69d1e9b7`
- workflow validation binding: commit `04dab58eafc6d47779f1196486c1384d5fe1ed3a`

Current checked-in projection:

```text
state = PAPER_ACCESSIBLE
publisher_status = VERIFIED
publisher_status_digest = sha256:36a2f6da4b5af18375fd798ef954ec703ea719beefbab2d5949954b79ca1e477
paper_trading_accessible = true
live_trading_accessible = false
publication_authority = NOT_GRANTED
release_authority = NOT_GRANTED
execution_authority = NOT_GRANTED
live_authority = NOT_GRANTED
```

Current projection digest:

```text
sha256:ce064993487fa872ef79a79ba43fb9991e29cb12cc1b57c6aeeb83c213d0fbd3
```

## Validation

The production Site contract was executed locally against the checked-in projection:

```bash
PYTHONPATH=. pytest -q tests/test_marketplace_coinbase_accessibility.py
```

Result:

```text
4 passed in 0.03s
```

The tests verify the committed projection digest, paper-only state, valid Publisher acceptance, authority-escalation rejection after re-signing, and tampered-status rejection.

The workflow `.github/workflows/import-marketplace-coinbase-accessibility.yml` is active and the bot commit `99eeb59f757e4bdbaf020817b6ece5267349e93b` proves machine persistence. The later test-bound workflow run ID, job logs, and artifact ID have not yet been directly recorded.

## Exact evidence bindings

- intent: `intent-marketplace-release-73a0543ddb27`
- packet: `sha256:ae990ce837cac3077a80c966b4e2d960f4158065dcec9c7fdc4da8b8f26ea89b`
- sequence 1: `sha256:f6f41875a5e066fc348cac68691c1d4fb77f3559282eb4ede26a398c87ee7e64`
- acknowledgement: `sha256:c76c0decad6b82f9356a58598ef5e217f92802dc657e9f5ed95cae9b8f77f0a3`
- sequence 2: `sha256:805000ab776b00863f5962514bcb8f843ccaa27ab9e0ac7821b92499b2e347f1`
- Publisher projection: `sha256:4ab30925412757058f3f752fad1d7e452e95dcddf3d2e272ecd9605cee97e8d9`
- publication receipt: `sha256:0dc495cf5f7de0b4610d5b4fc7732f3ddb888543fbe6c9a55ef07ad7f175d240`

## Machine-owned continuation

1. The hourly Site importer continues to revalidate Publisher state.
2. Invalid digest, schema, source, binding, or authority evidence becomes `REJECTED_UPSTREAM` and fails after preserving the bounded record.
3. Missing Publisher evidence becomes `PENDING_UPSTREAM` without halting adjacent Site development.
4. Crypto-bot finalization proceeds independently at `StegVerse-Labs/crypto-bot#6` and `.github/workflows/finalize-paper-release.yml`.

## Incomplete work

- Record the test-bound Site workflow run, job logs, and uploaded projection artifact when observable.
  - Owner: `StegVerse-Labs/Site#131`
  - Workflow: `.github/workflows/import-marketplace-coinbase-accessibility.yml`
  - Release condition: inspectable successful run and retained projection artifact.
- Complete exact paper-release tag evidence in crypto-bot.
  - Owner: `StegVerse-Labs/crypto-bot#6`
  - Required tag: `marketplace-coinbase-paper-v1.0.0`
  - Required target: `73a0543ddb27a88fd4913e7dcfa2127132299baa`

## Archive conditions

The Site portion is activated and self-continuing, but the complete session is not archive-ready until crypto-bot finalization and hosted evidence identities are preserved. No unspecified external task remains.

## Progress

- developed files: 5/5 = 100%
- deterministic validation: 100%
- Site integration: 100%
- complete session goal activation: 90%
