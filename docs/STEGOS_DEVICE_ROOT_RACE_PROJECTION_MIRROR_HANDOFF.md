# StegOS Device Continuity Root-Race Projection Mirror Handoff

Updated: 2026-08-24T23:04:00-05:00

```text
goal_id: SITE-STEGOS-DEVICE-ROOT-RACE-PROJECTION-485
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#485
canonical_source_owner: StegVerse-Labs/StegOS#19
source_repair_pr: StegVerse-Labs/StegOS#39
branch: main
claim: data/session-work-claims.d/site-stegos-device-root-race-projection-485.json
state: COMPLETE_RELEASED_TO_STEGOS_23
credential_authority: TV/TVC
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
github_token_runtime_authority: NONE
render_authority: NONE
archive_ready: true
```

## Goal result

The canonical StegOS cross-context device-continuity root establishment repair is now present in the public Site bootstrap projection **and directly observed from the deployed public asset**.

Historical Site#294 remains completed and was not reopened. This bounded maintenance lane existed only because real physical iPod evidence later exposed a duplicate-root race in StegOS#19.

## Canonical source repair

```text
StegOS PR #39
merge: fc23a8b1cb2f350ba44c73dd868738f2fd6cb73d
CI: 32763906700 SUCCESS
canonical source: mobile/web-bootstrap/device-local-autostart.js
canonical blob: 3927e2aa650f3267c53af73f3ef8bea2379805b9
```

The repaired semantics use atomic fixed-key IndexedDB `add()` create-if-absent behavior. A `ConstraintError` means another context won establishment; the loser reads/reuses the persisted winner and does not append a duplicate `stegos.web_device_continuity_root_receipt.v1`.

## Site exact projection

PR #486 projected the exact canonical repaired source and advanced the Site exact-source validator/tests.

```text
Site PR #486: MERGED
merge: eb525953a616b99bcfb40bc0d7af238542c15644
Site projected blob: 3927e2aa650f3267c53af73f3ef8bea2379805b9
canonical StegOS blob: 3927e2aa650f3267c53af73f3ef8bea2379805b9
exact byte parity: TRUE
```

PR-time hosted evidence:

```text
Site Handoff Orchestrator: SUCCESS
Ecosystem Heartbeat Orchestration: SUCCESS
Site Bootstrap Validate: SUCCESS for PR #486
```

## Direct public deployment proof

PR #487 installed a credential-free public observer and merged as:

```text
Site PR #487: MERGED
merge: e1cd86efff372bb641759e91bd160bd134620529
```

The main-push observer then fetched the actual deployed asset:

```text
URL: https://stegverse.org/stegos-bootstrap/device-local-autostart.js
workflow run: 32807454009 SUCCESS
job: 97680223226 SUCCESS
result: STEGOS_DEVICE_ROOT_RACE_PUBLIC_OBSERVATION_PASS
observed Git blob: 3927e2aa650f3267c53af73f3ef8bea2379805b9
expected Git blob: 3927e2aa650f3267c53af73f3ef8bea2379805b9
artifact: 9548620838
artifact zip sha256: f857f2bc4348a09e37e20c90b0aa4b98f5da2492628d7aab256a6529e75cabb3
```

The observer also verified the deployed asset contains:

```text
function addMetaIfAbsent(db, key, value)
objectStore(META_STORE).add({ key: key, value: value })
ConstraintError
wonCreate
persisted-winner reuse
no losing-context duplicate establishment receipt path
```

The observation explicitly recorded:

```text
AUTHORITY_EFFECT=NONE
PHYSICAL_NODE_ACTIVATION_CLAIMED=false
NETWORK_ACTIVATION_CLAIMED=false
```

## Independent aggregate failure accounting

The PR #487 aggregate Site Bootstrap run failed only at the separately owned StegFin phone projection validator because its canonical defer-script order is stale relative to current Site source. Before that independent failure, the same aggregate recorded:

```text
SESSION_WORK_CLAIMS_PASS
SITE_HANDOFF_ORCHESTRATION_PASS
ECOSYSTEM_HEARTBEAT_ORCHESTRATION_PASS
check_stegos_ipod_bootstrap_projection.py PASS inside canonical Site application
```

That StegFin lane remains owned by Site#388 and `docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md`; Site#485 did not duplicate or mutate it.

## Authority boundaries

```text
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
node_and_device_continuity_authority: StegVerse-Labs/StegOS
model_output_authority: NONE
non_tv_tvc_secret_or_token_used: false
github_token_runtime_authority: NONE
render_authority: NONE
physical_activation_claimed: false
network_activation_claimed: false
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
```

## Completion accounting

```text
fresh collision-safe claim: COMPLETE
canonical source repair: COMPLETE_MERGED_VALIDATED
exact Site projection: COMPLETE_MERGED
exact blob parity: PASS
projection validator/tests: COMPLETE
hosted claim/orchestration validation: PASS
public observer source: COMPLETE_MERGED
actual deployed asset fetch: PASS
actual deployed blob parity: PASS
claim release: RELEASED_TO_STEGOS_23
Site activation authority effect: NONE
```

## Canonical continuation

The Site projection lane is complete. Do not create additional first-node/root-race Site work unless a new deployed regression is observed.

Return to `StegVerse-Labs/StegOS#23` for:

1. current HB32 + separate Interlock observation against the reconciled real iPod chain;
2. genuinely distinct active peer Node evidence;
3. real Network Manifold transition proof and reconstruction.
