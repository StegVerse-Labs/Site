# Governed Site Measurement

## Status

`IMPLEMENTATION_IN_PROGRESS`

This layer measures whether a public StegVerse surface works. It does not identify, profile, score, or reconstruct a visitor.

## Canonical boundary

```text
usage measurement != user identification
page interaction != consent to profiling
event receipt != content capture
aggregate statistics != individual history
guide completion != claim submission
analytics evidence != admissibility authority
```

## Data path

```text
browser allowlisted event
-> local field filter
-> first-party collector
-> schema validation
-> prohibited-field rejection
-> aggregate counter
-> raw-event expiry within 300 seconds
-> thresholded public projection
```

Unknown event names and unknown fields fail closed. No event may contain free text, question content, medical content, claim content, filenames, persistent identifiers, cookies, fingerprints, exact location, query strings, or full referrer URLs.

## Repository-owned work

- Policy: `data/governed-site-measurement-policy.json`
- Task: `data/tasks/SITE-0001-GOVERNED-MEASUREMENT.json`
- Schema: `schemas/governed-site-measurement-event.schema.json`
- Validator: `scripts/check_governed_site_measurement.py`
- Coordination record: Site issue #143

## Activation gates

The layer is not active until all are observed:

1. Policy and schema validation pass.
2. Positive fixtures pass.
3. PII and unknown-field fixtures are rejected.
4. First-party collector is deployed.
5. Aggregate projection is deployed.
6. Raw-event expiry behavior is verified.
7. A live receipt records zero prohibited fields and no persistent identity.
8. `docs/SITE_MIRROR_HANDOFF.md` records the verified state.

No third-party analytics script is authorized by this document.
