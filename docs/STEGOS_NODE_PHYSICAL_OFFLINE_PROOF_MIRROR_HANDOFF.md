# StegOS Node Physical Offline Proof Mirror Handoff

Updated: 2026-08-24T10:25:00-05:00

```text
goal_id: SITE-STEGOS-NODE-PHYSICAL-OFFLINE-PROOF-480
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#480
source_owner: StegVerse-Labs/StegOS#23
branch: main
claim: data/session-work-claims.d/site-stegos-node-physical-offline-proof-480.json
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
site_authority: PROJECTION_MATERIALIZATION_ONLY
authority_effect: NONE
```

## Goal

Make the real-device `Register Device` + offline-reload portion of StegOS#23 machine-recordable on the device itself, deploy that capability, and transfer the remaining physical proof to StegOS#23.

## Implemented proof semantics

A local offline proof is created only when:

```text
registered Node exists
AND canonical local receipt head exists
AND navigator.serviceWorker.controller is present
AND navigator.onLine == false
```

`stegos-node/stegos-node.js` persists `stegos.node_offline_reload_proof.v1` in the existing local IndexedDB metadata store. The proof binds Node ID, Interlock ID, persisted local receipt head, canonical-chain receipt count, service-worker control observation, browser-offline observation, descriptive observation time, and deterministic proof digest.

It explicitly states:

```text
current_network_required=false
network_topology_claimed=false
heartbeat_interlock_observation_verified=false
physical_activation_claimed=false
network_activation_claimed=false
authority_effect=NONE
credential_authority=TV/TVC
```

`navigator.onLine=false` is accepted only as browser-local offline evidence. It does not prove StegOS Network absence, fragmentation, or external topology state.

## Export integration

`stegos.node_physical_evidence_export.v1` includes:

```text
offline_reload_proof: <validated proof or null>
network_activation_claimed: false
```

Absence remains `null`; the export never fabricates offline validation. The UI exposes `Offline Reload Proof: Not yet observed | Recorded` as a human projection only.

## Source and merge evidence

```text
Site PR #481: MERGED
merge: 41eed6f76e58f054efda6a3d1be9e09ed4c4c5df
source/PR hosted gates: PASS
```

## Exact deployed offline-proof capability observation — PASS

Because the connector cannot enumerate push/main workflow runs, validation-only PR #482 temporarily caused the existing hosted observer to require the live deployment contract on a PR-visible run. PR #482 was closed without merge after evidence capture, so Site `main` was not changed by the validation carrier.

Hosted evidence:

```text
validation PR: Site #482 CLOSED / NOT MERGED
validation head: 7cde3aae5dc8aeea71754262aaa4ce11ab1560d4
workflow: StegOS Node Public Observation
run: 32744547474 SUCCESS
job: 97486821322 SUCCESS
observed URL: https://stegverse.org/stegos-node/
STEGOS_NODE_PROJECTION_PASS
STEGOS_NODE_OFFLINE_PROOF_SOURCE_PASS
STEGOS_NODE_PUBLIC_OBSERVATION_PASS
STEGOS_NODE_OFFLINE_PROOF_PUBLIC_OBSERVATION_PASS
AUTHORITY_EFFECT=NONE
PHYSICAL_NODE_ACTIVATION_CLAIMED=false
NETWORK_ACTIVATION_CLAIMED=false
artifact: 9526492248
artifact digest: sha256:e677b11989d2aeaa79d6726f710bd30eb9f717af67a4209207a7455db1a11082
```

The validation-only PR's general Site orchestration/bootstrap checks failed because that temporary branch was intentionally not the implementation branch recorded by the active claim. The task-specific live observer itself passed source validation, exact deployed observation, receipt construction, and artifact upload. PR #482 was then closed unmerged; no production branch inherited the validation-only workflow condition.

## Authority boundaries

1. Site remains projection/materialization only.
2. Browser offline evidence does not establish Network topology.
3. Public deployment evidence does not establish a physical Node event.
4. HeartBeat authority remains `StegVerse-Labs/.github`.
5. TV/TVC remains sole credential/route authority.
6. No GitHub-token runtime authority or Render production authority is created.
7. Observation/export artifacts have `authority_effect=NONE`.

## Completion / transfer

```text
claim admission: COMPLETE
source implementation: COMPLETE_MERGED_VALIDATED
source contract tests: PASS
hosted Site source validation: PASS
deployed offline-proof capability: PASS_DIRECT_HOSTED_OBSERVATION
real physical Receipt #1: TRANSFERRED_TO_STEGOS_23 / PENDING_REAL_DEVICE_EVENT
real physical offline reload proof: TRANSFERRED_TO_STEGOS_23 / PENDING_REAL_DEVICE_EVENT
real physical evidence export: TRANSFERRED_TO_STEGOS_23 / PENDING_REAL_ARTIFACT
StegOS validation of real exported proof: TRANSFERRED_TO_STEGOS_23 / PENDING_REAL_ARTIFACT
```

Site has completed the software, publication, and deployment-evidence responsibilities for this lane. Remaining completion is irreducibly physical and belongs to `StegVerse-Labs/StegOS#23`.

Do not infer physical Node or Network activation from this Site completion.

## Site#1509 — live observation follows the bootstrap graph (2026-10-29)

Existing claim `SITE-STEGOS-NODE-OFFLINE-PRECACHE-20260922` is rebound on the PR branch `claude/site-main-stegos-node-live-impl`, following verified merged predecessor Site #1455 (`804e58f0576138aef26fb013968ae0430f74fb54`; branch deleted). This is a source-level lane reconciliation, not a new WorkerCoordinator claim or sovereign admission (Goal StegVerse-org/.github#164).

Since a3bd73f0c the deployed `stegos-node.js` is the parser-load bootstrap that `document.write`s `stegos-node-impl.js`. The source path already validated the implementation file; the live path checked implementation markers against the bootstrap alone, so every post-deployment `StegOS Node Public Observation` run failed closed regardless of what was served. `scripts/check_stegos_node_projection_impl.py` now follows the document.written scripts from the deployed directory, validates markers on bootstrap plus loaded scripts, and applies the same precache script-graph invariant as the source path. `tests/test_stegos_node_live_observation.py` (stdlib unittest) serves the repository tree as the CNAME origin through the observer's fetch seam. Evidence class: SOURCE + LOCAL_TEST; the deployed observation is re-attempted by the next completed Pages deployment or a manual dispatch. No physical Node or Network activation is claimed.

Review follow-ups on the same lane:

- Origin binding: written script URLs are resolved against the deployed directory and must be `https` on the base URL's exact host. Anything else (`//evil.example/x.js`, `https://evil.example/y.js`, `http://` on the same host) returns a single `live observation failed: bootstrap writes off-origin script …` refusal, and nothing foreign is fetched.
- CI wiring gap: `.github/workflows/stegos-node-public-observation.yml` is pinned byte-for-byte in `control/workflow-surface-registry.json` (`KEEP_EXISTING_SURFACE_UNCHANGED`, KEEP_PENDING_LATER_BATCH). Its `pull_request.paths` therefore still omit `scripts/check_stegos_node_projection_impl.py` and `tests/test_stegos_node_live_observation.py`, and its PR step runs only `tests.test_hil_intr_node_sync`. Following the registry's own rule ("a new check is a group in tools/tasks/task_catalog.json, never a new workflow file"), the test runs as catalog group `stegos-node-live-observation.verify` on every pull_request and push through the stable validation dispatcher. When the later G17 batch dispositions that surface, its PR paths and unittest line should be reconciled with this group (fold it or drop the duplication).
