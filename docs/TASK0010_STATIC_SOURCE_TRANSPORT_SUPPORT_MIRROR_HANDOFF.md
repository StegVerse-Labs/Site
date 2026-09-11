# TASK-2026-0010 Static Source Transport Support Mirror Handoff

Updated: 2026-09-10
Repository: `StegVerse-Labs/Site`
Support Task: `SITE-TASK0010-STATIC-SOURCE-TRANSPORT-001`
Parent Goal: `GLOBAL-RUNTIME-EVIDENCE-CLOSURE-001`
Product Task: `TASK-2026-0010`
Status: `ACTIVE / EXACT SOURCE TRANSPORT SUPPORT IN VALIDATION`

## Purpose

Provide deterministic source/evidence transport for the exact current-iPhone TestFlight bootstrap bytes into the already-designated Site product branch without widening the authentic allocator claim or granting GitHub Actions runtime authority.

## Authentic upstream allocation evidence

The current-iPhone retained node journal recovered the authentic canonical allocation for `TASK-2026-0010`:

```text
selected task: TASK-2026-0010
claim registry generation: 6
fencing token: 6
claim state: CLAIM_GRANT_OBSERVED
canonical allocator receipt: ALLOCATION_COMPLETE
node journal replay: PASS
allocator mutation during recovery: false
```

The recovered artifact is evidence of the existing canonical grant; this support task does not mint, renew, replace, or reinterpret it.

## Exact pinned source

Canonical successor package:
`StegVerse-Labs/StegOS/release/current-iphone-site-projection/successors/current-iphone-testflight-static-bootstrap.json`

Pinned source commit:
`57f32a9e8b9dfbc70e66e0df3cb7de419fc0701b`

Required binary commitments:

```text
StegOSMobile-unsigned-device.ipa
sha256 557d559082bdefca5fcc69c86f342d8cc035c2d803d154de5ed45b5677f80c35
bytes 389564

stegos_current_iphone_ipa_signer_bg.wasm
sha256 699dc3054788d779ba7920e332c661ef7eac001156f93ab7b1fe1b64ee5a4b93
bytes 2277815

stegos_current_iphone_ipa_signer.js
sha256 17fe61cfdae43cbe5a1d1b211beb39838f58e982efdba90c7156fc36402f3adb
```

## Support transport contract

`.github/workflows/task0010-static-source-transport.yml` is source/evidence transport only. It:

1. runs only for the designated product branch `claim/current-iphone-testflight-static-bootstrap-r1` when its bounded task-state file changes;
2. fetches only the pinned public StegOS source commit;
3. verifies all fourteen source Git blob identities before commit;
4. verifies exact IPA/WASM byte counts and SHA-256 commitments;
5. commits only the fourteen product-task destination files;
6. performs no Apple signing, provider execution, claim selection, fencing, InTr admission, runtime activation, or publication decision.

GitHub Actions runtime authority remains `NONE`. Credential authority remains `TV/TVC`.

## Current validation state

Support PR: `StegVerse-Labs/Site#1219`.

The first validation exposed incomplete support-claim metadata and was repaired. A later orchestration attempt correctly rejected the branch because the support claim pointed at the not-yet-created product handoff. This dedicated support handoff is the remediation; the product handoff remains reserved for the actual fenced product branch.

## Required next sequence

1. Validate and merge support PR #1219.
2. Re-observe current Site `main` and fast-forward the designated product branch without force.
3. Before triggering transport, verify that the pinned successor package still contains the current KV-bound projection-consumer semantics; if it does not, reconcile StegOS source/successor first rather than transport stale bootstrap bytes.
4. If current, create the bounded Site product task-state file carrying exact G6/fence-6 provenance; this triggers the support transport.
5. Verify the transport commit changed only task-scoped destinations and every byte/hash matches pinned source.
6. Create the product mirror handoff and open the fenced Site projection PR.

## Authority invariants

```text
canonical allocator / WorkerCoordinator claim-fence authority: unchanged
Interlock/InTr transition authority: unchanged
TV/TVC credential/provider authority: unchanged
HB authority: observability only
GitHub Actions runtime authority: NONE
Site source transport authority: NONE
second user-operated machine required: false
Render fallback: forbidden / unused
```

## Manual work

None.
