# Ecosystem Chat Backend Authority Handshake

## Status

```text
mode: machine-readable preview contract
Site local mode before: true
Site local mode after: true
authority result: DENY
execution result: NOT_ATTEMPTED
provider invoked: false
solver executed: false
repository mutated: false
receipts issued: false
```

## Purpose

The authority handshake defines the minimum contract that must be satisfied before `STEGVERSE_LOCAL_MODE` can ever be changed. The existence of this schema does not enable live execution.

## Request fixture

```text
fixtures/ecosystem-chat/authority-handshake-request.example.json
```

The request distinguishes:

- actor identity and verification state
- delegation presence, scope, and request-time validity
- policy identity, version, hash, and currentness
- evidence references, completeness, and freshness
- requested operation and allowlist status
- shell and repository-mutation boundaries
- provider and solver posture
- resource limits
- authority and execution receipt expectations

The preview request intentionally contains no standing to activate a backend path.

## Response fixture

```text
fixtures/ecosystem-chat/authority-handshake-response.example.json
```

The preview response returns:

```text
authority.result=DENY
execution.result=NOT_ATTEMPTED
site_local_mode_after=true
```

Required denial reasons include unverified identity, absent delegation, non-current policy, incomplete evidence, and a non-allowlisted operation.

## Validator

```text
python scripts/check_ecosystem_chat_authority_handshake.py
```

The validator confirms that:

- the request and response share one request ID
- preview-only posture is preserved
- all resource limits remain zero
- provider, solver, shell, and repository mutation remain disabled
- authority is denied
- execution is not attempted
- no receipt identity or issuer is claimed
- the decision fails closed
- the request remains replayable
- the decision remains reconstructable
- local mode remains enabled

The validator is included in both:

```text
python scripts/run_site_task.py validate
python scripts/run_site_task.py public-guard
```

## Activation boundary

A future non-preview handshake must independently reconstruct and validate identity, delegation, policy, evidence freshness, operation allowlisting, resource limits, provider or solver posture, and receipt authority at commit time.

An `ALLOW` authority result is necessary but not sufficient for execution. Execution must remain a separate transition with its own bounded result and backend-issued receipt.
