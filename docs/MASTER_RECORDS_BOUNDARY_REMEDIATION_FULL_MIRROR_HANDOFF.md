# Master Records Boundary Remediation (Full) — Site Mirror Handoff

- Goal Task ID: `MASTER-RECORDS-BULK-SEMANTIC-REMEDIATION-002` (COSV `50000000100000`)
- Site task: `MASTER-RECORDS-BULK-SEMANTIC-REMEDIATION-002-SITE-FULL`
- Claim: `data/session-work-claims.d/SITE-MASTER-RECORDS-BOUNDARY-REMEDIATION-FULL-20261008.json`
- Branch: `claude/master-records-boundary-remediation`
- Predecessor: `docs/MASTER_RECORDS_BOUNDARY_WORDING_MIRROR_HANDOFF.md` (released after #1505)

## Rule

Master Records relates to organization records; the only other permitted
reference is reconstruction. The Organization owns custody and runtime/observed
reality, Interlock/InTr owns admission, gates and the transition API, and the
organization transition ledger owns ledger roles.

## Scope on Site

Prose, data, identifiers and code across the repository, including lines whose
wording is asserted by Site scripts and tests (each changed together with its
assertion). Renamed wire fields follow the shared identifier mapping: writers
emit the new name and readers also accept the legacy name through a single
`LEGACY_...` constant.

Left unchanged: hash-bound or signed evidence (receipts, frozen evaluator
records, the framework-evaluation receipt set), files that are exact blob-pinned
projections of `StegVerse-Labs/StegOS`, released claim identities (worker ids,
branches, work keys, dependency surface keys, handoff revisions), and
cross-repository identifiers that are not in the mapping.

Authority effect: NONE. Activation effect: NONE.
