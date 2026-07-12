# External Chat Mirror Handoff

## Current goal

```text
Goal: public compatibility testing, delegated review, publication candidacy, and separately authorized wiki mutation
Phase: live-verification-receipt-and-staging-ci-integration-installed
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
reports/external-chat-live-verification.json
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

Every execution writes `reports/external-chat-live-verification.json` with the exact URLs, observation times, HTTP status, content type, bounded body preview or JSON contract, failure class, and authority boundary.

Network or DNS resolution failure is recorded distinctly and is not converted into a product failure, deployment success, or activation claim.

The live-route verifier is registered in canonical Site application validation. No workflow was added.

## Gateway validation integration

Repository: `StegVerse-org/LLM-adapter`

The existing `.github/workflows/validate.yml` now:

```text
installs the package with [dev] service/test dependencies
runs the staging verifier in non-mutating mode
executes compatibility and authenticated-review tests
executes publication-transition and mutation-adapter tests
preserves recursive comparison and provider-usage validation
```

No additional workflow was created.

## Gateway mutation surfaces

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
live verification receipt != deployment authority
network resolution failure != product failure
```

## Validation status

Repository implementation, test registration, staging posture validation, and evidence-producing live checks are installed. The current execution environment could not resolve the public hostnames, so no deployed success or failure is claimed from that attempt. Current-main green CI, a successful externally networked live-route receipt, and one separately authorized disposable-path staging mutation remain unobserved.

## Next tasks

```text
1. Confirm the current-main LLM-adapter validation run includes and passes External Chat review, publication, mutation, and staging checks.
2. Confirm the Admissibility Wiki Goal 5 aggregate validates the mutation-receipt contract.
3. Deploy the gateway with mutation disabled and run the live verifier from an environment with public DNS/network access.
4. Retain the generated live-verification receipt as deployment evidence.
5. Conduct one separately authorized mutation under docs/external-frameworks/staging/.
6. Inspect commit/blob identities and mutation receipt before any production publication enablement.
7. Expand the framework catalog after verified report imports.
```

## Sharing posture

External Chat implements the governed path from compatibility intake through delegated review, publication candidacy, and a separately authorized commit-time-revalidated mutation adapter. Public verification is now evidence-producing and the existing gateway workflow validates the full non-mutating review/publication/mutation contract. Production mutation remains disabled and unverified.
