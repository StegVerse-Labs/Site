# My KV Node Registration Recheck Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#774`
Branch: `fix/my-kv-node-registration-recheck-774-v2`
State: RELEASED_COMPLETE
Authority effect: NONE
Activation effect: false
Updated: 2026-08-30

## Purpose

Prevent My KV onboarding from offering duplicate device registration after the canonical local Node continuity state is already REGISTERED.

## Source-of-truth behavior

My KV must use the canonical `StegVerseNodeContinuity` status before exposing any registration mutation.

Required state machine:

```text
REGISTERED
 -> Step 1 DONE
 -> hide Register action
 -> optional status recheck only through canonical Node continuity

UNKNOWN / not yet checked
 -> show Check current registration
 -> no registration mutation

CONFIRMED_UNREGISTERED
 -> show Register this device
 -> final canonical status recheck
 -> register only if still unregistered
```

## Invariants

1. Receipt #1 semantics are unchanged.
2. Registered state never exposes a duplicate registration action.
3. A missing or unreadable Node status fails closed.
4. Cross-browser/cross-device registration discovery is not fabricated.
5. No provider, KV, execution, heartbeat, or credential authority is added.
6. TV/TVC remains credential authority.
7. No GitHub runtime authority is introduced.

## Claimed surfaces

- `my-kv.html`
- `tests/test_site_node_continuity.py`
- `docs/MY_KV_NODE_REGISTRATION_RECHECK_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-my-kv-node-registration-recheck-774-20260830.json`

## Completion gates

- registered My KV state hides registration mutation;
- unresolved state offers a recheck first;
- only confirmed unregistered state exposes registration;
- final register action rechecks canonical status;
- focused tests pass;
- Site orchestration/bootstrap/heartbeat gates pass;
- PR merges;
- public iPhone route is re-observed separately.

## Current boundary

Implementation is active. The screenshots from 2026-08-30 demonstrate the defect: Step 1 is DONE while `Register this device` remains visible. Step 2 / private directory bridge failures are separate upstream runtime gaps and are not claimed by this lane.


## Release reconciliation — 2026-09-02

The canonical claim is already terminalized:

```text
claim: SITE-MY-KV-NODE-REGISTRATION-RECHECK-774-20260830
state: RELEASED_COMPLETE
pull_request: #776
release_commit: 8f947096830777fe19252cc4a77a75469bf21422
archive_eligible: true
```

Current `main` contains the required My KV state machine and regression coverage:

- registered state hides the mutation control;
- unresolved state exposes only `Check current registration`;
- confirmed-unregistered state may expose `Register this device`;
- the register path rechecks canonical Node status before mutation.

The older PR #775 is superseded by released PR #776 and must not remain an active implementation signal.
