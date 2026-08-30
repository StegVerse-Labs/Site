# StegOS SV002 InTr Runtime Target Projector Mirror Handoff

Updated: 2026-08-30
Repository: `StegVerse-Labs/Site`
Issue: #715
State: IMPLEMENTED_ON_BRANCH_VALIDATION_PENDING

## Purpose

Promote `stegos-node/sv002-intr-sync-target.json` only from independently captured evidence that a credentialless HTTPS sovereign `/intr/profile` is live and explicitly supports `SV002:PublicObservation`.

The merged default remains fail-closed:

```text
state: AWAITING_SOVEREIGN_INTR_INGRESS
ingress_url: null
runtime_ingress_observed: false
```

Source, CI, a configured public origin, or the existence of Service Gateway code is not runtime observation.

## Accepted evidence

Input schema: `stegverse.universal-intr-ingress-observation/v1`.

Required predicates include exact HTTPS `/intr/profile`, HTTP 200, no credential, canonical profile hash, durable evidence reference, and no GitHub-token or execution authority.

The observed profile may be either:
- `stegverse.universal-intr-profiled-ingress/v1`, with `profiles` containing `SV002:PublicObservation`; or
- backward-compatible `stegverse.hil-intr-materialization-ingress-profile/v1`, with `additional_materialization_profiles` containing `SV002:PublicObservation`.

Both must prove event-triggered, G18-independent, TV/TVC-bound, non-authorizing sovereign ingress with TLS observed.

## Projection

Only then may the projector emit `CONFORMING_SOVEREIGN_INTR_INGRESS` and derive the exact same-origin `/intr/materialization` URL. It explicitly leaves receiver readiness, observation round trip, principal experiment execution, and Master Records reconstruction false.

No synthetic fixture may be committed as live observation evidence or used to promote the merged target.
