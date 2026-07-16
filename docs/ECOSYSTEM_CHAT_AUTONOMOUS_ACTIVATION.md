# Ecosystem Chat Autonomous Activation

```yaml
local_manual_tasks: eliminated
continuation_mode: workflow_managed_owner_routed
activation_state_source: data/ecosystem-chat-activation-state.json
refresh_trigger: scheduled_and_current_main_site_task_runner
manual_user_action_required: false
```

## Automated loop

```text
Site Task Runner
-> consolidated local validation
-> Pages deployment
-> public route verification
-> external chat activation evidence
-> ecosystem chat activation state
-> owner-routed unresolved gates
-> generated data committed by the scheduled/current-main workflow
```

`scripts/build_external_chat_activation_evidence.py` automatically invokes
`scripts/update_ecosystem_chat_activation_state.py`. The state generator writes
`data/ecosystem-chat-activation-state.json` and assigns every unresolved gate to
the repository that owns it.

The scheduled `Site Task Runner` runs every six hours and after successful
`Site Bootstrap Validate` completion. Generated `data/` and `docs/` state is
committed from `main`; no user observation, confirmation, file movement, or
manual workflow dispatch is required for continuation.

## Owner routing

- `StegVerse-Labs/Site` owns current-main validation, public-route verification,
  mutation-disabled verification, and Site activation evidence.
- `StegVerse-org/LLM-adapter` owns destination current-main verification,
  authorized same-origin deployment, and retrieval/provider receipt emission.
- `master-records/orchestration` owns authenticated custody and reconstructability
  evidence.

A blocked external gate is not converted into a user task. It remains a
machine-readable owner-routed action until matching evidence arrives.

## Authority boundary

The generated state does not grant deployment, mutation, custody, publication,
release, or certification authority. Activation becomes complete only when all
required gates are evidenced as true.
