# VA Federal-Plus Security Mirror Handoff

## Identity

```text
Task ID: VA-SEC-FEDERAL-PLUS-001
Originating goal: federal security requirements are the minimum and StegVerse VA capabilities must exceed them
Repository: StegVerse-Labs/Site
Branch: main
Canonical parent: docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
Canonical issue: StegVerse-Labs/Site#113
Document workspace issue: StegVerse-Labs/Site#116
Contract: data/va-claim-assistant/federal-plus-security-baseline.json
Validator: scripts/validate_va_federal_plus_security_baseline.py
Workflow: .github/workflows/va-federal-plus-security-baseline.yml
Receipt: data/va-claim-assistant/federal-plus-security-baseline-validation.json
```

## Claim

```text
role: SECURITY_BASELINE_AND_CONTINUOUS_ASSURANCE_CONTRACT
claim state: MACHINE_OWNED_VALIDATION
claim created: 2026-08-02T21:54:00Z
release condition: committed PASS receipt and acceptance into Site#113, Site#116, LLM-adapter#90, TVC, and Master Records continuation records
collision boundary: no compliance certification claim, no production activation, no credential handling, no document processing, and no filing transport
```

## Federal floor

The baseline treats applicable federal requirements as a floor, not a target. It references:

- NIST SP 800-53 Rev. 5 Release 5.2.0 control families;
- NIST digital identity expectations including phishing-resistant authentication for privileged and filing actions;
- zero-trust principles of explicit verification, least privilege, assume breach, and service identity;
- FedRAMP-style automated continuous assurance rather than point-in-time paperwork alone.

Impact categorization, tailoring, overlays, agency requirements, legal review, and independent assessment remain required before any compliance claim.

## StegVerse-plus controls

The contract adds controls above the floor for:

- phishing-resistant MFA, device binding, step-up authentication, short-lived credentials, and revocation;
- raw-document isolation, encryption, field-level protection, minimized retention, deletion receipts, and no model training without separate consent;
- sandboxed parsing, malware and active-content scanning, egress allowlists, decompression limits, and prompt-injection/data-exfiltration defenses;
- cryptographic hashes and append-only custody for every source, derived record, package, authorization, attempt, and confirmation;
- exact-package veteran authorization, dual transport admission, idempotency, duplicate prevention, revocation, and partial-failure reconstruction;
- continuous security evidence, tamper-evident audit, signed builds, dependency and secret scanning, incident containment, and privacy-event decisions;
- purpose limitation, data minimization, veteran-visible history and deletion state, and no hidden rating optimization.

## Activation gates

No private document or filing capability may activate until all recorded gates pass, including control mapping, impact categorization, threat model, trust-boundary verification, identity tests, encryption/key tests, parser-abuse tests, custody reconstruction, incident exercise, independent assessment, current continuous-monitoring receipt, and zero unresolved high or critical findings.

## Prohibited claims

Without directly inspectable independent evidence, the system must not claim:

- FedRAMP authorized;
- FISMA compliant;
- NIST compliant;
- VA approved;
- federal compliant.

## Cross-repository continuation

```text
Site#113:
public status, security posture projection, filing and veteran-authorization surfaces

Site#116:
private document isolation, parser defenses, privacy, retention, deletion, export, and derived-record security

LLM-adapter#90:
service identity, sanitized-context boundary, route-level fail closed, provider isolation, and execution receipts

TVC:
scoped capability, credential, provider, document-processing, and future transport admission

master-records/orchestration:
append-only custody, reconstruction, incident evidence, package and confirmation records
```

## Validation

```text
python scripts/validate_va_federal_plus_security_baseline.py
```

Success requires the full federal floor, seven StegVerse-plus domains, phishing-resistant authentication, continuous assurance, independent-evidence gating, and no authority or activation effect.

## Transfer

```text
MERGED INTO: StegVerse-Labs/Site#113
MERGED INTO: StegVerse-Labs/Site#116
```

After a PASS receipt and issue acceptance, this bounded baseline task may release. Implementation and operational assessment remain owned by the named repositories and cannot be inferred from the contract.

## Archive condition

This security requirement is durable when the contract, validator, workflow, PASS receipt, handoff, and canonical issue acceptance exist. The broader session remains active while operational controls, independent assessment, document runtime, filing transport, route expansion, and Ecosystem Chat activation remain incomplete.
