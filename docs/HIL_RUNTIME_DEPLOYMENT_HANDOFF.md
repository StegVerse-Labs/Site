# HIL Runtime Deployment Handoff

## Upstream deployment contract

The gateway repository now owns a fail-closed deployment profile at:

```text
StegVerse-org/LLM-adapter/docs/HIL_DEPLOYMENT_PROFILE.md
```

It defines:

- minimum merged gateway commit;
- service entry point;
- required HIL endpoints;
- durable-storage requirements;
- separate review and publication credentials;
- readiness acceptance values;
- redacted credential fingerprint evidence;
- actual restart-proof requirements;
- Site evidence handoff paths.

The matching upstream files are:

```text
deploy/hil.env.example
scripts/verify_hil_deployment_profile.py
.github/workflows/hil-deployment-profile.yml
```

## Current boundary

This handoff does not establish that the gateway is deployed. It establishes that the deployment configuration is now explicit, versioned, fail-closed, and CI-verifiable before runtime secrets or infrastructure are applied.

The next external/runtime action is to deploy `StegVerse-org/LLM-adapter` main at or after commit `b2e612dd74d311e0cbe66cd1c1d4758bff129fd4` using durable mounted storage and distinct secret-store credentials.

## Required return evidence

The deployment operator must return only governed, redacted evidence:

```text
deployment URL or service identifier
resolved deployed commit
persistent volume or storage-class reference
intake credential fingerprint
private-review credential fingerprint
publication credential fingerprint
readiness JSON
publication-readiness JSON
restart timestamps and deployment identifiers
post-restart response and provenance hashes
```

Raw credentials must not be returned or committed.

## Site continuation

Returned evidence is recorded in:

```text
data/hil-activation-state.json
data/hil-deployed-controlled-cycle-evidence.json
```

No public acquisition, publication, release, or Master Record append becomes authorized merely because the deployment profile exists or passes CI.
