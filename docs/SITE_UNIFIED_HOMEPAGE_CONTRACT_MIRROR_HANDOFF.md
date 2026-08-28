# Site Unified Homepage Contract Mirror Handoff

Issue: #586
Claim: SITE-UNIFIED-HOMEPAGE-586-20260828
State: CLAIM_PENDING_ADMISSION
Authority effect: NONE

## Defect

Current Site Task Runner run `33192559738` fails because `scripts/check_site_unified_governed_experience.py` still validates the retired transition-directory homepage.

## Canonical current homepage contract

The homepage itself is the conversational shell.

Required user-visible hierarchy:

- StegVerse
- My KV
- Organizational KV
- How can I help?
- How do I use this chat?
- What is StegVerse?
- What is My KV?
- chat composer / log
- canonical existing Ecosystem Chat runtime assets

Internal/proof/specialty destinations remain available through direct routes and conversational routing but are hidden from primary homepage navigation by default.

## Non-goals

- no index.html mutation;
- no transition menu restoration;
- no execution or receipt authority;
- no duplicate chat runtime;
- no credential changes.
