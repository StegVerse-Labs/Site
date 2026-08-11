# VA Claim Assistant Record Awareness Mirror Handoff

## Canonical ownership

Parent handoff: `docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`

Canonical secure-document owner: `StegVerse-Labs/Site#116`

Goal: extend the standard VACC health-record review with a claim-independent Veteran Record Awareness lane.

## Installed contract

- `docs/VA_CLAIM_ASSISTANT_VETERAN_RECORD_AWARENESS_STANDARD.md`
- `data/va-claim-assistant/veteran-record-awareness.schema.json`
- `data/va-claim-assistant/fixtures/veteran-record-awareness-session.json`
- `scripts/check_va_document_evidence.py`
- `.github/workflows/va-document-evidence.yml`

## Invariants

1. Awareness findings are not automatically claim evidence.
2. A separate relevance determination is required before a finding enters claim development.
3. The veteran controls non-claim escalation.
4. Behavioral labels are contextualized against observable conduct and surrounding chronology when evidence exists.
5. Refusal of available care is distinguished from inability to obtain care.
6. Contradictions, uncertainty, access failures, medication gaps, referral gaps, problem-list integrity concerns, and unresolved abnormal findings may be surfaced.
7. The lane does not assign fault, negligence, causation, diagnosis, nexus, rating, representation, adjudication, filing, or publication authority.
8. Public private-document processing remains fail-closed under the existing Goal 2/Goal 3 gates.

## Validation

The existing deterministic document-evidence validator now validates the awareness fixture and requires:

- non-empty evidence references and observed facts;
- zero authority flags;
- `automatically_include_in_claim=false`;
- `requires_separate_relevance_determination=true`;
- `veteran_controls_escalation=true`;
- stable canonical SHA-256 over the awareness record.

The existing VA Document Evidence workflow is extended to cover the new standard, schema, fixture, and receipt assertion.

## Remaining work

Public/runtime integration remains downstream of the already-established VACC Goal 2/Goal 3 activation gates. When private document review becomes active, the document processor must emit this awareness record separately from claim-evidence output and the veteran-facing UI must visibly label it as not automatically part of the claim.

No Publisher/Site mirror, admissibility-wiki, or stegguardian-wiki propagation is required until this contract reaches a release/activation milestone or the parent handoff names those consumers.
