# iPhone Heartbeat Transition Projection Mirror Handoff

Updated: `2026-08-17T10:04:00-05:00`

## Active goal and ownership

```text
goal_id: SITE-IPHONE-HB30-TRANSITION-CAPSULE-322
originating_goal: publish the canonical non-authorizing HB29->HB30 transition capsule so CURRENT_USER_IPHONE can produce the portable receipt without another machine or NON-TV/TVC secret/token
repository: StegVerse-Labs/Site
branch: feat/heartbeat-transition-iphone-322
canonical_issue: StegVerse-Labs/Site#322
canonical_source_owner: StegVerse-Labs/.github#209
source_merge: 9015c67d8356bf7e9e3db71488b2468581829e7a
source_contract: StegVerse-Labs/.github/management/SHWP_IPHONE_TRANSITION_CAPSULE_CONTRACT.json
credential_authority: TV/TVC
credential_requirement: NONE
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
github_token_runtime_authority: NONE
render_production_authority: NONE
active_claim: SITE-IPHONE-HB30-TRANSITION-CAPSULE-322-20260817
claim_state: CLAIMED_FOR_INTEGRATION
```

## Authoritative sources read

Before mutation this lane read:

- `docs/SITE_MIRROR_HANDOFF.md`
- `data/site-orchestration-state.json`
- `data/ecosystem-heartbeat-state.json`
- `data/session-work-claims.json`
- `StegVerse-Labs/.github/docs/ORG_MIRROR_HANDOFF.md`
- `StegVerse-Labs/.github/management/SHWP_STATE_TRANSITION_CONTINUITY_CONTRACT.json`
- `StegVerse-Labs/.github/docs/IPHONE_HEARTBEAT_TRANSITION_MIRROR_HANDOFF.md`

The active HIL upload work owns `humans-as-interoperability-layer.html`, `assets/hil-*`, and `scripts/check_hil_*upload*`. This capsule uses distinct `heartbeat-transition/**` paths and does not modify the upload surface.

The stale Site #298 admitted-inference claim is reconciled to its already-proven terminal state in this branch: source projection PR #309 merged as `1f5ab3acde796d2787edf0493c19e193ca72eda4`, Pages build `1156543676` was built from that exact merge, Site #298 is closed completed, and physical continuation is `StegVerse-Labs/StegOS#15`.

## Installed browser capsule

```text
heartbeat-transition/index.html
heartbeat-transition/heartbeat-transition.js
scripts/check_iphone_heartbeat_transition_projection.py
```

The browser capsule is intentionally computation-only. It performs no network request and uses no credential. Readiness fails closed unless all of the following are true:

```text
origin = https://stegverse.org
secure_context = true
WebCrypto = available
user_agent = iPhone
```

The user-visible action emits exactly one bounded portable candidate receipt for the canonical transition:

```text
seed repository: StegVerse-Labs/.github
legacy state ref: control/heartbeat-state.json
legacy git blob: d18d57d83cf19b7799cde1a1b4487e496eca7f76
legacy epoch/generation: 29/29
successor epoch/generation: 30/30
successor authority_effect: NONE
physical execution surface: CURRENT_USER_IPHONE
credential authority: TV/TVC
credential requirement: NONE
github_token_runtime_authority: NONE
non_tv_tvc_secret_or_token_used: false
worker authority: false
claim/fence mutation: false
route authority: false
wallet authority: false
model output authority: NONE
another physical machine required: false
```

The JS recursively canonicalizes JSON with sorted object keys, computes SHA-256 using `crypto.subtle.digest`, appends `receipt_sha256`, stores the receipt only in browser `localStorage`, displays it, and permits copy/share preservation. No Authorization/Bearer header, GitHub API, provider endpoint, wallet endpoint, WebSocket, EventSource, XHR, or fetch path exists.

## Critical activation distinction

The browser state `HB30_CANDIDATE_EMITTED` is **not** canonical HB30 activation. Site is transport/materialization only.

The completion chain remains:

```text
Site exact capsule publication
-> CURRENT_USER_IPHONE physical receipt emission
-> preserve exact receipt evidence
-> StegVerse-Labs/.github independent receipt verifier revalidates immutable HB29
-> non-hosted canonical materializer writes HB30 carrier/cutover/transition state without changing HB29
-> independent WorkerCoordinator observes HB30+
-> reconstruction/no-duplicate-claim predicates PASS
-> .github#60 continues local-model -> TVC -> LLM-adapter -> Master Records
```

No second non-StegVerse machine is part of the required chain. If any implementation later makes one necessary, that implementation remains incomplete.

## Validation

Canonical projection validator:

```text
python scripts/check_iphone_heartbeat_transition_projection.py
```

It verifies source merge/blob/contract constants, exact HB29/HB30 bounds, TV/TVC/NONE authority semantics, iPhone + secure-context/WebCrypto gates, canonical SHA-256 generation, local persistence, absence of network/credential execution markers, and the publication-vs-activation boundary.

This validator must be bound into the existing canonical Site application aggregate; no new standalone GitHub workflow should be created. Hosted validation remains source/publication evidence only.

## Required publication evidence

```text
projection validator: PASS
canonical Site application aggregate: PASS
Site Handoff Orchestrator: PASS
Ecosystem Heartbeat Orchestration: PASS
Site Bootstrap Validate: PASS
fresh-current-main Site PR: MERGED
GitHub Pages: BUILT from exact merge
```

## Physical continuation

After exact Pages publication, open the published capsule on the current iPhone. The only physical output required from Site is the exact portable receipt and its visible SHA-256. The canonical `.github` verifier/materializer owns acceptance and HB30 materialization. WorkerCoordinator remains independently machine-owned.

## Collision boundaries

- Site is transport/materialization only.
- Do not acquire, renew, release, or modify G18's claim/fence/lease.
- Do not grant WorkerCoordinator authority.
- Do not mint TVC route/credential authority.
- Do not introduce or consume NON-TV/TVC secrets or tokens.
- Do not use Render, Vercel, Cloudflare, or GitHub-hosted execution as production heartbeat authority.
- Do not modify HIL upload-owned paths.
- Do not imply HB30 from source merge, CI, Pages build, browser load, or receipt emission alone.

## Completion accounting

```text
developed_files: 4/4 capsule/projection surfaces installed on branch
scaffolding_or_stubs: 0
missing_required_files: 0
validation: source validator installed, execution pending
integration: source -> Site projection installed; aggregate binding + merge + Pages pending
goal_activation: 45% TO PHYSICAL PORTABLE TRANSITION RECEIPT
session_consolidation: 8/8 prior goal groups durable; HB repair is the current distinct-support lane
archive_state: NOT_READY_CURRENT_HB_REPAIR_WORK_REMAINS
```
