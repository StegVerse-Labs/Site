# Site Unified Governed Experience Status

## Status

```text
Repository: StegVerse-Labs/Site
Goal: unified-governed-experience
Status: unified-conversational-capability-contract-integration
Primary operating surface: ecosystem-chat.html
Homepage posture: one primary conversational entry plus contextual governed destinations
Shared capability contract: data/unified-conversational-capabilities.json
Capability handoff: docs/UNIFIED_CONVERSATIONAL_CAPABILITY_MIRROR_HANDOFF.md
Shared runtime owner: StegVerse-org/LLM-adapter
Execution authority from Site: none
Receipt authority from Site: none
```

## Product shape

The Site has one primary conversational experience. Users should not need to choose between competing technical applications before asking a question.

```text
user request
-> ecosystem-chat.html
-> shared intent/context classification
-> capability family selection
-> governed evidence/tool/runtime route
-> conversational response
-> contextual destination or bounded action only when useful and separately admitted
```

Current capability families:

```text
general_ecosystem
vacc_va
mathematics_educator
hil_experiment
```

Dedicated specialty pages remain allowed as deterministic guides, deep-work workspaces, experiment-specific participant surfaces, compatibility paths, or proof destinations. They are not alternate primary general-chat/provider/runtime stacks.

## Public user-experience contract

The public conversational surface should expose only information that helps the user accomplish the current task. Internal runtime names, capability-state enums, receipt mechanics, worker state, governance implementation labels, and transition machinery remain machine-readable unless a user-visible limitation actually needs explanation.

```text
technical competency assumption: none
ordinary-language conversation: primary
specialty selection: automatic where deterministically identifiable
contextual links/actions: shown only when useful
internal architecture: hidden by default
false authority: prohibited
```

## Shared capability routing

General/Ecosystem remains the default conversational capability. VA-related prompts route to VACC through `ecosystem-chat.html`; `va-claims-chat.html` and VA Guide/workflow pages remain specialty destinations. Mathematics prompts route to the mathematics educator specialty; `math-solver/index.html` remains deep-work/tooling. HIL remains discoverable/routable from the shared conversation while retaining its participant-specific surface where experiment protocol requires it.

## Runtime posture

Repository-local preview classification remains available as a bounded fallback, but it is no longer the target product definition. The target is real shared conversational execution through the canonical runtime owners with specialty-specific evidence/tool constraints.

```text
shared runtime/provider owner: StegVerse-org/LLM-adapter
canonical StegGate owner: StegVerse-Labs/StegCore
local/sovereign model owner: StegVerse-002/micro-node-runtime
route authority: StegVerse-Labs/TVC
custody/reconstruction: master-records/orchestration
browser/device-local execution: admitted StegOS service-worker runtime where applicable
```

A browser/device-local execution may satisfy the runtime gate for the topology it actually proves. A distinct resident-carrier topology requires its own evidence; one does not invalidate the other.

## Completion semantics

```text
plan != done
issue != done
task != done
handoff != done
assigned != done
ready != done
source_complete != activated
workflow_pass != runtime
release_ready != released
```

Unified contract installation is not product activation. Site#239 reaches completion only when each capability family's required deployed execution/evidence/custody/reconstruction/public-observation gates pass.

## Current continuation

```text
TASK-2026-0007: reconcile shared capability contract and legacy four-app/two-entry semantics
VACC: Site#113 + StegVerse-org/LLM-adapter#90
General runtime: Site#242 + StegVerse-org/LLM-adapter#18
Mathematics educator: Site#240 + shared runtime/tool owners
HIL: Site#81/#136/#243
```

After TASK-2026-0007 validates and merges, runtime work continues through those canonical owners without creating duplicate chat/runtime lanes.
