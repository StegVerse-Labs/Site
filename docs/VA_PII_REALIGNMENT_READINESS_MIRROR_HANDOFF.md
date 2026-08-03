# VA PII Realignment Readiness Mirror Handoff

## Identity

```text
Task ID: VA-PII-REALIGNMENT-READINESS-001
Originating goal: move PII redaction and post-credential identity linkage from policy into machine-observable implementation readiness
Repository: StegVerse-Labs/Site
Branch: main
Canonical parent: docs/VA_PII_REDACTION_CREDENTIAL_REALIGNMENT_MIRROR_HANDOFF.md
Canonical implementation issue: StegVerse-Labs/Site#116
Reference-validation issue: StegVerse-Labs/Site#170
Public-state issue: StegVerse-Labs/Site#113
Registry: data/va-claim-assistant/pii-realignment-readiness.json
Registry validator: scripts/validate_va_pii_realignment_readiness.py
Registry workflow: .github/workflows/va-pii-realignment-readiness.yml
Registry receipt: data/va-claim-assistant/pii-realignment-readiness-validation.json
Production detector schema: data/va-claim-assistant/pii-production-detector-evidence.schema.json
Production detector observer: scripts/observe_va_pii_production_detector_evidence.py
Production detector workflow: .github/workflows/va-pii-production-detector-evidence.yml
Production detector receipt: data/va-claim-assistant/pii-production-detector-readiness.json
Redaction evidence schema: data/va-claim-assistant/pii-redaction-working-copy-evidence.schema.json
Redaction evidence observer: scripts/observe_va_pii_redaction_working_copy_evidence.py
Redaction evidence workflow: .github/workflows/va-pii-redaction-working-copy-evidence.yml
Redaction readiness receipt: data/va-claim-assistant/pii-redaction-working-copy-readiness.json
```

## Claim

```text
role: CROSS_REPOSITORY_INTEGRATION_VALIDATION
claim state: MACHINE_OWNED
release condition: all nine readiness requirements COMPLETE, current continuous-monitoring evidence, independent assessment retained, and zero unresolved high or critical findings
collision boundary: do not modify Site#116 document processors, adapter route implementation, TVC credentialing implementation, or Master Records custody implementation
```

## Current readiness

```text
PII-RDY-01 Site#116 production PII detection and uncertain-result review: CLAIMED
PII-RDY-02 Site#116 redaction and pseudonymous working copy: BLOCKED
PII-RDY-03 Site#116 model-facing leakage verification: BLOCKED
PII-RDY-04 TVC credentialing handoff admission: BLOCKED
PII-RDY-05 TVC post-credential identity-linkage admission: BLOCKED
PII-RDY-06 LLM-adapter raw PII rejection and sanitized-context enforcement: BLOCKED
PII-RDY-07 Master Records privacy-event custody and reconstruction: BLOCKED
PII-RDY-08 Site#113 veteran-visible privacy controls: BLOCKED
PII-RDY-09 independent privacy and security assessment: BLOCKED
```

## PII-RDY-01 evidence state

Reference evidence under `Site#170` is complete only for the synthetic evaluation lane:

```text
data/va-claim-assistant/pii-detection-evaluation-receipt.json
state: PASS
required_class_recall: 1.0
clean_case_false_positive_rate: 0.0
review_required_count: 1
production_detector_ready: false
private_document_upload_enabled: false
```

The production observer has emitted:

```text
data/va-claim-assistant/pii-production-detector-readiness.json
state: BLOCKED
blocker: production_detector_evidence_missing
reference_receipt_is_insufficient: true
```

A production or controlled-production-equivalent receipt must prove an admitted preprocessing runtime, at least 0.99 required-class recall, no more than 0.05 clean-case false-positive rate, uncertain-case review routing, no model processing before the privacy gate, no raw PII in prompts/outputs/traces/logs, private upload disabled, custody retained, and false authority and activation effects.

Installed PII-RDY-01 controls:

```text
schema commit: 7f9ed06ed066bc0fb836b76e85550c56730baeb3
observer commit: 048e8ec454db36566b1a486eb06c86e7e64ba7a8
workflow commit: dc7d253ca9dbfa399741e55f058bc0ca9bc7edd0
```

## PII-RDY-02 evidence gate

`PII-RDY-02` now has a separate machine-observable release gate. A production or controlled-production-equivalent receipt must prove:

- runtime class `ADMITTED_PRIVATE_DOCUMENT_PREPROCESSOR`;
- exact processor path and immutable commit SHA;
- distinct original-document and redacted-document SHA-256 values;
- a redaction-manifest SHA-256 bound to both document hashes;
- at least one direct-identifier replacement;
- page and region anchors retained;
- a purpose-limited, non-global pseudonymous token;
- raw document did not leave the privacy zone;
- no raw PII remains in the working copy;
- model release occurred only for the verified redacted copy;
- private upload remains disabled;
- custody reference retained;
- authority and activation effects false.

Installed PII-RDY-02 controls:

```text
schema commit: d4a43c68e7ebdb19f762cec5c2b5d270095ae5f1
observer commit: 7be64a12dd083424810ab5c8e5bdab6050b66f0b
workflow commit: 7da682c506ff1d232c85314d0661c23c64d5d044
```

Expected implementation evidence:

```text
data/va-claim-assistant/pii-redaction-working-copy-evidence.json
```

Expected machine receipt:

```text
data/va-claim-assistant/pii-redaction-working-copy-readiness.json
```

Until implementation evidence exists and passes, `PII-RDY-02` remains `BLOCKED`; a missing initial observer receipt is not interpreted as success.

## State and ownership

Each owner updates only its own requirement after exact evidence exists. `Site#116` owns production detector and redaction implementation; `Site#170` owns synthetic detector reference validation. Plans, schemas, fixture-only receipts, or self-attestation cannot complete an operational requirement.

The registry and evidence observers grant no identity, credential, document-processing, medical, representation, rating, filing, publication, or activation authority. They cannot activate private upload, identity linkage, or filing.

## Transfer

```text
MERGED INTO: StegVerse-Labs/Site#116
MERGED INTO: StegVerse-Labs/Site#170
MERGED INTO: StegVerse-Labs/Site#113
```

The continuation path is durable and machine-owned. This task remains active until all nine requirements complete or are superseded by equivalent inspectable evidence.
