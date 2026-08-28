# Site Unified Homepage Contract Mirror Handoff

Issue: #586
Claim: SITE-UNIFIED-HOMEPAGE-586-20260828
State: IMPLEMENTED_VALIDATED_MERGED / POST_MERGE_TASK_RUNNER_PENDING
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


## Implemented source

- `scripts/check_site_unified_governed_experience.py`
  - validates the current conversational `index.html` shell;
  - requires My KV / Organizational KV primary navigation;
  - requires exactly three starter prompts;
  - requires canonical existing Ecosystem Chat runtime assets;
  - requires Node status visibility;
  - rejects the retired transition-directory/proof-status homepage.
- `docs/SITE_UNIFIED_GOVERNED_EXPERIENCE_STATUS.md`
  - now identifies `index.html` as the primary public operating surface;
  - records specialty/proof destinations as direct/conversational, hidden by default.
- `tests/test_site_unified_governed_experience.py`
  - deterministic regression coverage for the simplified homepage contract.

No homepage product file was modified by this repair.


## Validation and merge evidence

- final validated head: `bf7acb52f8f798af486656f29a2dde92c7e08675`
- Site Handoff Orchestrator `33200231978`: PASS
- Ecosystem Heartbeat Orchestration `33200232291`: PASS
- Site Bootstrap Validate `33200232204`: PASS
- PR: #588
- merge: `e2de89b33dc4539e053f476b5a59e83a2aa43710`
- claim release commit: `d355e52da8ef9b5c8f509f3f432db3a5df12b0e7`

The source defect that caused Site Task Runner run `33192559738` is repaired. Full lane completion still requires a post-merge `all-local` Site Task Runner observation.
