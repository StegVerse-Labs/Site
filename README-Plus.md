# MS-012 Independent Replay Check Candidate v1

Upload-safe bundle.

## Files

```text
transition-replay-packet.html
data/transition-replay-fixtures-v1.json
data/transition-replay-verifier-v1.json
data/page-contracts-v1.json
tools/transition_replay_check.py
github/workflows/transition-replay-check.yml
```

Note: `github/workflows/transition-replay-check.yml` is displayed without the leading dot here. The bundle preserves the correct `.github/workflows/transition-replay-check.yml` path for GitHub upload.

## What this does

This creates the first narrow independent replay packet for:

```text
T13 — Receipt-Bound Transition
T14 — Reconstruction Transition
```

## Done checks

After upload:

```text
1. Wait for Pages deployment to finish.
2. Run Actions → Transition Replay Check.
3. Confirm the workflow passes.
4. Run Actions → Page Contract Check.
5. Confirm the workflow passes.
```

## Release rule

MS-012 remains a candidate until both workflows pass.
