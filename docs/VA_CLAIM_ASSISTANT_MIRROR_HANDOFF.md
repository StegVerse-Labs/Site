# VA Claim Assistant Mirror Handoff

## Identity and authority

```text
Goal ID: SV-VA-DUAL-FLOW-001
Active continuation goal: SV-VA-COORDINATED-LLM-002
Final planned goal: SV-VA-SECURE-DOCUMENTS-003
Originating session goal: replace text-heavy VA claims guidance with IKEA-style instructions for veterans who are uncomfortable online
Repository: StegVerse-Labs/Site
Branch: main
Canonical issue: StegVerse-Labs/Site#113
Document module issue: StegVerse-Labs/Site#116
LLM runtime owner: StegVerse-org/LLM-adapter#90
Canonical handoff: docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
Repository collision authority: docs/SITE_MIRROR_HANDOFF.md and data/site-orchestration-state.json
Public instruction page: va-disability-claim-guide.html
Focused walkthrough: va-claims-guided-workflow.html
Help surface: va-claims-chat.html
```

No guide, walkthrough, chat, validator, receipt, or deployment grants authority to adjudicate, diagnose, rate, sign, represent, or file a claim. The veteran retains submission authority.

## Required goal sequence

```text
GOAL 1 — COMPLETE: IKEA-style dual-flow instruction system
GOAL 2 — ACTIVE: coordinated VA Resources LLM
GOAL 3 — QUEUED FINAL: secure document retrieval and upload modules
```

Goal 2 must be activated before Goal 3 is treated as the active implementation target. Goal 3 may define interfaces and collision boundaries in parallel, but public document upload and private document retrieval remain disabled until the coordinated LLM path is validated and the secure module exit gates pass.

## Active design contract

```text
PRIMARY_CHECKLIST_PLUS_FOCUSED_HELP
Primary page: all steps visible in order
Primary controls per step: DONE + Help me with this
DONE effect: persist completion, dim card, brighten DONE state
Help effect: open matching walkthrough step with ?step=N
Walkthrough: one selected step visible
Walkthrough controls: Return to Instruction Page + Continue with help me complete this
Shared browser-local state key: vaClaimsStepStateV1
Instruction limit: one visual and a few action words in the main path
Additional explanation: focused walkthrough or Claims Chat only
```

## Completed presentation inventory

| Task ID | Requirement | Canonical location | Claim state | Completion | Validation / evidence |
|---|---|---|---|---|---|
| SV-VA-DF-001 | Remove internal capability telemetry and text-heavy veteran-facing copy | `va-disability-claim-guide.html` | RELEASED_COMPLETE | COMPLETE | commits `9a6d69c902d47382ebf58b5997869b6e77c0ea73`, `5f1188287283afa1ce8fac66211610e82ece7604` |
| SV-VA-DF-002 | Show all six instruction cards on one page | `va-disability-claim-guide.html` | RELEASED_COMPLETE | COMPLETE | commit `5f1188287283afa1ce8fac66211610e82ece7604` |
| SV-VA-DF-003 | Add DONE state, card dimming, summary, and reset | primary instruction page | RELEASED_COMPLETE | COMPLETE | shared-state implementation commit `5f1188287283afa1ce8fac66211610e82ece7604` |
| SV-VA-DF-004 | Add Help me with this routing to the exact step | primary instruction page | RELEASED_COMPLETE | COMPLETE | six `?step=N` links |
| SV-VA-DF-005 | Focus walkthrough on one selected step | `va-claims-guided-workflow.html` | RELEASED_COMPLETE | COMPLETE | commit `1fdf7e52edc8e0d53918411626ed41e2e642ce9d` |
| SV-VA-DF-006 | Share completion state between both pages | both HTML surfaces | RELEASED_COMPLETE | COMPLETE | `vaClaimsStepStateV1` on both pages |
| SV-VA-DF-007 | Add return and continue-help controls | focused walkthrough | RELEASED_COMPLETE | COMPLETE | commit `1fdf7e52edc8e0d53918411626ed41e2e642ce9d` |
| SV-VA-DF-008 | Enforce dual-flow contract automatically | validators + workflow | MACHINE_OWNED | COMPLETE | run `31134444619` PASS |
| SV-VA-DF-009 | Persist inspectable validation receipts | GitHub Actions artifact | MACHINE_OWNED | COMPLETE | artifact `8977344125`, digest `sha256:84cf875ef5028cd1ddfe17d95d37c0184537654c6cec44bc7a3e43bf3dce3481` |
| SV-VA-DF-010 | Activate current pages on public Site | GitHub Pages | MACHINE_OWNED | COMPLETE | deployment `5786525421`, status `success` |

## Active Goal 2 — Coordinated VA Resources LLM

```text
Goal ID: SV-VA-COORDINATED-LLM-002
Canonical runtime owner: StegVerse-org/LLM-adapter#90
Site projection owner: StegVerse-Labs/Site#113
Current public Site chat: scripted procedural preview, not live LLM
Current LLM-adapter state: governed VA Claims Chat profile and provider-neutral session layers already implemented
Active collision boundary: StegVerse-org/LLM-adapter PR #120 owns the hosted VA provider-preflight repair lane
Session role: integration, validation, and Site projection until PR #120 releases its claim
```

Required activation evidence for Goal 2:

1. A live provider-backed VA request completes through the governed adapter.
2. The request is classified into a VA claim route.
3. Only admitted official VA sources support external factual claims.
4. The response contains proposition-level citations, source authority classes, retrieval/effective dates, contradiction and uncertainty labels, and false-authority flags.
5. The provider execution produces a stable secret-free receipt.
6. The Site chat calls the governed endpoint rather than local scripted answer rules.
7. A deployed end-to-end request is observed from Site through adapter and back.
8. Private upload remains disabled during Goal 2.

Goal 2 claim classification:

```text
LLM profile and provider-neutral session: COMPLETE
VA governed retrieval contract: IMPLEMENTED / requires current live activation evidence
Hosted provider preflight repair: CLAIMED_FOR_IMPLEMENTATION by PR #120
Site live LLM projection: UNCLAIMED after PR #120 release, otherwise CLAIMED_FOR_INTEGRATION by this session
Public coordinated LLM activation: INCOMPLETE
```

## Final Goal 3 — Secure document retrieval and upload modules

```text
Goal ID: SV-VA-SECURE-DOCUMENTS-003
Canonical Site owner: StegVerse-Labs/Site#116
Runtime privacy/retrieval dependency: StegVerse-org/LLM-adapter
Custody/reconstruction dependency: master-records/orchestration
State: QUEUED_FINAL
Public upload: DISABLED
Private retrieval: DISABLED
```

Required modules and exit gates:

- consent-bound upload intake;
- malware/type/size validation;
- encrypted temporary storage with retention and deletion state;
- stable file hash and document index;
- page-level extraction and citation anchors;
- privacy classification and redaction controls;
- user-record facts separated from inference and official authority;
- favorable, unfavorable, conflicting, and unresolved evidence retained;
- secure retrieval scoped to the active veteran session;
- contradiction and missing-evidence views;
- custody and reconstruction references;
- deterministic receipts and fail-closed public activation;
- representative multi-document fixture with stable hashes and page citations;
- deployed runtime receipt before upload controls become public.

## Claims and convergence

```text
Dual-flow presentation implementation: COMPLETE / RELEASED
Dual-flow validation and deployment: COMPLETE / MACHINE_OWNED
Coordinated VA LLM: ACTIVE CANONICAL WORKSTREAM under LLM-adapter#90 and Site#113
Secure document modules: QUEUED under Site#116; no competing implementation should begin while Goal 2 activation remains unresolved
Automated filing: INACTIVE / FAIL-CLOSED
```

No duplicate implementation claim may be created against PR #120 files or provider-preflight capability. Until that PR is merged, closed, superseded, or its claim expires, this session may validate, reconcile, prepare nonconflicting Site integration, and preserve Goal 3 contracts only.

## Requirements transferred from this session

- IKEA-style main-path rule: see one thing, do one thing, confirm one thing;
- more than a few words belongs outside the primary instruction path;
- all steps remain visible on one primary page;
- each step has DONE and Help me with this;
- DONE visually dims the card and brightens completion;
- help opens the same step in a focused walkthrough;
- walkthrough returns to the instruction page or continues into step-specific help;
- both pages share persistent completion state;
- primary page shows completed and incomplete steps;
- the chat must become a coordinated VA Resources LLM, not remain a scripted browser preview;
- the coordinated LLM is the next goal;
- secure document retrieval and upload are the final goal;
- validation must reject regressions and produce receipts;
- activation must be proven separately from repository presence.

`MERGED INTO: StegVerse-Labs/Site/docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`

## Archive conditions and measures

This session is not archive-ready. Goal 2 remains active and Goal 3 remains queued with unique sequencing and activation requirements now preserved here.

```text
presentation task completion: 10/10
coordinated LLM activation: incomplete
secure document modules: queued
session requirement transfer: complete
session consolidation: active, not archive-ready
```
