# Device Node Portable Private Source Bootstrap Mirror Handoff

Updated: 2026-08-29
Repository: StegVerse-Labs/Site

## Goal
Provide a versioned, distributable StegVerse device-node bootstrap projection for credential-free exact-source packages produced only after TV/TVC resident private-source materialization.

## Canonical flow

```text
TV/TVC private-source resident boundary
  -> exact immutable private source
  -> secret-free portable package v1
  -> established StegVerse device-node continuity
  -> package/file/hash validation
  -> browser-local source custody
  -> node journal materialization receipt
  -> exportable replay evidence
```

The browser is never a GitHub credential owner. It may not accept a package as TV/TVC-authenticated merely because a JSON field says TV/TVC. Admission requires a retained TVC private-source execution receipt showing COMPLETE, exact authorized/observed SHA identity, SYSTEMD_LOADCREDENTIAL transport, and no credential exposure or persistence.

## Version 1 surfaces
- `stegos-node/private-source-portable-package-v1.schema.json`
- `stegos-node/portable-source-bootstrap-v1.html`
- `tests/test_portable_private_source_bootstrap_contract.py`

## Continuity
The receiver reuses `stegos-web-bootstrap-v1` node + device-continuity root when visible. If that IndexedDB is partitioned by an iOS browser context, a previously exported `stegos.web_bootstrap_evidence_bundle.v1` may be replayed and used as continuity evidence. No new node identity is minted by this surface.

## Authority
credential_authority: TV/TVC
browser_credential_material_allowed: false
github_token_runtime_authority: NONE
hosted_ci_activation_authority: NONE
package_grants_repository_authority: false
package_grants_runtime_authority: false
authority_effect: NONE

## First concrete consumer
TVC PR #92 repository-broker governed validation source:
- exact head: `b5288f9910ada26c6ab2e9bca3f7701afaae2cef`
- exact 16-file validation bundle SHA-256: `0369ed677a014a99a983415a9094e6aaa0c570d163d9818d9a086fee6042dd6a`

The portable device package is an additional distributable projection. The immediate resident validation lane may use TVC's local materialized filesystem directly and does not need to round-trip through the browser.

## Runtime truth
source/package contract: IMPLEMENTED_PENDING_VALIDATION
device receiver: IMPLEMENTED_PENDING_VALIDATION
first authentic TVC-produced portable package: NOT OBSERVED
distributable bootstrap release: NOT YET VERSION-TAGGED
