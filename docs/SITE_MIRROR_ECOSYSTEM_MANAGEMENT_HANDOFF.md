# Site Mirror Ecosystem Management Handoff

## Purpose

This file is the Site-side ecosystem-management handoff for Publisher-to-Site mirror activation.

It exists so future sessions, Site automation, or ecosystem management logic can continue Site evidence production without prior chat context.

## Current Assessment Goal

```text
Continue building without manual actions needed through completion OR until task handoff and task completion is capable of being handled by the ecosystem's own management.
```

## Current State

```text
management_state: self_managed_handoff_ready
site_state: ready_for_automated_site_evidence_and_closure_nudge
publisher_repo: GCAT-BCAT-Engine/Publisher
site_repo: StegVerse-Labs/Site
source_path: papers
target_path: papers
manual_action_requirement: none_for_site_evidence_entry
remaining_dependency: live workflow artifact production and Publisher closure observation
```

## Site Responsibilities

```text
1. Resolve Publisher source repository/ref/path.
2. Check Site paper display policy.
3. Check transition-table public copy.
4. Check public ingestion contract.
5. Validate pending evidence packet and live evidence state before mirror.
6. Check out Publisher papers source.
7. Mirror papers and generate public indexes.
8. Validate mirrored manifest metadata.
9. Validate paper aliases.
10. Write Site evidence packet and live evidence state.
11. Upload site-mirror-evidence artifact.
12. Nudge Publisher closure workflow when cross-repo credentials are available.
13. Commit mirrored papers and evidence updates when changed.
```

## Publisher Responsibilities

```text
1. Produce Publisher verification receipt artifact.
2. Run closure workflow on dispatch completion, schedule, push, or direct dispatch.
3. Retry artifact discovery with bounded retry.
4. Reject stale or out-of-order artifact pairs.
5. Write pending probe while artifacts are missing or stale.
6. Write closure receipt when Publisher and Site artifacts are fresh, ordered, and evidence-valid.
7. Activate Publisher verification tracker and activation status.
```

## Source Of Truth Files

```text
StegVerse-Labs/Site/docs/SITE_MIRROR_HANDOFF.md
StegVerse-Labs/Site/docs/SITE_MIRROR_EVIDENCE_PACKET.md
StegVerse-Labs/Site/docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json
StegVerse-Labs/Site/scripts/write_site_mirror_evidence.py
StegVerse-Labs/Site/scripts/check_site_mirror_evidence_packet.py
StegVerse-Labs/Site/scripts/check_site_mirror_live_evidence_state.py
StegVerse-Labs/Site/.github/workflows/mirror-papers.yml
GCAT-BCAT-Engine/Publisher/docs/MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md
GCAT-BCAT-Engine/Publisher/docs/PUBLISHER_MIRROR_HANDOFF.md
GCAT-BCAT-Engine/Publisher/tools/close_site_mirror_activation.py
GCAT-BCAT-Engine/Publisher/.github/workflows/close-site-mirror-activation.yml
```

## Acceptance Criteria

The Site-side task is complete when one of these conditions is true:

```text
A. Activated completion:
   - Site mirror workflow produced site-mirror-evidence artifact.
   - Publisher closure workflow consumed the Site artifact and Publisher receipt artifact.
   - Publisher closure receipt exists.
   - Publisher tracker/status are activated.

B. Self-managed handoff completion:
   - This file exists.
   - Site handoff points to automated evidence production and Publisher closure nudge.
   - Publisher management handoff exists and points to automated fresh ordered closure.
   - Remaining work is live artifact production/observation, not manual evidence entry.
```

## Current Completion Classification

```text
classification: self_managed_handoff_completion
activated_completion: not_yet_observed
reason: live workflow artifacts have not been observed in this repository state, but Site evidence production and Publisher closure handoff are sufficient for the ecosystem to continue without this chat.
```

## Non-Claims

This handoff does not claim:

```text
- live mirror activation has occurred;
- Site evidence artifact has been observed;
- Publisher closure receipt has been generated;
- Publisher tracker/status have been activated by closure workflow.
```

## Archive Readiness

```text
thread_archive_ready: true
archive_reason: Site-side task state is repo-resident and linked to Publisher-side management handoff. No additional content from this chat is required for Site evidence production or Publisher closure continuation.
```
