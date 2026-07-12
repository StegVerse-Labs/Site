# External Chat Mirror Handoff

## Current goal

```text
Goal: public compatibility testing, delegated review, publication candidacy, and separately authorized wiki mutation
Phase: commit-time-revalidated-repository-mutation-adapter-installed
Result: implementation installed; live validation pending
```

## Public paths

```text
https://stegverse-labs.github.io/Site/external-chat.html
https://stegverse-labs.github.io/Site/external-review.html
```

## Installed Site surfaces

```text
external-chat.html
external-review.html
assets/external-chat.js
assets/external-chat-review.js
assets/external-review.js
scripts/check_external_chat_compatibility.py
scripts/check_external_review_console.py
scripts/check_ecosystem_chat_application.py
scripts/acquire_external_framework_catalog.py
```

## Governed gateway path

Repository: `StegVerse-org/LLM-adapter`

```text
framework submission
-> compatibility receipt
-> explicit cooperative-review opt-in
-> authenticated package-only intake
-> delegated reviewer correction receipt
-> independently delegated publication candidate
-> commit-time-revalidated repository mutation request
-> GitHub-confirmed commit and blob identity
-> repository mutation receipt
```

Installed mutation surfaces:

```text
llm_adapter/external_publication_mutation.py
tests/test_external_publication_mutation.py
llm_adapter/combined_gateway.py
render-production.yaml
```

Endpoint:

```text
GET  /api/external-review/repository-mutation/health
POST /api/external-review/repository-mutations
```

## Mutation activation boundary

The mutation adapter is disabled by default:

```text
STEGVERSE_EXTERNAL_MUTATION_ENABLED=false
```

Activation additionally requires externally configured:

```text
STEGVERSE_EXTERNAL_MUTATORS_JSON
STEGVERSE_EXTERNAL_GITHUB_TOKEN
STEGVERSE_EXTERNAL_MUTATION_RECEIPT_KEY
STEGVERSE_EXTERNAL_MUTATION_POLICY_REF
```

No credential is stored in Site, a review packet, a publication transition, or a mutation receipt.

## Commit-time predicates

The adapter consumes only a stored:

```text
ALLOW_PUBLICATION_CANDIDATE
```

It must revalidate all of the following immediately before a GitHub contents mutation:

```text
mutator identity and token hash
delegation validity window
delegation reference
repository mutation scope
framework scope
repository allowlist
path prefix allowlist
authority reference
policy reference
freshness window
publication-transition identity
correction and review-package evidence chain
expected repository head SHA
expected target blob SHA
```

Any mismatch fails closed before the write.

## Mutation constraints

```text
allowed repository: StegVerse-Labs/admissibility-wiki
allowed branch: main
allowed path prefix: docs/external-frameworks/
path traversal: rejected
repository-head drift: rejected
target-blob drift: rejected
publication target mismatch: rejected
policy/delegation mismatch: rejected
mutation disabled or incompletely configured: rejected
```

The adapter uses the GitHub contents API only after all predicates pass. A successful response must contain both a new commit SHA and a new blob SHA before a mutation receipt is issued.

## Canonical wiki receipt contract

Repository: `StegVerse-Labs/admissibility-wiki`

```text
docs/external-frameworks/schemas/external-chat-repository-mutation-receipt.schema.json
docs/external-frameworks/examples/external-chat-repository-mutation-receipt.example.json
scripts/check_external_chat_review_packets.py
scripts/check_goal5_external_frameworks_all.py
```

A successful write produces:

```text
external-framework-repository-mutation-receipt:hmac-sha256:...
```

The receipt binds:

```text
publication transition
repository and target path
previous blob SHA
new blob SHA
content SHA-256
commit SHA
mutator identity
delegation, authority, and policy references
commit timestamp
all commit-time predicate results
```

## Boundary

```text
compatibility evidence != certification
review package != publication authority
reviewer delegation != publisher delegation
publisher delegation != mutation delegation
correction receipt != publication transition
publication transition != repository mutation
mutation request != successful mutation
GitHub commit confirmation != certification
mutation receipt != standing
a published finding != general compatibility proof
```

## Validation status

Tests now cover:

```text
mutation disabled fail-closed behavior
successful commit-time revalidation with mocked GitHub confirmation
repository-head drift rejection
policy mismatch rejection
path-boundary rejection
receipt non-certification boundary
```

No workflow was added. Current-main CI and deployed-route evidence remain required before launch claims.

## Next tasks

```text
1. Verify current-main gateway mutation tests and wiki Goal 5 aggregate.
2. Add live-route checks for External Chat, reviewer console, review health, and mutation health.
3. Deploy the gateway with mutation disabled and verify all non-mutating public paths.
4. Conduct one separately authorized staging mutation against a disposable external-framework test path.
5. Inspect the returned commit/blob identities and mutation receipt before enabling any production publication path.
6. Expand the framework catalog after verified report imports.
```

## Sharing posture

External Chat now implements the full governed path from compatibility intake through delegated review, publication candidacy, and a separately authorized commit-time-revalidated repository mutation adapter. The mutation capability remains disabled by default and is not yet publicly verified or authorized for production writes.
