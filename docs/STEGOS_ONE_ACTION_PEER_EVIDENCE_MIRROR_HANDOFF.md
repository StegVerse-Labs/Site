# StegOS One-Action Peer Evidence Mirror Handoff

Updated: 2026-08-25T12:22:00-05:00

```text
goal_id: SITE-STEGOS-ONE-ACTION-PEER-EVIDENCE-488
canonical_issue: StegVerse-Labs/Site#488
source_owner: StegVerse-Labs/StegOS#23
branch: feat/stegos-one-action-peer-evidence-488
state: ACTIVE_UNIQUE_WORK
claim: data/session-work-claims.d/site-stegos-one-action-peer-evidence-488.json
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
site_authority: PROJECTION_MATERIALIZATION_ONLY
github_token_runtime_authority: NONE
render_authority: NONE
archive_ready: false
```

## Goal

Reduce capture of the genuinely distinct peer input required by StegOS#23 PR #48 from two user actions to one mobile-friendly action without changing Node genesis, identity, export schema, or authority.

## Implemented branch behavior

`stegos-node/index.html` now retains both existing controls:

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

## Validation

`tests/test_stegos_peer_capture.py` requires:

- exactly one old Register control, one old Export control, and one combined control;
- combined flow reuses `StegOSNodeProjection.registerDevice()`;
- Receipt #1 validation before export;
- unchanged bounded export schema and non-authority markers;
- no Site-side distinct-peer or Network-presence claim;
- prohibited identity/credential markers absent.

## Completion gates

```text
fresh bounded issue: COMPLETE
collision-safe claim: COMPLETE
one-action source implementation: COMPLETE_ON_BRANCH
focused tests: COMPLETE_ON_BRANCH
hosted validation: PENDING
merge: PENDING
direct deployed observation: PENDING
release to StegOS#23: PENDING
```

Source completion or CI success does not by itself prove public deployment.
