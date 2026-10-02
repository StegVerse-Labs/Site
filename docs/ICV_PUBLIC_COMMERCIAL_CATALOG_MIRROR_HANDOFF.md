# ICV Public Commercial Catalog Mirror Handoff

Status: SOURCE_IMPLEMENTED / PUBLICATION_NOT_YET_OBSERVED
Updated: 2026-10-01
Repository: `StegVerse-Labs/Site`
Source authority: `Infrastructure-Continuity-Ventures/.github`
Source catalog merge: `dcc176eea7e4ecc69e9b05c76036a337d987e650`
Site posture: `MIRROR`

## Goal

Use the existing Site public commercial-services owner rather than create a new hosted service or authority plane. Mirror the twelve customer-facing ICV catalog entries on `services.html` and provide one credential-free discovery/contact route.

## Existing owner evidence

Site already owns public commercial/support publication under `PUBLICATION_PROCESS.md`. `services.html` is the existing public service directory. HydraSafe already demonstrates the bounded pattern: public Site mirror, canonical service authority retained upstream, and `mailto:rigel@stegverse.org` as a credential-free contact CTA. GP10's public service handoff establishes the same Site/public-mirror versus source-authority separation.

## Implemented source

- `services.html#icv-commercial-catalog` — human-facing catalog mirror.
- `data/icv-commercial-catalog-public.json` — machine-readable public mirror.
- `public-registry.json#ICV-PUBLIC-COMMERCIAL-CATALOG-001` — Site publication posture.
- `mailto:rigel@stegverse.org` — existing public contact owner reused; no credential or backend required.

Every entry preserves the ICV maturity label and a bounded description. The first-contact instruction explicitly excludes credentials, private keys, regulated personal data, facility records and other sensitive source material until scope and an authorized transfer method exist.

## Purchase-path disposition

```text
DOCUMENTED_TRANSACTION_READY = preserved from ICV
PUBLIC_SOURCE_INTEGRATION = IMPLEMENTED
PUBLIC_SERVED_BODY_OBSERVED = false
PUBLICLY_DISCOVERABLE_AND_REQUESTABLE = not yet promoted pending served-body observation
PAYMENT_OR_CONTRACT_EXECUTION_READY = false
NO_PAYMENT_EXECUTION_PATH = true
```

A mailto click or sent email is discovery/contact only. It does not create a buyer record, accepted scope, contract, payment, delivery or acceptance.

## Authority boundaries

Site does not become product/service authority. ICV commercial descriptions and the named source repositories remain authoritative for scope/maturity. This integration creates no hosted form, CRM write, buyer record, payment credential, checkout, runtime activation, execution authority, credential authority, Task Registry binding or COSV binding.

## Validation / continuation

Source merge is not public deployment proof. After exact-head repository validation and merge, independently observe the served `https://stegverse.org/services.html` body. Only an authentic served-body observation containing the ICV catalog and request boundary may advance the ICV purchase-path census from source integration to `PUBLICLY_DISCOVERABLE_AND_REQUESTABLE`. Payment/contract execution remains separately unproven.
