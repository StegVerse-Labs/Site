# Site Mirror Handoff

## Status

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current Priority

StegTalk non-production local candidate status has been mirrored to Site and propagated through the known downstream targets.

## Source Artifacts

Destination source: `StegVerse-Labs/StegTalk`

- `STEGTALK_MIRROR_HANDOFF.md`
- `STEGTALK_CANDIDATE_STATUS.json`
- `STEGTALK_LOCAL_CANDIDATE.json`
- `STEGTALK_RELEASE_HANDOFF.json`

## Site Install Complete

Destination: `StegVerse-Labs/Site`

- `data/stegtalk-local-candidate.json`
- `data/stegtalk-local-candidate-receipt.json`

## Downstream Propagation Complete

Destination: `GCAT-BCAT-Engine/Publisher`

- `PUBLISHER_MIRROR_HANDOFF.md`
- `data/stegtalk-local-candidate.json`
- `data/stegtalk-local-candidate-publisher-receipt.json`

Destination: `StegVerse-Labs/admissibility-wiki`

- `ADMISSIBILITY_MIRROR_HANDOFF.md`
- `pages/stegtalk-admissibility-boundary.md`
- `receipts/stegtalk-admissibility-boundary-receipt.json`

Destination: `StegVerse-002/stegguardian-wiki`

- `STEGGUARDIAN_WIKI_MIRROR_HANDOFF.md`
- `pages/stegtalk-guardian-account-boundary.md`
- `receipts/stegtalk-boundary-receipt.json`

## Build Rule

Before continuing any Site mirror task, check this file first and treat it as the current handoff and task source of truth.

## Boundary

StegTalk remains a non-production local prototype candidate. Do not publish it as production ready.

## Next Integration Candidate

No additional StegTalk propagation target is currently known from this handoff.
