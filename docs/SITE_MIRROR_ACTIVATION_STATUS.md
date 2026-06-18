# Site Mirror Activation Status

## Current State

```text
activation_state: ready_for_mirror_verification
repository: StegVerse-Labs/Site
activation_target: Mirror Papers from Publisher
source_target: GCAT-BCAT-Engine/Publisher
```

## What Is Complete

```text
Mirror Papers from Publisher workflow exists
workflow accepts source_repository and source_ref inputs
workflow resolves Publisher defaults
workflow checks Site paper display policy before mirroring
workflow checks out Publisher source repository
workflow verifies Publisher source path
mirror script records source metadata in papers/papers_manifest.json
manifest metadata checker exists
workflow validates manifest metadata before commit
public aliases are regenerated
```

## What Is Not Yet Complete

```text
live Publisher-triggered Site mirror has not been recorded
Site mirror completion receipt has not been captured
public Site aliases have not been verified after live mirror
Publisher verification tracker has not been updated to activated
```

## Activation Boundary

Site mirror activation occurs when:

```text
1. Publisher Dispatch Site Paper Mirror passes with dry_run: false.
2. Site Mirror Papers from Publisher starts from that dispatch.
3. Site mirror workflow completes successfully.
4. papers/papers_manifest.json contains Publisher source repository, source ref, source path, source of truth, target repository, display policy, mirror protocol, workflow, aliases, and entries.
5. public aliases resolve: Papers.html, papers.html, papers/index.html, publisher/papers.html, publisher/papers/index.html.
6. Publisher verification tracker and receipt are updated with the completed live mirror evidence.
```

## Current Site Validation Contract

After mirroring and before commit, Site runs:

```text
python scripts/check_papers_manifest_metadata.py
```

That checker validates:

```text
source_repository
source_ref
source_path
source_of_truth
target_repository
target_path
display_policy
mirror_protocol
workflow
generated_utc
count
aliases
entries
```

## Next Action

```text
Run Publisher Dispatch Site Paper Mirror with dry_run: false after Publisher dry_run: true passes.
```

## Activation Evidence Files

```text
.github/workflows/mirror-papers.yml
scripts/mirror_papers.py
scripts/check_papers_manifest_metadata.py
papers/papers_manifest.json
Papers.html
papers.html
papers/index.html
publisher/papers.html
publisher/papers/index.html
```
