# Current News Releases Mirror Handoff

## Source of truth

This is the bounded continuation record for StegVerse-Labs/Site issue #967. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`.

## Goal

Create a first-class **Current News Releases** public surface on StegVerse.org for timely StegVerse LLC statements tied to current developments, with newest releases shown first and older releases preserved at stable canonical URLs.

## Current implementation

Public routes:

- `news-releases.html`
- `news-releases/ai-is-becoming-infrastructure-sovereignty-must-go-further.html`
- homepage discovery via `index.html`

The inaugural release is dated 2026-09-03 and titled **AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model.**

It uses South Korea's "AI for All" initiative as an external convergence indicator and distinguishes national/model sovereignty from StegVerse's entity-, credential-, data-, action-, transition-, evidence-, and economics-level architecture.

## Homepage claim correction — 2026-09-03

The Workspace interoperability claim had retained `index.html` after the Workspace homepage entry had already been integrated. That ownership was narrowed at commit `1d2ab3a0e87f6422bc4278611ace10e198f88418`; Workspace now retains only its actual implementation/runtime paths.

The existing Current News Releases claim then temporarily acquired `index.html` for completion of its already-recorded follow-on work. Homepage discovery was committed at `36d7299b361b60a83c2c8da26d90162aeeef15da`.

Exact-SHA GitHub Pages run `33820111887` completed successfully for that homepage commit. A fresh public HTTP crawler observation immediately afterward still returned the pre-change homepage, so homepage visibility remains `PENDING_FRESH_HTTP_REOBSERVATION`; this stale observation is not treated as contradictory deployment evidence.

The active HIL and Workspace implementation paths remain untouched.

## Ordering contract

The landing page is reverse chronological by machine-readable publication date. New releases prepend. Existing canonical release URLs remain stable.

## Classification boundary

Current News Releases is distinct from Papers, Thought Experiments, runtime evidence, product releases, and activation receipts. A Site news release is a company/public communication surface and does not establish execution, activation, custody, certification, admissibility, or release authority.

## Source references

Primary:
https://www.msit.go.kr/eng/bbs/view.do?bbsSeqNo=42&mId=4&mPid=2&nttSeqNo=1285&sCode=eng

Secondary:
https://www.techspot.com/news/113664-south-korea-giving-entire-population-free-access-ai.html

## Remaining work

1. Obtain one fresh public observation showing the homepage `Current News Releases` link after Pages propagation/cache refresh.
2. Terminalize the Current News Releases claim after that observation.
3. Use the canonical StegVerse.org statement URL for LinkedIn publication.
4. Continue future releases through prepend semantics.
5. Evaluate downstream reference propagation to GCAT-BCAT-Engine/Publisher, admissibility-wiki, and stegguardian-wiki without inferring publication authority.

## Release posture

No tag or product release is implied. Pages deployment is verified for the homepage discovery commit; public HTTP visibility remains separately observed evidence.

## Archive readiness

Repository state is self-contained. No conversation-only information is required to continue.
