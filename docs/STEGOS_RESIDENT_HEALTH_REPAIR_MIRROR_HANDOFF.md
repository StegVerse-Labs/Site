# Resident StegOS Device Health and Bounded Repair Mirror Handoff

Repository: `StegVerse-Labs/Site`
Goal Task ID: `KV-ICLOUD-AUTOMATED-UPGRADE-001`
COSV ID: `40000100100000`
Updated: 2026-10-31
State: `BASELINE_MERGED / DISCOVERY_AND_HEALTH_CORRECTION_DRAFT`
Authority effect: `NONE`
Activation effect: `false`

## Objective

Provide one canonical resident StegOS device-health and bounded-repair client underneath MyKV. StegOS remains the minimal resident device/runtime substrate, but it is no longer a separate owner-facing installation destination. MyKV is the sole owner-facing install/launch surface and automatically loads the existing StegOS bootstrap, device-continuity, Node-continuity, and resident-health components on the same origin.

The resident StegOS/Node remains after a KV is installed or adopted on an owner-selected storage host. It is not a second KV and does not duplicate owner data.

## Source implementation

- `assets/stegos-resident-health.js` remains the canonical diagnostic and bounded-repair client. Its cached `last()` accessor is read-only; `diagnose()` calls existing local probes that can initialize or upgrade IndexedDB storage.
- `assets/stegverse-node-continuity.js` loads, in parser order, the existing StegOS schema compatibility layer, StegOS bootstrap implementation, device-local autostart/continuity layer, Node-continuity implementation, and resident-health client.
- `my-kv-install.html` invokes diagnosis and bounded repair automatically only after standalone/Home Screen launch, then opens canonical MyKV only when health is acceptable.
- `cloud-kv-peers.html` hides owner-selectable KV-host panels until the same resident-health contract reports `HEALTHY` and a registered Node is observed.

## Bounded repair contract

Repair remains limited to device-install infrastructure:

1. retain the pre-repair valid Node ID when one exists;
2. refresh or register the canonical same-origin StegOS service-worker shell through the existing bootstrap API;
3. establish a Node only when no valid Node exists;
4. re-diagnose and fail closed if a valid Node ID changes;
5. fail closed if already-visible KV relationship state changes during repair;
6. never create, replace, renumber, migrate, rehost, connect, sync, or expose a KV merely to repair resident device substrate.

Because MyKV loads the bootstrap implementation directly through the canonical Node-continuity loader, the owner is not required to visit a separate StegOS bootstrap site for normal installation or repair.

## Authority and identity boundaries

- Health results remain non-authorizing. Diagnostic probes can initialize or upgrade local storage; they must not be advertised as strictly read-only. Static discovery and the cached `last()` accessor perform no such probe.
- Device-substrate repair does not grant provider, KV, relationship, governance, credential, or execution authority.
- Interlock/InTr remains the authority boundary for state-changing governed KV transitions.
- MyKV is the single owner-facing install surface; StegOS is the underlying resident substrate.
- KV identity remains separate from its storage endpoint.
- No second user-operated device is required.

## Merge evidence

The shared resident-health client originally merged through Site #1351 at `3c78c5da968ae746ddaedfe6c68c3a148fc56f0c`, with documentation reconciliation through #1352 and claim retirement through #1353.

The unified MyKV integration merged through Site #1355. Final validated source head: `2aae799336464b290b230074992b2bf3899523d2`. Merge commit: `0d5df579e98ae44ad2f4358dd89efaae5d9809ed`. All 13 workflows observed at that final head completed successfully.

## Preserved adjacent state

The pending Google Drive KV #2 request `SITE-CLOUD-KV-4347408852127319cbda574f02e03edb` remains unchanged and must not be re-emitted or replaced by this integration.

## Runtime completion boundary

Runtime proof is now one owner-facing sequence: install MyKV, launch MyKV once, observe resident StegOS/Node health and continuity, then proceed to KV-host selection only after the substrate is healthy. No separate StegOS owner installation is part of the runtime contract. Source/CI/merge do not prove that physical current-iPhone sequence has occurred.

## 2026-10-31 bounded discovery and health correction

Authoring session: ChatGPT Work / 443534f2165a. Recovery goal:
`STEGOS-NODE-MANIFOLD-001`, canonical Registry coordination `ACTIVE`, checkout
`CHECKED_OUT`, COSV `40000100100000`; its worker claim is explicitly
`CURRENT_SESSION_COORDINATION_ONLY`, not a WorkerCoordinator grant. Existing
resident-health ownership remains `KV-ICLOUD-AUTOMATED-UPGRADE-001`. This draft
does not mint a claim, change Registry state, or establish runtime authority.

Source baseline: Site `ecc018aa2ec12b53d6b7aff2b70ebf10aa1e37ab`.

Implemented in this proposed revision:

- Read-only `stegos-node/capabilities.json`, linked from the Node page, describes
  existing interfaces and explicitly leaves remote runtime endpoints null.
- Shared JSON schema for the existing resident-health report. It distinguishes
  local substrate health from Node authority and Network membership.
- Existing health classifier now requires operational IndexedDB/WebCrypto probes
  from StegOS and an active, activated worker at the exact same-origin script path
  and scope. Capability-only, READY-prefix and worker-path lookalikes fail closed.
- Corrected diagnostic side-effect disclosure: existing probes call `openDb()`;
  their storage initialization/upgrade is not a read-only operation. No new
  probe, registration, repair or transport is added by discovery.
- Both existing loader cache keys and the existing MyKV publication observer
  reference the revised health client. Existing repair/Node/KV ownership remains.
- Dependency-free behavior tests and an exact-byte GET publication verifier are
  invoked by the existing resident-health unittest module. The shared folded
  validation step and catalog pins remain unchanged.

Local checks: 17 Node behavior/contract tests, 5 existing resident-health tests,
3 publication-verifier tests and 4 existing MyKV observer tests passed before draft submission (29 total). These use
fixtures, not the owner's browser or sovereign ledger. New contract checks reject
stale publication bytes, redirects and JSON served as HTML. No CI or public
deployment success is inferred from these checks.

Read-only live discovery attempt on 2026-10-31 returned HTTP 404 (Firecrawl scrape
`01a190ff-379a-7264-8b3a-96f797956bf8`). Publication is pending authorized integration;
there are no new published contract bytes to certify yet.

Integration disposition: `FAIL_CLOSED / SOURCE_PREPARATION_ONLY` until the
existing allocator/owner binds this exact branch and paths, independent review
and required checks pass, and protected expected-head integration is admitted.
Do not fabricate a pre-work claim or treat the central coordination checkout as
a runtime fence. Retry publication verification after that transition.

Prompt accounting: new session prompt 1. Recovery session counter was 28 and
Goal Prompt Count was UNRECONCILED; preserve that history plus this contribution.
No task-ID reset is performed. Registry owner must reconcile cumulative history
and retain the physical cycle/replay work under StegOS#23; local diagnostic work
belongs to the existing resident-health owner, not a new authority or goal.

Remaining independent work: owner claim/fence binding, exact-head independent
review/CI, protected integration and publication byte comparison. Original
manifold receipt/replay predicates remain separately open. Do not create a
release/tag or propagation-complete assertion from this draft.

