# Site Mirror Closure Guard

## Purpose

This packet defines the no-secret Site closure guard workflow and the boundaries it must preserve.

The guard exists to verify closure-readiness documentation without dispatching Publisher, consuming cross-repo credentials, writing repository contents, or claiming activation.

## Guard Workflow

```text
github/workflows/site-mirror-closure-guard.yml
```

Actual repository path:

```text
.github/workflows/site-mirror-closure-guard.yml
```

## Required Guard Behavior

```text
1. Run on workflow_dispatch.
2. Run on pushes that affect Site mirror closure documentation or checkers.
3. Use read-only contents permission.
4. Check docs/SITE_MIRROR_HANDOFF.md through scripts/check_site_mirror_handoff.py.
5. Check docs/SITE_MIRROR_CLOSURE_NEXT_BUILD.md through scripts/check_site_mirror_closure_next_build.py.
6. Check this guard packet through scripts/check_site_mirror_closure_guard.py.
7. Write a workflow summary stating that Publisher closure remains required before activation can be claimed.
```

## Forbidden Guard Behavior

The guard workflow must not contain or perform:

```text
secrets.
STEGVERSE_REPO_SYNC_TOKEN
contents: write
curl -sS
workflow_dispatches
git push
Activation Ready: `yes`
Activation state: activated
```

## Non-Activation Rule

The closure guard confirms documentation and checker integrity only.

It does not prove:

```text
Publisher workflow run URL
Publisher verification receipt artifact
Site evidence artifact
Publisher closure receipt
Publisher verification tracker activation commit
Publisher activation-status update commit
```

## Completion Condition

This packet is complete when:

```text
python scripts/check_site_mirror_closure_guard.py
```

passes.

## Archive Readiness

This file is sufficient for a future session to verify the Site mirror closure guard boundary without prior chat context.
