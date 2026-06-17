# StegVerse Build Hub Repo Install Matrix

Generated: 2026-06-17

## Purpose

This matrix records the first P0 verification pass for the StegVerse Build Hub.

It checks actual installed files in the three connector-confirmed repos:

1. `StegVerse-Labs/Site`
2. `StegVerse-Labs/admissibility-wiki`
3. `StegVerse-Labs/StegCore`

This file separates confirmed installed files from missing files and prevents future build chats from treating unverified prior discussion as installed repo state.

## Assumptions

1. `StegVerse-Labs/Site`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-Labs/StegCore` are the current P0 anchor repos.
2. A file is marked **installed** only if it was fetched successfully from GitHub during this verification pass.
3. A file is marked **missing** only if GitHub returned `404 Not Found` for the exact checked path.
4. A file is marked **needs follow-up** when it exists but does not fully satisfy the next required build role.
5. This matrix does not verify repos outside the three anchor repos.
6. This matrix does not claim workflow success, deployment success, or runtime activation unless such evidence is separately fetched.

## Done Looks Like

This matrix is done when:

1. Each checked path has a clear status.
2. Missing paths are listed with next action.
3. Installed paths are not re-created redundantly.
4. The next build step is specific enough to execute without restarting planning.
5. Public mirror files remain clearly separated from proof authority files.

## Status Legend

| Status | Meaning |
|---|---|
| installed | File exists in GitHub at the checked path |
| missing | Exact checked path returned not found |
| needs follow-up | File exists, but additional alignment or companion file is needed |
| verified boundary | File includes or supports required authority-boundary language |
| do not duplicate | File exists; do not create a redundant replacement |
| unknown | Not checked in this pass |

## Repo: `StegVerse-Labs/Site`

| Path | Status | Verification Result | Next Action |
|---|---|---|---|
| `README.md` | installed / verified boundary | README defines Site as public mirror only and states Site must never become the authority for receipts, transitions, or accreditation. | Do not duplicate; preserve boundary language. |
| `data/formalism-tests/transition-proof-surface.json` | installed / verified boundary | JSON includes `authority_boundary`, `site_role: public_mirror`, and `source_authority: formalism-tests`. | Keep as historical/current transition proof-surface mirror data. |
| `admissibility-wiki.html` | installed / verified boundary | Bridge page exists and states Site is public mirror; wiki is vocabulary/explanation layer; formalism-tests remains proof authority. | Do not duplicate; continue to use as public bridge. |
| `data/formalism-tests/current-admissibility-status.json` | installed / verified boundary | Current status JSON exists and separates Site, admissibility-wiki, and formalism-tests roles. | Keep as current public status artifact; preserve non-claims. |
| `docs/build-hub/REPO_INSTALL_MATRIX.md` | missing before this build | Exact path returned not found before creation. | Installed by this build step. |

## Repo: `StegVerse-Labs/admissibility-wiki`

| Path | Status | Verification Result | Next Action |
|---|---|---|---|
| `README.md` | installed | README establishes the wiki as a public vocabulary layer and Docusaurus-ready knowledge base. | Preserve; no replacement needed now. |
| `docs/proof-path/minimal-public-proof-path.md` | installed | Minimal proof path exists with required artifacts and reviewer success criteria. | Extend later only if adding concrete examples. |
| `docs/stegverse/current-status.md` | missing | Exact path returned not found. | Create as a wiki-side current-status explanation page. |
| `docs/stegverse/page-governance-template.md` | missing | Exact path returned not found. | Create as a governance template requiring proposal, decision, replay, reconstruction, and authority-boundary links. |

## Repo: `StegVerse-Labs/StegCore`

| Path | Status | Verification Result | Next Action |
|---|---|---|---|
| `README.md` | installed / verified boundary | README states StegCore consumes verified continuity output and is not the continuity truth system. | Preserve; no replacement needed now. |
| `meta/provider_status.json` | installed / verified boundary | Provider status artifact exists and says it does not replace decisions, continuity receipts, consent, or authority policy. | Preserve; use as downstream provider signal only. |
| `docs/DECISION_MODEL.md` | installed | Decision model exists and defines allow / deny / defer semantics and stable reason codes. | Preserve; consider adding REFUSE / ESCALATE mapping later if StegCore must align with admissibility-wiki outcomes. |
| `docs/ACTIVATION_CHECKLIST.md` | missing | Exact path returned not found. | Create StegCore activation checklist before claiming repo activation. |

## Confirmed Installed Files

| Repo | Path |
|---|---|
| `StegVerse-Labs/Site` | `README.md` |
| `StegVerse-Labs/Site` | `data/formalism-tests/transition-proof-surface.json` |
| `StegVerse-Labs/Site` | `admissibility-wiki.html` |
| `StegVerse-Labs/Site` | `data/formalism-tests/current-admissibility-status.json` |
| `StegVerse-Labs/admissibility-wiki` | `README.md` |
| `StegVerse-Labs/admissibility-wiki` | `docs/proof-path/minimal-public-proof-path.md` |
| `StegVerse-Labs/StegCore` | `README.md` |
| `StegVerse-Labs/StegCore` | `meta/provider_status.json` |
| `StegVerse-Labs/StegCore` | `docs/DECISION_MODEL.md` |

## Confirmed Missing Files

| Repo | Path | Priority | Reason |
|---|---|---:|---|
| `StegVerse-Labs/Site` | `docs/build-hub/REPO_INSTALL_MATRIX.md` | P0 | Build Hub needed an installed coordination artifact; installed by this build. |
| `StegVerse-Labs/admissibility-wiki` | `docs/stegverse/current-status.md` | P1 | Wiki needs human-readable status explanation matching Site JSON. |
| `StegVerse-Labs/admissibility-wiki` | `docs/stegverse/page-governance-template.md` | P1 | Wiki needs a reusable governance template for pages and proof-path explanations. |
| `StegVerse-Labs/StegCore` | `docs/ACTIVATION_CHECKLIST.md` | P1 | StegCore needs activation gates before activation can be claimed. |

## Boundary Findings

The Site repo is currently aligned with the required public mirror boundary.

Key confirmed boundary posture:

```text
Site publishes receipts.
Site does not generate receipts.
Site must never become the authority for receipts, transitions, or accreditation.
```

The current Site status JSON also preserves the role split:

```text
Site = public mirror
admissibility-wiki = vocabulary authority
Data-Continuation/formalism-tests = proof/test authority
```

The StegCore repo also preserves a clean boundary:

```text
StegCore consumes verified continuity output.
StegCore is not the continuity truth system.
Provider status does not replace decisions, receipts, consent, or authority policy.
```

## Immediate Build Queue From This Matrix

### P0 — Install This Matrix

Status: complete in this build.

Installed path:

```text
docs/build-hub/REPO_INSTALL_MATRIX.md
```

Target repo:

```text
StegVerse-Labs/Site
```

Reason:

The Site repo is the public mirror and coordination surface. This matrix is operational documentation and does not claim proof authority.

### P1 — Add Missing Wiki Current Status Page

Create:

```text
docs/stegverse/current-status.md
```

Target repo:

```text
StegVerse-Labs/admissibility-wiki
```

Required content:

- current workstream status
- role split
- public Site status link
- proof authority boundary
- non-claims
- next actions

### P1 — Add Missing Wiki Page Governance Template

Create:

```text
docs/stegverse/page-governance-template.md
```

Target repo:

```text
StegVerse-Labs/admissibility-wiki
```

Required content:

- proposal block
- decision block
- authority class
- policy reference
- receipt/replay links
- reconstruction links
- non-claims
- review posture
- stale-status handling

### P1 — Add Missing StegCore Activation Checklist

Create:

```text
docs/ACTIVATION_CHECKLIST.md
```

Target repo:

```text
StegVerse-Labs/StegCore
```

Required content:

- activation assumptions
- activation gates
- continuity input boundary
- consent boundary
- authority policy boundary
- provider status boundary
- test requirements
- done criteria
- non-claims

## Do Not Rebuild These In This Pass

The following files already exist and should not be overwritten unless a later task specifically requires a targeted update:

```text
StegVerse-Labs/Site/README.md
StegVerse-Labs/Site/admissibility-wiki.html
StegVerse-Labs/Site/data/formalism-tests/current-admissibility-status.json
StegVerse-Labs/Site/data/formalism-tests/transition-proof-surface.json
StegVerse-Labs/admissibility-wiki/README.md
StegVerse-Labs/admissibility-wiki/docs/proof-path/minimal-public-proof-path.md
StegVerse-Labs/StegCore/README.md
StegVerse-Labs/StegCore/meta/provider_status.json
StegVerse-Labs/StegCore/docs/DECISION_MODEL.md
```

## Verification Steps

To verify this matrix:

1. Open `StegVerse-Labs/Site`.
2. Confirm `docs/build-hub/REPO_INSTALL_MATRIX.md` exists.
3. Confirm the matrix lists only files actually checked in this pass.
4. Confirm missing paths are not claimed as installed.
5. Confirm Site remains public mirror only.
6. Confirm proof authority remains outside Site.
7. Confirm the next build task is one of the three P1 missing files.

## Next Concrete File To Build

Build this full drop-in-ready file next:

```text
docs/stegverse/current-status.md
```

Target repo:

```text
StegVerse-Labs/admissibility-wiki
```

Reason:

It is the smallest missing wiki-side page that aligns the installed Site current-status JSON with the private vocabulary/proof-path documentation layer.
