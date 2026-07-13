# External Chat Mirror Handoff

## Current goal

```text
Goal: public compatibility testing, delegated review, publication candidacy, and separately authorized wiki mutation
Phase: post-deployment-live-verification-boundary-installed
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

## Site verification surfaces

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
scripts/check_ecosystem_chat_application.py
.github/workflows/site-task-runner.yml
reports/external-chat-live-verification.json
```

## Validation phase separation

External Chat local application checks run before Pages deployment:

```text
compatibility page and client contract
reviewer console and client contract
catalog and receipt contract
review packet and authority boundaries
verification-phase regression guard
```

The network-dependent live verifier is intentionally excluded from the pre-deployment `COMMANDS` aggregate. This prevents the deployment from being blocked because a newly added page is not yet present on the prior Pages revision.

The existing Site Task Runner now performs this order on `main`:

```text
run local Site validation
-> upload local diagnostic
-> deploy Pages
-> verify governed transition public surfaces
-> verify External Chat public pages and gateway health with retries
-> upload External Chat live-verification receipt even on failure
```

The regression guard requires:

```text
live route checker absent from pre-deployment COMMANDS
site application result declares POST_DEPLOYMENT live verification
External Chat verification follows Deploy Pages
live receipt upload follows verification
receipt upload uses if: always()
```

No workflow was added.

## Live verification receipt

`scripts/check_external_chat_live_routes.py` writes:

```text
reports/external-chat-live-verification.json
```

Each observation records the exact URL, timestamp, reachability, HTTP status, content type, bounded body preview or parsed JSON contract, failure class, required disabled-mutation posture, and non-authority boundary.

It verifies:

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

Network or DNS resolution failure is recorded separately and is not converted into product failure, deployment success, or activation standing.

The Site Task Runner uploads this receipt as:

```text
external-chat-live-verification-<run_id>-<run_attempt>
```

with 30-day retention.

## Gateway validation integration

Repository: `StegVerse-org/LLM-adapter`

The existing `.github/workflows/validate.yml` installs the package with development/service dependencies and runs:

```text
non-mutating staging verification
compatibility evaluator and API tests
authenticated review tests
publication-transition tests
repository-mutation tests
recursive comparison and provider-usage checks
existing authority, receipt, recovery, transition, and Goal 4 checks
```

No additional workflow was created.

## Mutation activation boundary

The mutation adapter remains disabled by default:

```text
STEGVERSE_EXTERNAL_MUTATION_ENABLED=false
```

Activation requires externally configured mutator registry, GitHub credential, mutation receipt key, and required policy reference. No credential is stored in Site, review packets, publication transitions, live receipts, or mutation receipts.

The adapter consumes only a stored `ALLOW_PUBLICATION_CANDIDATE` and revalidates immediately before a write:

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

Any mismatch fails closed before mutation.

## Disposable staging verifier

```text
python scripts/verify_external_publication_staging.py
```

Default mode is non-mutating and requires the public mutation-health route to report `mutation_enabled = false`.

A real staging write requires explicit:

```text
STEGVERSE_STAGING_MUTATION_EXECUTE=true
```

and all identity, delegation, authority, policy, expected-head, target-path, content, and mutator-token values. The target must remain under:

```text
docs/external-frameworks/staging/
```

Success requires a mutation receipt, commit SHA, new blob SHA, and content SHA-256 while preserving `certification_created = false` and `standing_created = false`.

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
pre-deployment validation != deployed-route verification
```

## Latest validation sequence

The earlier Site Bootstrap run failed because the live verifier was executed before the new Pages content could be deployed and because marker validation initially used a bounded preview. Marker validation was corrected to inspect the complete transient response while retaining only bounded receipt content.

The successor architectural repair is now installed:

```text
21c82e834dc23facda43bdc59e1b7ea22e487900
  remove live network check from pre-deployment application aggregate

e88126a29afde6bfa74afafc4005e97be71dc387
  run External Chat verification after Pages deployment and upload receipt

a895ddb5b75396ea3a12f148c914e79624c8d0ef
  add verification-phase regression guard

0c726313017cb97c168788c679023e4f8dcf76b8
  register regression guard in canonical Site application validation
```

No deployment, mutation, credential, publication, certification, or standing authority changed through these repairs.

## Next tasks

```text
1. Confirm Site Bootstrap Validate passes on 0c726313017cb97c168788c679023e4f8dcf76b8 or a successor.
2. Confirm Site Task Runner reaches Pages deployment and executes External Chat verification afterward.
3. Preserve the local diagnostic and external-chat-live-verification artifacts with run and commit identity.
4. Confirm current-main LLM-adapter validation passes External Chat review, publication, mutation, staging, comparison, and usage checks.
5. Confirm the Admissibility Wiki Goal 5 aggregate validates the mutation-receipt contract and current Pages build repair.
6. Deploy the gateway with mutation disabled before accepting any public review submissions.
7. Conduct one separately authorized mutation under docs/external-frameworks/staging/ only after non-mutating health evidence passes.
8. Inspect commit/blob identities and the mutation receipt before any production publication enablement.
```

## Sharing posture

External Chat implements the governed path from compatibility intake through delegated review, publication candidacy, and a separately authorized commit-time-revalidated mutation adapter. Local validation no longer depends on an undeployed page; live checks now occur after Pages deployment and always produce an artifact. Production mutation remains disabled and unverified.
