# Governed VA Claims Chat Mirror Handoff

## Identity

```text
Goal ID: SV-VA-CLAIMS-CHAT-001
Repository: StegVerse-Labs/Site
Branch: main
Canonical issue: StegVerse-Labs/Site#113
Document workspace issue: StegVerse-Labs/Site#116
Compatibility/deep-work surface: va-claims-chat.html
Primary conversational surface: ecosystem-chat.html
Capability state: data/va-claim-assistant/chat-capability-state.json
Repository receipt: data/va-claim-assistant/chat-surface-validation.json
Deployment receipt: data/va-claim-assistant/governed-surfaces-deployment.json
```

## Product requirement — veteran-first public UI

Public UI must expose only information and controls that help the veteran complete the task in front of them.

```text
technical competency assumed: NONE
internal capability labels: HIDDEN
runtime/governance terminology: HIDDEN unless needed to explain a user-visible limitation
scaffolding/stub labels: HIDDEN
internal transition state: MACHINE-READABLE ONLY
primary interaction: ordinary-language conversation
common intents: direct one-tap starting points
instructions: one step at a time
sensitive-data warning: short, plain-language, visible
veteran authority: preserved
```

Do not require a veteran to understand StegVerse architecture, runtime projection, source-grounding terminology, LLM state, governance state, receipt state, fail-closed terminology, card architecture, or implementation status in order to use the public product.

## Current surface change — 2026-08-21

The public VA Claims Chat compatibility/deep-work surface was simplified for nontechnical users.

```text
commit: 9660783aece28450de01f63e7d400ccf5ad8ac68
surface: va-claims-chat.html
validator update: c82cb10caa6d2271296b91a2af880d892b06f2ea
policy: VETERAN_FIRST_MINIMAL_UI
```

Removed from the visible interface:

- internal capability-state badge;
- SOURCE-GROUNDED / coordinated-LLM implementation terminology;
- “choose how to use” architecture language;
- confirmation-rule panel;
- document-safety-gate panel;
- unsupported-route/fail-closed implementation language;
- card-page navigation as a primary user decision.

Installed instead:

- “What can I help you with?” as the primary prompt;
- ordinary free-text VA claims question entry;
- one-tap common starting points;
- step-by-step help only when relevant;
- plain-language privacy warning;
- conversational runtime use when verified, with local bounded fallback when it is not.

## Completion state

```text
public compatibility/deep-work UI simplification: IMPLEMENTED
repository validation contract: UPDATED
primary unified conversational topology: ACTIVE PROGRAM GOAL
coordinated VA Resources LLM activation: NOT YET VERIFIED
private document upload: DISABLED pending Goal 3 gates
automated filing: DISABLED pending filing gates
veteran submission authority: RETAINED
authority effect: NONE
```

The prior `RELEASED_COMPLETE` surface claim applied to the earlier procedural presentation layer only. It must not be interpreted as 100% completion of the VA conversational product.

## 100% product exit condition

This work remains open until the veteran-visible product is fully conversational and the required governed runtime is actually observed end to end.

Required exit evidence:

1. a VA-related prompt enters the primary `ecosystem-chat.html` surface;
2. VACC classifies and handles the VA intent without exposing internal routing complexity;
3. a real provider-backed governed request executes through the canonical adapter/runtime path;
4. external factual claims use admitted authoritative VA sources;
5. the answer is conversational and presents only relevant user-facing links/citations;
6. Master Records custody is `RECORDED` and reconstruction is `PASS` for the real execution;
7. the Site runtime projection becomes `VERIFIED` only from that evidence;
8. deployed browser observation confirms the full Site -> VACC -> runtime -> answer path;
9. mobile usability requires no technical knowledge and no internal architecture interpretation;
10. downstream activation information is propagated after verified activation to Publisher, admissibility-wiki, and stegguardian-wiki.

## Canonical continuation

```text
Unified surface / VA specialty goal: StegVerse-Labs/Site#113
Runtime continuation: StegVerse-org/LLM-adapter#90
Canonical runtime carrier: StegVerse-Labs/.github#60 / SHWP-ECOSYSTEM-CHAT-INFERENCE-001
Document continuation: StegVerse-Labs/Site#116
Custody/reconstruction: master-records/orchestration#15
Filing transport: future TVC-backed admitted transport lane
Downstream after verified activation:
  GCAT-BCAT-Engine/Publisher
  StegVerse-Labs/admissibility-wiki
  StegVerse-002/stegguardian-wiki
```

## Archive condition

Do not archive the broader VA conversational product as complete until the 100% product exit condition above is satisfied. The compatibility/deep-work UI mutation is durable; runtime activation remains machine-owned and active.
