# Site Mirror Handoff

## Current source of truth

This file is the authoritative continuation record for `StegVerse-Labs/Site`.

## Active goal state

```text
Goal: governed Ecosystem Chat and AI Entry application with fail-closed live activation, recoverability, release, and downstream evidence boundaries
Repository-local result: COMPLETE
Continuation mode: SCHEDULED_FAIL_CLOSED_EVIDENCE_MONITOR
Manual user tasks: NONE
Recursive repository-local goal expansion: DISABLED
```

## Installed application and governance surfaces

The repository contains the cohesive StegVerse AI entry window, chat and comparison routes, SDK guidance, governed backend preview, activation request/response fixtures, authority-decision fixtures, provider and receipt boundaries, operator-recoverability records, release-readiness lockfile, tag gate, downstream propagation records, and terminal monitoring records.

Canonical validation:

```bash
python scripts/check_ecosystem_chat_application.py
```

Active workflow:

```text
.github/workflows/validate.yml
```

The iOS-safe restoration mirror remains:

```text
iosnoperiod/github/workflows/validate.yml
```

## Completed terminal chain

```text
cohesive AI Entry application
-> governed backend activation preview
-> authority service boundary
-> receipt/provider/SDK access boundaries
-> operator recoverability boundary
-> recovery fixtures and completion
-> cross-repository handoff consolidation
-> green-run visibility consolidation
-> release-readiness lockfile
-> tag gate
-> stable archive checkpoint
-> post-archive monitor
-> loop checkpoint
-> terminal loop cycle record
```

Key terminal records:

```text
data/ai-entry-backend-activation-progress.json
data/ai-entry-recovery-completion.json
data/ai-entry-cross-repo-handoff.json
data/ai-entry-post-archive-monitor-completion.json
data/ai-entry-loop-checkpoint-completion.json
data/ai-entry-loop-cycle-record.json
docs/ECOSYSTEM_CHAT_TERMINAL_LOOP_HANDOFF.md
```

The canonical validator includes `scripts/check_ai_entry_loop_cycle_record.py` and rejects manual tasks, recursive next-goal creation, or authority escalation.

## Current evidence posture

```text
repository-local implementation: COMPLETE
manual tasks remaining: 0
connector-visible green run: NOT CONFIRMED
live provider use: NOT CONFIRMED
live SDK/runtime use: NOT CONFIRMED
authenticated custody: NOT CONFIRMED
reconstructability PASS: NOT CONFIRMED
release or tag authority: NOT GRANTED
```

Absent CI or live evidence does not reopen design or implementation work. Existing scheduled workflows and authority-bearing systems own re-evaluation. Missing evidence remains fail-closed and is never treated as success.

## Cross-repository continuation

```text
StegVerse-org/LLM-adapter
  -> scheduled validation and live verification
  -> stable pending blocker status
  -> immutable verified activation receipt after all gates pass

master-records/orchestration
  -> authenticated custody and reconstruction evidence

StegVerse-Labs/Site
  -> automatic import, hash verification, activation-state recomputation, and propagation

GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
  -> automatic non-authorizing downstream projections
```

No browser credential, artifact download, workflow dispatch, file transfer, screenshot confirmation, or manual publication task is required.

## Adjacent StegGate stable-rendezvous lane

Site issue #24 is also the canonical endpoint-publication/fail-closed-routing owner for the StegGate stable rendezvous required by `StegVerse-Labs/StegCore#68`. This is an adjacent integration lane and does not reopen the completed Site application implementation.

Installed surfaces:

```text
src/steggate-rendezvous-worker.js
wrangler.steggate.jsonc
.github/workflows/steggate-rendezvous-deploy.yml
data/steggate-rendezvous-activation.json
```

Intended stable origin:

```text
https://stegverse.org/api/steggate
```

The Worker contains no StegGate policy engine. It resolves the current verified micro-node, independently verifies canonical health, proxies only the bounded StegGate HTTP evaluation contract, and fails closed when no verified node exists.

Deployment run `31286621905`, job `93176517796`, directly observed both `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` as unavailable in the Actions runtime and therefore stopped before Wrangler deployment. No deployment success is claimed.

The deployment workflow is now machine-owned and scheduled hourly at minute 41. Every run emits `deployment-evidence/activation-observation.json`; missing credentials remain an explicit `BLOCKED` result and a failing workflow, not success. When both authorized bindings become available, the same workflow deploys the rendezvous, verifies readiness, canonical health and the exact four-disposition self-test, writes `LIVE_ACCEPTANCE_PASS` to `data/steggate-rendezvous-activation.json`, and comments issue #24. StegCore's independent hourly observer then discovers the stable rendezvous and owns the final complete-matrix evaluation and canonical issue #68 finalization.

Machine-observable release condition:

```text
CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID are both non-empty in the Site Actions runtime,
OR an already-authorized endpoint-publication plane deploys the same non-authorizing contract.
```

This lane has no remaining chat-only execution requirement. Its current claimant is repository automation, and the originating session may transfer/merge this lane to `StegVerse-Labs/Site#24 + data/steggate-rendezvous-activation.json + .github/workflows/steggate-rendezvous-deploy.yml`.

## Authority boundary

```text
provider output != authority
SDK validation != execution
usage measurement != admissibility
local persistence != custody
submission != custody
custody receipt != execution authority
reconstruction PASS != execution authority
workflow artifact != live evidence
pending status != activation
verified receipt != release authority
terminal monitor != CI success
rendezvous routing != StegGate policy authority
credential availability != deployment authority beyond the declared workflow contract
```

## Release posture

No release or tag is authorized until the existing machine gates receive visible validation, live runtime, custody, reconstruction, and downstream evidence. The decision is machine-gated; no manual review task is created.

## Archive posture

Repository-local implementation is archive-ready because all local modules, contracts, validators, handoffs, and automation required by the original Site workstream are installed. The adjacent StegGate rendezvous lane is also repository-owned and machine-observed: implementation is installed, the precise credential blocker is durable, hourly retry is active, and successful deployment automatically hands final acceptance back to StegCore. Archive readiness does not assert that the stable rendezvous is live.

## Archive determination

No Site-local requirement from the originating conversations needs to remain only in chat. Remaining live-evidence conditions are owned by scheduled workflows and authority-bearing systems, including the StegGate rendezvous credential release condition above.

**ARCHIVE NOW for the Site-local workstream; unresolved StegCore activation remains separately governed by its canonical handoff.**
