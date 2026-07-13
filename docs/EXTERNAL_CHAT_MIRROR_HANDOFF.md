# External Chat Mirror Handoff

## Current goal

```text
Goal: public compatibility testing, delegated review, publication candidacy, and separately authorized wiki mutation
Phase: deployment-correlated-activation-evidence-installed
Result: implementation installed; successor validation and deployed evidence pending
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

## Site surfaces

```text
external-chat.html
external-review.html
assets/external-chat.js
assets/external-chat-review.js
assets/external-review.js
scripts/check_external_chat_compatibility.py
scripts/check_external_review_console.py
scripts/check_external_chat_verification_phase.py
scripts/check_external_chat_live_routes.py
scripts/build_external_chat_activation_evidence.py
scripts/check_external_chat_activation_evidence.py
scripts/check_ecosystem_chat_application.py
.github/workflows/site-task-runner.yml
reports/external-chat-live-verification.json
reports/external-chat-activation-evidence.json
```

## Validation phase separation

Repository-local validation runs before deployment and includes compatibility, catalog, reviewer-console, packet, authority, verification-phase, and activation-evidence contract checks.

Network-dependent verification runs only after Pages deployment. The existing Site Task Runner performs:

```text
local Site validation
-> local diagnostic artifact
-> Pages deployment
-> governed transition live verification
-> External Chat page and gateway-health verification with retries
-> live-verification receipt
-> deployment-correlated activation evidence
-> evidence artifact upload
```

No workflow was added.

## Live verification receipt

`scripts/check_external_chat_live_routes.py` writes:

```text
reports/external-chat-live-verification.json
```

It records exact URLs, timestamps, reachability, HTTP status, content type, bounded response evidence, parsed health contracts, failure class, and required disabled-mutation posture.

It verifies:

```text
External Chat page and boundary markers
reviewer console and delegated-review markers
package-only review health contract
raw artifact storage prohibited
publication authority false
mutation service repository/path allowlist
commit-time revalidation required
publication transition is not mutation authority
mutation_enabled = false
```

Network or DNS failure is recorded distinctly and is not converted into product failure, deployed success, activation standing, or authority.

## Deployment-correlated activation evidence

`scripts/build_external_chat_activation_evidence.py` writes:

```text
reports/external-chat-activation-evidence.json
```

The activation evidence binds:

```text
repository and exact commit SHA
GitHub ref and event
workflow, run ID, run attempt, and job
Pages deployment URL
gateway base URL
local Site diagnostic status and SHA-256
post-deployment live receipt status and SHA-256
mutation-disabled observation
observation count
evidence SHA-256
```

Result classes:

```text
OBSERVED_NON_MUTATING_PUBLIC_PATHS
LOCAL_VALIDATION_NOT_CONFIRMED
LIVE_EVIDENCE_NOT_AVAILABLE
LIVE_EVIDENCE_NOT_CONFIRMED
```

`OBSERVED_NON_MUTATING_PUBLIC_PATHS` requires all three:

```text
local diagnostic status = PASSED
live verification result = PASS
mutation_required_disabled = true
```

The workflow builds this record with `if: always()` after External Chat live verification and uploads it as:

```text
external-chat-activation-evidence-<run_id>-<run_attempt>
```

with 30-day retention.

## Activation evidence authority boundary

```text
activation evidence != deployment authority
activation evidence != repository mutation authority
activation evidence != publication authority
activation evidence != certification
activation evidence != standing
mutation remains separately authorized
```

The evidence record describes what a specific workflow run observed. It does not authorize deployment, publication, mutation, certification, compatibility standing, or external consequence.

## Gateway and mutation boundary

Repository: `StegVerse-org/LLM-adapter`

The gateway implements compatibility intake, authenticated package-only review, delegated correction, publication candidacy, and the separately authorized mutation adapter.

The mutation adapter remains disabled by default:

```text
STEGVERSE_EXTERNAL_MUTATION_ENABLED=false
```

It consumes only a stored `ALLOW_PUBLICATION_CANDIDATE` and revalidates immediately before a write:

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

Allowed destination:

```text
repository: StegVerse-Labs/admissibility-wiki
branch: main
path prefix: docs/external-frameworks/
```

Any mismatch fails closed before mutation. A receipt is issued only after GitHub returns both commit and blob identities.

## Disposable staging verifier

```text
python scripts/verify_external_publication_staging.py
```

Default mode is non-mutating and requires mutation health to report disabled. A real staging write additionally requires:

```text
STEGVERSE_STAGING_MUTATION_EXECUTE=true
```

and a target under:

```text
docs/external-frameworks/staging/
```

Success requires mutation receipt, commit SHA, new blob SHA, content SHA-256, `certification_created = false`, and `standing_created = false`.

## Boundary summary

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
pre-deployment validation != deployed-route verification
live verification receipt != deployment authority
activation evidence != authority
```

## Latest build commits

```text
c2e14cd5897557c0a93325b0e477554e4c022909
  add activation evidence builder

1e67ca11846ab8b2cc42fb9c0ae92d48faf69b5e
  add activation evidence contract validator

a9eae7cf1c32d96686381826fbd964638933c0c5
  register validator in canonical Site application checks

de65366abc0a6f0b05863a7fce64356205ffe7d8
  bind workflow, deployment URL, live receipt, local diagnostic, and commit/run identity
```

No deployment, mutation, credential, publication, certification, or standing authority changed through these repository-local additions.

## Next tasks

```text
1. Confirm Site Bootstrap Validate passes on this handoff commit or a successor.
2. Confirm Site Task Runner reaches Pages deployment and post-deployment External Chat verification.
3. Preserve site-task-diagnostic, external-chat-live-verification, and external-chat-activation-evidence artifacts together.
4. Verify activation evidence binds the exact deployed commit and reports mutation disabled.
5. Confirm current-main LLM-adapter validation passes review, publication, mutation, staging, comparison, and usage checks.
6. Confirm Admissibility Wiki Goal 5 validates mutation-receipt contracts and current Pages repair.
7. Deploy the gateway with mutation disabled before accepting public review submissions.
8. Conduct one separately authorized disposable staging mutation only after non-mutating public evidence passes.
9. Inspect commit/blob identities and mutation receipt before any production publication enablement.
```

## Sharing posture

External Chat implements the governed path from compatibility intake through delegated review, publication candidacy, and separately authorized commit-time-revalidated mutation. The Site now produces a single content-bound activation-evidence record correlating local validation, deployment identity, live route observations, and mutation-disabled posture. Production mutation remains disabled and unverified.
