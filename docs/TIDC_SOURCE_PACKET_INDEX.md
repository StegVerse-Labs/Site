# TIDC Independent-Coding Source Packet Index

## Status

```text
posture: SOURCE_PACKET_INDEX
research_state: PILOT_NOT_CONFIRMATORY
packet_version: v0.1
records: 11
source_records: 13
archival_completeness: PARTIAL_LIMITATIONS_RETAINED
source_receipts_complete_or_limited: 9
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
| AI-003 | SRC-008 | Nature article, DeepMind announcement, tranche-02 split, and receipt at `data/tidc/source-receipts/AI-003.json` | `LIMITATION_RETAINED`: child-specific generation/verification and reproduction evidence remain unresolved. |
| QNT-001 | SRC-009 | Quantum article, arXiv preprint, and receipt at `data/tidc/source-receipts/QNT.json` | `LIMITATION_RETAINED`: adoption, replication, downstream use, and exact run dates remain unresolved. |
| QNT-002 | SRC-010 | PRL article, arXiv preprint, and receipt at `data/tidc/source-receipts/QNT.json` | `LIMITATION_RETAINED`: theoretical self-capability is preserved; empirical use/adoption remains unresolved. |

## Access-precursor sources

| Record | Source ID | Primary source posture | Known limitation |
|---|---|---|---|
| QAI-2025-JP-OSAKA | QAI-SRC-001 | University of Osaka institutional announcement; terminal receipt at `data/tidc/source-receipts/QAI-2025-JP-OSAKA.json` | `LIMITATION_RETAINED`: launch/access posture does not establish sustained access, usage, downstream output, or discovery clustering. |
| QAI-2025-JP-OSAKA | QAI-SRC-002 | RIKEN institutional announcement | `LIMITATION_RETAINED`: independent usage evidence remains unresolved. |
| QAI-2025-JP-OSAKA | QAI-SRC-003 | University of Osaka OQTOPUS release announcement | `LIMITATION_RETAINED`: open-source release does not establish practical external usability or research impact. |

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
SRC-001 LIMITATION_RETAINED at data/tidc/source-receipts/COMP-001.json
SRC-002 LIMITATION_RETAINED at data/tidc/source-receipts/COMP-002.json
SRC-003 LIMITATION_RETAINED at data/tidc/source-receipts/COMP-003.json
SRC-004 LIMITATION_RETAINED at data/tidc/source-receipts/NET-POLYMATH.json
SRC-005 LIMITATION_RETAINED at data/tidc/source-receipts/AI-001.json
SRC-006 LIMITATION_RETAINED at data/tidc/source-receipts/AI-002.json
SRC-007 LIMITATION_RETAINED at data/tidc/source-receipts/AI-003.json
SRC-008 LIMITATION_RETAINED at data/tidc/source-receipts/QNT.json
SRC-009 LIMITATION_RETAINED at data/tidc/source-receipts/QAI-2025-JP-OSAKA.json
```

## Completion boundary

The repository-owned archival retrieval queue is exhausted with nine terminal source receipts, several intentionally `LIMITATION_RETAINED`. This is sufficient to expose the full pilot source packet and its unresolved evidence boundaries to the reliability workflow, but it is not sufficient for confirmatory historical analysis. Archival incompleteness remains visible in confidence coding, blinded comparison, disagreement handling, and Release-2 gate review.
