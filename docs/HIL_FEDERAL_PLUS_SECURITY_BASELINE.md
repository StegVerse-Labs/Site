# HIL Federal-Plus Security Baseline

## Status

Canonical security requirement for the Humans as the Interoperability Layer (HIL) experiment and its connected runtime, intake, review, publication, custody, and projection surfaces.

Security posture: `FEDERAL_REQUIREMENTS_ARE_MINIMUMS`

Authority effect: none. This document defines admission gates; it does not itself certify compliance, authorize execution, permit publication, or establish custody.

## Governing requirement

Every applicable United States federal cybersecurity requirement is treated as a minimum control floor. HIL production activation requires evidence that the implemented control set meets the applicable floor and adds StegVerse-specific controls for cryptographic continuity, authority separation, fail-closed operation, replayability, reconstructability, and cross-repository provenance.

A declaration, checklist, dependency file, workflow configuration, or vendor claim is not evidence of effective control operation.

The versioned machine-readable floor is `data/hil-federal-control-floor.json`, validated against `schemas/hil-federal-control-floor.schema.json`. A missing, incomplete, unversioned, duplicated, authority-inflating, or inventory-drifted floor causes validation failure. The floor registry is not a certification or authorization to operate.

## Baseline families

The applicable control floor must be mapped, at minimum, against current authoritative versions. The pinned floor currently includes:

- NIST SP 800-53 Revision 5, Release 5.2.0 security and privacy controls;
- NIST SP 800-218 Secure Software Development Framework Version 1.1, until superseded by a final authoritative publication;
- NIST SP 800-207 Zero Trust Architecture;
- CISA Zero Trust Maturity Model Version 2.0;
- OMB Memorandum M-22-09 where federal zero-trust objectives apply.

Applicability review must also cover:

- NIST Cybersecurity Framework;
- NIST SP 800-171 when controlled unclassified information is in scope;
- FIPS-validated cryptographic modules when required by deployment or data classification;
- applicable CISA secure-by-design, vulnerability, logging, incident-response, and zero-trust directives;
- applicable FedRAMP or agency authorization controls when a federal cloud authorization boundary exists.

The machine-readable floor and security profile intentionally record applicability, ownership, version, freshness, and evidence state rather than claiming universal applicability.

## StegVerse controls above the floor

Production HIL activation additionally requires:

1. **Independent authority planes** — intake, private review, publication, Master Record release, deployment, and execution use separately scoped credentials and independently reviewable receipts.
2. **Cryptographic chain continuity** — Primary, prompt, response bytes, provenance manifest, receiver receipt, review receipt, publication record, runtime receipt, and Master Record release remain hash-bound and replay-verifiable.
3. **No implicit authority propagation** — successful validation, custody, reconstruction, publication, model output, or human approval does not silently grant execution or release authority.
4. **Protected-value non-disclosure** — tokens, keys, credentials, protected values, and raw sensitive payloads never enter public Site projections, workflow summaries, issue comments, or downstream mirrors.
5. **Fail-closed evidence admission** — missing, stale, simulated, unverifiable, conflicting, authority-escalating, or noncanonical evidence blocks activation.
6. **Dual-control release** — public publication, production activation, and Master Record release require distinct authenticated transitions; no single browser or service credential can perform the complete chain.
7. **Immutable append-only receipts** — accepted review, publication, activation, and release receipts are write-once and hash chained; replacement requires a superseding record rather than mutation.
8. **Software supply-chain provenance** — production artifacts require dependency locking, vulnerability analysis, signed or attestable build provenance, and an inspectable software bill of materials.
9. **Continuous control observation** — repository-native workflows periodically revalidate security profile completeness, federal-floor version and inventory, evidence freshness, authority boundaries, and unresolved blockers.
10. **Recovery without authority inflation** — backup, restore, replay, reconstruction, and disaster recovery preserve original authority limits and produce new recovery receipts.
11. **Cross-repository least disclosure** — downstream repositories receive only the minimum validated fields required for their role.
12. **Security regression gate** — a previously passing deployment returns to blocked status whenever required evidence expires, a control is removed, a pinned floor reference drifts, cryptographic identity changes unexpectedly, or a validation path fails.

## Activation gates

`HIL_SECURITY_STATE=PASS` is permitted only when:

- every control marked `required` has state `IMPLEMENTED`;
- each required control has at least one repository, workflow, runtime, or receipt evidence reference;
- every evidence reference has an owner and freshness rule;
- no control is `FAILED`, `MISSING`, `STALE`, or `UNVERIFIED`;
- the exact federal-floor reference inventory and versions validate;
- all authority booleans in the security profile and floor remain false;
- deployment and runtime evidence are distinguished from static and CI evidence;
- the validator passes on the exact committed profile and floor;
- the applicable HIL handoff records the same security state and blockers.

Until then:

```text
HIL_SECURITY_STATE=BLOCKED
HIL_PRODUCTION_ACTIVATION_AUTHORITY=NONE
HIL_PUBLIC_ACQUISITION_AUTHORITY=NONE
```

## Canonical files

- `data/hil-federal-plus-security-baseline.json`
- `schemas/hil-federal-plus-security-baseline.schema.json`
- `data/hil-federal-control-floor.json`
- `schemas/hil-federal-control-floor.schema.json`
- `scripts/check_hil_federal_plus_security_baseline.py`
- `.github/workflows/check-hil-federal-plus-security-baseline.yml`
- `docs/HIL_SESSION_CONSOLIDATION_MIRROR_HANDOFF.md`
- `data/session-goal-inventories/HIL-RUNTIME-SESSION-2026-08-02.json`

## Ownership and collision boundary

- Canonical policy and public projection owner: `StegVerse-Labs/Site`.
- Runtime control implementation owner: the repository that owns the applicable runtime surface.
- Custody and reconstruction evidence owner: `master-records/orchestration`.
- Provider execution evidence owner: `StegVerse-org/LLM-adapter`.
- TVC execution and protected-value boundary owner: `StegVerse-Labs/TVC`.

Site does not duplicate runtime enforcement owned elsewhere. It admits only sanitized, commit-pinned, independently verifiable evidence.

## Release condition

This security requirement is durably transferred when the machine-readable profile, versioned federal floor, schemas, validator, workflow, canonical session inventory, and canonical handoff all resolve and the repository validator passes. Operational security remains blocked until control-specific evidence is supplied by each owner repository.
