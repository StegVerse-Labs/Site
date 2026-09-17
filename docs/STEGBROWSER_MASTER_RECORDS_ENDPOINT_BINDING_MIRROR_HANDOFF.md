# StegBrowser Master Records Endpoint Binding Mirror Handoff

Updated: 2026-09-17
Repository: `StegVerse-Labs/Site`
Canonical Goal: `StegVerse-Labs/.github:MASTER-RECORDS-STEGBROWSER-ENDPOINT-BINDING-001`
COSV: `40000100100000`
Authority effect: `NONE_BINDING_ONLY`

## Scope

Repair only the immutable StegBrowser browser-to-authoritative Master Records state-transition custody binding. The immutable nonce remains:

```text
STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z
requested_invocation_count = 1
second_request_allowed = false
```

The separate `.github` Python local-adapter defect is not part of this Site change.

## Provider-neutral binding

`assets/canonical-master-records-transition-custody-browser.js` now treats `/api/master-records/state-transitions` as the canonical path, not as an assumption that the static Site origin hosts Master Records.

It discovers an existing StegVerse gateway using these provider-neutral sources:

```text
query:master_records_gateway
query:gateway
runtime injection
persisted local configuration
same origin
loopback fallback
```

Each candidate must return a hash-valid `stegverse.node.endpoint-advertisement.v1`, be health-bound, expose no execution/publication authority, preserve `credential_authority=TV/TVC`, and advertise the exact Master Records transport endpoint owned by `master-records/orchestration`. The advertised node must also return health `status=ok`.

The browser sends no Master Records bearer, token, cookie credential, or credential-authority placeholder. Server-side TV/TVC materialization remains outside Site.

## Canonical receipt correction

The authoritative Master Records state-transition contract does not allow `INGRESS_ADMITTED` as a top-level transition outcome. The StegBrowser page now records:

```text
transition_outcome = OBSERVED
transition_evidence.intr_ingress_state = INGRESS_ADMITTED
transition_evidence.intr_governance_decision = ALLOW
```

This preserves the observed ingress state without inventing a noncanonical custody outcome.

## Completion boundary

Source binding is not authentic custody evidence. Progression still requires the sole authoritative Master Records result to satisfy:

```text
state = RECORDED
reconstruction_status = PASS
receipt_sha256 = reconstructed_receipt_sha256 = browser-recomputed canonical receipt digest
master_records_grants_transition_authority = false
master_records_grants_execution_authority = false
master_records_grants_credential_authority = false
```

Only then may the same immutable invocation return to the existing A1-A4 execution owner. A3, A4, and Round Trip 1 are not entered by this binding repair.

## Manual work

None.
