# MS-012K.1 Site Path Category Authority Extension

## Purpose

The previous transition authority map governed bundle lifecycle paths, but it did not explicitly classify repo construction categories such as:

```text
scripts/
snippets/
root-level files
public/
assets/
js/
tools/
data/
docs/
legacy/
```

MS-012K.1 extends the live authority map so these categories are no longer implicit.

## Key distinction

```text
path category is not the same thing as authority level
```

A path may be public-facing, executable, authority-bearing, legacy, report-only, or ordinary data. Each requires different transition-table authority.

## Added action classes

```text
modify_public_research_surface
modify_executable_support
```

## Added transition elements

```text
TE-011-public-research-surface-update
TE-012-executable-support-surface-update
TE-013-content-fragment-update
TE-014-legacy-surface-touch
TE-015-root-surface-touch
```

## Run audit

```text
python tools/site_path_category_authority_audit.py \
  --authority-map data/transition-table/transition-element-action-authority-map-v1.json \
  --out-dir transition_authority_reports
```

## Safety

```text
No workflow changes.
No authority expansion by execution.
No deletion.
No automatic privileged execution.
```
