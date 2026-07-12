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

## Latest Site validation failure and bounded repair

```text
Workflow: Site Bootstrap Validate
Run: 29209702373
Commit: e86775b00c7fd57d33e4be959af558f68c1c3eae
Job: bootstrap-validate
First failing command: python scripts/check_external_chat_live_routes.py
Failure: external-review.html missing marker: delegated reviewer
Artifact: site-application-validation-result
Artifact ID: 8264785721
Artifact SHA-256: 20bc478640e0188339fd6150e2bdb661493d1fdac4a234ec52aefeb6db2fda11
Repair commit: b7050a0ef9c7b9792642b7fbbeafccd24c02e127
Verification: pending on repair commit or successor
```

The page already contained the required delegated-review marker. The checker validated markers against the 500-character receipt preview rather than the complete HTTP response body. The repair now validates against the transient complete body while retaining only the bounded preview and parsed contract in the receipt. No deployment, route, mutation, credential, publication, or authority state changed.

## Validation status

Repository implementation, test registration, staging posture validation, and evidence-producing live checks are installed. The latest bounded marker-validation repair is installed. Current-main green CI, successful gateway health evidence, and one separately authorized disposable-path staging mutation remain unobserved.

## Next tasks

```text
1. Confirm Site Bootstrap Validate passes on b7050a0ef9c7b9792642b7fbbeafccd24c02e127 or a successor.
2. Preserve the passing Site application validation receipt.
3. Confirm the current-main LLM-adapter validation run includes and passes External Chat review, publication, mutation, and staging checks.
4. Confirm the Admissibility Wiki Goal 5 aggregate validates the mutation-receipt contract.
5. Deploy the gateway with mutation disabled and run the live verifier from an environment with public DNS/network access.
6. Retain the generated live-verification receipt as deployment evidence.
7. Conduct one separately authorized mutation under docs/external-frameworks/staging/.
8. Inspect commit/blob identities and mutation receipt before any production publication enablement.
```

## Sharing posture

External Chat implements the governed path from compatibility intake through delegated review, publication candidacy, and a separately authorized commit-time-revalidated mutation adapter. Public verification is evidence-producing and now validates page markers against complete responses while retaining bounded receipts. Production mutation remains disabled and unverified.
