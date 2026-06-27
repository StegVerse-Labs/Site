# Site Mirror Activation Status

## Current State

```text
activation_state: pending
repository: StegVerse-Labs/Site
activation_target: Mirror Papers from Publisher
source_target: GCAT-BCAT-Engine/Publisher
source_path: papers
target_path: papers
source_of_truth: Publisher
ledger: docs/SITE_MIRROR_ACTIVATION_LEDGER.json
```

## Status Rule

Site-side evidence alone does not activate the mirror. Publisher closure remains required before activation can be claimed.

The machine-readable activation ledger is the Site-side status source of truth:

```text
docs/SITE_MIRROR_ACTIVATION_LEDGER.json
```

## What Is Complete

```text
Mirror Papers from Publisher workflow exists
workflow accepts source_repository and source_ref inputs
workflow resolves Publisher defaults
workflow checks Site paper display policy before mirroring
workflow checks public ingestion contract
workflow checks Site mirror evidence packet
workflow checks Site mirror live evidence state
workflow checks Site mirror handoff
mirror script records source metadata in papers/papers_manifest.json
checked-in papers/papers_manifest.json includes source metadata
manifest metadata checker exists
paper alias checker exists
Site mirror closure next-build packet exists
Site mirror closure guard packet exists
Site mirror activation ledger exists
closure guard workflow runs handoff, closure, guard, activation ledger, TT mirror, TT public page, and Governance Observatory checks
TT code-representation public page exists
TT code-representation sync workflow exists
Governance Observatory public page exists
Governance Observatory status validation workflow exists
```

## What Is Not Yet Complete

```text
Publisher workflow run URL has not been recorded
Publisher verification receipt artifact has not been recorded
Publisher live dispatch workflow URL has not been recorded
Site mirror workflow URL has not been recorded
Site mirror commit SHA has not been recorded
Site evidence artifact has not been recorded
Publisher closure nudge result has not been recorded
Publisher closure receipt has not been recorded
Publisher verification tracker has not been updated to activated
Publisher activation status has not been updated to activated
TT sync workflow first bundle-fed commit has not been recorded
Governance Observatory status validation pass has not been recorded
```

## Non-Activation Mirror Evidence

The following surfaces are public mirrors, not activation authorities:

```text
tt-code-representation.html
governance-observatory.html
docs/SITE_TT_CODE_REPRESENTATION_STATUS.md
docs/SITE_TT_CODE_REPRESENTATION_STATUS.json
docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.md
docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.json
```

These surfaces may become current after their validation workflows run, but they do not activate the Publisher paper mirror and do not grant execution authority.

## Activation Boundary

Site mirror activation occurs only after:

```text
1. Publisher automated dispatch workflow produces a verification receipt artifact.
2. Publisher workflow dispatches Site mirror workflow successfully.
3. Site mirror workflow completes.
4. Site mirror workflow writes and uploads Site evidence artifact.
5. Site manifest metadata is verified.
6. Site paper aliases are verified.
7. Publisher closure workflow consumes Publisher and Site evidence artifacts.
8. Publisher closure workflow writes docs/mirror-activation-closures/<closure>.json.
9. Publisher verification tracker is updated to activated.
10. Publisher activation status is updated to activated.
```

## Current Site Validation Contract

Site-side status and closure readiness are checked by:

```text
python scripts/check_papers_manifest_metadata.py
python scripts/check_paper_aliases.py
python scripts/check_site_mirror_evidence_packet.py
python scripts/check_site_mirror_live_evidence_state.py
python scripts/check_site_mirror_handoff.py
python scripts/check_site_mirror_closure_next_build.py
python scripts/check_site_mirror_closure_guard.py
python scripts/check_site_mirror_activation_ledger.py
python scripts/check_site_mirror_activation_status.py
python scripts/check_site_tt_code_representation_mirror.py
python scripts/check_site_tt_public_page.py
python scripts/check_site_governance_observatory_status.py
```

## Next Action

```text
Keep Site activation status pending until Publisher and Site evidence artifacts exist and Publisher closure updates the verification tracker and activation status.
Keep TT and Governance Observatory surfaces public-mirror-only until their own workflows produce current status evidence.
```

## Activation Evidence Files

```text
github/workflows/mirror-papers.yml
github/workflows/site-mirror-closure-guard.yml
github/workflows/sync-tt-code-representation.yml
github/workflows/validate-governance-observatory-status.yml
scripts/mirror_papers.py
scripts/check_papers_manifest_metadata.py
scripts/check_paper_aliases.py
scripts/check_site_mirror_evidence_packet.py
scripts/check_site_mirror_live_evidence_state.py
scripts/check_site_mirror_handoff.py
scripts/check_site_mirror_closure_next_build.py
scripts/check_site_mirror_closure_guard.py
scripts/check_site_mirror_activation_ledger.py
scripts/check_site_mirror_activation_status.py
scripts/check_site_tt_code_representation_mirror.py
scripts/check_site_tt_public_page.py
scripts/check_site_governance_observatory_status.py
papers/papers_manifest.json
tt-code-representation.html
governance-observatory.html
docs/SITE_MIRROR_LIVE_VERIFICATION.md
docs/SITE_MIRROR_EVIDENCE_PACKET.md
docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json
docs/SITE_MIRROR_CLOSURE_NEXT_BUILD.md
docs/SITE_MIRROR_CLOSURE_GUARD.md
docs/SITE_MIRROR_ACTIVATION_LEDGER.md
docs/SITE_MIRROR_ACTIVATION_LEDGER.json
docs/SITE_MIRROR_HANDOFF.md
docs/SITE_TT_CODE_REPRESENTATION_STATUS.md
docs/SITE_TT_CODE_REPRESENTATION_STATUS.json
docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.md
docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.json
```

## Archive Readiness

This status file now defers activation state to the machine-readable activation ledger, preserves the Publisher closure boundary, and records TT/Governance Observatory mirrors as non-activation public status surfaces. The prior chat thread is not required to continue activation-status work.
