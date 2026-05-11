# MS-012K.2 Site Construction Plane Discovery Report

## Purpose

MS-012K.2 audits recent Site construction activity against the path-category authority map from MS-012K.1.

It answers:

```text
Which repo construction paths were touched?
Which path category owns each path?
Was the activity routine, conditional, sandbox-required, human-approval-required, unmapped, or forbidden?
```

## Inputs

```text
data/transition-table/transition-element-action-authority-map-v1.json
ingestion_reports/
sandbox_reports/
transition_authority_reports/
transition_discovery_reports/
```

## Outputs

```text
transition_discovery_reports/site-construction-plane-discovery-report.json
transition_discovery_reports/site-construction-plane-discovery-report.md
transition_discovery_reports/site-construction-path-inventory.json
transition_discovery_reports/site-construction-path-inventory.md
```

## Run

```text
python tools/site_construction_plane_discovery.py \
  --policy data/transition-table/site-construction-plane-discovery-policy-v1.json
```

## Safety

```text
Evidence only.
No workflow changes.
No authority expansion.
No deletion.
No installation.
```
