# Build Trajectory Mirror Handoff

## Source of truth

This is the bounded continuation record for the public StegVerse Build Trajectory and weekly accomplishment log in `StegVerse-Labs/Site`. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`.

## Goal

Publish a durable public page that explains why the log exists and prepends concise weekly reports while keeping implementation, validation, release or deployment, runtime proof, and governed activation distinct. A plan, assignment, issue, source merge, CI success, deployment, runtime event, or activation must never be presented as another stage.

## Intended public routes

- `build-trajectory.html` — public explanation and newest-first weekly log.
- `news-releases.html` — stable discovery link under Current News Releases.

## Canonical truth and projection contract

`data/build-trajectory.json` is the only semantic source of truth.

`scripts/render_build_trajectory.py` deterministically projects that record into `build-trajectory.html`. The generated HTML must never be interpreted or edited as an independent report source. `scripts/check_build_trajectory.py` requires exact-byte reconstruction and fails closed on projection drift.

The canonical record owns the evidence-stage definitions, newest-first ordering, incomplete and unproven-claim classifications, append-only corrections, destination-specific remaining work, public/private boundaries, and PR-only publication policy. Broad percentage claims remain excluded unless a stable public denominator and calculation method are added to the schema.

Every evidence citation is pinned to the exact 40-character Git commit whose artifact was inspected and separately records the observed blob SHA. Moving branch references such as `blob/main/...` are forbidden. The URL commit, `source_commit`, artifact path, and blob fingerprint are validated as a single provenance record.

## Implemented on successor branch

- public page: `build-trajectory.html`
- sole canonical report record: `data/build-trajectory.json`
- deterministic renderer: `scripts/render_build_trajectory.py`
- exact-projection and immutable-provenance validator: `scripts/check_build_trajectory.py`
- adversarial incoherency suite: `scripts/test_build_trajectory_contract.py`
- durable task record: `data/tasks/SITE-BUILD-TRAJECTORY-001.json`
- Current News Releases discovery link: `news-releases.html`, reconciled onto the current Hugging Face/NVIDIA analysis → Coherent Life → Entity Economy Volume II → Volume I → South Korea ordering
- canonical bounded validation: `PASS`
- adversarial validation: `PASS` — one baseline plus six rejected incoherency mutations, including a moving-main evidence reference
- evidence availability: `PASS` — all nine cited artifacts resolved at immutable commits on 2026-09-05

Latest bounded implementation head before task/handoff refresh: `4a83ffc57932e025cd1474d750702389bb5d166b`.

Current-main Current News Releases reconciliation: `661121a0602bac899e7d0efbce99017d69a396c1`.

This proves branch implementation and bounded validation. It does not prove merge, deployment, public observation, runtime execution, or activation.

## Current state

`SOURCE_COMPLETE_VALIDATED_AWAITING_MACHINE_ADMISSION`

PR `StegVerse-Labs/Site#989` remains draft. It must not merge while claim `SITE-CURRENT-NEWS-RELEASES-967-20260903` owns `news-releases.html`. The older claim currently covers the conjoined Coherent Life and Entity Economy publication lane and remains non-terminal.

## Validation contract

The bounded checks establish that:

- the discovery link exists and the page explains its purpose;
- entries are newest-first and all five stages remain explicit;
- completed, incomplete, and unproven claims stay separate;
- completion counts reconcile to canonical outcomes;
- HTML exactly reconstructs from JSON;
- corrections remain dated and append-only;
- publication remains PR-only and non-authorizing;
- every evidence URL is HTTPS, GitHub-hosted, immutable-commit-pinned, path-matched, uniquely cited, and paired with a 40-character blob SHA;
- manual projection divergence, direct-publication enablement, duplicate evidence, undeclared stages, invalid corrections, and moving evidence refs are rejected.

Validation does not establish merge, deployment, independent public observation, runtime proof, or governed activation.

## Remaining machine work

1. Release or supersede claim `SITE-CURRENT-NEWS-RELEASES-967-20260903` after its own evidence gate closes.
2. Admit `SITE-BUILD-TRAJECTORY-001` through Site orchestration and add its bounded validator to the normal Site validation sequence.
3. Reconcile `news-releases.html` once more if main changes, then validate and merge PR `#989`.
4. Verify the Pages deployment and independently observe `https://stegverse.org/build-trajectory.html` plus its Current News Releases discovery link.
5. On future Fridays, change only `data/build-trajectory.json`, run the deterministic renderer and validators, and open a PR.
6. Verify new citations at immutable commits before merge; corrections to published history must be appended, not silently rewritten.

## Downstream installation posture

No propagation to `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, or `StegVerse-002/stegguardian-wiki` is required for this Site-only reporting surface. Evaluate those repositories only if they later require explicit awareness, and never create a second semantic report authority there.

## Release posture

No tag or product release is appropriate for this static, unmerged Site publication lane.

## Archive readiness

This handoff and the durable task record are self-contained. No conversation-only information is required to continue.
