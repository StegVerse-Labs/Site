# HIL TV/TVC Runtime Handoff

## Upstream runtime contract

The gateway repository owns the platform-agnostic runtime profile at:

```text
StegVerse-org/LLM-adapter/docs/HIL_DEPLOYMENT_PROFILE.md
```

It defines:

- minimum gateway implementation commit;
- application entry boundary;
- required HIL endpoints;
- abstract governed persistence requirements;
- separate private-review and publication capabilities;
- readiness acceptance values;
- redacted capability-binding evidence;
- TV/TVC-governed runtime replacement proof;
- Site evidence handoff paths.

## Architectural correction

HIL does not require a hosting platform, deployment provider, persistent mounted disk, vendor secret store, container service, or public service URL.

TV/TVC owns:

```text
runtime construction
configuration resolution
compatibility-value injection
capability issuance
storage binding
process lifecycle
runtime replacement
transition receipts
evidence return
```

Environment-variable names used by the adapter are compatibility inputs only. They do not assign configuration ownership to a shell, operator, `.env` file, host, or platform.

## Current boundary

The runtime contract and automated process-cycle proof exist. The next ecosystem action is a TV/TVC-controlled cycle using a governed state namespace and separately bound review and publication capabilities.

This is an internal ecosystem orchestration action, not a request for the user to select or configure external infrastructure.

## Required return evidence

TV/TVC must return governed, redacted evidence:

```text
TV/TVC cycle identifier
resolved gateway commit
prior runtime-instance identifier
successor runtime-instance identifier
termination transition identifier
start transition identifier
governed storage-state reference
intake capability-binding fingerprint
private-review capability-binding fingerprint
publication capability-binding fingerprint
readiness JSON before replacement
readiness JSON after replacement
publication-readiness JSON
post-restart response and provenance hashes
receiver receipt
private-review receipt
publication record
stable lookup result
```

Raw credentials and capability material must not be returned or committed.

## Site continuation

Returned evidence is recorded in:

```text
data/hil-activation-state.json
data/hil-deployed-controlled-cycle-evidence.json
```

No public acquisition, publication, release, orchestration, or Master Record append becomes authorized merely because TV/TVC completes runtime construction or produces a controlled-cycle receipt.
