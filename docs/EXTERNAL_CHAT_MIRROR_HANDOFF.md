# External Chat Mirror Handoff

## Current goal

```text
Goal: public compatibility testing for external frameworks
Phase: intake-and-evaluator-installed
Result: implementation installed; live validation pending
```

## Public path

```text
https://stegverse-labs.github.io/Site/external-chat.html
```

## Installed Site files

```text
external-chat.html
assets/external-chat.js
data/external-chat-example.json
scripts/check_external_chat_compatibility.py
docs/SITE_PUBLIC_PATHS.md
scripts/check_site_public_paths.py
```

## Installed gateway files

Repository: `StegVerse-org/LLM-adapter`

```text
llm_adapter/external_framework_compatibility.py
llm_adapter/external_chat_api.py
llm_adapter/combined_gateway.py
tests/test_external_framework_compatibility.py
render.yaml
render-production.yaml
```

Endpoint:

```text
POST /api/external-framework-compatibility
```

## Result classes

```text
COMPATIBILITY_EVIDENCE_READY
PARTIAL_COMPATIBILITY_INTAKE
FAIL_CLOSED_BOUNDARY_REVIEW
```

The evaluator returns required-field coverage, missing fields, applicable failure classes, a content-bound compatibility receipt, and links to matching Admissibility Wiki framework findings when available.

## Wiki source

```text
StegVerse-Labs/admissibility-wiki/docs/external-frameworks/external-chat-submission-contract.md
StegVerse-Labs/admissibility-wiki/docs/external-frameworks/EXTERNAL_FRAMEWORKS_MIRROR_HANDOFF.md
StegVerse-Labs/admissibility-wiki/docs/external-frameworks/reports/*.compatibility.json
```

Published wiki reports remain the source for published findings.

## Data handling

```text
submission_retained = false
raw_artifact_published = false
wiki_record_created = false
execution_performed = false
review_required_before_publication = true
```

## Boundary

```text
compatibility evidence != certification
structural overlap != semantic equivalence
matching findings != general compatibility
compatibility receipt != execution authority
compatibility receipt != commit-time admissibility
submission != publication
publication != standing
```

## Next tasks

```text
1. Register the External Chat validator in Site validate and public-guard.
2. Generate the known-framework catalog from admissibility-wiki reports.
3. Import that catalog through a receipted artifact.
4. Add downloadable result packets without retaining raw submissions.
5. Add opt-in challenge and correction packets.
6. Verify the deployed page and API route.
7. Record current-main CI and live-route evidence before launch claims.
```

## Sharing posture

External Chat is a bounded compatibility-intake prototype. It is not framework certification, automatic wiki publication, or proof of general interoperability.
