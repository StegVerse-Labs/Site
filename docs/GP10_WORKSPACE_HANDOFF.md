# GP10 Temporary Workspace Handoff

Status: INSTALLED_UNLINKED
Updated: 2026-07-21
Source repository: `StegVerse-Labs/GP10`
Site route: `gp10-workspace.html`

## Purpose

Provide a tomorrow-ready, browser-local GP10 intake and commercial-posture workspace while evaluation continues before a distinct domain is purchased.

## Installed files

- `gp10-workspace.html`
- `assets/gp10-workspace.js`
- `scripts/check_gp10_workspace.py`

## Isolation

The page is intentionally not linked from Site navigation, the homepage, other HTML pages, or XML indexes. It includes `noindex`, `nofollow`, and `noarchive`. This is obscurity and search guidance, not authentication.

## Behavior

- captures candidate identity, lineage, grade, tier, evidence references, unresolved conditions, and stop-work conditions;
- captures bounded economics and operating metrics;
- optionally evaluates locally entered threshold values;
- returns `PROCEED`, `DISCOVERY_ONLY`, `COST_PLUS`, `RE_SCOPE`, or `REJECT` using fail-closed ordering;
- stores up to 50 records in browser local storage;
- supports JSON copy and export;
- emits `BROWSER_LOCAL_UNCUSTODIED` and `execution_authority: false` in every record.

## Authority boundary

The Site page is a temporary user interface. It does not establish condition, fitment, safety, compliance, pricing validity, profitability, threshold approval, pilot approval, custody, or execution authority.

## Domain migration trigger

A distinct domain is justified only after actual use demonstrates value and the intended service scope is known. Migration should add authentication, durable persistence, governed repository or Master-Records ingestion, privacy terms, monitoring, and explicit service ownership. The temporary page must not become a competing source of truth.

## Verification

Run:

```bash
python scripts/check_gp10_workspace.py
```

The checker fails if required authority markers are absent or if Site HTML/XML surfaces link the temporary page.