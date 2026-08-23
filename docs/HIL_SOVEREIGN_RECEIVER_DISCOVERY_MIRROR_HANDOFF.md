# HIL Sovereign Receiver Discovery Mirror Handoff

Updated: 2026-08-22
Repository: `StegVerse-Labs/Site`
Goal: `HIL-LIFECYCLE-ACTIVATION-001`
PR: `#435`
Merge: `1d9575fa0f2ee19b78b9232f79313c5e12426b94`

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

## Corrected defect

The prior Site projection named a historical Cloudflare receiver as active, populated `https://stegverse.org` before live receiver proof existed, and exposed provider branding. Several old validation checks also conflated a source-valid upload surface with proof that the public receiver was already configured.

PR #435 corrected those surfaces without weakening the live-evidence gate.

## Merged implementation

```text
PR: 435
validated PR head: 5da4817de2ab3abc51bef117cc25bcae7fd4ce58
merge: 1d9575fa0f2ee19b78b9232f79313c5e12426b94
state: MERGED_MAIN
```

Key implementation lineage:

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
5da4817de2ab3abc51bef117cc25bcae7fd4ce58  record validated scoped handoff
```

`data/hil-receiver-config.json` is now intentionally fail-closed:

```text
receiver_base_url: null
participant_visible_provider: false
service_operator: StegVerse sovereign receiver runtime
configuration_state: AWAITING_CONFORMING_HTTPS_RECEIVER
```

The canonical route identities remain:

```text
readiness: /api/hil/readiness
submission: /api/hil/submissions
```

Transport remains HTTPS-only, credential-free, query-free, and fragment-free. Site discovery grants no execution, publication, release, or Master Records authority.

The participant page now exposes both immutable experiment identities:

```text
Primary SHA-256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Prompt SHA-256:  cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
```

The browser polls readiness periodically, but failed discovery remains failed discovery. Source-contract validation accepts exactly two states:

```text
CONFIGURED:
  receiver_base_url = https://stegverse.org
  configuration_state = CONFORMING_HTTPS_RECEIVER_CONFIGURED

FAIL_CLOSED:
  receiver_base_url = null
  configuration_state = AWAITING_CONFORMING_HTTPS_RECEIVER
```

Only the configured state may represent public receiver readiness, and only after the required runtime evidence exists.

## Pre-work ownership and release

The implementation branch was governed by:

```text
data/session-work-claims.d/hil-sovereign-receiver-discovery-435.json
claim_id: SITE-HIL-SOVEREIGN-RECEIVER-DISCOVERY-435-20260822
dependency_surface: site:hil-sovereign-receiver-discovery
authority_effect: false
activation_effect: false
```

The claim was an ownership record only. After merge it is eligible for release from the active-claim set; downstream runtime work remains owned by the resident HIL worker lane rather than this Site implementation claim.

## Exact branch validation evidence

The final PR head and its immediately preceding implementation head retained green validation. Exact successful runs observed on the final PR head include:

```text
Check HIL v1 Upload Surface                       32608760847 SUCCESS
Check HIL LinkedIn Launch Readiness              32608760802 SUCCESS
Check HIL v1.1 Release                           32608760774 SUCCESS
HIL Post-Submit Continuity                       32608760804 SUCCESS
HIL Site Contract                                32608760830 SUCCESS
Site Handoff Orchestrator                        32608760827 SUCCESS
Site Handoff Orchestrator follow-up              32608790069 SUCCESS
Ecosystem Heartbeat Orchestration                32608760772 SUCCESS
Site Bootstrap Validate - No Non-TV/TVC Authority 32608760811 SUCCESS
Session Retirement Validate                      32608760834 SUCCESS
```

These prove source/integration consistency, not live receiver execution.

## Relationship to resident receiver activation

`StegVerse-Labs/.github` has already merged and validated the sovereign HIL worker/admission path through PR #259 / merge `2f20b0c55cab8e28923955bfde8972090ae562b4`.

The Site correction deliberately leaves discovery fail-closed until the resident receiver produces real local READY evidence and an admitted public HTTPS rendezvous is actually observed. No source, merge, CI, or Site configuration state substitutes for that observation.

## Required next evidence

1. Resident WorkerCoordinator gives `SHWP-HIL-SOVEREIGN-RECEIVER-001` a real claim/fresh fence.
2. The receiver reaches exact HIL v1.1 READY on the sovereign runtime.
3. A public HTTPS rendezvous is bound without gaining execution/lifecycle authority.
4. Site directly observes the HTTPS readiness endpoint.
5. Only then may discovery move to `CONFORMING_HTTPS_RECEIVER_CONFIGURED`.
6. A real browser submission returns and preserves `HIL-RECEIVER-RECEIPT-v2`.
7. Exact submitted bytes survive controlled receiver restart/replacement with SHA-256 equality.
8. The exact package/receipt continues into the existing TVC HIL lifecycle.

## Completion boundary

```text
source/config correction: COMPLETE_MERGED_MAIN
participant identity exposure: COMPLETE_MERGED_MAIN
fail-closed discovery semantics: COMPLETE_MERGED_MAIN
branch validation: PASS
public receiver READY: NOT_PROVEN
browser receipt: NOT_PROVEN
restart exact-byte proof: NOT_PROVEN
TVC lifecycle continuation: NOT_PROVEN
HIL product activation: NOT_COMPLETE
```

This Site source/integration correction is complete and merged. The HIL product goal remains open until the machine-owned runtime/public evidence chain is actually observed.
