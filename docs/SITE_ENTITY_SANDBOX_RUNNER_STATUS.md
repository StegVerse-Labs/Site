# Entity Sandbox Runner Site Status

## Status

```text
source_repo: StegGhost/entity-sandbox-runner
release_goal: admissibility_plane_activation_candidate
site_status: display_only_integration_pending
activation_boundary: Site does not certify runtime admissibility or issue commit-time permission.
```

## Source packet

```text
release/entity_sandbox_runner_admissibility_plane_release_packet.json
release/entity_sandbox_runner_downstream_tasks.md
```

## Local capabilities reported by source repo

```text
schema-aware manifest validation
transition-table-driven routing
CGE route fingerprinting
transition receipt emission
sandbox repair routing
repair result re-entry through ingestion
startup admissibility verification
release integration verification
```

## Site role

Site may display the source repository's release/integration status after source evidence exists.

Site must not become the source of truth for:

```text
manifest schema authority
transition table authority
CGE fingerprint authority
transition receipt authority
sandbox repair authority
release activation authority
```

## Required evidence before claiming ready

```text
StegGhost/entity-sandbox-runner brain_reports/admissibility_plane_verification.json exists
StegGhost/entity-sandbox-runner brain_reports/release_integration_verification.json exists
StegGhost/entity-sandbox-runner release packet exists
Downstream publication surfaces have verified the packet or recorded pending_external_evidence
```

## Current result

```text
site_mirror_state: installed_display_only
release_activation_state: pending_external_evidence
```
