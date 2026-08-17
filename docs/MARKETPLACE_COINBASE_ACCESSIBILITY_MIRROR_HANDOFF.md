# Marketplace–Coinbase Accessibility Mirror Handoff

## Canonical authority

```text
goal_id: MARKETPLACE-COINBASE-PAPER-ACCESSIBILITY-001
released_task: SITE-MARKETPLACE-COINBASE-PROJECTION-LOCAL-IMPORT-CORRECTION-20260817
repository: StegVerse-Labs/Site
canonical_branch: main
owner_issue: Site#131
parent_cleanup: Site#268
cross_repository_owner: StegVerse-Labs/StegVerse-Healer#8
scheduler_owner: SHWP-HEALER-SOVEREIGN-SCHEDULER-001
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
github_production_authority: NONE
```

## Product boundary

`PAPER_ACCESSIBLE` remains true; live trading remains false; publication, release, execution, live, and financial authority remain `NOT_GRANTED`. USER_ONLY remains the sole StegFin signing/broadcast authority.

## Released local-only integration

Healer PR #9 installed fixed target `marketplace-coinbase-local-projection-import` using already-materialized Site and Publisher roots. Site PR #352 completes that contract: the Site importer now requires `STEGVERSE_REPO_ROOTS_JSON`, reads `GCAT-BCAT-Engine/Publisher/data/marketplace-coinbase-release-evidence-status.json` locally, removes `raw.githubusercontent.com` acquisition, refuses GitHub/project credential environments, and fails closed to `PENDING_UPSTREAM` if local evidence is unavailable. Existing digest, schema, VERIFIED-state, paper-only, and authority-escalation checks remain intact.

```text
PR #352 final head: 1706f22da79fd8e8c90cbad4d9ff5f088410142d
merge: 218fee91a7d2214fec328f74247e079292c45ce0
Site Bootstrap Validate: 32050796944 SUCCESS
Site Handoff Orchestrator: 32050796941 SUCCESS
Ecosystem Heartbeat Orchestration: 32050797014 SUCCESS
Check StegFin Phone Projection: 32050785197 SUCCESS
claim: MERGED_INTO_CANONICAL_WORKSTREAM
credential_requirement: NONE
raw GitHub acquisition: NONE
runtime_activation_effect: NONE
financial_authority_effect: NONE
```

`.github/workflows/import-marketplace-coinbase-accessibility.yml` remains absent after released B16R1.

## Continuation

Recurring projection import belongs to `StegVerse-Labs/StegVerse-Healer#8` through existing `SHWP-HEALER-SOVEREIGN-SCHEDULER-001`. Ordinary Healer scheduler activation remains separately `MACHINE_OWNED` and requires its sovereign runtime receipt; source merge or CI does not prove activation.

TV/TVC remains credential authority. No NON-TV/TVC secret/token, second scheduler, second heartbeat, Render path, publication authority, financial authority, or wallet authority is introduced.

## Session consolidation

B16R1 and the local-import correction are `MERGED_INTO_CANONICAL_WORKSTREAM`. This Marketplace migration no longer requires unique chat implementation state. Broader Site #268 workflow/token minimization remains active separately.
