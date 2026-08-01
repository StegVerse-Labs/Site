# VA Claim Assistant — Next Execution Session

Use the connected GitHub repositories directly and continue the governed VA Claim Assistant program.

Treat live repository state, Git history, issue state, workflow runs, receipts, and directly verified deployment evidence as authoritative over prior chat claims.

## Read first

1. `StegVerse-Labs/Site/docs/VA_CLAIM_ASSISTANT_GOVERNED_SESSION.md`
2. `StegVerse-Labs/Site/data/va-claim-assistant/source-registry.json`
3. `StegVerse-Labs/Site/data/va-claim-assistant/build-coordination.json`
4. `StegVerse-Labs/Site/issues/113`
5. `StegVerse-Labs/Site/issues/115`
6. `StegVerse-Labs/Site/issues/116`
7. `StegVerse-org/LLM-adapter/issues/90`
8. `StegVerse-Labs/TVC/issues/9`
9. `master-records/orchestration/issues/12`

## Current state

```text
state: BUILDING
current public capability: BOUNDED_PROCEDURAL_ASSISTANT
next capability: SOURCE_GROUNDED_ASSISTANT
activation target: GOVERNED_CLAIM_SESSION
activation authorized: false
```

## Execute now

Parallel sequence:

1. Complete Site issue #115: source registry schema, validator, answer record schema, fixtures, and CI binding.
2. Complete TVC issue #9: scoped capability declaration and secret-free readiness receipt.

Then:

3. Complete LLM-adapter issue #90 using the validated registry and TVC capability.
4. Complete Site issue #116 for document hashes, page anchors, privacy classes, contradictions, and missing evidence.
5. Complete master-records/orchestration issue #12 for custody and reconstruction.
6. Activate `GOVERNED_CLAIM_SESSION` only after one deployed end-to-end session verifies all gates and the public page derives its status from the verified receipt.

## Boundaries

- Do not claim the assistant represents VA or provides legal or medical opinions.
- Do not invent diagnoses, nexus opinions, facts, outcomes, or rating percentages.
- Do not suppress contrary evidence.
- Do not treat lower-authority sources as overriding controlling law.
- Do not classify missing repository-local secrets as a blocker before TVC capability resolution.
- Do not expose provider or retrieval secrets outside TV/TVC authority boundaries.
- Do not activate a capability based on code presence alone.

## Session closure

Update `data/va-claim-assistant/build-coordination.json` and all affected issues before closure. If no executable or coordinatable task remains, announce `ARCHIVE THIS SESSION` at both the top and bottom of the response.
