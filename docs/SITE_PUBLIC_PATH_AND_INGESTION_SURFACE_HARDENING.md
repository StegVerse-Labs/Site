# Site Public Path And Ingestion Surface Hardening

## Purpose

This packet defines how the Site repository should treat high-interest public paths and ingestion-facing surfaces while the Publisher-to-Site paper mirror is still awaiting live activation evidence.

The goal is not to claim adoption, activation, endorsement, or production readiness. The goal is to make externally visible paths explicit, non-misleading, and safe to inspect.

## Current Scope

```text
Repository: StegVerse-Labs/Site
Surface class: public documentation and static mirror surface
Activation state: pre-live-mirror-evidence
Source of truth: GCAT-BCAT-Engine/Publisher for mirrored papers
Public mirror role: display and receipt publication only
Proof authority: formalism-tests and source repositories, not Site
```

## High-Interest Path Classes

The following path classes must be handled deliberately because they are common crawler, user, or integration targets:

```text
/upload
/uploads
/incoming
/tools
/data
/actions
/papers
/papers_manifest.json
/docs
/api
/.well-known
```

Note: `/.well-known` is displayed here without the leading dot in ordinary path references when needed for user-facing copy. The actual web path includes the leading dot.

## Required Public-Path Behavior

Each high-interest path must resolve to one of the following states:

```text
1. canonical_public_path
2. intentional_static_documentation_path
3. mirror_surface_pending_live_evidence
4. unsupported_path_with_safe_explanation
5. blocked_or_unimplemented_path
```

No high-interest path should silently imply that uploads, actions, data ingestion, or live execution are available unless the backing governance evidence exists.

## Path Treatment Table

| Path Class | Current Treatment | Required Copy Boundary |
|---|---|---|
| `/papers` | Mirror display surface | Publisher remains source of truth until live evidence completes. |
| `/papers_manifest.json` | Mirror metadata surface | Manifest must preserve source repository, source ref, source path, target repository, target path, display policy, mirror protocol, workflow, generated UTC, count, aliases, and entries. |
| `/upload`, `/uploads` | Not a Site execution surface | Must not imply user-upload intake exists on Site. Use unsupported-path copy unless a governed intake route is later built. |
| `/incoming` | Not a Site ingestion queue | Must not imply pending submissions are accepted. Use unsupported-path copy unless a governed intake route is later built. |
| `/tools` | Documentation or navigation only | Must not imply browser tools can mutate repositories or execute governed actions. |
| `/data` | Documentation or static data only | Must not imply live data intake, private storage, or authority-bearing records. |
| `/actions` | Documentation only | Must not imply GitHub Actions can be triggered by public visitors. |
| `/docs` | Documentation surface | Must preserve proof-source boundaries and avoid activation overclaims. |
| `/api` | Unsupported unless explicitly implemented | Must not imply a live API exists on Site. |
| `/.well-known` | Manifest/declaration surface only if present | Must separate boundary declarations from runtime enforcement. |

## Unsupported-Path Copy

Use this copy pattern for public paths that are visible or guessed but not implemented:

```text
This Site path is not an execution, upload, ingestion, or authority surface.

StegVerse Site publishes public documentation, mirror metadata, and evidence packets. Source authority remains with the upstream repository named in the relevant manifest or receipt.

If this path becomes active later, it must be backed by commit-time admissibility evidence, receipt capture, and handoff documentation before being described as live.
```

## Mirror-Surface Copy

Use this copy pattern for public mirror pages before live evidence is complete:

```text
This page is a public mirror/display surface.

Publisher remains the source of truth. Live mirror activation is not complete until Publisher dry-run evidence, live dispatch evidence, Site workflow evidence, alias verification, Site evidence-packet completion, Site live-state completion, Publisher receipt update, Publisher verification tracker activation, and Publisher activation-status update are all captured.
```

## Governance Requirements

A public path may be called active only if all applicable requirements are satisfied:

```text
- source repository named
- source path named
- target repository named
- target path named
- authority class declared
- source-of-truth boundary declared
- activation evidence captured
- receipt or manifest present
- stale or pending evidence clearly marked
- unsupported execution claims absent
```

## Done Definition

This packet is done when:

```text
1. The high-interest path classes are explicitly listed.
2. Each path class has a required public behavior.
3. Unsupported path copy is available.
4. Mirror-surface pending-evidence copy is available.
5. The Site handoff references this packet.
6. Future sessions can continue public path hardening without prior chat context.
```

## Verification

Manual verification for this packet:

```text
- Confirm this file exists at docs/SITE_PUBLIC_PATH_AND_INGESTION_SURFACE_HARDENING.md.
- Confirm docs/SITE_MIRROR_HANDOFF.md lists this file under Built Files.
- Confirm docs/SITE_MIRROR_HANDOFF.md includes this file under Public Path And Ingestion Surface Packet.
- Confirm no claim in this packet marks the Site mirror as activated.
```

## Current Status

```text
Status: documentation packet added
Activation impact: no activation claim
Remaining work: wire public unsupported-path pages or redirects, then capture live mirror evidence
```

## Archive Readiness

This packet contains the current public path and ingestion-surface hardening rules needed for future sessions. The prior chat thread is not required to continue this work once the Site handoff references this file.
