# Generic Login / KV Projection Mirror Handoff

Issue: `StegVerse-Labs/Site#491`
Branch: `main`
State: PUBLICATION_OBSERVED_ON_IPHONE / LOGIN_AUDIT_PHYSICAL_UI_PROOF_CAPTURED / KV_ONBOARDING_SUCCESSOR_DEPENDENT_ON_PRODUCTION_INTR_KV

## Goal

Provide a bounded Site surface that requests credential verification through InTr, consumes a short-lived assertion instead of retrieving a stored password, exposes the KnowledgeVault projection only after admitted identity proof, appends searchable login-attempt/outcome evidence to Account Info, and retains a distinct step-up boundary for SKAP.

This surface is also the selected successor UI candidate for KnowledgeVault acquisition, ownership binding, installation, recovery and daily directory-tree access. That onboarding successor is **planned**, not yet production-implemented or activated.

## Authority topology

```text
cloud hosting control plane
  != user identity authority
  != KV ownership authority
  != SKAP authority

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

Site remains an assertion/UI consumer, not canonical KV state authority, SKAP custody authority, or cloud credential authority. Cloud-host credentials are infrastructure-control-plane credentials and must never become browser, account, KV or SKAP credentials.

## Login audit contract

`generic-login-test.html` appends audit evidence into Account Info for every login submission:

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

## Account-created forward transition

PR `#498` fixed the iPhone-observed terminal account-creation state.

After the account is actually saved:

- remaining sensitive inputs are cleared;
- the creation/verification form is hidden;
- an explicit `Continue to login` action is shown;
- the page automatically returns to `generic-login-test.html` after a short delay;
- no new identity, KV, SKAP or credential authority is granted by the navigation transition.

Merged evidence:

```text
PR: #498
head: 4d5f5c7482bff150482c2c37920f6c8fe5d7ff91
merge: 726409ae50f58884cffaeadffce6a1e0904e0df4
merged_at: 2026-08-26T07:05:08Z
```

## Other existing contracts

- Production InTr remains fail-closed `NOT_PROVISIONED` until a real verifier is attached.
- The TEST_ONLY local verifier emits the same bounded identity assertion shape without credential disclosure.
- Personal Info Save remains a TEST_ONLY KV projection receipt bound to the current identity assertion.
- Ordinary account/KV login never unlocks SKAP; `_Vault/SKAP` requires a separate `stegverse.intr.step-up-assertion/v1`.
- Account creation/recovery retains verified Email/Text metadata and never persists plaintext passwords.

## Deterministic validation

`scripts/validate_generic_login_test.py` proves the currently implemented test/projection behavior, including:

- successful page login appends exact `LOGIN_ATTEMPT -> LOGIN_SUCCESS`;
- later invalid login appends exact `LOGIN_ATTEMPT -> LOGIN_FAILED`;
- all event hashes recompute from canonical non-secret event bodies;
- every prior-event hash links correctly;
- all events share one deterministic account search hash;
- raw username/password are absent from audit records;
- success audit binds assertion ID/assurance metadata;
- failed audit does not invent an assertion;
- production verifier absence remains fail closed;
- identity and SKAP assertion boundaries remain non-disclosing;
- successful account creation reaches an explicit terminal `ACCOUNT CREATED -> login` forward transition without granting authentication authority.

Prior hosted evidence retained:

```text
PR: #495
head: 107f51cf25e15a1117903ebfb05d7005e8714d79
Generic Login Test Validation run: 32911794044 SUCCESS
Site Handoff Orchestrator run: 32911794056 SUCCESS
merge: dc95c5fe52740273088e6bfbd54c3807f4014de7
```

PR #498 is separately merged as recorded above. Merge is not public-propagation proof.

## KV onboarding / ownership successor

The current page is the selected human-facing candidate for a future KnowledgeVault onboarding state machine.

Planned durable user states:

```text
NO_KV
  -> Create My KnowledgeVault
  -> Attach Existing KnowledgeVault

KV_OWNED_NOT_INSTALLED
  -> Ownership Verified
  -> Install on This Device
  -> View Ownership Receipt

KV_ACTIVE
  -> Open KnowledgeVault
  -> Register Another Device
  -> Recovery / Ownership
  -> SKAP Status
```

Account creation or successful login must **not** imply KV ownership. Ownership is a separate future state transition requiring canonical KV/InTr evidence.

Planned ownership/install sequence:

```text
KV_CREATED
-> OWNER_BOUND
-> DEVICE_REGISTERED
-> INSTALLATION_ADMITTED
-> KV_ACTIVE
```

The ownership/installation receipt should bind non-secret identifiers and evidence such as KV identifier, owner identity reference, originating device/node, creation timestamp, InTr receipt chain, installation state, recovery authority and migration/transfer rules. It must not embed secret credential material.

SKAP initialization remains separate and stronger than ordinary KV login. A newly created KV may exist before SKAP is initialized. Opening or initializing `_Vault/SKAP` requires a separate step-up assertion and the mandatory KV -> SKAP InTr boundary.

## Production dependency boundary for onboarding

The onboarding successor can continue at the UI/schema/validator level now, but physical completion depends on live KV/InTr work.

Required before production activation:

```text
real production InTr verifier/session path
real KV create/attach/read/write surface
real owner-identity binding
real device registration binding
real KV directory enumeration
real Personal Info mutation into KV custody
real installation/ownership receipts
real recovery/transfer semantics
real SKAP step-up admission with chained KV -> SKAP receipt
```

Until those exist, the Site must fail closed rather than silently promote browser-local state into canonical KV ownership or custody.

## Cloud-host credential boundary

The hosted Site may depend on infrastructure-provider credentials for deployment/routing/origin access, but that is a separate machine-facing control-plane boundary. Those credentials must remain TV/TVC-governed references/use capabilities and must never be disclosed to the browser or treated as account/KV/SKAP authority.

A hosting-route/rendezvous receipt may be correlated with later InTr evidence, but it is not itself an InTr KV receipt and grants no KV ownership or SKAP authority.

## Publication target

```text
https://stegverse.org/generic-login-test.html
https://stegverse.org/create-account-test.html
https://stegverse.org/forgot-password-test.html
```

Public propagation is now physically observed on the current-user iPhone at `stegverse.org/generic-login-test.html`.

Observed public/runtime evidence on 2026-08-26:
- page status visibly reached `SUCCESS`;
- `Successful Login` rendered with `InTr identity ADMITTED / TEST_ACCOUNT`;
- the KnowledgeVault directory projection rendered;
- `_Vault/SKAP` remained visibly locked and required `Validate`;
- Account Info rendered the saved recovery attributes;
- Login History visibly contained `LOGIN_ATTEMPT` followed by `LOGIN_SUCCESS`;
- both events displayed searchable `sha256:` login-event hashes;
- the success record visibly linked to the prior attempt hash.

This is public UI / physical browser evidence for the TEST_ONLY projection. It is not production InTr identity authority, real KV custody, real SKAP custody, or proof of production account-audit persistence.

## Current authority boundary

```text
Site presentation authority: UI ONLY
production identity authority: NOT PROVISIONED
Site credential custody: NONE
login audit authority: AUDIT_ONLY / TEST_ONLY LOCAL PROJECTION
searchable login-event hash chain: HOSTED VALIDATED / MERGED
account-created forward transition: MERGED
KV onboarding/ownership successor: PLANNED
real KV authority/custody: NOT CLAIMED
real KV ownership binding: NOT IMPLEMENTED
real device-install binding: NOT IMPLEMENTED
real SKAP authority/custody: NOT CLAIMED
cloud credential authority in browser: NONE
public propagation of latest merged state: OBSERVED ON CURRENT-USER IPHONE
```

## Next executable boundary

1. Preserve the now-observed public UI/source contract and retain the captured physical publication evidence.
2. Continue onboarding state-machine/schema/validator design without claiming live KV ownership.
3. Connect the assertion consumer to the real production InTr verifier when provisioned.
4. Bind `Create/Attach KV`, owner binding, device registration, install admission and live directory enumeration to canonical KV operations/receipts.
5. Replace TEST_ONLY Personal Info and login-audit custody with real InTr/KV custody while preserving the same non-disclosure and hash-chain contracts.
6. Preserve SKAP as a separately stepped-up double-Interlock surface.

## User action boundary

No user credential or manual provider action is required merely to continue source/UI work. When live activation reaches the physical owner/device boundary, the user must perform the requested owner-authorized iPhone/device validation and any SKAP step-up interaction through the trusted browser surface. Credentials must never be pasted into chat, Drive or GitHub.
