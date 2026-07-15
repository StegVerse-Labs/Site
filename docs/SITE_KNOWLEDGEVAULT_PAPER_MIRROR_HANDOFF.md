# Site KnowledgeVault Paper Mirror Handoff

## Source of truth

This handoff owns the bounded publication of the KnowledgeVault conversation-continuity paper on `StegVerse-Labs/Site`.

## Current route

`papers/knowledgevault/conversation-continuity.html`

Stable aliases:

- `paper.html`
- `papers/knowledgevault/index.html`

## Index surface

`Papers.html`

## Current state

```text
paper_html: INSTALLED_ON_MAIN
papers_index_entry: INSTALLED_ON_MAIN
publication_boundary_doc: INSTALLED_ON_MAIN
publication_validator: INSTALLED_ON_MAIN
site_validation: PASSED
pull_request: MERGED_PR_18
merge_commit: 4920684d8ec1b8ef8f2ff587bf318de995687d7f
direct_pdf_binary: NOT_INSTALLED
public_deployment_verification: EXTERNAL_OBSERVATION_PENDING
canonical_public_url: https://stegverse.org/paper.html
```

## Validation evidence

PR-triggered `Site Bootstrap Validate` run `29387525605` completed successfully against head commit `4e3d9783de53150ab88e5c82182ad5f216b3dffa` before merge.

The bounded publication validator is:

`scripts/check_site_knowledgevault_paper.py`

The same validation sequence also exposed and repaired one exact stale literal mismatch in the existing company-testbed sample contract. No check was removed or weakened.

## Durable boundary

Site publishes and helps users discover the paper. Site publication does not independently validate the claims, certify production readiness, grant authority, or represent the larger production architecture as complete.

The linked implementation remains `StegVerse-Labs/continuity-vault-kit`, where the local-first prototype provides canonical events, chained hashes, a Merkle root, retention classes, structured indexing, provenance-bearing reconstruction, and adversarial mutation detection.

## Direct PDF status

The existing PDF is preserved outside the repository, with SHA-256:

`52e0c99efcb9ca1bf7e69aa8d2ad8a649e29d1669d426bc5dada9b75eb0e141d`

The current connected GitHub write path supports UTF-8 repository files but does not accept binary file payloads. The stable public HTML route is therefore the canonical publication route. A direct PDF asset may be added later without changing the LinkedIn or canonical paper link.

## Remaining externally observable task

Verify that `https://stegverse.org/paper.html` resolves after the Site deployment provider consumes merge commit `4920684d8ec1b8ef8f2ff587bf318de995687d7f`.

Failure or delay of that external deployment observation does not require this conversation. Continuation can proceed entirely from this handoff, PR #18, the successful validation run, and the merge commit.

## Archive note

All unique publication decisions, implementation paths, validation evidence, binary-PDF limitations, canonical routes, remaining observation, and continuation rules are durably preserved here. The complete thread is ready for archiving without any additional part of the thread needed to move forward.
