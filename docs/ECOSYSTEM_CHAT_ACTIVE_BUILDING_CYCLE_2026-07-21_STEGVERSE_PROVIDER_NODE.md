# Ecosystem Chat Active Building Cycle — StegVerse-Owned Provider Node

## Cycle date

2026-07-21

## Active goal

Complete the existing Ecosystem Chat path:

request → governed provider response → usage persistence → authenticated custody → reconstruction → immutable VERIFIED receipt → Site activation → downstream propagation.

## Required capability

A StegVerse-owned text-generation service that satisfies the existing `StegVerse-org/LLM-adapter` governed provider contract without Render or another hosted inference platform.

## Existing candidates evaluated

- `StegVerse-org/LLM-adapter/llm_adapter/governed_provider.py`: reused unchanged as the HTTPS, allowlist, credential, quota, cost, identity, usage, fallback, and receipt broker.
- `StegVerse-Labs/governed-llm`: existing empty repository selected as the inference owner; no repository was created.
- `core-node-runtime-demo`, `entity-sandbox`, and `micro-node-runtime`: governance/runtime patterns only; no token-generation implementation.
- deterministic adapter fallback: unsuitable because it cannot prove a real provider response.

## Reuse-first decision

Add a bounded provider node to the existing `StegVerse-Labs/governed-llm` repository. Do not embed inference into `LLM-adapter` and do not replace the existing gateway or provider broker.

## Work performed

- Implemented an in-process GGUF engine using `llama-cpp-python`.
- Implemented authenticated `POST /generate` matching the existing broker JSON contract.
- Preserved transition and run identity in the provider response.
- Added input/output usage fields and a SHA-256 provider receipt.
- Kept provider output, execution, publication, and governance authority false.
- Added fail-closed readiness and health reporting.
- Added an HTTPS launcher that requires local certificate, key, provider token, and model file.
- Added unprivileged container packaging with externalized model and TLS storage.
- Added repository contract tests and a focused verifier.
- Added `compose.stegverse-provider.yaml` that connects the provider node to the canonical `LLM-adapter` image over HTTPS.
- Reused standard `REQUESTS_CA_BUNDLE` support already honored by Python `requests`; no broker weakening or replacement was required.

## Authoritative implementation

- Repository: https://github.com/StegVerse-Labs/governed-llm
- Provider API: `governed_llm/app.py`
- Local inference engine: `governed_llm/engine.py`
- HTTPS launcher: `governed_llm/serve.py`
- Container: `Dockerfile`
- Integrated composition: `compose.stegverse-provider.yaml`
- Contract tests: `tests/test_provider_contract.py`
- Validation PR: https://github.com/StegVerse-Labs/governed-llm/pull/1

## Runtime tests actually executed

GitHub created validation run `29876624303`, but the run completed before any job steps were exposed and no job log was available. This is not counted as a test pass or a code-level failure.

No real GGUF model was loaded and no token generation was executed in this cycle.

## State classification

- Provider-node design: DESIGNED
- Provider-node service: IMPLEMENTED
- Existing broker interface binding: INTEGRATED in source/configuration
- Repository contract validation: UNPROVEN
- Real local model loading: UNPROVEN
- Real governed provider response: UNPROVEN
- Provider-usage persistence: UNPROVEN
- Provider-usage custody and reconstruction: UNPROVEN
- Immutable zero-blocker activation receipt: UNPROVEN
- Site activation: UNPROVEN
- Downstream propagation: UNPROVEN

## Exact blocker

The provider runtime requires locally retained GGUF model bytes and locally generated trusted TLS material. Neither model bytes nor private credentials belong in GitHub. No authorized StegVerse machine with those runtime artifacts is evidenced yet.

## Removals proposed but not performed

None. Render PR #23, Site PR #29, and other retained branches or files were not closed, deleted, or superseded.

## Goal delta

A StegVerse-owned provider runtime and canonical gateway composition now exist where no inference implementation existed before.

## Reuse delta

The existing provider broker, canonical gateway image, quota/cost policies, usage persistence, Master-Records submission, identity checks, and receipt logic eliminated the need for a replacement gateway, provider protocol, custody service, or hosted platform.

## Non-progress

- No model output was produced.
- No provider usage event was persisted or placed in custody.
- No completion percentage should increase for the unexecuted runtime path.

## Next executable step

Run `compose.stegverse-provider.yaml` on an authorized StegVerse-controlled machine with a locally retained GGUF model and trusted local TLS material. Execute one governed request through the canonical gateway, then retain the first exact model, TLS, provider, usage-persistence, custody, reconstruction, or activation-receipt failure.

## Manual user action requirement

False for routine repository work. Establishing model provenance and machine execution authority remains a separate runtime-authority boundary.
