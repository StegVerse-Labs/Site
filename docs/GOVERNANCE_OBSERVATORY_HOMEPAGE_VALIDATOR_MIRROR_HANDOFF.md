# Governance Observatory Homepage Validator Mirror Handoff

Issue: #594
Claim: SITE-GOVOBS-HOMEPAGE-VALIDATOR-594-20260828
State: IMPLEMENTED_VALIDATED_MERGED / POST_MERGE_OBSERVATION_PENDING
Authority effect: NONE

## Machine-discovered defect

Site Task Runner `33228250707` passes the refreshed homepage/governance validators and then fails:

```text
scripts/check_site_governance_observatory_status.py
FAIL: landing page missing required phrase: governance-observatory.html
```

The Governance Observatory public/status surface itself is not failing. Site #512 is already RELEASED_COMPLETE and publicly observed.

## Current architecture

```text
index.html = simplified conversational shell
primary navigation = My KV | Organizational KV
governance-observatory.html = dedicated public/direct specialty surface
Site #512 release awareness = COMPLETE / preserved
```

## Repair boundary

This lane owns only the stale checker, its regression test, this handoff, task metadata, and claim fragment.

It must not modify:
- `index.html`
- `governance-observatory.html`
- `docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.md`
- `docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.json`

Completion requires a successor authoritative Site Task Runner to advance beyond the status checker.


## Implemented repair

- `scripts/check_site_governance_observatory_status.py` preserves the full v0.1.0 release/status/public-path verification.
- The checker now validates the current simplified homepage rather than requiring a Governance Observatory homepage link.
- The checker rejects restoration of the retired primary-homepage specialty link.
- `tests/test_site_governance_observatory_status.py` adds deterministic regression coverage.
- `index.html`, `governance-observatory.html`, and Governance Observatory status evidence are unchanged.

State remains source-only until exact-head gates pass.


## Validation and merge evidence

Validated implementation head:

`d3bef6d8bf463a069d2beae5272b29a4e9e33cf9`

Exact-head gates:

- Site Bootstrap Validate `33228420908`: PASS
- Site Handoff Orchestrator `33228420926`: PASS
- Ecosystem Heartbeat Orchestration `33228420923`: PASS

Integration:

- PR `#596`
- merge `f4839665a703ed8b037282c8629dac3efe8be5e2`
- claim release commit `ba09875eb214c211f0ff8ab4489b7e877bf9dcab`

Full completion still requires a successor authoritative `Site Task Runner` to advance beyond `scripts/check_site_governance_observatory_status.py`.
