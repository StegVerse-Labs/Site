# State Transition Receipts v1

Upload-safe bundle. No leading-dot paths.

This bundle replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

It adds replayable state transition receipts for experiment ledger rows.

## New generated outputs

```text
data/transition-receipts.json
data/receipts/RCPT-*.json
```

## Page section order

```text
Run Manifests
Knowledge Deltas
Recent Ledger Rows
State Transition Receipts
Consequential Test Changelog
```

## Important

This patch does not promote evidence to 5/5 Receipt-backed yet. It only creates and exposes replayable receipts. A later verifier should replay receipt JSON before any 5/5 promotion.
