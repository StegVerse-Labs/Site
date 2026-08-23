# HIL Sovereign Receiver Discovery Mirror Handoff

Updated: 2026-08-22
Repository: `StegVerse-Labs/Site`
Goal: `HIL-LIFECYCLE-ACTIVATION-001`

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

The same file also had `participant_visible_provider=true`, while `scripts/verify_hil_site_contract.py` requires provider-neutral discovery and fails closed unless an actually configured receiver has a conforming HTTPS URL and `CONFORMING_HTTPS_RECEIVER_CONFIGURED` state.

The stale projection therefore conflicted with both the active architecture and the repository's own verifier.

## Applied correction

Branch: `fix/hil-sovereign-receiver-discovery`
Config commit: `81dc15f1a2f84f904f1d26b03987965b636959d6`

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

## Relationship to resident receiver activation

`StegVerse-Labs/.github` has already merged and validated the sovereign HIL worker/admission path through PR #259 / merge `2f20b0c55cab8e28923955bfde8972090ae562b4`.

This Site correction intentionally does not fabricate public activation. The discovery configuration stays fail-closed until the resident receiver produces real local READY evidence and an admitted public HTTPS rendezvous is actually observed. Only then may `receiver_base_url` be populated and `configuration_state` become `CONFORMING_HTTPS_RECEIVER_CONFIGURED`.

## Required next evidence

1. Resident WorkerCoordinator gives `SHWP-HIL-SOVEREIGN-RECEIVER-001` a real claim/fresh fence.
2. The receiver reaches exact HIL v1.1 READY on the sovereign runtime.
3. A public HTTPS rendezvous is bound without gaining execution/lifecycle authority.
4. Site directly observes the HTTPS readiness endpoint.
5. Only after that observation may the receiver discovery config be promoted from `AWAITING_CONFORMING_HTTPS_RECEIVER`.
6. A real browser submission must then preserve `HIL-RECEIVER-RECEIPT-v2`, followed by restart exact-byte proof and TVC lifecycle continuation.

## Completion boundary

This correction is complete only when repository validation confirms the fail-closed discovery state. It does not complete HIL product activation and must not be used as evidence of a live receiver.
