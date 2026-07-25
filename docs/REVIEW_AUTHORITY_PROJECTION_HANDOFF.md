# Site Review Authority Projection Handoff

## Source

This is the durable continuation record for the Site visibility/authority projection integration derived from `StegVerse-org/StegVerse-SDK` Goal 7 and `GCAT-BCAT-Engine/Publisher` publication-boundary enforcement.

## Installed surface

```text
review-authority.html
assets/review-authority-projection.js
data/review-authority-projection.fixture.json
scripts/check_review_authority_projection.py
.github/workflows/validate-review-authority-projection.yml
```

## Enforced invariants

```text
visibility_state is displayed independently from process_state
PUBLICLY_VISIBLE is not authority_source
REVIEW_ONLY cannot grant claim, publication, attribution, or public-association authority
REVIEW_ONLY cannot assert endorsement, compatibility, or interoperability
one machine-readable envelope drives formatted and raw projections
projection does not mutate the envelope
Site rendering does not create publication authority
```

## Validation

```bash
python scripts/check_review_authority_projection.py
```

The canonical CI workflow runs the validator on Python 3.9, 3.11, and 3.12.

## Boundary

Site renders governed state. It does not create source authority, delegation, endorsement, attribution consent, compatibility, interoperability, public-association permission, publication authorization, admissibility, or custody.

## Next integration

`master-records/orchestration` should custody review manifests, acknowledgement receipts, transition receipts, and Publisher decision envelopes; independently recompute hashes; and return reconstruction receipts without converting custody into authority.
