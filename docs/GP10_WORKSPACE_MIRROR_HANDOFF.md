# GP10 Workspace Mirror Handoff

Status: ACTIVE — CANONICAL SITE CONTINUATION
Updated: 2026-08-02
Goal ID: `GP10-SITE-SECURE-GUIDED-WORKSPACE-001`
Originating session goal: provide a simplified, logically narrowing GP10 evidence and commercial-posture workspace, a beginner examples surface, and browser security controls that treat applicable federal cybersecurity requirements as a minimum baseline rather than a target ceiling.
Repository: `StegVerse-Labs/Site`
Branch: `main`

## Canonical ownership

- GP10 domain logic, schemas, evidence custody, ingestion, runtime validation, and commercial governance remain canonical in `StegVerse-Labs/GP10`.
- This repository owns only the unlisted browser workspace, examples surface, browser-side security controls, and Site isolation verification.
- Canonical GP10 continuation: `StegVerse-Labs/GP10/GP10_MIRROR_HANDOFF.md`.
- Canonical Site continuation for this surface: this file.

MERGED INTO: `StegVerse-Labs/Site/docs/GP10_WORKSPACE_MIRROR_HANDOFF.md`

## Authoritative files

- `gp10-workspace.html`
- `gp10-workspace-examples.html`
- `assets/gp10-workspace.js`
- `assets/gp10-evidence-integration.js`
- `assets/gp10-workspace-wizard.js`
- `assets/gp10-validation-feedback.js`
- `assets/gp10-examples-adaptive.js`
- `assets/gp10-security.js`
- `scripts/check_gp10_workspace.py`
- `docs/GP10_WORKSPACE_SECURITY_BASELINE.md`
- `docs/GP10_WORKSPACE_HANDOFF.md` (legacy descriptive handoff; redirected here)

## Active claims

### `GP10-SITE-SECURITY-HARDENING`

- Claimant: `StegVerse-Labs/Site` browser-security lane
- Role: `CLAIMED_FOR_IMPLEMENTATION`
- Created: `2026-08-02T19:30:00-05:00`
- Surfaces: the authoritative files listed above, excluding GP10 repository runtime-validation surfaces
- Release condition: security controls, static verification markers, and session-transfer records are committed; remaining deployment/runtime observation is assigned to a machine-observable Site deployment task
- Expected evidence: commits touching this handoff, security baseline, security script, workspace pages, and Site checker
- Collision boundary: no session may alter GP10 repository validators, workflows, receipts, schemas, or claimed runtime surfaces through this Site claim
- Next task after release: direct hosted-page observation and preservation of the deployed commit identity

## Preserved interaction requirements

1. Show one logical decision at a time.
2. Hide fields that do not follow from prior answers.
3. Skip economics and threshold pages when a hard-stop condition already controls the result.
4. Preserve missing information as missing; never synthesize evidence, prices, thresholds, or approval.
5. Maintain a separate beginner examples page with safe synthetic files and plain-language governance explanations.
6. Keep both pages unlisted and marked `noindex`, `nofollow`, and `noarchive`.
7. Preserve `execution_authority: false` and browser-local uncustodied state.
8. Site is an interface and must not become the source of truth for GP10 evidence or authority.

## Security objective

Applicable federal security requirements are treated as a minimum baseline. Browser controls must fail closed, minimize ambient authority, reduce injection and data-leak surfaces, preserve cryptographic evidence integrity, and make local data exposure visible.

Implemented controls and remaining controls are defined in `docs/GP10_WORKSPACE_SECURITY_BASELINE.md`.

## Validation

```bash
python3 scripts/check_gp10_workspace.py
```

The checker must verify page isolation, authority boundaries, adaptive gating, examples synchronization, security policy markers, security-script loading, and cryptographic browser controls.

## Cross-repository integration

- Source authority: `StegVerse-Labs/GP10`.
- Site does not promote browser records into repository custody.
- Exported bundles must continue through GP10 validation and ingestion contracts.
- No Publisher, wiki, Master-Records, or public Site propagation is authorized before a genuine GP10 release and destination-owned verification.

## Incomplete work and durable owners

1. Hosted deployment observation — owner: Site deployment/runtime observation lane; release condition: deployed page source contains the committed security markers and current script references.
2. Authenticated durable service — owner: future named service repository after service scope and domain are approved; not implied by this static page.
3. Server-delivered HTTP security headers — owner: future hosting/deployment control plane supporting headers; current GitHub Pages surface can enforce CSP only through document policy and browser controls.
4. Real field validation — owner: `StegVerse-Labs/GP10/data/operations/continuation_tasks.json`.

## Session consolidation and archive conditions

This handoff receives the unique Site UX and federal-floor security requirements from the originating session. Once the security implementation, checker update, legacy-handoff redirect, and GP10 cross-reference are committed, no Site-specific requirement needs to remain in chat. Hosted observation remains repository/deployment-owned and does not require the originating session.

## Metrics denominator

Required Site deliverables for this workstream: 12.

- Developed-file completion: 8/12 before security implementation.
- Validation completion: 5/9 before security implementation.
- Integration completion: 3/5 before security implementation.
- Goal activation: 5/10 before security implementation.
- Session transfer: 0/1 before this handoff; complete when GP10 and Site handoffs cross-reference the transferred goal.
