# StegOS Device Continuity Root-Race Projection Mirror Handoff

Updated: 2026-08-24T17:58:00-05:00

```text
goal_id: SITE-STEGOS-DEVICE-ROOT-RACE-PROJECTION-485
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#485
canonical_source_owner: StegVerse-Labs/StegOS#19
source_repair_pr: StegVerse-Labs/StegOS#39
branch: fix/stegos-device-root-race-projection-485
claim: data/session-work-claims.d/site-stegos-device-root-race-projection-485.json
state: ACTIVE_UNIQUE_WORK
credential_authority: TV/TVC
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
github_token_runtime_authority: NONE
render_authority: NONE
```

## Goal

Project the exact canonical StegOS cross-context device-continuity root establishment repair to the public `stegos-bootstrap/device-local-autostart.js` surface and prove the repaired bytes are actually deployed.

Historical Site#294 remains completed and is not reopened. This is a new bounded projection maintenance lane created because real physical iPod evidence exposed a root-creation race after #294 completed.

## Canonical source evidence

```text
StegOS PR #39
merge: fc23a8b1cb2f350ba44c73dd868738f2fd6cb73d
CI: 32763906700 SUCCESS
canonical source: mobile/web-bootstrap/device-local-autostart.js
canonical blob: 3927e2aa650f3267c53af73f3ef8bea2379805b9
```

Before this lane, Site still projected blob `ef8d0c0da429365589d7559bfbcdc77cc3452ebd` with ordinary `put()` root establishment.

## Branch implementation

The Site branch now contains the exact canonical repaired bytes:

```text
Site path: stegos-bootstrap/device-local-autostart.js
Site projected blob: 3927e2aa650f3267c53af73f3ef8bea2379805b9
canonical StegOS blob: 3927e2aa650f3267c53af73f3ef8bea2379805b9
exact byte parity: TRUE
projection commit: c263046276f557e687b8c25f05ad4a2bc4255575
```

The canonical repair includes:

```text
objectStore(META_STORE).add({ key: key, value: value })
ConstraintError
addMetaIfAbsent
wonCreate
FAIL_CLOSED: device continuity root race lost without persisted winner
```

Only the winning context may append `stegos.web_device_continuity_root_receipt.v1`. A losing context reads/reuses the persisted winner and cannot append the establishment receipt.

The exact-source validator was advanced at commit `0e07c87893a8632fcb87d9daf41fcf7dc35abf89` to require canonical blob `3927e2aa...`, source merge `fc23a8b1...`, atomic-create markers, and zero duplicate-root-receipt permission.

The projection tests were advanced at commit `94dfa0cd68758ea2bdda9521b32c93746a63d43f` to verify exact blob identity, the current source provenance, create-if-absent semantics, the losing-context no-append branch, and the unchanged local/fail-closed authority boundary.

## Authority boundaries

Site does not own Node identity, device continuity truth, historical physical evidence, HeartBeat, credentials/routes, model execution, or activation.

```text
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
non_tv_tvc_secret_or_token_used: false
github_token_runtime_authority: NONE
render_authority: NONE
physical_activation_claimed: false
network_activation_claimed: false
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
```

## Completion gates

```text
fresh claim: COMPLETE
exact canonical source projection: COMPLETE_ON_BRANCH
exact source blob parity: PASS
validator advancement: COMPLETE_ON_BRANCH
projection tests advancement: COMPLETE_ON_BRANCH
hosted session claim/orchestration validation: PENDING
hosted bootstrap/projection validation: PENDING
merge: PENDING
direct deployed observation: PENDING
claim release to StegOS#23: PENDING
```

Source parity or CI success does not by itself prove public deployment.
