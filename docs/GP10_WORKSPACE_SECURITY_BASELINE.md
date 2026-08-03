# GP10 Workspace Security Baseline

Status: ACTIVE IMPLEMENTATION BASELINE
Updated: 2026-08-02
Owner: `StegVerse-Labs/Site`
Canonical handoff: `docs/GP10_WORKSPACE_MIRROR_HANDOFF.md`

## Governing objective

Applicable federal cybersecurity requirements are the minimum floor. The GP10 browser workspace should exceed that floor where a static, unlisted GitHub Pages surface can do so safely, while refusing to imply authentication, durable custody, regulatory compliance, or execution authority.

This document is a control mapping and implementation contract, not a certification or attestation of federal compliance.

## Reference families

The implementation is organized around control outcomes represented in NIST SP 800-53 Revision 5 and CISA Secure by Design guidance:

- access enforcement and least privilege;
- information-flow restriction;
- audit event content and integrity;
- identification and authentication boundaries;
- system and information integrity;
- cryptographic protection;
- secure-by-default operation;
- high-quality logging and radical transparency;
- explicit failure and recovery behavior.

## Installed browser controls

1. **Script execution restriction**
   - Document Content Security Policy permits scripts only from the same origin.
   - Plugins and embedded objects are denied.
   - Base URI mutation is denied.
   - Form submission to remote endpoints is denied.
   - Network connections are limited to the same origin.

2. **Information-flow minimization**
   - Referrer policy is `no-referrer`.
   - The workspace performs no automatic upload or telemetry.
   - Imported evidence remains browser-local until the user explicitly exports it.
   - File inputs are cleared when the security lock engages.

3. **Ambient-authority reduction**
   - The workspace is unlisted and excluded from indexing, but this is not treated as authentication.
   - No execution authority is created by local records, imports, posture calculations, exports, or integrity receipts.
   - New windows use `noopener`.

4. **Session exposure controls**
   - A 15-minute inactivity timer locks the workspace.
   - A page hidden for five minutes locks on return.
   - Unlocking requires an explicit local user action.
   - Locking does not falsely claim deletion or encryption of existing browser storage.

5. **Cryptographic integrity controls**
   - Imported source files retain SHA-256 hashes in canonical evidence packets.
   - The security module can emit a SHA-256 integrity receipt over the current candidate record, evidence packets, and evidence reviews.
   - The receipt includes a session nonce, timestamp, digest algorithm, payload digest, custody warning, and `execution_authority: false`.
   - Integrity receipts prove byte-level consistency of the locally assembled payload, not truth, authority, identity, or approval.

6. **Local-data control**
   - The user can explicitly clear GP10 workspace local data.
   - The clear operation targets only GP10-namespaced local-storage keys and does not claim secure media erasure.

7. **Fail-closed validation**
   - `scripts/check_gp10_workspace.py` verifies required policy markers, security-module loading, adaptive gating, examples synchronization, authority denial, and isolation from public Site navigation.
   - Missing markers fail validation rather than silently degrading the security posture.

## Known static-host limitations

The current GitHub Pages surface cannot itself provide:

- authenticated user identity;
- server-side authorization;
- centrally managed session revocation;
- server-delivered HSTS, COOP, COEP, CORP, or Permissions-Policy guarantees controlled by this repository;
- durable encrypted storage;
- protected audit-log custody;
- key management or hardware-backed signing;
- qualified reviewer identity;
- remote monitoring or incident response.

These remain explicit service-boundary requirements. They may only be activated in a future named hosting/service control plane with inspectable deployment configuration and receipts.

## Required migration controls before authenticated service operation

A future service must add, at minimum:

- phishing-resistant MFA and role-scoped authorization;
- least-privilege service identities and short-lived credentials;
- server-side encrypted persistence with managed key rotation;
- append-only protected audit records;
- signed custody and review receipts;
- dependency and build provenance verification;
- vulnerability and secret scanning;
- incident logging, alerting, retention, and recovery testing;
- server-enforced security headers;
- privacy, records-retention, and legal/regulatory controls;
- independent penetration testing before production authority is enabled.

## Validation and release conditions

The Site security-hardening claim releases when:

1. this baseline is committed;
2. `assets/gp10-security.js` is committed and loaded by both GP10 pages where applicable;
3. both pages contain the policy markers required by the checker;
4. the checker enforces the controls;
5. the canonical Site mirror handoff records the implementation and remaining hosting boundary;
6. deployment observation is transferred to a durable Site-owned task or issue.
