# Site Paper Display Policy

## Purpose

This policy governs how `StegVerse-Labs/Site` displays current papers and Publisher case-study surfaces.

The Site is a public display surface. It is not the source of truth for papers, publication status, governance case posture, source posture, receipt posture, or admissibility posture.

## Source of Truth

Current papers and governance case records should be derived from:

```text
GCAT-BCAT-Engine/Publisher
```

The default paper source path is:

```text
papers/
```

The Site mirror target is:

```text
StegVerse-Labs/Site/papers/
```

The public paper display surfaces are:

```text
Papers.html
papers.html
papers/index.html
publisher/papers.html
publisher/papers/index.html
```

## Display Rule

The Site may display papers and case-study links only as mirrored or summarized Publisher-controlled records.

The Site may not strengthen, finalize, or reinterpret Publisher status. If Publisher marks something as draft, unresolved, under review, provisional, or admissibility-limited, Site display must preserve that posture.

## Update Protocol

Use this order for Site paper updates:

```text
1. Update Publisher paper or case source record.
2. Validate Publisher source record.
3. Run or dispatch the Site mirror workflow.
4. Confirm mirrored files update under Site/papers/.
5. Confirm generated public indexes update.
6. Commit or accept the mirror workflow commit.
7. Verify public links resolve.
```

## Mirror Workflow

The Site mirror workflow is:

```text
.github/workflows/mirror-papers.yml
```

The workflow defaults to:

```text
source repository: GCAT-BCAT-Engine/Publisher
source ref: main
source path: papers
target path: papers
```

The workflow may be run manually or on schedule.

## Current Paper Display Requirements

Each public paper listing should preserve at least:

```text
title or filename
relative path
file type
link to mirrored paper asset
generated timestamp or manifest timestamp
Publisher source path
```

## Governance Case Display Requirements

If Site displays governance case studies, it should preserve at least:

```text
case_id
title
case type
evidence posture
admissibility posture
link to Publisher public case page
link or reference to machine-readable Publisher case object
```

## Failure Conditions

Do not treat a Site paper display update as complete if:

```text
Publisher source path is missing
mirror workflow fails
papers_manifest.json is not regenerated
public index files do not update
links point to stale or non-Publisher-controlled copies
Site display omits required posture for governance cases
```

## Done State

A Site paper display update is complete when:

```text
Publisher remains the source of truth
Site mirror workflow succeeds
papers_manifest.json reflects the current mirrored set
Papers.html and papers/index.html render the current mirrored papers
aliases resolve back to the public paper display
commit message or workflow summary identifies Publisher as the source
```
