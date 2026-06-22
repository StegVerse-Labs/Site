# Site Mirror Handoff

## Status

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current Priority

Publish or update StegTalk non-production local candidate status from `StegVerse-Labs/StegTalk`.

## Source Artifacts

Destination source: `StegVerse-Labs/StegTalk`

- `STEGTALK_MIRROR_HANDOFF.md`
- `STEGTALK_CANDIDATE_STATUS.json`
- `STEGTALK_LOCAL_CANDIDATE.json`
- `STEGTALK_RELEASE_HANDOFF.json`

## Required Site Install

Destination: `StegVerse-Labs/Site`

- Site-visible StegTalk status page or data record
- Site mirror receipt that records source artifacts and non-production boundary

## Downstream Propagation Still Required

Destination: `GCAT-BCAT-Engine/Publisher`

- publish/update StegTalk local candidate status

Destination: `admissibility-wiki`

- add/update StegTalk admissibility boundary notes

Destination: `stegguardian-wiki`

- add/update StegTalk guardian/account boundary notes

## Build Rule

Before continuing any Site mirror task, check this file first and treat it as the current handoff and task source of truth.

## Boundary

StegTalk remains a non-production local prototype candidate. Do not publish it as production ready.
