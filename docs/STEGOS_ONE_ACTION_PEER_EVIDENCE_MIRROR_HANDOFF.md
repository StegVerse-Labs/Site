# StegOS One-Action Peer Evidence Mirror Handoff

Updated: 2026-08-25T12:31:00-05:00

```text
goal_id: SITE-STEGOS-ONE-ACTION-PEER-EVIDENCE-488
canonical_issue: StegVerse-Labs/Site#488
source_owner: StegVerse-Labs/StegOS#23
branch: validate/stegos-one-action-peer-public-488
state: DEPLOYED_VALIDATION_ACTIVE
claim: data/session-work-claims.d/site-stegos-one-action-peer-evidence-488.json
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
site_authority: PROJECTION_MATERIALIZATION_ONLY
github_token_runtime_authority: NONE
render_authority: NONE
archive_ready: false
```

## Goal

Reduce capture of the genuinely distinct peer input required by StegOS#23 PR #48 from two user actions to one mobile-friendly action without changing Node genesis, identity, export schema, or authority, then directly prove that exact control is deployed.

## Source implementation — merged

Site PR #489 merged the source implementation:

```text
PR #489 merge: 8e75ab52c9b4275b6794d72212e04d131911b7d6
```

`stegos-node/index.html` retains:

```text
Register Device
Export Node Evidence
```

and adds:

```text
Register & Export Evidence
```

The combined action:

```text
StegOSNodeProjection.registerDevice()
-> existing validated/reused local registration
-> historyProjection()
-> validateGenesis(Receipt #1)
-> validateOfflineReloadProof(optional existing proof)
-> build unchanged stegos.node_physical_evidence_export.v1
-> browser JSON download
```

The page explicitly states that StegOS, not Site, decides whether the resulting export is a genuinely distinct peer.

## Stale observer-ownership repair

The first PR #489 observer run exposed a stale validator requirement that historical Site#480 remain `CLAIMED_FOR_INTEGRATION`. Site#480 is correctly `RELEASED_TO_STEGOS_23` after its completed deployment proof.

The observer was repaired to accept either active integration or the durable released state. Site#480 was not reactivated or rewritten.

After repair:

```text
StegOS Node Public Observation PR source run: 32877897785 SUCCESS
Site Handoff Orchestrator: 32877897808 SUCCESS
Ecosystem Heartbeat Orchestration: 32877897761 SUCCESS
```

The aggregate Site Bootstrap job still failed later in the separately owned StegFin Site#388 lane. The canonical Site application and Site#488-specific checks had already passed; this lane does not duplicate Site#388.

## Exact deployed-control observer — active

The main-push observer after PR #489 proved the existing `/stegos-node/` surface remained publicly reachable and valid, but its marker set did not specifically require the new combined control.

PR #490 therefore advances `scripts/check_stegos_node_projection.py` to require in both source and live fetched HTML:

```text
id="capture-peer-evidence"
Register &amp; Export Evidence
```

A successful live run emits:

```text
STEGOS_NODE_ONE_ACTION_PEER_PUBLIC_OBSERVATION_PASS
AUTHORITY_EFFECT=NONE
PHYSICAL_NODE_ACTIVATION_CLAIMED=false
NETWORK_ACTIVATION_CLAIMED=false
```

PR #490 source validation run `32878194906` passed. Its initial handoff orchestration failed only because the still-active #488 claim named the implementation branch. The same claim has now been transferred—not duplicated—to `validate/stegos-one-action-peer-public-488` with `CLAIMED_FOR_VALIDATION` posture.

## Authority and privacy invariants

The combined action does not:

```text
create a different Node schema
mint Network presence
declare distinct peer admission
claim physical or Network activation
include raw registration random bytes
include hardware serials
include Apple account identity
use GitHub runtime credentials
use Render authority
```

The export retains:

```text
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
authority_effect: NONE
physical_activation_claimed: false
network_activation_claimed: false
```

## Completion gates

```text
fresh bounded issue: COMPLETE
collision-safe claim: COMPLETE
one-action source implementation: COMPLETE_MERGED
focused tests: COMPLETE
stale Site#480 observer assertion repair: COMPLETE
PR-time task-specific source observation: PASS
PR #490 orchestration after claim transfer: PENDING
PR #490 merge: PENDING
exact direct deployed one-action observation: PENDING
release to StegOS#23: PENDING
```

Source completion, merge, or generic public-surface observation does not by itself prove the exact one-action control is deployed.
