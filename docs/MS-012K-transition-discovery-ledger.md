# MS-012K Transition Discovery Ledger

## Purpose

MS-012K turns real repo outcomes into transition-table discovery evidence.

It records:

```text
observed path
event type
tool invoked
transition element matched
action class unlocked
authority level used
route/result
receipt path
receipt hash
human approval required?
sandbox required?
new transition candidate?
```

## Why this matters

Transition elements should not be added by assertion alone. They should emerge from repeated observed outcomes, receipts, and boundary checks.

## Run

```text
python tools/transition_discovery_ledger.py \
  --policy data/transition-table/transition-discovery-policy-v1.json
```

## Safety

```text
Evidence only.
No workflow changes.
No authority expansion.
No deletion.
No installation.
```
