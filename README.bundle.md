# Site Dynamic Transition Pages Schema Fix Bundle

## Assumptions

1. This bundle targets StegVerse-Labs/Site.
2. The current transition-proof-surface.json is schema v2.
3. The dynamic renderer must support v2 and v4 data.
4. transition-table-classes.json should be preserved but annotated as legacy Stage 5 class data under Stage 10 Site context.
5. No workflow files are included.

## Done Definition

1. transition-proof-surface.json includes pages, stages, release, and artifact_paths.
2. transition-page-renderer.js normalizes legacy v2 proof-surface JSON.
3. transition-table-classes.json is preserved and annotated for Stage 10 context.
4. All six dynamic page shells remain dynamic.
5. Local verification passes.
