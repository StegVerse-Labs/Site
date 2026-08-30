# TIDC Independent-Coding Source Packet Index

## Status

```text
posture: SOURCE_PACKET_INDEX
research_state: PILOT_NOT_CONFIRMATORY
packet_version: v0.1
records: 11
source_records: 13
archival_completeness: PARTIAL
source_receipts_complete_or_limited: 6
```

This index defines the source set that an independent coder is permitted to use for the first reliability pass. A citation entry is not equivalent to a complete archival packet. Missing or inaccessible material must be reported rather than inferred.

## Discovery-event sources

| Record | Source ID | Primary source posture | Known limitation |
|---|---|---|---|
| COMP-001 | SRC-001 | Primary 1977 Parts I and II, published microfiche class-check supplement, and University of Illinois Appel archive holdings identified; receipt at `data/tidc/source-receipts/COMP-001.json` | `LIMITATION_RETAINED`: physical punch cards and data printouts were located archivally but not digitally retrieved; exact run dates, program versions, hardware logs, and full execution transcripts remain unresolved. |
| COMP-002 | SRC-002 | Lam primary author account | Exact run dates and independent verification remain incomplete. |
| COMP-003 | SRC-003 | McCune author archive and published proof record | Exact publication chronology requires completion. |
| NET-001 | SRC-004 | Gowers launch post, arXiv preprint, Annals publication, and terminal receipt at `data/tidc/source-receipts/NET-POLYMATH.json` | `LIMITATION_RETAINED`: contribution-level archive reconstruction and proof-completion date remain unresolved. |
| NET-002 | SRC-005 | Tao project launch/progress/writing records, retrospective account, and tranche-02 split | `LIMITATION_RETAINED`: child-specific verification, recognition, and contribution-level chronology remain unresolved. |
| AI-001 | SRC-006 | Nature primary article, first-party disclosure, tranche-02 split, and receipt at `data/tidc/source-receipts/AI-001.json` | `LIMITATION_RETAINED`: child-level dimensions, chronology, baselines, and independent reproduction remain unresolved where not evidenced. |
| AI-002 | SRC-007 | Nature paper, DeepMind announcement, LLVM review/commit, and receipt at `data/tidc/source-receipts/AI-002.json` | `LIMITATION_RETAINED`: exact internal discovery and one canonical verification date remain unresolved. |
| AI-003 | SRC-008 | Primary Nature paper | Cap-set and bin-packing results require separate records and exact generation dates. |
| QNT-001 | SRC-009 | Primary Quantum paper | Adoption and downstream use remain unmeasured. |
| QNT-002 | SRC-010 | Primary published paper | Theoretical infrastructure versus empirical capability status remains unresolved. |

## Access-precursor sources

| Record | Source ID | Primary source posture | Known limitation |
|---|---|---|---|
| QAI-2025-JP-OSAKA | QAI-SRC-001 | University of Osaka institutional announcement | Does not establish sustained access or downstream clustering. |
| QAI-2025-JP-OSAKA | QAI-SRC-002 | RIKEN institutional announcement | Independent usage evidence remains required. |
| QAI-2025-JP-OSAKA | QAI-SRC-003 | University of Osaka OQTOPUS release announcement | Open-source release does not establish practical external usability. |

## Packet admissibility rules

1. Coders may use the cited primary or authoritative records and clearly identified supplements.
2. Search snippets, social-media summaries, and unattributed reposts are not source evidence.
3. Missing dates remain null or Unresolved.
4. A publication date must not be substituted for candidate generation without explicit proxy labeling.
5. Institutional announcements may support launch posture but not downstream impact.
6. Source disagreement must be retained in the coder response.
7. Sources added after packet freeze require a new packet version.
8. A `LIMITATION_RETAINED` source receipt closes the retrieval task without converting absent bytes or logs into verified evidence.

## Archival retrieval queue

```text
COMP-001 LIMITATION_RETAINED at data/tidc/source-receipts/COMP-001.json
COMP-002 original computational reports and later certificate verification
COMP-003 exact journal chronology and simplified-proof sequence
SRC-004 LIMITATION_RETAINED at data/tidc/source-receipts/NET-POLYMATH.json
SRC-005 LIMITATION_RETAINED at data/tidc/source-receipts/AI-001.json
SRC-006 LIMITATION_RETAINED at data/tidc/source-receipts/AI-002.json
AI-003 separate cap-set and bin-packing generation records
QNT-001 benchmark adoption and downstream-use records
QNT-002 later experimental use records
QAI-2025-JP-OSAKA sustained-access, eligibility, usage, and downstream-output records
```

## Completion boundary

The source packet is sufficient to open a pilot reliability exercise but not sufficient for confirmatory historical analysis. Archival incompleteness must remain visible in both confidence coding and disagreement records.
