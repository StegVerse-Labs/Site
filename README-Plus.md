# MS-012 Release Directory Wiring Fix v1

Upload-safe bundle.

## Replaces

```text
transition-release-index.html
data/transition-release-index-v1.json
data/transition-replay-packet-v1.json
data/page-contracts-v1.json
```

## What this fixes

The previous MS-012 candidate added replay fixtures and verifier files but did not fully wire them into the public release directory.

This fix makes the release index expose:

```text
Replay Fixtures v1
data/transition-replay-fixtures-v1.json

Replay Verifier v1
data/transition-replay-verifier-v1.json
```

It also updates the replay packet JSON to point to those files.

## Done check

After upload:

```text
1. Wait for Pages deployment to finish.
2. Run Actions → Transition Replay Check.
3. Run Actions → Page Contract Check.
```

Expected:

```text
Both workflows pass.
MS-012 remains candidate until both pass.
```
