# Site Stale Pull Request Reconciliation

This record reconciles Site PRs `#8`, `#9`, and `#10` against current `main`.

```text
PR #8: stale and superseded; repair-queue validator installed directly on main
PR #9: stale and conflicted; useful workflow guards and validator reconciled onto main
PR #10: stale and conflicted; Governance Observatory Boundary already present on main
```

Current-main reconciliation commits:

```text
e91c767b3342725d4e279fcc338dc6b43b2178b5
1c4a8ae4c0bfd655e136bb48babd610ac8456864
e9e0f79717ed6c490c19058f5c74ea9804680f3e
250831149b9c56fce68ff2a51a31be44e59905d5
```

`scripts/check_repo_operations_repair_queue.py` is registered in both `validate` and `public-guard`.

Closing the stale PRs does not merge their branches, resolve conflicts into current `main`, grant deployment authority, or infer validation success. Current-main checks remain authoritative.
