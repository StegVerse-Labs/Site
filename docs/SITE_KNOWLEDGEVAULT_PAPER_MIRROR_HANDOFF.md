# Site KnowledgeVault Paper Mirror Handoff

## Source of truth

This handoff owns the bounded publication of the KnowledgeVault conversation-continuity paper on `StegVerse-Labs/Site`.

## Current route

`papers/knowledgevault/conversation-continuity.html`

## Index surface

`Papers.html`

## Current state

```text
paper_html: INSTALLED_ON_PUBLICATION_BRANCH
papers_index_entry: INSTALLED_ON_PUBLICATION_BRANCH
publication_boundary_doc: INSTALLED_ON_PUBLICATION_BRANCH
publication_validator: INSTALLED_ON_PUBLICATION_BRANCH
direct_pdf_binary: NOT_INSTALLED
site_validation: PENDING
merge: PENDING
public_deployment_verification: PENDING
```

## Durable boundary

Site publishes and helps users discover the paper. Site publication does not independently validate the claims, certify production readiness, grant authority, or represent the larger production architecture as complete.

The linked implementation remains `StegVerse-Labs/continuity-vault-kit`, where the local-first prototype provides canonical events, chained hashes, a Merkle root, retention classes, structured indexing, provenance-bearing reconstruction, and adversarial mutation detection.

## Direct PDF status

The existing PDF is preserved outside the repository, with SHA-256:

`52e0c99efcb9ca1bf7e69aa8d2ad8a649e29d1669d426bc5dada9b75eb0e141d`

The current connected GitHub write path supports UTF-8 repository files but does not accept binary file payloads. The stable public HTML route is therefore the active publication route. A direct PDF asset may be added later without changing the canonical paper link.

## Next task

1. Open the publication pull request.
2. Run Site validation.
3. Repair only exact failures attributable to this bounded publication.
4. Merge after required checks pass.
5. Verify the public route resolves after deployment.
6. Update this handoff with the merge commit and verified public URL.
