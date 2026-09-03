# Current News Releases Mirror Handoff

## Source of truth

This is the bounded continuation record for StegVerse-Labs/Site issue #967. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`.

## Goal

Create a first-class **Current News Releases** public surface on StegVerse.org for timely StegVerse LLC statements tied to current developments, with newest releases shown first and older releases preserved at stable canonical URLs.

## Current implementation

Branch: `claim/site-current-news-releases-967`

Planned public routes:

- `news-releases.html`
- `news-releases/ai-is-becoming-infrastructure-sovereignty-must-go-further.html`

The inaugural release is dated 2026-09-03 and is titled:

**AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model.**

It uses South Korea's "AI for All" initiative as an external convergence indicator and distinguishes national/model sovereignty from StegVerse's entity-, credential-, data-, action-, transition-, evidence-, and economics-level architecture.

## Ordering contract

The landing page is reverse chronological by machine-readable publication date. New releases prepend. Existing canonical release URLs remain stable.

## Classification boundary

Current News Releases is distinct from:

- Papers
- Thought Experiments
- runtime evidence
- product releases
- activation receipts

A Site news release is a company/public communication surface. It does not establish execution, activation, custody, certification, admissibility, or release authority.

## Source references

Primary:
https://www.msit.go.kr/eng/bbs/view.do?bbsSeqNo=42&mId=4&mPid=2&nttSeqNo=1285&sCode=eng

Secondary:
https://www.techspot.com/news/113664-south-korea-giving-entire-population-free-access-ai.html

## Remaining work

1. Run deterministic validation.
2. Run Site claim/orchestration validation on the pull request.
3. Merge only if required gates pass.
4. Verify the exact public StegVerse.org routes after deployment.
5. Use the canonical StegVerse.org statement URL for LinkedIn.
6. Evaluate downstream reference propagation to GCAT-BCAT-Engine/Publisher, admissibility-wiki, and stegguardian-wiki without inferring publication authority.

## Release posture

No tag or product release is implied. Public deployment must be observed separately from repository merge.

## Archive readiness

This handoff, issue #967, task record, claim fragment, implementation branch, and repository history preserve continuation state without requiring conversation context.
