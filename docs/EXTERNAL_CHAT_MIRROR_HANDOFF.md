# External Chat Mirror Handoff

## Current goal

```text
Goal: public compatibility testing, delegated review, publication candidacy, and separately authorized wiki mutation
Phase: live-route-and-disposable-staging-verification-installed
Result: implementation installed; deployed validation pending
```

## Public paths

```text
https://stegverse-labs.github.io/Site/external-chat.html
https://stegverse-labs.github.io/Site/external-review.html
```

## Implemented lifecycle

```text
framework submission
-> compatibility evidence receipt
-> explicit cooperative-review opt-in
-> authenticated package-only intake
-> delegated reviewer correction receipt
-> independently delegated publication candidate
-> separately delegated repository mutation request
-> commit-time authority/delegation/policy/freshness revalidation
-> repository-head and target-blob drift checks
-> GitHub-confirmed commit and blob identity
-> repository mutation receipt
```

## Site verification surfaces

```text
external-chat.html
external-review.html
assets/external-chat.js
assets/external-chat-review.js
assets/external-review.js
scripts/check_external_chat_compatibility.py
scripts/check_external_review_console.py
scripts/check_external_chat_live_routes.py
scripts/check_ecosystem_chat_application.py
```

`scripts/check_external_chat_live_routes.py` verifies:

```text
External Chat page HTTP 200 and expected boundary markers
reviewer console HTTP 200 and expected delegated-review markers
GET /api/external-review/health contract
GET /api/external-review/repository-mutation/health contract
public mutation_enabled = false
allowed repository = StegVerse-Labs/admissibility-wiki
allowed path prefix = docs/external-frameworks/
commit-time revalidation required
publication transition is not mutation authority
```

The live-route verifier is registered in canonical Site application validation. No workflow was added.

## Gateway mutation surfaces

Repository: `StegVerse-org/LLM-adapter`

```text
llm_adapter/external_publication_mutation.py
scripts/verify_external_publication_staging.py
tests/test_external_publication_mutation.py
llm_adapter/combined_gateway.py
render-production.yaml
```

Endpoints:

```text
GET  /api/external-review/repository-mutation/health
POST /api/external-review/repository-mutations
```

## Mutation activation boundary

The mutation adapter remains disabled by default:

```text
STEGVERSE_EXTERNAL_MUTATION_ENABLED=false
```

Activation requires externally configured mutator registry, GitHub credential, mutation receipt key, and required policy reference. No credential is stored in Site, packets, publication transitions, or receipts.

## Commit-time predicates

The adapter consumes only a stored `ALLOW_PUBLICATION_CANDIDATE` and revalidates:

```text
mutator identity and token hash
delegation validity and reference
repository, path, framework, and mutation scopes
authority reference
policy reference
freshness window
publication-transition identity
correction and review-package evidence chain
expected repository head SHA
expected target blob SHA
```

Any mismatch fails closed before a write.

## Disposable-path staging verifier

```text
python scripts/verify_external_publication_staging.py
```

Default behavior is non-mutating and requires the public mutation health route to report `mutation_enabled = false`.

A real staging mutation requires explicit:

```text
STEGVERSE_STAGING_MUTATION_EXECUTE=true
```

and all required identity, delegation, authority, policy, expected-head, target-path, content, and mutator-token environment values. The target must remain under:

```text
docs/external-frameworks/staging/
```

The verifier accepts success only when the service returns a mutation receipt, commit SHA, new blob SHA, and content SHA-256 while preserving `certification_created = false` and `standing_created = false`.

## Authority boundary

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
published finding != general compatibility proof
```

## Validation status

Repository implementation and validation contracts are installed. Current-main green CI, deployed gateway verification, and one separately authorized disposable-path staging mutation have not yet been observed.

## Next tasks

```text
1. Confirm current-main gateway mutation tests and wiki Goal 5 aggregate.
2. Deploy the gateway with mutation disabled and run the live-route verifier.
3. Record page, review-health, and mutation-health evidence.
4. Conduct one separately authorized mutation under docs/external-frameworks/staging/.
5. Inspect commit/blob identities and mutation receipt before any production publication enablement.
6. Expand the framework catalog after verified report imports.
```

## Sharing posture

External Chat implements the governed path from compatibility intake through delegated review, publication candidacy, and a separately authorized commit-time-revalidated mutation adapter. Public non-mutating route verification and a disposable staging protocol are installed; production mutation remains disabled and unverified.
