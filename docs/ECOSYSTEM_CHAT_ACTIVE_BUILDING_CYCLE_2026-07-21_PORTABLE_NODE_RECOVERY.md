# Ecosystem Chat Active Building Cycle — Portable-Node Recovery

## Date

2026-07-21

## Active goal

Complete the existing governed Ecosystem Chat path:

request → provider response → durable persistence → provider-usage custody → transition custody → reconstruction PASS for both chains → immutable zero-blocker VERIFIED receipt → Site ACTIVATION_COMPLETE → verified downstream ingestion.

## Existing capability reused

The adapter already contained a zero-touch portable-node runtime:

- `llm_adapter.node_bootstrap`
- `llm_adapter.node_service`
- `stegnode-bootstrap`
- `stegnode`
- `llm_adapter.combined_gateway:app`
- `llm_adapter.custody_worker`
- existing provider, Master-Records, verifier, receipt, Site-import, and downstream-consumer contracts

No replacement gateway, provider service, custody service, scheduler, monitor, or deployment platform was created.

## Concrete defects repaired

1. The generated node capability bound the gateway to `127.0.0.1` unconditionally.
2. The node daemon applied fail-closed manifest defaults after reading the process environment, overwriting authorized host, provider, and custody settings.

## Changes

- `042faaaca4d1c1babc8d7d7bc8c8e408356cc337`
  - added `${HOST}` binding support;
  - retained `127.0.0.1` as the fail-closed default;
  - recorded authorized host-binding support.
- `3f8165686b86419cadfdd093a1e5a3876915801f`
  - added bounded runtime-environment construction;
  - defaults now fill missing values only;
  - authorized provider, custody, host, port, and storage configuration is preserved.
- `97bef70d3683cfae7029cb9bc368f0b17d955c9c`
  - added portable-node runtime contract tests.
- `398a4a39523d2a21b2331866593a92c2eba4dc81`
  - bound the same portable-node assertions into the existing validation contract rather than creating another workflow.
- `c71292511deaa2f064b3c4f87b3b08e03415e3b3`
  - updated the Site build goal to activate the existing portable node as a deployment-recovery path.

## Options evaluated

1. Restore the existing Render service: still valid, but no connected Render control-plane mutation tool is available.
2. Create another hosted gateway: rejected because it duplicates the existing combined gateway and portable-node runtime.
3. Reuse the portable-node runtime unchanged: rejected because the two concrete defects prevented authorized sovereign hosting.
4. Repair the existing portable-node runtime: selected as the lowest-risk, reuse-first path.

## Current evidence state

- Portable-node bootstrap: IMPLEMENTED
- Portable-node process supervision and reconstruction: IMPLEMENTED
- Authorized host binding: IMPLEMENTED
- Authorized provider/custody environment preservation: IMPLEMENTED
- Existing-validation contract binding: IMPLEMENTED
- Validation result for the latest commit: NOT YET OBSERVED through available commit-status evidence
- Sovereign host execution: UNPROVEN
- Live provider response: UNPROVEN
- Custody and reconstruction: UNPROVEN
- Immutable VERIFIED receipt: UNPROVEN
- Site activation: UNPROVEN
- Downstream ingestion: UNPROVEN

## Exact blocker

No connected, already-authorized machine host has yet executed the repaired `stegnode` runtime and exposed a live endpoint. The existing Render hostname still reports `x-render-routing: no-server`.

The blocker is now host execution, not gateway implementation or portable-node runtime configuration inheritance.

## Machine-owned continuation

`StegVerse-org/LLM-adapter#18` owns the deployment recovery task. It is assigned to the repository identity and labeled `machine-owned`, `ecosystem-chat`, and `portable-node`.

Next machine action:

1. bind the repaired `stegnode` runtime to an existing authorized sovereign host or restore the existing Render service;
2. point the existing verifier to the live endpoint;
3. retain the first exact provider, persistence, custody, reconstruction, or receipt result through the normal validation workflow;
4. repair only the first concrete failing boundary;
5. allow Site and the three downstream consumers to advance automatically only after verified evidence exists.

## Manual user action requirement

False.

No deployment, credential copying, workflow dispatch, node start, evidence transcription, or downstream publication task is assigned to the user.

## Removals

None proposed or performed.
