# External Chat Mirror Handoff

## Current goal

```text
Goal: public compatibility testing, delegated cooperative review, and separately authorized publication candidacy for external frameworks
Phase: reviewer-console-and-publication-transition-installed
Result: implementation installed; live validation pending
```

## Public paths

```text
https://stegverse-labs.github.io/Site/external-chat.html
https://stegverse-labs.github.io/Site/external-review.html
```

## Installed Site files

```text
external-chat.html
external-review.html
assets/external-chat.js
assets/external-chat-review.js
assets/external-review.js
data/external-chat-example.json
data/external-framework-catalog.json
data/external-framework-catalog.receipt.json
data/external-framework-catalog-import-status.json
scripts/acquire_external_framework_catalog.py
scripts/check_external_chat_compatibility.py
scripts/check_external_review_console.py
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
llm_adapter/external_review_store.py
llm_adapter/external_review_api.py
llm_adapter/combined_gateway.py
tests/test_external_framework_compatibility.py
tests/test_external_review_api.py
tests/test_external_review_publication.py
render.yaml
render-production.yaml
```

Endpoints:

```text
POST /api/external-framework-compatibility
GET  /api/external-review/health
POST /api/external-review/packages
GET  /api/external-review/packages/{package_id}
GET  /api/external-review/reviewer/packages/{package_id}
POST /api/external-review/corrections
POST /api/external-review/publication-transitions
```

## Reviewer console

The reviewer console consumes the package ID, reviewer reference, and reviewer token. It performs a delegated package lookup requiring `package:read`, then may issue a correction only when the reviewer token, delegation window, delegation reference, and every requested field scope pass.

Reviewer credentials:

```text
are held only in current page memory
are sent only in Authorization headers
are cleared after each lookup or correction attempt
are not written to browser storage
are not included in packets or receipts
```

The console displays the package, review state, prior corrections, and delegated correction result. It does not expose raw framework artifacts because the review service never stores them by default.

## Publication transition separation

A correction receipt cannot publish a wiki result. Publication candidacy requires a separate publisher registry and token configured through:

```text
STEGVERSE_EXTERNAL_PUBLISHERS_JSON
```

A publisher must have:

```text
current token hash match
current valid_from / valid_until window
publisher delegation reference
publication:wiki scope
framework:<framework_id> scope
```

A successful publisher action creates an append-only:

```text
external-framework-publication-transition:hmac-sha256:...
```

The transition binds:

```text
review package ID
correction receipt ID
publisher reference
publisher delegation reference
target wiki path
source commit reference
evidence references
decision
```

Even `ALLOW_PUBLICATION_CANDIDATE` returns:

```text
publication_executed = false
repository_mutation_authorized = false
certification_created = false
standing_created = false
required_next_transition = separately_authorized_repository_mutation
```

The publication-transition record is not itself a GitHub write or wiki publication.

## Canonical wiki contracts

Repository: `StegVerse-Labs/admissibility-wiki`

```text
docs/external-frameworks/schemas/external-chat-cooperative-review-package.schema.json
docs/external-frameworks/schemas/external-chat-correction-receipt.schema.json
docs/external-frameworks/schemas/external-chat-reviewer-delegation.schema.json
docs/external-frameworks/schemas/external-chat-publication-transition.schema.json
docs/external-frameworks/examples/external-chat-cooperative-review-package.example.json
docs/external-frameworks/examples/external-chat-correction-receipt.example.json
docs/external-frameworks/examples/external-chat-reviewer-delegation.example.json
docs/external-frameworks/examples/external-chat-publication-transition.example.json
scripts/check_external_chat_review_packets.py
scripts/check_goal5_external_frameworks_all.py
```

## Append-only storage and conflict behavior

SQLite maintains separate append-only tables for review packages, correction receipts, and publication transitions.

```text
same identity + same content -> idempotent return
same identity + different content -> 409 conflict
challenged receipt or submission identity drift -> fail closed
expired or out-of-scope reviewer delegation -> fail closed
wrong or out-of-scope publisher delegation -> fail closed
publication target outside docs/external-frameworks -> rejected
INSUFFICIENT_EVIDENCE cannot ALLOW_PUBLICATION_CANDIDATE
```

## Automated catalog import

The existing Site Task Runner executes `scripts/acquire_external_framework_catalog.py` before `all-local` validation and preserves the checked-in receipted fallback on remote failure.

```text
RECEIPTED_WIKI_CATALOG_IMPORTED
LOCAL_RECEIPTED_CATALOG_RETAINED
```

No workflow was added.

## Data handling

```text
compatibility submission retained = false
raw artifact stored by review service = false
review package stored after explicit opt-in = true
reviewer credential stored = false
publisher credential stored = false
wiki record created automatically = false
publication transition stored = true
publication executed by transition = false
execution performed = false
```

## Boundary

```text
compatibility evidence != certification
structural overlap != semantic equivalence
catalog inclusion != endorsement
review package != publication authority
review intake receipt != correction receipt
reviewer delegation != publisher delegation
correction receipt != publication transition
publication transition != repository mutation
publication candidate != published wiki record
publication != standing
```

## Next tasks

```text
1. Verify current-main gateway, reviewer console, correction, and publication-transition tests.
2. Add a separately authorized repository-mutation adapter that consumes only ALLOW_PUBLICATION_CANDIDATE records and still performs commit-time revalidation.
3. Add live endpoint and public page verification for external-chat.html and external-review.html.
4. Record current-main CI and deployed-route evidence before launch claims.
5. Expand the catalog beyond the initial checked-in report identifiers.
```

## Sharing posture

External Chat now provides bounded compatibility intake, authenticated cooperative review, a delegated reviewer console, append-only correction receipts, and separately authorized publication-candidate transitions. It still does not certify frameworks, automatically mutate the wiki, or prove general interoperability.
