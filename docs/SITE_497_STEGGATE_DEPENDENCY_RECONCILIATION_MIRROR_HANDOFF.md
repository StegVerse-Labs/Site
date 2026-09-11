# Site #497 StegGate Dependency Reconciliation Mirror Handoff

Updated: 2026-09-10
Repository: `StegVerse-Labs/Site`
Goal: `KV-CONNECTION-REVALIDATION-WORKER-001`
Site lane: `SITE-497-THIRD-PARTY-DEPENDENCY-ERADICATION`
COSV: `50000000102000`
Upstream handoff: `StegVerse-Labs/StegCore/docs/STEGGATE_HOSTED_CARRIER_RETIREMENT_MIRROR_HANDOFF.md`
Current continuation branch: `fix/site-497-remove-render-20260909`

## Merged provider-independent evidence

- PR #1155 merged external recovery-bundle retention, off-GitHub restore, and off-GitHub validation for archive SHA-256 `a9b81dfb7a34e7b4c627145e6ab817466b92c1ea9176fc41f76e420a2b201b0f` with 3400 verified entries.
- PR #1158 merged provider-neutral `STEGVERSE_SITE_STATIC_PUBLICATION_V1` materialization and exact per-file validation.
- PR #1162 merged the fail-closed authentic publication-observation evidence seam.
- PR #1168 merged the no-Render remediation at `9d9ffb7ef5cee256588dcdd3790846b5943867da` after all exact-head Site gates passed.

## No-hosted-origin invariant

Render is prohibited for Site #497 recovery/publication. `data/publication-origin-selection-2026-09-09.json` requires `selection_state=NO_HOSTED_ORIGIN_SELECTED`, `selected_origin=null`, and includes `RENDER` in `prohibited_providers_for_this_lane`. Historical Render service/deploy identifiers remain only as `REJECTED_DO_NOT_USE` audit evidence and are ineligible for equivalence proof or DNS binding.

A stale post-#1168 contradiction was found on current main: `data/publication-equivalence-contract.json` and `scripts/check_site_publication_artifact.py` still required the previously rejected Render origin. This continuation removes that contradiction.

## Resident publication rendezvous continuation

This branch now adds `data/resident-publication-rendezvous-contract.json` and `scripts/check_resident_publication_rendezvous_contract.py` and binds them into the focused Site #497 workflow.

The contract requires:

```text
runtime class = RESIDENT_STEGVERSE
hosted provider required = false
hosted provider allowed = false
Render allowed = false
GitHub Actions as runtime = false
Cloudflare quick tunnel allowed = false
resident executor observation required = true
resident endpoint identity observation required = true
exact artifact-manifest binding required = true
independent HTTP readback required = true
exact path + SHA-256 equivalence required = true
canonical-domain and TLS proof = separate authentic evidence
```

Current resident/public observations remain fail-closed and false until authentic runtime evidence exists. Source/CI validation cannot upgrade them.

## README maintenance

Root `README.md` was reviewed against this continuation. Its provider-independent boundary remains accurate; no broad README rewrite is required.

## Current truth

```text
canonical runtime = RESIDENT_STEGVERSE
GitHub Actions runtime required = false
hosted publication origin selected = false
Render allowed = false
provider-neutral static publication artifact = MERGED_SOURCE_VALIDATED
publication observation evidence contract = MERGED_SOURCE_VALIDATED
resident publication rendezvous contract = SOURCE_IMPLEMENTED_VALIDATION_PENDING
resident executor observed = false
resident endpoint identity observed = false
independent public reachability = PENDING
exact public-content equivalence proof = PENDING
canonical-domain DNS/TLS recovery proof = PENDING
```

## Remaining work

1. Validate and merge this stale-Render-contract remediation plus resident rendezvous contract.
2. Feed authentic resident executor + endpoint identity evidence into the resident rendezvous contract from the sovereign runtime lane; do not synthesize it in Site or CI.
3. Bind the exact publication artifact manifest to that authentic resident rendezvous.
4. Perform independent HTTP byte readback and exact-path/SHA-256 comparison against the resident endpoint.
5. Execute controlled `stegverse.org` DNS/TLS recovery only after resident equivalence is proven.
6. At release readiness, tag/release and create the separate downstream propagation-verification task for StegVerse-Labs/Sit, GCAT-BCAT-Engine/Publisher, admissibility-wiki, and stegguardian-wiki.

## Manual work

None for this source continuation. Historical Render service deletion remains outside the connected Render tool's capabilities and is not required for canonical Site execution because Render is fail-closed and prohibited by contract.
