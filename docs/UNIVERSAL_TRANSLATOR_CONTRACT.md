# StegVerse Universal Translator Contract

## Status

```text
surface: universal-translator.html
client_runtime: assets/universal-translator.js
state: CLIENT_IMPLEMENTED_GATEWAY_PENDING
execution_authority: false
manual_user_action_required: false
```

## Purpose

The Universal Translator provides a shared multilingual layer for StegVerse requests, responses, documentation, public communications, and future agent interfaces.

Translation changes language only. It does not create or modify authority, consent, custody, admissibility, standing, delegation, policy, or execution rights.

## Runtime order

```text
source text
-> explicit source language or local detection
-> browser-native translation when available
-> governed gateway fallback when local translation is unavailable
-> translated text
-> non-authorizing translation receipt
```

The original source text remains preserved throughout the translation operation.

## Initial language identifiers

```text
en       English
es       Spanish
zh-Hans  Simplified Chinese
zh-Hant  Traditional Chinese
ar       Arabic
hi       Hindi
pt       Portuguese
fr       French
de       German
ja       Japanese
ko       Korean
```

Additional languages may be added without changing the authority boundary.

## Gateway

```http
POST /api/universal-translator
Content-Type: application/json
```

### Request

```json
{
  "text": "string",
  "source_language": "auto|BCP-47 language tag",
  "target_language": "BCP-47 language tag",
  "preserve_formatting": true,
  "preserve_named_entities": true,
  "authority_required": false,
  "execution_authority": false,
  "receipt_requested": true,
  "client": "StegVerse-Labs/Site",
  "surface": "universal-translator.html"
}
```

### Success response

```json
{
  "translation": "string",
  "detected_source_language": "BCP-47 language tag",
  "target_language": "BCP-47 language tag",
  "provider": "provider-neutral identifier",
  "governed": true,
  "receipt_id": "optional immutable receipt identifier"
}
```

### Failure response

A failed translation must return a non-2xx status and no translated text. The client preserves the original text and reports:

```text
translation_state=failed
original_preserved=true
authority=none
```

## Receipt requirements

A completed translation receipt may record:

```text
translation_state
source_language
target_language
engine
governed
remote
receipt_id when issued
execution_authority=false
original_preserved=true
```

A translation receipt is not:

```text
execution authority
publication authority
consent
custody
admissibility
standing
delegation
policy approval
proof that the translated wording is legally equivalent
```

## Data handling

1. Prefer local browser translation when available.
2. Do not send text to a remote provider unless local translation is unavailable.
3. Do not accept credentials, tokens, or secrets as translation input.
4. Preserve the original text and its language identifier.
5. Keep provider selection behind the governed gateway.
6. Reject empty or oversized requests.
7. Fail closed when the gateway returns no translation.
8. Keep Simplified Chinese and Traditional Chinese as separate locale paths.

## Integration destinations

```text
StegVerse-Labs/Site
StegVerse-Labs/StegTalk
StegVerse-Labs/Comms-Gateway
StegVerse-org/LLM-adapter
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

## Remaining implementation

```text
StegVerse-org/LLM-adapter:
  implement POST /api/universal-translator
  connect governed provider routing
  emit immutable translation receipts when configured

StegVerse-Labs/Site:
  add translator link to shared navigation surfaces
  add browser validation tests
  add gateway contract tests

StegVerse-Labs/StegTalk:
  consume translator contract for message composition and display

GCAT-BCAT-Engine/Publisher and wiki destinations:
  consume translated publication projections while retaining canonical source text
```

## Release boundary

No release or tag is authorized by this client-only implementation. Release readiness requires a validated gateway response path, provider-neutral tests, original-text preservation tests, and downstream terminology checks for Spanish, Simplified Chinese, and Traditional Chinese.
