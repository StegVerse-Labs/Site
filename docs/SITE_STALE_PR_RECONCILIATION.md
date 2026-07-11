# Site Stale Pull Request Reconciliation

## Scope

This record reconciles Site PRs `#8`, `#9`, and `#10` against current `main`.

## Findings

```text
PR #8
Status: stale and superseded by PR #9
Useful content: repair-queue validator
Current-main disposition: validator installed directly on main

PR #9
Status: stale and conflicted with current task-runner and repair-queue state
Useful content:
- main-only generated-state publication
- main-only Pages deployment
- read-only repair-queue validator
Current-main disposition:
- publication and deployment guards already present
- rebase-safe publication already present
- validator installed directly on main
- stale PR references removed from repair queue

PR #10
Status: stale and conflicted with docs/SITE_PUBLIC_PATHS.md
Useful content: Governance Observatory Boundary
Current-main disposition: equivalent boundary already present on main
```

## Current-main commits

```text
e91c767b3342725d4e279fcc338dc6b43b2178b5
1c4a8ae4c0bfd655e136bb48babd610ac8456864
e9e0f79717ed6c490c19058f5c74ea9804680f3e
250831149b9c56fce68ff2a51a31be44e59905d5
```

## Validation integration

```text
scripts/check_repo_operations_repair_queue.py
```

is registered in both:

```text
python scripts/run_site_task.py validate
python scripts/run_site_task.py public-guard
```

## Reconciliation result

```text
PR #8: superseded; close without merge
PR #9: superseded by current-main implementation; close without merge
PR #10: useful content already represented on current main; close without merge
```

## Boundary

Closing these stale PRs does not merge their branches, resolve their conflicts into current `main`, grant deployment authority, or infer validation success. Current-main checks remain authoritative.
