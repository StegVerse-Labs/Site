# VA PII Redaction and Credential Realignment Mirror Handoff

## Identity

```text
Task ID: VA-PII-REALIGNMENT-001
Originating goal: strip PII from VA Claims Chat documents before model-facing processing and realign approved records to the veteran only after credentialing handoff
Repository: StegVerse-Labs/Site
Branch: main
Canonical parent: docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
Canonical security parent: docs/VA_FEDERAL_PLUS_SECURITY_MIRROR_HANDOFF.md
Canonical issue: StegVerse-Labs/Site#116
Public and consent issue: StegVerse-Labs/Site#113
Contract: data/va-claim-assistant/pii-redaction-credential-realignment-contract.json
Validator: scripts/validate_va_pii_redaction_credential_realignment.py
Workflow: .github/workflows/va-pii-redaction-credential-realignment.yml
Receipt: data/va-claim-assistant/pii-redaction-credential-realignment-validation.json
```

## Claim

```text
role: PRIVACY_BOUNDARY_AND_IDENTITY_LINKAGE_CONTRACT
claim state: RELEASED_COMPLETE
validation: PASS
validation receipt SHA-256: f249a74bdacdbeb11434130670093cf1c189f29797aaa41974bbe5dc0a3ab319
contract SHA-256: 7af4c9448ec0bca5165037c0bb9bbf0b34a8e8d9cc8bdb4d57c36ca4356d33e1
release evidence: committed PASS receipt plus acceptance in Site#113 and Site#116
collision boundary: no production credentialing, no raw-document processor mutation, no identity proofing, no credential storage, no filing activation
```

## Required architecture

The validated contract separates four trust zones:

1. `credentialing_vault` — verified veteran identity and credential assurance only;
2. `document_privacy_zone` — encrypted raw upload, malware scan, PII detection, redaction manifest, pseudonymous token, and redacted working copy;
3. `claims_reasoning_zone` — redacted documents and sanitized derived evidence only;
4. `identity_linkage_zone` — post-credentialing binding of an approved derived record or exact filing package hash to a verified veteran identity reference.

Raw documents and direct identifiers must not enter the LLM adapter, analytics, logs, or public surfaces.

## PII lifecycle

```text
encrypted upload
→ malware and active-content scan
→ original hash
→ PII/PHI detection
→ redaction manifest
→ pseudonymous document token
→ leakage verification
→ model-facing processing of redacted copy only
→ sanitized derived record
→ verified credentialing handoff
→ scoped and expiring identity-linkage receipt
→ hash-bound association of approved record/package to veteran identity reference
```

Pseudonymization is not anonymization. Identity is not restored into AI context. The linkage capability remains separately protected, purpose-limited, expiring, and revocable.

## Federal floor and StegVerse-plus requirement

Applicable NIST security, privacy, and digital-identity controls and VA privacy principles are the minimum floor. StegVerse adds:

- raw-document isolation before model processing;
- cryptographically bound redaction manifests;
- no permanent cross-context tracking identifier;
- post-credentialing linkage only;
- exact derived-record or filing-package hash binding;
- purpose-limited and expiring linkage;
- veteran-visible access, export, deletion, and linkage history;
- immutable custody and deterministic reconstruction;
- no PII restoration into prompts or outputs.

No compliance or VA-approval claim is authorized by this contract.

## Validation result

```text
state: PASS
privacy zones: 4
release gates: 13
federal floor required: true
StegVerse must exceed floor: true
raw PII to adapter prohibited: true
verified credentialing handoff required: true
pre-credential re-association prohibited: true
authority effect: false
activation effect: false
```

## Fail-closed states

```text
PII_DETECTION_UNCERTAIN_REVIEW_REQUIRED
REDACTION_VERIFICATION_FAILED
CREDENTIALING_HANDOFF_MISSING
CREDENTIALING_HANDOFF_EXPIRED
CREDENTIALING_HANDOFF_REVOKED
LINKAGE_SCOPE_MISMATCH
PACKAGE_HASH_MISMATCH
DELETION_OR_CUSTODY_EVIDENCE_MISSING
```

## Cross-repository ownership

```text
StegVerse-Labs/Site#113
- consent, privacy notice, veteran-visible status, export and deletion surfaces

StegVerse-Labs/Site#116
- document privacy zone, PII detection, redaction, redaction verification, raw-document deletion

StegVerse-org/LLM-adapter#90
- reject raw PII and accept only redacted or sanitized derived context

StegVerse-Labs/TVC
- credentialing-vault capability, scoped identity-linkage capability, expiry and revocation

master-records/orchestration
- redaction manifest, credentialing handoff, identity-linkage, deletion, access, custody, and reconstruction receipts
```

## Operational activation conditions

Private document upload or filing cannot activate until:

- PII detector/redactor tests pass;
- leakage tests pass;
- uncertain detections enter human review;
- credentialing handoff validation passes;
- linkage scope, expiry, and revocation are enforced;
- raw documents remain isolated;
- logs and analytics contain no direct identifiers;
- deletion and custody reconstruction pass;
- independent privacy and security assessment is retained;
- no unresolved high or critical findings remain.

## Transfer

```text
MERGED INTO: StegVerse-Labs/Site#116
MERGED INTO: StegVerse-Labs/Site#113
MERGED INTO: StegVerse-org/LLM-adapter#90
MERGED INTO: StegVerse-Labs/TVC credentialing and linkage capability lane
MERGED INTO: master-records/orchestration custody lane
```

The bounded contract-definition and validation task is complete. Operational PII detection, redaction, credentialing, linkage, deletion, custody, and independent assessment remain assigned to the named owners.

## Archive condition

This requirement is durable and no longer depends on chat history. The broader session remains active while the operational privacy boundary, credentialing handoff, document runtime, filing transport, route expansion, and Ecosystem Chat activation remain incomplete.
