# Transition Discovery Public Surface

Assumptions:
- Repository: `StegVerse-Labs/Site`
- Target branch: `main`
- The existing transition pages should become public views of one canonical discovery model.
- The release state is downstream of transition discovery state, not independently hardcoded per page.

Done means:
- `transition-table.html`, `transition-milestones.html`, `transition-development-status.html`, `transition-release-snapshot.html`, `transition-release-index.html`, `transition-verification-guide.html`, and `transition-replay-packet.html` all render from `assets/transition-discovery-state.js`.
- T13 and T14 are consistently shown as `RECEIPT_BACKED` under MS-012.
- MS-012F is consistently shown as the current frontier.
- The pages present the exploration as Map, Ledger, Frontier, Frozen Knowledge Boundary, Discovery-State Index, Verification Procedure, and Replayable Evidence.
- Stale milestone drift is prevented by the canonical state file.

Install:
1. Upload all files into the matching paths in `StegVerse-Labs/Site`.
2. Commit to `main`.
3. Open `https://stegverse-labs.github.io/Site/transition-table.html`.
4. Verify that the page renders "Current Release: MS-012" and "Current Frontier: MS-012F".
5. Open each transition page and confirm the content changes by view while the state remains consistent.

Files:
- `assets/transition-discovery-state.js`
- `assets/transition-page-renderer.js`
- `transition-table.html`
- `transition-milestones.html`
- `transition-development-status.html`
- `transition-release-snapshot.html`
- `transition-release-index.html`
- `transition-verification-guide.html`
- `transition-replay-packet.html`
