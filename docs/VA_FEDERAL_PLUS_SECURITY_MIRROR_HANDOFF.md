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

## Claim state

```text
role: SECURITY_BASELINE_AND_CONTINUOUS_ASSURANCE_CONTRACT
claim state: RELEASED_COMPLETE
validation: PASS
release evidence: federal-plus-security-baseline-validation.json
collision boundary: no compliance certification claim, no production activation, no credential handling, no document processing, and no filing transport
```

The bounded baseline-definition task is complete. Operational implementation, independent assessment, and production authorization remain separate active tasks.

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

## Validation result

```text
state: PASS
federal floor required: true
StegVerse exceeds floor required: true
NIST control families: 20
StegVerse-plus domains: 7
phishing-resistant authentication required: true
continuous assurance required: true
independent evidence required for compliance claims: true
authority effect: false
activation effect: false
```

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

## Transfer

```text
MERGED INTO: StegVerse-Labs/Site#113
MERGED INTO: StegVerse-Labs/Site#116
```

The contract, validator, workflow, PASS receipt, handoff, and issue acceptance preserve the session requirement durably. No chat history is required to recover the security baseline.

## Remaining operational work

- map and tailor controls to the final impact categorization;
- implement controls in Site#116, LLM-adapter#90, TVC, and Master Records;
- retain control-level test evidence and continuous receipts;
- complete threat modeling, parser-abuse tests, incident exercises, and custody reconstruction;
- obtain independent assessment before any federal compliance or authorization claim;
- keep document upload and filing blocked while high or critical findings or missing evidence remain.

## Archive condition

This subordinate baseline task is archive-safe. The broader session remains active while operational controls, independent assessment, document runtime, filing transport, route expansion, and Ecosystem Chat activation remain incomplete.
