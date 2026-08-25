# Generic Login / KV Projection Mirror Handoff

Issue: `StegVerse-Labs/Site#491`
Branch: `main`
State: LOGIN_AUDIT_HOSTED_VALIDATED_MERGED_PUBLICATION_PENDING

## Goal

Provide a bounded Site surface that requests credential verification through InTr, consumes a short-lived assertion instead of retrieving a stored password, exposes the KnowledgeVault projection only after admitted identity proof, appends searchable login-attempt/outcome evidence to Account Info, and retains a distinct step-up boundary for SKAP.

## Authority topology

```text
Browser / Device
  -> Site presentation
  -> InTr identity verification request
  -> identity assertion
  -> KV directory projection
  -> Account Info login audit projection
  -> Personal Info transition requests
  -> separate SKAP step-up request
  -> KV -> SKAP InTr boundary
```

Canonical credential topology remains:

```text
Device <-InTr-> KV <-InTr-> SKAP Vault
```

Site remains an assertion/UI consumer, not canonical KV state authority, SKAP custody authority, or cloud credential authority.

## Login audit contract

`generic-login-test.html` now appends audit evidence into Account Info for every login submission:

```text
LOGIN_ATTEMPT -> LOGIN_SUCCESS
```

or:

```text
LOGIN_ATTEMPT -> LOGIN_FAILED
```

Each record uses:

```text
schema: stegverse.intr.login-audit-event/v1
transport_protocol: InTr
account_ref_sha256: sha256:<deterministic account correlation handle>
prior_login_event_hash: <prior event hash or null>
login_event_hash: sha256:<canonical event hash>
secret_plaintext_present: false
credential_material_recorded: false
authority_effect: AUDIT_ONLY
```

`login_event_hash` is the exact searchable/correlation handle for reviewing other available evidence about that login. `account_ref_sha256` permits account-scoped search without writing the submitted username into each audit event. Successful records bind the non-secret assertion ID and assurance level when available; failure records do not invent assertion evidence.

The event chain is append-only in the current TEST_ONLY browser projection. Each new record binds the prior hash, making removed/reordered/tampered history detectable by deterministic verification. Raw username and password values are prohibited from audit records.

Production successor requirement: preserve this event schema/search/hash-chain behavior when moving history from browser-local TEST_ONLY state into real InTr/KV account-audit custody.

## Other existing contracts

- Production InTr remains fail-closed `NOT_PROVISIONED` until a real verifier is attached.
- The TEST_ONLY local verifier emits the same bounded identity assertion shape without credential disclosure.
- Personal Info Save remains a TEST_ONLY KV projection receipt bound to the current identity assertion.
- Ordinary account/KV login never unlocks SKAP; `_Vault/SKAP` requires a separate `stegverse.intr.step-up-assertion/v1`.
- Account creation/recovery retains verified Email/Text metadata and never persists plaintext passwords.

## Deterministic validation

`scripts/validate_generic_login_test.py` proves:

- successful page login appends exact `LOGIN_ATTEMPT -> LOGIN_SUCCESS`;
- later invalid login appends exact `LOGIN_ATTEMPT -> LOGIN_FAILED`;
- all event hashes recompute from canonical non-secret event bodies;
- every prior-event hash links correctly;
- all events share one deterministic account search hash;
- raw username/password are absent from audit records;
- success audit binds assertion ID/assurance metadata;
- failed audit does not invent an assertion;
- production verifier absence remains fail closed;
- identity and SKAP assertion boundaries remain non-disclosing.

Hosted evidence:

```text
PR: #495
head: 107f51cf25e15a1117903ebfb05d7005e8714d79
Generic Login Test Validation run: 32911794044
result: SUCCESS
Site Handoff Orchestrator run: 32911794056
result: SUCCESS
merge: dc95c5fe52740273088e6bfbd54c3807f4014de7
```

## Publication target

```text
https://stegverse.org/generic-login-test.html
```

Public propagation of the merged audit UI has not yet been independently observed in this handoff, so physical-public completion remains open.

## Current authority boundary

```text
Site presentation authority: UI ONLY
production identity authority: NOT PROVISIONED
Site credential custody: NONE
login audit authority: AUDIT_ONLY / TEST_ONLY LOCAL PROJECTION
searchable login-event hash chain: HOSTED VALIDATED / MERGED
real KV authority/custody: NOT CLAIMED
real SKAP authority/custody: NOT CLAIMED
cloud credential authority in browser: NONE
```
