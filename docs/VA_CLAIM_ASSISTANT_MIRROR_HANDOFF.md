# VA Claim Assistant Mirror Handoff

## Identity

```text
Goal family: SV-VA
Repository: StegVerse-Labs/Site
Canonical issue: StegVerse-Labs/Site#113
Parent unified capability goal: StegVerse-Labs/Site#239
Primary public conversational surface: ecosystem-chat.html
VACC role: VA specialty capability consumed by the shared conversational surface
Compatibility/deep-work surface: va-claims-chat.html
Deterministic Guide: va-disability-claim-guide.html
Secure-document owner: StegVerse-Labs/Site#116
Claimant/submission binding: StegVerse-Labs/Site#180
Canonical runtime owner: StegVerse-org/LLM-adapter#90
Custody/reconstruction owner: master-records/orchestration#15
Shared capability contract: data/unified-conversational-capabilities.json
```

No Site surface, model output, receipt, deployment, authentication event, or validator grants authority to adjudicate, diagnose, rate, represent, sign, or file a VA claim. The veteran remains claimant, fact confirmer, certifier, and submission authority unless an independently authorized representative acts within an admitted scope.

## Canonical topology

VACC is not a competing primary chat application.

```text
VA-related user prompt
-> ecosystem-chat.html
-> VA intent classification
-> VACC specialty context / admitted official VA sources / VA tools
-> conversational answer
-> relevant authoritative links/citations
-> optional deterministic VA Guide / claim workflow / document workflow destination
```

`va-claims-chat.html` remains a compatibility, deterministic-help, testing, and deep-work destination. It must not evolve into a second general provider/runtime stack.

## Required goal sequence

```text
GOAL 1 — SV-VA-DUAL-FLOW-001 — COMPLETE
GOAL 2 — SV-VA-COORDINATED-LLM-002 — IMPLEMENTED / PUBLIC UNIFIED-SURFACE ACTIVATION EVIDENCE INCOMPLETE
GOAL 3 — SV-VA-SECURE-DOCUMENTS-003 — QUEUED PUBLIC ACTIVATION / CONTRACTS AND PRIVACY PREPROCESSOR PARTIALLY COMPLETE
GOAL 4 — SV-VA-FINAL-SUBMISSION-FALLBACK-004 — COMPLETE
```

## Goal 2 — coordinated conversational VACC

The canonical adapter now contains broad VA intent classification, admitted official-source grounding, plain-language conversational rendering, TVC-bound sovereign/local execution, per-turn identity/usage evidence, and same-execution Master Records reconstruction paths. It does not grant filing or private-document authority.

Two runtime topologies must remain distinct:

1. Browser/device-local execution — prior iPod touch/iPhone browser confirmations are valid evidence for the device-local service-worker path they actually observed.
2. Resident sovereign carrier/server execution — requires its own persistent carrier/runtime evidence before that distinct topology is claimed complete.

Lack of one topology's evidence does not invalidate evidence for the other.

### Goal 2 public activation gates

1. a VA prompt enters `ecosystem-chat.html` and is classified to VACC;
2. a real admitted runtime executes the request;
3. external factual VA claims use admitted official VA sources;
4. the answer remains conversational and user-focused with useful citations/links where appropriate;
5. execution identity and false-authority flags are retained;
6. required custody/reconstruction evidence is PASS for the execution topology being claimed;
7. Site projection becomes VERIFIED only from actual evidence;
8. deployed browser observation confirms the shared-surface path;
9. no duplicate provider/runtime authority is introduced.

## VACC intent domain

VACC covers disability claims/appeals, benefits eligibility, VA health care, community care, pharmacy/billing, records/forms, education, home loans/housing, VR&E, caregiver/family benefits, burial/memorial, and other VA-administered programs. Disability claims remain a deep specialty rather than the entirety of VACC.

## Source/evidence invariants

```text
external factual VA claims -> admitted official VA sources
source fact != inference
contradictions remain explicit
uncertainty remains explicit
no fabricated diagnosis/nexus/event/onset/severity/limitation facts
no unsupported rating-percentage targeting
no award-size optimization
claim language only from supported facts
```

## Goal 3 — secure document/evidence lifecycle

Canonical owner: Site#116 with #178-#184. Required controls include consent-bound upload, redirect-only authoritative retrieval by default, separately controlled originals, sanitized/tokenized derivatives, stable hashes, page/source-bound facts, privacy classification, contradiction handling, chronology reconciliation, evidence-to-criteria/claim-language provenance, workload metrics, custody/reconstruction, veteran-controlled packet state, and claimant binding only at the separately authorized submission boundary.

Public private-document upload, retrieval, model review, and filing remain disabled until their specific gates pass.

## Goal 4 — final VA.gov submission fallback — COMPLETE

Until an independently authorized connected filing path exists, the veteran uses the official VA.gov submission flow, reviews the claim, certifies it, and submits it directly. VACC does not silently acquire submission authority.

## Public UI requirement

The public UI assumes no technical competency. Internal capability enums, runtime names, receipt mechanics, worker state, governance labels, and scaffolding status are hidden unless needed to explain a user-visible limitation.

## Collision boundaries

- Do not create a second VACC provider/runtime lane.
- Do not create a second primary VA chat shell.
- Do not duplicate TVC route authority.
- Do not replace Master Records custody/reconstruction with local persistence claims.
- Do not enable private document upload/retrieval or filing before its gates pass.
- No NON-TV/TVC secret/token.
- Model output never grants authority.

## Current continuation

```text
shared capability reconciliation: TASK-2026-0007 / Site#239
VACC public activation: Site#113
runtime implementation/execution: StegVerse-org/LLM-adapter#90
resident carrier continuation: StegVerse-Labs/.github#60 / SHWP-ECOSYSTEM-CHAT-INFERENCE-001
secure documents: Site#116
custody/reconstruction: master-records/orchestration#15
```

## Current completion posture

```text
Goal 1 deterministic Guide: COMPLETE
Goal 2 runtime implementation: IMPLEMENTED
Goal 2 device-local browser runtime proof: OBSERVED FOR DEVICE-LOCAL TOPOLOGY
Goal 2 resident carrier runtime proof: DISTINCT EVIDENCE STILL REQUIRED FOR THAT TOPOLOGY
Goal 2 unified public activation projection: INCOMPLETE
Goal 3 secure-document public activation: INCOMPLETE
Goal 4 VA.gov submission fallback: COMPLETE
Product-level VACC completion: INCOMPLETE
```
