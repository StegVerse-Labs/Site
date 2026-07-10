# Ecosystem Chat Provider Status Preview

## Status

```text
mode: fixture-bound preview
live provider invocation: false
current pricing: false
billing: false
authority: none
execution: disabled
Site-issued receipt: false
```

## Purpose

This surface shows the shape of provider routing, fallback, quota, usage, cost, and latency telemetry before any live model provider is connected.

It is a display contract, not proof that a provider was called. It must not be used to infer current pricing, current quota, model availability, account standing, execution authority, billing, or receipt issuance.

## Fixture

```text
fixtures/ecosystem-chat/provider-status.example.json
```

Required posture:

- `preview_only=true`
- `live_invocation=false`
- `authority_granted=false`
- `execution_enabled=false`
- `receipt_issued_by_site=false`
- `pricing_current=false`
- `billable_units=0`
- `provider_ms=null`
- estimated and billed cost remain zero

## Renderer

```text
assets/ecosystem-chat-provider.js
```

The renderer self-mounts before the chat console, validates the fixture, and fails closed when fields are missing or unsafe.

## Validator

```text
python scripts/check_ecosystem_chat_provider_status.py
```

The validator is included in:

```text
python scripts/run_site_task.py validate
python scripts/run_site_task.py public-guard
```

## Live integration boundary

A future live provider path must return explicit provider identity, model identity, invocation status, quota window, usage accounting, pricing provenance, latency, fallback outcome, authority posture, execution posture, and receipt posture.

Changing the display from fixture data to live data does not itself grant authority. Payment, quota, provider availability, or model capability must never be treated as execution standing.
