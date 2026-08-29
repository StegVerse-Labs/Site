# Governance Observatory Homepage Validator Mirror Handoff

Issue: #594
Claim: SITE-GOVOBS-HOMEPAGE-VALIDATOR-594-20260828
State: CLAIM_PENDING_ADMISSION
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
