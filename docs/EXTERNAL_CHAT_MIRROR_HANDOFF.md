# External Chat Mirror Handoff

## Current goal

```text
Goal: public compatibility testing for external frameworks
Phase: receipted-catalog-and-packet-generation-installed
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
data/external-framework-catalog.json
data/external-framework-catalog.receipt.json
scripts/check_external_chat_compatibility.py
docs/SITE_PUBLIC_PATHS.md
scripts/check_site_public_paths.py
scripts/check_ecosystem_chat_application.py
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

## Canonical wiki catalog

Repository: `StegVerse-Labs/admissibility-wiki`

```text
docs/external-frameworks/external-chat-catalog.json
docs/external-frameworks/external-chat-catalog.receipt.json
docs/external-frameworks/external-chat-submission-contract.md
docs/external-frameworks/reports/*.compatibility.json
```

The Site catalog is a checked-in projection of the canonical wiki catalog and is bound by SHA-256 and framework count. The catalog is not certification, execution authority, or general compatibility proof.

## Result classes

```text
COMPATIBILITY_EVIDENCE_READY
PARTIAL_COMPATIBILITY_INTAKE
FAIL_CLOSED_BOUNDARY_REVIEW
```

The evaluator returns required-field coverage, missing fields, applicable failure classes, a content-bound compatibility receipt, and links to matching Admissibility Wiki framework findings when available.

## Browser-local packets

External Chat can now generate two downloadable JSON packets without retaining the submitted raw artifact:

```text
external_framework_compatibility_result_packet
external_framework_compatibility_challenge_packet
```

The result packet contains the returned compatibility result and its receipt. The challenge packet identifies the challenged receipt and submission hash, with empty fields for the challenged field, reason, supporting evidence, and requested correction or standing change.

Neither packet publishes a wiki record, creates standing, or authorizes a correction.

## Validation registration

The dedicated validator is now included in the canonical Site application validation through:

```text
scripts/check_ecosystem_chat_application.py
```

The public guard checks the page, client, validator, catalog, and receipt through:

```text
scripts/check_site_public_paths.py
```

No workflow was added.

## Data handling

```text
submission_retained = false
raw_artifact_published = false
wiki_record_created = false
execution_performed = false
review_required_before_publication = true
browser_packet_generation = local only
```

## Boundary

```text
compatibility evidence != certification
structural overlap != semantic equivalence
matching findings != general compatibility
compatibility receipt != execution authority
compatibility receipt != commit-time admissibility
catalog inclusion != endorsement
challenge packet != automatic correction
submission != publication
publication != standing
```

## Next tasks

```text
1. Replace manual catalog projection with an automated, receipted cross-repository import.
2. Add opt-in submission packaging for cooperative review without automatic publication.
3. Add reviewer-side packet validation and correction receipt schemas.
4. Add live endpoint and public page verification.
5. Record current-main CI and deployed-route evidence before launch claims.
6. Expand the catalog beyond the initial 12 checked-in report identifiers.
```

## Sharing posture

External Chat is a bounded compatibility-intake prototype with a receipted known-framework catalog and downloadable evidence/challenge packets. It is not framework certification, automatic wiki publication, or proof of general interoperability.
