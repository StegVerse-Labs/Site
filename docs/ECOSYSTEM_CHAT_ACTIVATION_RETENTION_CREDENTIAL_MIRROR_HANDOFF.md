# Ecosystem Chat Activation Retention Credential Mirror Handoff

Updated: 2026-08-23
Repository: `StegVerse-Labs/Site`
Issue: `#471`
Claim: `SITE-ECOSYSTEM-CHAT-ACTIVATION-RETENTION-CREDENTIAL-CLEAN-471-20260823`
Branch: `claim/site-ecosystem-chat-activation-retention-credential-clean-471`
State: `IMPLEMENTATION_IN_PROGRESS`

## Goal

Remove the non-TV/TVC repository-sync secret dependency from the existing Ecosystem Chat activation-retention observer while preserving its active evidence-observation, persistence, and fail-closed activation responsibilities.

## Canonical sources of truth

- `docs/ECOSYSTEM_CHAT_ACTIVATION_MIRROR_HANDOFF.md`
- `docs/ACTIONS_COST_CONTAINMENT_MIRROR_HANDOFF.md`
- `docs/SITE_MIRROR_HANDOFF.md`

The activation goal remains incomplete. This task is **not** clock retirement and must not claim runtime, provider, custody, reconstruction, publication, release, or activation completion.

## Proven credential defect

`.github/workflows/ecosystem-chat-activation-retention.yml` currently passes:

```text
STEGVERSE_REPO_SYNC_TOKEN: ${{ secrets.STEGVERSE_REPO_SYNC_TOKEN }}
```

to `scripts/import_ecosystem_chat_external_activation_states.py`.

The importer uses that token only when retrieving:

```text
master-records/orchestration
reports/ecosystem-chat-custody-activation-state.json
```

That exact current-main record is publicly readable without authentication. The observed record remains fail-closed:

```text
state: CUSTODY_ACTIVATION_PENDING_EXTERNAL_EVIDENCE
authenticated_custody_receipt.complete: false
reconstructability_pass.complete: false
live_receipt.present: false
live_receipt.verified: false
```

Therefore anonymous acquisition can preserve the same evidence semantics without a non-TV/TVC secret.

## Required retained behavior

- hourly schedule remains;
- `workflow_run` trigger remains;
- source push trigger remains;
- `workflow_dispatch` remains;
- adapter activation receipt acquisition remains;
- destination and custody external-state validation remains hash-bound and fail-closed;
- activation state remains pending unless every existing gate is actually satisfied;
- existing state persistence remains in this bounded repair;
- no provider execution is added;
- no custody/reconstruction authority is added;
- no publication/release/activation authority is added.

## Required credential repair

- remove `STEGVERSE_REPO_SYNC_TOKEN` from the workflow environment;
- remove token discovery from the importer;
- remove Authorization-header construction from the importer;
- fetch the Master Records custody state anonymously from the public raw GitHub path;
- retain schema, record-type, canonical-hash, gate-object, and authority-boundary validation;
- add deterministic source validation proving the non-TV/TVC secret/token path cannot regress.

## Collision boundaries

- Do not modify `StegVerse-org/LLM-adapter` provider/runtime execution files.
- Do not modify `master-records/orchestration` custody evidence.
- Do not change `data/ecosystem-chat-activation-state.json` semantics by hand.
- Do not retire the retention clock while activation evidence is pending.
- Do not modify `.github/workflows/validate.yml` while Site #388 owns it.
- No Render.
- No NON-TV/TVC credential.
- No GitHub-token production/runtime authority.

## Completion gate

Release requires exact-head deterministic credential-boundary validation, activation-retention workflow validation, repository claim/orchestration validation, integration merge, durable release evidence in this handoff and the claim fragment, and issue #471 closure. Workflow success is not Ecosystem Chat activation.
