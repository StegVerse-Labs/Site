# StegBrowser llm.v1 Conformance Page Handoff

## Purpose

`integration/llm-browser-test/v1/` is a static, StegVerse-controlled HTTPS
surface for STEGBROWSER_LIVE_PATH_CONFORMANCE (SV-LLM/sandbox AT-04 Stage 1).
It accepts a prompt and echoes it after the fixed prefix
`STEGVERSE_CONFORMANCE_V1 `, then marks `#response` with `data-complete="true"`.

## Surfaces

```text
integration/llm-browser-test/v1/index.html
scripts/check_llm_browser_conformance_page.py
.github/workflows/llm-browser-conformance-page.yml
data/session-work-claims.d/sv-llm-stegbrowser-conformance-page-20261007.json
```

## Stable contract

```text
target_id: stegverse.integration.llm-browser-test.v1
automation_policy: PERMITTED_BY_OWNER
selectors: #prompt, #submit, #response, #response[data-complete='true']
credential_mode: NONE
network, storage, external resources: none
consumer: SV-LLM/sandbox live/target.json
```

## Boundaries

- Not a provider surface; a response here proves no OpenAI, Anthropic or other
  provider integration.
- No LLM-adapter hop and no InTr hop; ordinary HTTPS only.
- No authority, custody, ledger or Master Records effect.
- Changing the behaviour requires a new version path (`/v2/`), not an edit to v1.
