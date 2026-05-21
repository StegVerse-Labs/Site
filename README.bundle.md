# Site Dynamic Transition Pages Hotfix Bundle

## Assumptions

1. This bundle targets StegVerse-Labs/Site.
2. The broken transition pages should be dynamic, not hard-coded static status pages.
3. The shared source is data/formalism-tests/transition-proof-surface.json.
4. formalism-tests remains the proof authority.
5. No workflow files are included.

## Done Definition

1. The five listed pages are replaced with dynamic shells.
2. stage10-canonical-release.html is included as a dynamic shell.
3. assets/js/transition-page-renderer.js renders all pages from shared JSON.
4. assets/css/transition-pages.css controls layout.
5. Shared JSON data exists under data/formalism-tests/.
6. Local verification confirms all page shells reference the shared renderer and shared JSON.
