# SV Cost Terminal Verifier Retirement Mirror Handoff

Updated: 2026-08-22
Repository: `StegVerse-Labs/Site`
Parent cost handoff: `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`
Product/publication handoff: `papers/SV_COST_FIVE_LANE_MIRROR_HANDOFF.md`
Issue: `StegVerse-Labs/Site#412`
PR: `StegVerse-Labs/Site#415`
State: `RELEASED_INTEGRATION_VALIDATION_ONLY`

## Goal

Retire the obsolete hourly GitHub-hosted SV Cost public-verification loop after its publication claim and issue were already terminal, without reducing relevant source-change or manual public verification.

## Pre-repair state

`.github/workflows/sv-cost-five-lane-public-verification.yml` had:

- hourly cron `17 * * * *` = 24 scheduled hosted starts/day before push/manual runs;
- `contents: write` and `issues: write`;
- `actions/checkout@v4` and `actions/setup-python@v5`;
- artifact upload/custody;
- repository commits/pushes of terminal verification state;
- `${{ github.token }}` issue mutation to close already-completed Site #173.

The canonical publication handoff already recorded 8/8 publication deliverables, `public_paper_body_verification: PASS`, terminal receipt `COMPLETE`, and `COMPLETE — CLAIM RELEASED`.

## Implemented repair

Current main now retains only:

- `workflow_dispatch` for intentional public re-verification;
- selective `push` validation for the public paper source, verifier source, and workflow source;
- `permissions: {}`;
- concurrency cancellation;
- explicit credential-environment refusal;
- anonymous exact-SHA Git source acquisition;
- preinstalled Python;
- fail-closed public HTTP/marker verification;
- ephemeral `/tmp` verification receipt;
- explicit validation-only containment assertions.

Removed:

- hourly schedule;
- repository writeback;
- issue write/mutation authority;
- GitHub-token use;
- checkout/setup-python actions;
- artifact upload/custody;
- terminal handoff finalization on every run.

## Integration evidence

```text
claim: SITE-SV-COST-TERMINAL-VERIFIER-RETIREMENT-412-20260822
superseded PR: #414 CLOSED_UNMERGED_MAIN_ADVANCED
release PR: #415
final source head: 23826a3cf7868212c35f3425fe22aa9483216d6a
validated merge ref: edf275d815b1ffabe7e6616239e9fa63db843729
merge commit: 935840c30a03c079b7e441701c60eded9434bd5c
current workflow blob: 2c420fbc861e4f29349370a7ced2e9afdd959ef7
Ecosystem Heartbeat Orchestration: 32603969025 SUCCESS
Site Handoff Orchestrator: 32603969129 SUCCESS
StegFin Phone Projection: 32603969034 SUCCESS
Site Bootstrap Validate: 32603969036 FAIL_PREEXISTING_VACC_SURFACE_VALIDATOR_MISMATCH_SITE_113
```

The Site Bootstrap failure is unrelated to this repair and reproduces the already-routed Site #113 VACC mismatch: `va-claims-chat.html` lacks four historical guided/fallback markers. The #412 merge-ref log passed credential refusal, anonymous exact-source acquisition, HIL, Master Records import, and SV-CONTINUITY-109 before failing at that unchanged VA validator.

## Authority boundary

```text
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_used: false
github_token_runtime_authority: NONE
repository_writeback_authority: false
issue_mutation_authority: false
artifact_custody_required: false
render_required: false
runtime_authority_effect: false
activation_effect: false
publication_authority_effect: false
```

This repair changes hosted validation transport only. It does not alter the canonical five-lane values, hashes, pricing posture, publication claim, public result, or Site #173 completion state.

## Completion boundary

The workflow repair is physically merged and the required Site claim/orchestration gates are proven on the exact merge ref. The retained workflow will run on future relevant main source changes and remains manually dispatchable. No runtime/deployment activation is required for this validation-only cost-reduction tranche.

Next cost candidate: Site #413, if still unclaimed and VACC owner semantics remain non-overlapping. Heartbeat-response clock retirement remains separately gated on the real `SHWP-HEALER-SOVEREIGN-SCHEDULER-001` execution receipt.
