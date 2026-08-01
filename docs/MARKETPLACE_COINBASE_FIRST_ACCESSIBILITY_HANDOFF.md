# Marketplace–Coinbase First-Accessibility — StegVerse Site Handoff

## Determination

The crypto-bot paper-trading first-accessibility layer is active and PASS, but no equivalent bounded StegVerse Site projection existed before this work.

Current Site-side state:

```text
LAYER_BUILD_STARTED
ACTIVATION_PENDING_AUTHORITATIVE_WORKFLOW_RESULT
```

This work is parallel-safe with the active HIL upload task because it claims only:

```text
scripts/import_marketplace_coinbase_first_accessibility.py
.github/workflows/import-marketplace-coinbase-first-accessibility.yml
data/marketplace-coinbase-first-accessibility-status.json
docs/MARKETPLACE_COINBASE_FIRST_ACCESSIBILITY_HANDOFF.md
```

It does not touch the active HIL upload paths.

## Source

```text
repository: StegVerse-Labs/crypto-bot
path: data/first-accessibility-mark-status.json
verified source commit: 73a0543ddb27a88fd4913e7dcfa2127132299baa
verified workflow run: 30681165495
verified source receipt digest: sha256:5f6cc484c74f5795973cd2e6c52cc349e1cc464064841a29c3d28ed863e98758
verified outbound manifest digest: sha256:854bd485bb93a50a086778d21a33da33299ef3abc36552547a5bf41d9e797333
paper_trading_accessible: true
live_authority: NOT_GRANTED
```

## Installed Site components

```text
scripts/import_marketplace_coinbase_first_accessibility.py
.github/workflows/import-marketplace-coinbase-first-accessibility.yml
data/marketplace-coinbase-first-accessibility-status.json
```

The importer verifies:

- source schema;
- canonical receipt digest;
- PASS state;
- `paper_trading_accessible: true`;
- exact source commit format;
- workflow-run identity format;
- outbound manifest digest format;
- publication authority remains `NOT_GRANTED`;
- release authority remains `NOT_GRANTED`;
- live authority remains `NOT_GRANTED`;
- execution authority is no broader than `PAPER_ONLY`.

The Site output is projection-only and always preserves:

```text
publication_authority: NOT_GRANTED
release_authority: NOT_GRANTED
execution_authority: NOT_GRANTED
live_authority: NOT_GRANTED
custody_authority: NOT_GRANTED
withdrawal_authority: NOT_GRANTED
authority_effect: false
activation_effect: false
```

## Activation gate

Do not call this Site layer active until a workflow run is directly observed with:

```text
exact run ID
exact tested commit
job ID
all step conclusions
complete logs
artifact ID and digest
committed data/marketplace-coinbase-first-accessibility-status.json
status: ACCESSIBLE
valid status_digest
paper_trading_accessible: true
```

## Stop conditions

- `ACCESSIBLE`: activate the Site projection and coordinate any public surface or downstream consumer that requires it.
- `PENDING_SOURCE`: inspect the source fetch failure without substituting a manually copied file.
- `REJECTED`: inspect the exact source schema, digest, state, identity, or authority-boundary failure.
- no workflow result: verify Site Actions enablement and `contents: write` workflow permissions.

## Authority boundary

This Site layer is a verified public projection of repository-resident paper-trading accessibility. It is not:

- funded Coinbase authority;
- live-order authority;
- withdrawal or custody authority;
- publication or release authority;
- Marketplace settlement acceptance;
- Publisher reconstruction verification;
- final paper-release authorization.

## Next task

Observe the workflow triggered by this handoff commit, verify the complete run and artifact evidence, and activate the Site projection only if the committed output is `ACCESSIBLE` with a valid digest and all authority flags denied.
