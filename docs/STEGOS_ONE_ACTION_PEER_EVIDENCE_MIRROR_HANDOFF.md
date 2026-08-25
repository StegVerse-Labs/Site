# StegOS One-Action Peer Evidence Mirror Handoff

Updated: 2026-08-25T12:35:00-05:00

```text
goal_id: SITE-STEGOS-ONE-ACTION-PEER-EVIDENCE-488
canonical_issue: StegVerse-Labs/Site#488
source_owner: StegVerse-Labs/StegOS#23
branch: main
state: COMPLETE_RELEASED_TO_STEGOS_23
claim: data/session-work-claims.d/site-stegos-one-action-peer-evidence-488.json
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
site_authority: PROJECTION_MATERIALIZATION_ONLY
github_token_runtime_authority: NONE
render_authority: NONE
archive_ready: true
```

## Result

The public StegOS Node surface now provides a directly deployment-observed one-action physical evidence capture path for a new browser/device context without changing Node genesis, identity, export schema, peer admission, Network, or activation authority.

The historical Site#468 and Site#480 lanes remain completed/released and were not reopened.

## Source implementation

Site PR #489 merged the source implementation:

```text
PR #489 merge: 8e75ab52c9b4275b6794d72212e04d131911b7d6
```

`/stegos-node/` retains:

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

## Observer ownership repair

The initial source observer exposed a stale requirement that completed Site#480 still be `CLAIMED_FOR_INTEGRATION`. Site#480 is correctly `RELEASED_TO_STEGOS_23`.

The checker was corrected to accept either active integration or durable release; Site#480 was not reactivated or rewritten.

Post-repair PR #489 evidence:

```text
StegOS Node Public Observation source run: 32877897785 SUCCESS
Site Handoff Orchestrator: 32877897808 SUCCESS
Ecosystem Heartbeat Orchestration: 32877897761 SUCCESS
```

The aggregate Site Bootstrap validator remains independently red in the separately owned StegFin Site#388 lane after canonical Site/#488 validation; this lane did not duplicate that ownership.

## Exact deployed-control proof

PR #490 advanced the public observer to require the exact new control markers in the fetched production HTML:

```text
id="capture-peer-evidence"
Register &amp; Export Evidence
```

```text
PR #490 merge: d6d566dbe85686ff53760137d36ab978df93f54d
```

After the #488 claim was transferred from implementation to validation posture, PR-time gates passed:

```text
Site Handoff Orchestrator: 32878440948 SUCCESS
Ecosystem Heartbeat Orchestration: 32878441009 SUCCESS
StegOS Node exact-control source observer: 32878440974 SUCCESS
```

The main-push observer then fetched the actual deployed surface:

```text
URL: https://stegverse.org/stegos-node/
workflow run: 32878544969 SUCCESS
job: 97902262412 SUCCESS
result: STEGOS_NODE_ONE_ACTION_PEER_PUBLIC_OBSERVATION_PASS
artifact: 9574852579
artifact zip sha256: bb04ad880242f4e91729cbf46b62c241a4511ec9137dbcea0e05a4d84e795cbe
```

The same direct observation also recorded:

```text
STEGOS_NODE_PUBLIC_OBSERVATION_PASS
STEGOS_NODE_OFFLINE_PROOF_PUBLIC_OBSERVATION_PASS
AUTHORITY_EFFECT=NONE
PHYSICAL_NODE_ACTIVATION_CLAIMED=false
NETWORK_ACTIVATION_CLAIMED=false
```

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

## Completion accounting

```text
fresh bounded issue: COMPLETE
collision-safe claim: COMPLETE_RELEASED
one-action source implementation: COMPLETE_MERGED
focused tests: COMPLETE
stale Site#480 observer assertion repair: COMPLETE
PR-time claim/orchestration validation: PASS
exact deployed-control observer: COMPLETE_MERGED
actual production fetch of one-action control: PASS
release to StegOS#23: COMPLETE
Site activation authority effect: NONE
```

## Canonical continuation

Do not create more Site peer-capture work unless a new deployed regression is observed.

Return to `StegVerse-Labs/StegOS#23`:

1. On one genuinely distinct physical browser/device context, open the deployed `/stegos-node/` surface and tap `Register & Export Evidence` once.
2. Feed that exact exported JSON into merged PR #48. Valid distinct evidence should automatically produce the two-real-Node `LOCAL_ONLY -> NETWORK_PRESENT` proof and replay.
3. After Network presence exists, capture real divergent and reciprocal-recovery relationship observations and feed them through merged PR #50 for `NETWORK_FRAGMENTED -> NETWORK_PRESENT` proof and replay.
4. Only after those real physical inputs pass should activation/release be evaluated.
