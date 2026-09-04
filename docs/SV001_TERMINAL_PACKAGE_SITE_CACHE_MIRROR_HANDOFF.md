# SV001 Terminal Package Site Cache Mirror Handoff

Updated: 2026-09-04
Repository: `StegVerse-Labs/Site`
Issue: #985
Goal: `SITE-SV001-TERMINAL-CACHE-985`

## Purpose

Propagate the canonical terminal StegVerse-001 portable WorkerCoordinator package to the current-iPhone Site surface and force the installed service-worker cache to refresh that package without rerunning SV001 and without widening Site authority.

## Canonical upstream state

Canonical WorkerCoordinator package owner: `StegVerse-Labs/.github`

Terminal package source lineage:
- `.github` issue #976
- `.github` merge `1064b0b5bf2c4316778b03e51d5d13cf7477f733`
- StegOS issue #186 / PR #187
- StegOS merge `4c50bbc776f48332267b3c4b3f061256c30028ce`
- exact terminal package Git blob `1483eb45263e2f7745e8c3e76dc19492efd44cf1`

The package binds the first canonical terminal G23:

```text
claim/fence: G23 / 23
canonical cycle receipt: sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35
canonical custody eligible: true
task state: COMPLETED
claim state: TERMINAL_NO_FURTHER_CLAIM
execution_authorized: false
terminal_reexecution_allowed: false
```

The reset-lineage 2026-09-04 G23 receipt `sha256:7b66f6cf260a46fcb8555d207cd868eaf2d31aa67372f0701841f91c648d00d4` remains authentic duplicate/non-custodial evidence and MUST NOT replace the first canonical terminal G23 in Master Records custody.

## Site defect being repaired

Before #985, Site still projected checkoutable package blob `0e3eaaec3fb20b759b79f2ab9070f002b73be741` and cumulative service worker blob `99d652dc961855b0b89d093a3f5ad2e027352849` with cache `stegos-web-bootstrap-v9`.

The service worker loads the WorkerCoordinator package only through Cache Storage. Replacing the server JSON alone would therefore allow an already-installed v9 worker to retain stale `HANDOFF_READY` bytes.

## Exact repair

```text
stegos-bootstrap/workercoordinator-portable-sv001.json
  -> exact canonical terminal blob 1483eb45263e2f7745e8c3e76dc19492efd44cf1

stegos-bootstrap/service-worker.js
  -> preserve complete current cumulative post-custody code
  -> change only CACHE_NAME from stegos-web-bootstrap-v9 to stegos-web-bootstrap-v10
  -> exact successor blob 048ae96f211e28314fa91c6a34cbc29ec13a2a26
```

The legacy exact-identity validator may admit only that explicit service-worker successor. No wildcard or semantic-equivalence admission is permitted.

## Authority boundary

```text
WorkerCoordinator claim/fence authority: StegVerse-Labs/.github WorkerCoordinator
credential authority: TV/TVC
Site role: exact materialization + browser cache refresh carrier
Site WorkerCoordinator authority: false
Site TVC issuance authority: false
Site Master Records custody authority: false
HB authority effect: NONE
GitHub token runtime authority: NONE
second user-operated machine required: false
```

The cache bump is deployment/materialization behavior only. It does not execute SV001, mint a claim/fence, issue or consume a TVC lease, establish Master Records custody, or establish SV002 observation/disposition.

## Completion distinction

Source completion requires exact package projection, exact v10 service-worker successor, exact-successor validator admission, focused #985 validation, Site Bootstrap PASS, Site Handoff Orchestrator PASS, and merge.

Authentic downstream runtime completion remains separate:

```text
first canonical terminal G23
-> current-iPhone Master Records portable custody
-> reconstruction PASS retained on device
-> SV002 adversarial observation/disposition
```

No source, merge, CI, deployment, cache version, or publication state may substitute for those runtime predicates.
