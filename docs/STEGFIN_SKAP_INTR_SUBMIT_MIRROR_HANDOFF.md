# StegFin SKAP InTr Submit Mirror Handoff

Status: DOUBLE_INTERLOCK_PRIMARY_GATEWAY_ALIGNMENT_IN_PROGRESS
Repository: `StegVerse-Labs/Site`
Goal ID: `SITE-STEGFIN-SKAP-INTR-SUBMIT-001`
Claim: `SITE-STEGFIN-SKAP-INTR-SUBMIT-20260825`
Updated: 2026-08-25T13:48:00-05:00

## Purpose

Bind the current-user iPhone StegFin browser-sealed Coinbase capsule to the KV-hosted SKAP Vault without granting Site, Device, ordinary KV, GitHub, the public carrier, or the browser provider-operation authority or durable provider-secret custody.

Canonical credential topology is now:

```text
Device <-InTr-> KV <-InTr-> SKAP Vault
```

The SKAP Vault is logically inside the KnowledgeVault namespace at `_Vault/SKAP`, but the second `KV <-InTr-> SKAP Vault` boundary is mandatory. Ordinary KV may retain only references, ciphertext and non-secret evidence; it has no credential plaintext/decryption authority.

## Primary vs fallback public transport

Primary:

```text
current iPhone
-> browser ciphertext
-> StegVerse shared Service Gateway
-> DEVICE/KV InTr receipt
-> STAGED_FOR_TVC
-> machine-owned TVC drain
-> KV/SKAP_VAULT InTr receipt
-> ADMITTED_TO_SKAP_VAULT
```

Fallback:

```text
current iPhone
-> browser ciphertext
-> explicit zero-credential rotating resident tunnel
-> TVC resident ingress
-> both interlocks still required before SKAP Vault admission
```

The fallback does not bypass either interlock and does not become credential/provider/execution authority.

## Browser state semantics

Site must never collapse these states:

```text
STAGED_FOR_TVC
  = exact ciphertext crossed DEVICE -> KV through InTr
  = first interlock complete
  != SKAP Vault custody

ADMITTED_TO_SKAP_VAULT
  = DEVICE -> KV receipt verified
  + KV -> SKAP_VAULT receipt verified and chained
  + SKAP Vault custody admitted
  != provider permission
  != order authorization
```

For primary Gateway responses, Site must require:
- schema `stegverse.service_gateway.coinbase_skap_stage_receipt/v1`;
- `decision=STAGED_FOR_TVC`;
- embedded `device_kv_interlock_receipt` with `connector=InTr`, `DEVICE -> KV`, matching credential/operation binding and no secret plaintext/authority transfer;
- `gateway_credential_value_access=false`;
- `gateway_decryption_authority=false`;
- `gateway_execution_authority=NONE`;
- `tvc_admission_completed=false`;
- `next_required_transition=KV_SKAP_VAULT_INTERLOCK_ADMISSION`;
- `blind_retry_allowed=false`.

The browser emits a distinct local event for first-hop staging and must not emit the SKAP-Vault-admitted event from that response.

A later TVC/SKAP Vault admission observation may be rendered only when the response/evidence proves:
- `decision=ADMITTED_TO_SKAP_VAULT`;
- DEVICE/KV receipt;
- KV/SKAP_VAULT receipt whose prior hash binds the first receipt;
- matching credential reference and operation id;
- `kv_decryption_authority=false`;
- `device_durable_secret_custody=false`;
- no decryption/rewrap before endpoint verification;
- execution authority `NONE`.

## Recipient configuration and route discovery

Recipient-key configuration remains independent from public transport selection:

```text
recipient config = how/where the capsule is sealed
primary endpoint = StegVerse shared Service Gateway
fallback descriptor = resident rotating InTr route
```

Immediately before POST, Site must revalidate the active recipient lease and selected transport. Production repository state remains fail closed until live TVC recipient-key/liveness and public route evidence are projected.

## Production fail-closed state

`assets/stegfin-phone/coinbase-skap-ingress-config.json` and `assets/stegfin-phone/coinbase-skap-intr-route.json` remain `NOT_PROVISIONED`. Source/CI must not invent a synthetic production endpoint, public key, route, or admission receipt.

Credential entry must remain disabled until the current recipient key and primary Gateway endpoint (or explicit governed fallback) are both live and current.

## Authority boundaries

- credential authority: `TV/TVC`
- credential custody target: `KV_HOSTED_SKAP_VAULT`
- Site credential custody: `NONE`
- Device durable credential custody: `NONE`
- ordinary KV decryption authority: `NONE`
- public Gateway credential/decryption/execution authority: `NONE`
- fallback carrier credential/provider authority: `NONE`
- GitHub-token runtime authority: `NONE`
- Render: `PROHIBITED`
- wallet signing/broadcast authority: unchanged `USER_ONLY`

## Current evidence

- `continuity-vault-kit` SKAP Vault double-interlock run `32884444828`: `SUCCESS`.
- TVC SKAP Vault stage-drain run `32884923736`: `SUCCESS`.
- TVC full Coinbase validation run `32884923740`: `SUCCESS`.
- LLM-adapter primary Gateway double-interlock validation source repaired; runtime/provisioning remains separately evidence-gated.

## Completion boundary

This Site claim is source-complete only after the browser distinguishes primary `STAGED_FOR_TVC` from later `ADMITTED_TO_SKAP_VAULT`, validates the Device/KV boundary receipt, preserves ambiguity/no-blind-retry behavior, maintains ciphertext-only submission and remains fail closed while production config is unprovisioned. Production activation remains open until real recipient-key/route evidence and a real owner-authorized double-interlock receipt chain are observed.
