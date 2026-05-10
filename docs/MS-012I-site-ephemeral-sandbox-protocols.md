# MS-012I Site Ephemeral Sandbox Protocols

## Purpose

Close the `sandbox_queue/` dead-end in `StegVerse-Labs/Site`.

## Lifecycle

```text
sandbox_queue/*.zip
→ ephemeral sandbox temporary directory
→ inspect paths and bundle shape
→ write sandbox_reports/
→ if repairable, emit incoming/<bundle>.sandbox-candidate.zip
→ archive original into sandbox_reviewed/
→ normal ingestion decides final install/routing
```

## Invariant

```text
Sandbox may construct.
Sandbox may test.
Sandbox may recommend.
Sandbox may emit repaired candidate bundles.

Sandbox may not install.
Only ingestion installs.
```

## Run

```text
python tools/ephemeral_sandbox_runner.py \
  --policy data/sandbox/ephemeral-sandbox-policy-v1.json \
  --apply
```

## Current automatic repair behavior

The first version performs conservative repair only:

```text
missing bundle-manifest.json + safe payload
→ add bundle-manifest.json
→ emit sandbox candidate into incoming/
```

It does not auto-repair:

```text
workflow bundles
tools/bundle_ingest.py mutation bundles
unsafe path bundles
already-manifested bundles requiring human review
```
