# Site Traffic and Ingestion Signal

## Purpose

This document records the current GitHub traffic snapshot for `StegVerse-Labs/Site` and defines how to interpret the observed traffic without overstating adoption.

The traffic signal is treated as repository-behavior evidence only. It does not prove user adoption, production activation, or external endorsement.

## Snapshot Source

```text
Source: GitHub repository traffic screenshots supplied by Rigel Randolph
Repository: StegVerse-Labs/Site
Window: last 14 days
Captured context: GitHub mobile traffic view
```

## Snapshot Metrics

```text
Total clones: 6,903
Unique cloners: 1,545
Total views: 2,177
Unique visitors: 3
Referring site: github.com
Referring-site views: 198
Referring-site unique visitors: 2
```

## Popular Content Snapshot

```text
Overview: 420 views, 2 unique visitors
/upload: 243 views, 1 unique visitor
/tree/main: 196 views, 1 unique visitor
/actions: 93 views, 1 unique visitor
/tree/main/incoming: 80 views, 1 unique visitor
/upload/main: 74 views, 1 unique visitor
/upload/main/incoming: 50 views, 1 unique visitor
/tree/main/tools: 42 views, 1 unique visitor
/tree/main/data: 40 views, 1 unique visitor
/upload/main/tools: 37 views, 1 unique visitor
```

## Interpretation

The strongest signal is the difference between clone activity and visible visitor activity.

```text
Clone activity is high.
Visible unique visitor activity is low.
```

This means the repository is currently behaving more like a pulled artifact surface than a human-browsed project page.

Allowed interpretations:

```text
The repository is being cloned or fetched repeatedly.
The clone volume is high enough to justify adding evidence and ingestion documentation.
The traffic pattern is consistent with automation, indexing, scripted fetches, mirrors, or repeated Git access.
The upload, incoming, tools, data, and actions paths are receiving enough attention to deserve explicit public semantics.
```

Non-allowed interpretations:

```text
Do not claim adoption.
Do not claim active user conversion.
Do not claim institutional validation.
Do not claim that every clone represents a human.
Do not claim that traffic alone activates the Site mirror.
```

## Architectural Meaning

For StegVerse, this traffic signal supports a narrow architectural conclusion:

```text
StegVerse-Labs/Site should be treated as a public artifact endpoint and ingestion-facing repository, not only as a static website repository.
```

That conclusion affects the next build layer.

The repository should make the following surfaces legible:

```text
/upload
/upload/main
/upload/main/incoming
/upload/main/tools
/tree/main/incoming
/tree/main/tools
/tree/main/data
/actions
papers
```

Each surface should eventually answer:

```text
What is this path for?
What may appear here?
What must not appear here?
Which repository or workflow is authoritative?
Which receipts prove that a generated artifact is valid?
Which files are public evidence versus operational scaffolding?
```

## Public Path and Ingestion Surface Documentation

The public path and ingestion-surface hardening layer is now documented in:

```text
docs/SITE_PUBLIC_PATHS.md
docs/SITE_INGESTION_SURFACES.md
```

`docs/SITE_PUBLIC_PATHS.md` defines human-readable public semantics for frequently viewed paths.

`docs/SITE_INGESTION_SURFACES.md` defines machine-facing ingestion and evidence semantics for upload, incoming, tools, data, actions, and papers.

## Relationship To Site Mirror Activation

This traffic document does not replace the Site mirror handoff.

The active Site mirror handoff remains:

```text
docs/SITE_MIRROR_HANDOFF.md
```

Current activation state remains controlled by the evidence requirements in that handoff.

The traffic signal only adds supporting context for public path semantics and artifact documentation before or during live verification.

## Recommended Next Build Step

The documentation hardening step named by this traffic snapshot is complete.

Primary next action returns to live mirror verification evidence capture:

```text
1. Publisher dry-run dispatch.
2. Publisher dry-run receipt commit.
3. Publisher live dispatch.
4. Site workflow evidence capture.
5. Public alias verification.
6. Site evidence packet completion.
7. Site live evidence state completion.
8. Publisher receipt, tracker, and activation-status updates.
```

## Done Criteria

This traffic signal is considered documented when:

```text
The traffic snapshot is captured in a checked-in Markdown file.
Allowed and non-allowed interpretations are explicit.
The Site mirror handoff references the traffic signal document.
The public-path and ingestion-surface hardening documents exist.
The document does not claim adoption or activation from traffic alone.
```

## Current Status

```text
Status: documented_snapshot_with_public_path_and_ingestion_surface_hardening
Activation impact: supporting_context_only
Primary next action: live Publisher/Site mirror verification evidence capture
```
