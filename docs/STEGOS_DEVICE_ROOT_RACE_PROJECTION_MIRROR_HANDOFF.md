# StegOS Device Continuity Root-Race Projection Mirror Handoff

Updated: 2026-08-24T17:55:00-05:00

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

## Source evidence

Canonical StegOS repair:

```text
StegOS PR #39
merge: fc23a8b1cb2f350ba44c73dd868738f2fd6cb73d
CI: 32763906700 SUCCESS
canonical source: mobile/web-bootstrap/device-local-autostart.js
current canonical blob: 3927e2aa650f3267c53af73f3ef8bea2379805b9
```

Current Site projection before this lane still has blob `ef8d0c0da429365589d7559bfbcdc77cc3452ebd` and uses ordinary root `put()` establishment. It therefore does not yet contain the repaired cross-context create-if-absent behavior.

## Required semantics

The projected canonical source must include:

```text
objectStore.add({ key: key, value: value })
ConstraintError
addMetaIfAbsent
wonCreate
FAIL_CLOSED: device continuity root race lost without persisted winner
```

Only the winning context may append `stegos.web_device_continuity_root_receipt.v1`. A losing browser context must reuse the persisted winner.

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
exact canonical source projection: PENDING
projection tests: PENDING
session claim/orchestration validation: PENDING
merge: PENDING
direct deployed observation: PENDING
claim release to StegOS#23: PENDING
```

Source parity or CI success does not by itself prove public deployment.
