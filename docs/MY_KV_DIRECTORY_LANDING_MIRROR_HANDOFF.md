# My KV Directory Landing Mirror Handoff

Repository: `StegVerse-Labs/Site`  
Issue: `#582`  
Branch: `feature/my-kv-directory-landing-582`  
State: SOURCE_MERGED_VALIDATED / PUBLIC_ROUTE_READBACK_PENDING  
Authority effect: NONE  
Activation effect: false

## Purpose

Make `My KV` the user-facing landing surface for Personal KnowledgeVault continuity domains while preserving KnowledgeVault as the canonical storage and schema authority.

The Site surface projects canonical KV directory metadata only:

```text
My KV
 -> continuity-domain directory links
 -> directory page
 -> canonical read-only KV directory bridge
 -> file listing / file-open handoff
```

## Required landing domains

Initial user-facing domains:

- Pictures & Media
- Music
- Email
- Finance
- Assets
- Liabilities
- Personal Information
- Records
- Projects
- Research
- Archive

The displayed domain name is a user-facing label. The underlying canonical path must come from a bounded directory registry or canonical bridge response; Site may not invent provider or storage authority.

## Direct-source population contract

Directory contents are populated through the upstream canonical direct-source ingress contract:

`StegVerse-Labs/continuity-vault-kit/KV_DIRECT_SOURCE_INGRESS_MIRROR_HANDOFF.md`.

The Site surface may request a direct-source connection through `StegVerseKVDirectSourceBridge`, but reusable credentials must be resolved in SKAP Vault and never returned to or persisted by Site.

Canonical flow:

```text
My KV directory
 -> Connect / refresh direct source
 -> owner-authorized direct provider route
 -> SKAP Vault credential resolution
 -> READ_ONLY minimum-necessary provider session
 -> canonical KV ingress/admission
 -> directory readback
```

No aggregator or intermediary may silently be presented as the direct authoritative source.

## Directory-page contract

A directory link opens a dedicated page with:

- canonical directory label;
- canonical KV path;
- read-only file/folder listing;
- file metadata sufficient for navigation;
- fail-closed state if the canonical directory bridge is absent;
- no secret-bearing values;
- no upload/delete/move/rename authority in this lane.

A file open action must be delegated to the canonical KV file/open bridge. Site does not fetch private file contents from public source state.

## Finance dependency

Canonical finance authority remains upstream in:

- `StegVerse-Labs/continuity-vault-kit/KV_PERSONAL_FINANCE_MIRROR_HANDOFF.md`;
- `schemas/kv-personal-finance-snapshot.schema.json`;
- canonical private finance directory/index added by that lane.

The Site finance card must not duplicate or redefine the finance schema.

## Invariants

1. My KV is a projection of the user's private KnowledgeVault.
2. Directory existence is not fabricated.
3. File listings are never fabricated.
4. Missing canonical bridge fails closed.
5. Site does not persist private directory contents.
6. Public repository source contains only labels, canonical path contracts, synthetic fixtures, and UI logic.
7. Finance display is read-only in this lane.
8. Existing onboarding and Personal Information controls remain available.
9. Directory links must be mobile-first and keyboard accessible.
10. Source readiness does not prove connected-KV directory readback.
11. Direct-source population requires SKAP-backed owner authorization.
12. Site never receives or persists reusable provider credentials.
13. Source connection defaults to READ_ONLY / minimum-necessary access.
14. Unsupported or unavailable direct source fails closed.

## Implemented source

- `docs/MY_KV_DIRECTORY_LANDING_MIRROR_HANDOFF.md`
- `my-kv.html`
- `my-kv-directory.html`
- `assets/my-kv-directory.js`
- `tests/my-kv-directory.test.cjs`
- `scripts/check_my_kv_directory.py`
- `.github/workflows/my-kv-directory.yml`
- `SITE_MIRROR_HANDOFF.md`

## Completion gates

- finance upstream path contract reconciled;
- directory landing visible on My KV;
- directory page resolves only admitted registry entries;
- absent directory bridge fails closed;
- file-open requires canonical bridge;
- deterministic tests pass;
- static checker passes;
- existing My KV personal-info tests remain green;
- exact-head hosted validation observed;
- PR merged;
- public route re-observed separately.

## Current boundary

Issue #582 source is merged and validated. Public route/private-KV connected readback remains a separate runtime verification gate.

No private KV files are exposed by this source work.
No storage mutation, credential, provider, finance-execution, payment, trading, or transfer authority is granted.
