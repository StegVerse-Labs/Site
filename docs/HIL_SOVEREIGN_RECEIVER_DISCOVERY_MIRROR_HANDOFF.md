# HIL Sovereign Receiver Discovery Mirror Handoff

Updated: 2026-08-22
Repository: `StegVerse-Labs/Site`
Goal: `HIL-LIFECYCLE-ACTIVATION-001`
PR: `#435`

## Source of truth

This scoped handoff is subordinate to `docs/HIL_SITE_MIRROR_HANDOFF.md` and records only the participant-facing receiver-discovery correction needed to align Site with the sovereign HIL receiver path installed in `StegVerse-Labs/.github`.

Canonical authority remains:

```text
credential_authority: TV/TVC
github_token_runtime_authority: NONE
participant_surface_authority: StegVerse-Labs/Site
receiver_execution_authority: resident StegVerse sovereign runtime only
transport_authority: NONE
publication_authority: NONE
master_records_authority: NONE
```

## Defect observed

`data/hil-receiver-config.json` still projected the historical Cloudflare receiver as the active service operator and declared `https://stegverse.org` as a configured receiver even though the current HIL source-of-truth documents explicitly classify the Cloudflare/GitHub-secret path as historical only.

The same file also had `participant_visible_provider=true`, while the active Site contract requires provider-neutral discovery and requires an actually configured receiver to have a conforming HTTPS URL and `CONFORMING_HTTPS_RECEIVER_CONFIGURED` state.

Several older validators also conflated a source-valid upload surface with proof that the public receiver was already configured. That made the desired fail-closed state appear invalid and encouraged stale receiver projection rather than preserving uncertainty.

## Applied correction

Branch: `fix/hil-sovereign-receiver-discovery`

Key commits:

```text
81dc15f1a2f84f904f1d26b03987965b636959d6  fail closed stale receiver discovery
cb79029c69216cc2f2778cc257f440810902330e  restore periodic readiness retry
3da438602c97141942ac37c9e85b48b433ebd3be  align controlled-cycle fixture
 a92189ec90b6ad4867a21ff531c043d59a5bc8e2  accept fail-closed verifier reason from stderr
3caa02c4727151f02c84912863163971f20e3544  separate source continuity from runtime readiness
380f08a73c0f07c1f17a90e740a8bda409216ff1  decouple release verification from live receiver proof
9826094b6b1cfdaaa33967d3c6a56700c009311f  expose canonical prompt identity on participant page
5561760efb17f1ee401de8789490f459ae492596  derive launch wording from complete evidence gates
ffacceb37418982a3077ef0b6b889e92ba796371  fail closed upload verifier until public receiver is proven
```

`data/hil-receiver-config.json` now:

```text
receiver_base_url: null
participant_visible_provider: false
service_operator: StegVerse sovereign receiver runtime
configuration_state: AWAITING_CONFORMING_HTTPS_RECEIVER
```

The readiness and submission paths remain canonical:

```text
/api/hil/readiness
/api/hil/submissions
```

Transport requirements remain HTTPS-only, credential-free, query-free, and fragment-free. The Site configuration grants no execution, publication, or Master Record authority.

The participant page now exposes both immutable experiment identities:

```text
Primary SHA-256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Prompt SHA-256:  cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
```

The browser still polls readiness periodically, but a missing receiver cannot be converted into an availability claim. Source-contract validators accept either:

```text
CONFIGURED:
  receiver_base_url = https://stegverse.org
  configuration_state = CONFORMING_HTTPS_RECEIVER_CONFIGURED

or

FAIL_CLOSED:
  receiver_base_url = null
  configuration_state = AWAITING_CONFORMING_HTTPS_RECEIVER
```

Only the first state may set `HIL_PUBLIC_RECEIVER_READY_PROVEN=true` after the required runtime evidence exists.

## Pre-work ownership

This branch is represented by the scoped claim:

```text
data/session-work-claims.d/hil-sovereign-receiver-discovery-435.json
claim_id: SITE-HIL-SOVEREIGN-RECEIVER-DISCOVERY-435-20260822
state: CLAIMED_FOR_INTEGRATION
dependency_surface: site:hil-sovereign-receiver-discovery
authority_effect: false
activation_effect: false
```

The Site claim validator and handoff orchestrator consume the base registry plus bounded append-only claim fragments into the same collision set. The exact branch claim is an ownership proof only; it grants no HIL execution or activation authority.

## Exact validation evidence

Validated branch head: `ffacceb37418982a3077ef0b6b889e92ba796371`

```text
Check HIL v1 Upload Surface                       32608712918 SUCCESS
Check HIL LinkedIn Launch Readiness              32608712896 SUCCESS
Check HIL v1.1 Release                           32608712900 SUCCESS
HIL Post-Submit Continuity                       32608712910 SUCCESS
HIL Site Contract                                32608712911 SUCCESS
Site Handoff Orchestrator                        32608712906 SUCCESS
Ecosystem Heartbeat Orchestration                32608712905 SUCCESS
Site Bootstrap Validate - No Non-TV/TVC Authority 32608712941 SUCCESS
Session Retirement Validate                      32608712892 SUCCESS
```

These are source/integration validation results. They do not prove that the resident receiver is running, publicly reachable, or preserving real submitted bytes.

## Relationship to resident receiver activation

`StegVerse-Labs/.github` has already merged and validated the sovereign HIL worker/admission path through PR #259 / merge `2f20b0c55cab8e28923955bfde8972090ae562b4`.

This Site correction intentionally does not fabricate public activation. The discovery configuration stays fail-closed until the resident receiver produces real local READY evidence and an admitted public HTTPS rendezvous is actually observed. Only then may `receiver_base_url` be populated and `configuration_state` become `CONFORMING_HTTPS_RECEIVER_CONFIGURED`.

## Required next evidence

1. Resident WorkerCoordinator gives `SHWP-HIL-SOVEREIGN-RECEIVER-001` a real claim/fresh fence.
2. The receiver reaches exact HIL v1.1 READY on the sovereign runtime.
3. A public HTTPS rendezvous is bound without gaining execution/lifecycle authority.
4. Site directly observes the HTTPS readiness endpoint.
5. Only after that observation may the receiver discovery config be promoted from `AWAITING_CONFORMING_HTTPS_RECEIVER`.
6. A real browser submission must then preserve `HIL-RECEIVER-RECEIPT-v2`.
7. Exact submitted bytes must survive controlled receiver restart/replacement with SHA-256 equality.
8. The exact package/receipt must continue into the existing TVC HIL lifecycle.

## Completion boundary

```text
source/config correction: COMPLETE_VALIDATED_ON_BRANCH
participant identity exposure: COMPLETE_VALIDATED_ON_BRANCH
fail-closed discovery semantics: COMPLETE_VALIDATED_ON_BRANCH
public receiver READY: NOT_PROVEN
browser receipt: NOT_PROVEN
restart exact-byte proof: NOT_PROVEN
TVC lifecycle continuation: NOT_PROVEN
HIL product activation: NOT_COMPLETE
```

This correction may be merged after the final PR-head validation remains green. It must not be used as evidence of a live receiver or of completed HIL activation.
