# SV002 Sovereign InTr Profile Proof Mirror Handoff

Updated: 2026-08-31
Issue: #860

## Scope

This lane observes only:

`https://stegverse.org/intr/profile`

It does not mutate the canonical SV002 target/projector or any active #811/#814 surface.

## Conforming predicates

A profile is classified `OBSERVED_CONFORMING` only when credentialless HTTPS returns HTTP 200 and the exact JSON proves:

- canonical supported InTr profile schema;
- `SV002:PublicObservation`;
- event-triggered sovereign ingress;
- TV/TVC credential authority;
- GitHub token runtime authority `NONE`;
- execution authority `NONE`;
- no carrier-derived authority;
- if universal profile: canonical HB-derived carrier metadata including 100 Hz, 10 ms, oscillator-only progression, 16 H1 phase slots, and payload-SHA256-first64 channel selection.

Anything else is `OBSERVED_BLOCKED`.

## Evidence boundary

The workflow has read-only repository permissions and writes no repository state. Artifact evidence may establish public profile observation only. It cannot establish receiver readiness, materialization admission, a valid-Node observation round trip, principal execution, Transition Element evaluation, Master Records reconstruction, or SYSTEM_AI_ACTIVE.
