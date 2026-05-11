# MS-013 Vaulted Capability Transition Layer

## Purpose

MS-013 defines the first point where TV/TVC becomes a consequence of the transition table.

That point occurs when a table-authorized action requests a private, scarce, revocable, metered, or value-bearing capability.

## Boundary

```text
transition table
→ capability request
→ vault policy
→ claim/scope/pricing/revocation check
→ ALLOW / DENY / HOLD / FAIL_CLOSED
→ receipt
```

## TV / Token Vault role

```text
Controls private authority objects, capability pointers, revocation status, release conditions, and non-exposure of raw secrets.
```

## TVC role

```text
Represents value-bearing right, price, claim, stake, allowance, or metered access associated with using a vaulted capability.
```

## What is unlocked now

```text
capability request evaluation
claim validation placeholder
receipt generation
release denial
review hold
non-secret pointer receipt
```

## What is not unlocked

```text
real token issuance
payment settlement
raw credential storage
raw credential release
public financial promises
workflow mutation
```

## Run

```text
python tools/vaulted_capability_gate.py \
  --policy data/vault/vaulted-capability-policy-v1.json \
  --out-dir vault_reports
```
