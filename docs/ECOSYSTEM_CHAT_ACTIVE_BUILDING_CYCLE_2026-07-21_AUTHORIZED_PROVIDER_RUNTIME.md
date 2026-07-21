# Ecosystem Chat Active Building Cycle — Authorized Provider Runtime

## Cycle date

2026-07-21

## Required capability

Bind an already-authorized real-provider configuration to the existing canonical Ecosystem Chat runtime so the same path can execute:

request → governed provider response → provider-usage persistence → provider-usage custody → transition custody → reconstruction.

## Existing candidates evaluated

1. Existing `governed_provider.py` broker: directly reusable for HTTPS, host allowlist, token, model, quota, cost, response identity, and provider receipt enforcement.
2. Existing provider-usage ledger and middleware: directly reusable for local provider-owned measurement persistence.
3. Existing Master-Records provider-usage and transition clients: directly reusable for authenticated custody.
4. Existing live-activation workflow: reusable through bounded extension; it previously probed only an already-running gateway.
5. New provider executor or workflow: rejected as duplication.

## Work performed

- Extended the existing live-activation workflow with configuration-presence evaluation and secret-bound runtime startup.
- Added a bounded verifier requiring real provider use, provider receipt, provider-usage persistence, provider-usage custody, transition custody, reconstruction PASS, and false authority fields.
- Added adversarial tests proving fallback, local custody self-claims, missing usage custody, and authority escalation fail closed.
- Aligned two stale StegDeploy validation scripts with the installed image-publication v2 contract.
- Reapplied the exact validated blobs to current main after machine-owned status commits caused branch-history conflict.

## Existing capabilities reused

- `llm_adapter/governed_provider.py`
- `llm_adapter/provider_usage_persistence.py`
- `llm_adapter/master_records_usage_submission.py`
- `llm_adapter/master_records_client.py`
- `llm_adapter/combined_gateway.py`
- `.github/workflows/ecosystem-chat-live-activation.yml`
- Existing activation receipts, provider tests, custody tests, authority checks, recovery checks, and Goal 4 verification

## Evidence

- Original green validation: `29867306026`
- Current-mainline validation: `29867888624`
- Architecture Guard: `29867888688`
- Merge: `2d1533644d9e589fd441ba37a1bc4095ae5f4100`

## Observed result

Authorized provider execution plumbing is INTEGRATED. The workflow can execute automatically when the established provider and Master-Records configuration exists. Missing configuration is represented by a hash-bound `CONFIGURATION_REQUIRED` receipt without recording credential values.

At the latest observation, no main-branch authorized-provider activation receipt had been retained. Therefore real provider execution, provider-usage custody, immutable activation, Site activation, and propagation remain UNPROVEN.

## Authority boundaries

- Provider output is not authority.
- Local usage persistence is not custody.
- Custody does not grant execution or publication authority.
- Reconstruction does not grant publication authority.
- Repository mutation and publication remain false.
- Only the canonical provider token and Master-Records token may be consumed as workflow secrets.
- No credential value is printed or committed.

## Removals proposed but not performed

None. PR #27 remains retained and open after its branch-history conflict. No component, workflow, branch, or prior implementation was deleted, disabled, closed, or superseded.

## Goal delta

The canonical runtime can now automatically cross the real-provider boundary once established authorization exists. Before this cycle, the runtime components existed but no repository-owned workflow bound them into one executable path.

## Non-progress

No provider or downstream runtime gate is upgraded merely because the binding and verifier exist.

## Next executable step

Inspect the first repository-retained `ecosystem-chat-authorized-provider-activation.latest.json` receipt and repair only its first exact blocker.
