# External Chat Mirror Handoff

## Current goal

```text
Goal: public compatibility testing for external frameworks
Phase: automated-catalog-import-and-cooperative-review-packages-installed
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
data/external-framework-catalog-import-status.json
scripts/acquire_external_framework_catalog.py
scripts/check_external_chat_compatibility.py
docs/SITE_PUBLIC_PATHS.md
scripts/check_site_public_paths.py
scripts/check_ecosystem_chat_application.py
.github/workflows/site-task-runner.yml
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

## Automated catalog import

The existing Site Task Runner now runs:

```text
python scripts/acquire_external_framework_catalog.py
```

for `all-local` tasks before Site validation.

The importer retrieves:

```text
StegVerse-Labs/admissibility-wiki/docs/external-frameworks/external-chat-catalog.json
StegVerse-Labs/admissibility-wiki/docs/external-frameworks/external-chat-catalog.receipt.json
```

It validates catalog type, unique framework IDs, SHA-256, framework count, projection-only status, and non-authority boundaries before atomically replacing the Site projection.

Import states:

```text
RECEIPTED_WIKI_CATALOG_IMPORTED
LOCAL_RECEIPTED_CATALOG_RETAINED
```

An unavailable or invalid remote catalog does not erase the checked-in receipted fallback and does not claim hash verification.

## Canonical wiki review contracts

Repository: `StegVerse-Labs/admissibility-wiki`

```text
docs/external-frameworks/schemas/external-chat-cooperative-review-package.schema.json
docs/external-frameworks/schemas/external-chat-correction-receipt.schema.json
docs/external-frameworks/examples/external-chat-cooperative-review-package.example.json
docs/external-frameworks/examples/external-chat-correction-receipt.example.json
scripts/check_external_chat_review_packets.py
```

## Browser-local packets

External Chat can generate three local JSON packets without retaining the raw submitted artifact:

```text
external_framework_compatibility_result_packet
external_framework_compatibility_challenge_packet
external_framework_cooperative_review_package
```

A cooperative review package requires explicit submitter opt-in and at least one review-scope item. It may request publication review, but the request is not publication authority.

The cooperative package binds:

```text
framework_id
compatibility_receipt_id
submission_sha256
compatibility_result
review scope
evidence references
publication_requested
raw_submission_included = false
```

A reviewer correction must be represented by a distinct `external_framework_correction_receipt`. Corrections require reviewed fields, supporting evidence, reviewer reference, and—when a result changes—a replacement result and replacement receipt.

## Result classes

```text
COMPATIBILITY_EVIDENCE_READY
PARTIAL_COMPATIBILITY_INTAKE
FAIL_CLOSED_BOUNDARY_REVIEW
```

## Validation registration

The dedicated validator is included in canonical Site application validation through:

```text
scripts/check_ecosystem_chat_application.py
```

The existing Site Task Runner performs the catalog acquisition before `all-local` validation. No workflow was added.

## Data handling

```text
submission_retained = false
raw_artifact_published = false
wiki_record_created = false
execution_performed = false
review_required_before_publication = true
browser_packet_generation = local only
cooperative_review_requires_explicit_opt_in = true
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
review package != publication authority
correction receipt != certification
submission != publication
publication != standing
```

## Next tasks

```text
1. Register the review-packet validator in the wiki Goal 5 aggregate.
2. Add an authenticated opt-in review transport that stores only the submitted package, never the raw artifact by default.
3. Add reviewer identity/delegation verification before correction receipts may be issued.
4. Add live endpoint and public page verification.
5. Record current-main CI and deployed-route evidence before launch claims.
6. Expand the catalog beyond the initial checked-in report identifiers.
```

## Sharing posture

External Chat is a bounded compatibility-intake and cooperative-review prototype with an automated receipted wiki catalog, portable evidence/challenge packages, and explicit opt-in review packages. It is not framework certification, automatic publication, or proof of general interoperability.
