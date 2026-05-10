# MS-012G Human Design Authority + GCAT/BCAT Execution Gate

This milestone formalizes the missing rule:

```text
The human in the loop is not a fallback.
The human in the loop is the authority boundary for design intent.
```

## Execution order

```text
Trigger requests evaluation.
GCAT/BCAT evaluates admissibility.
The system proposes bounded transitions.
The human approves design direction at capability thresholds.
Only then does execution occur.
```

## Non-authority rules

```text
trigger ≠ authority
schedule ≠ permission
queue item ≠ permission
failed bundle ≠ repair authority
next action ≠ execution authority
```

## Decision classes

```text
implementation_detail
design_decision
authority_expansion
recursive_automation
workflow_mutation
milestone_promotion
```

Only `implementation_detail` can be allowed without human approval, and only when the GCAT/BCAT metrics are bounded, receipt-producing, observable, and non-recursive.

## Usage

```text
python tools/gcat_bcat_execution_gate.py \
  --request data/gcat-bcat/execution-request-template-v1.json \
  --policy data/gates/human-design-authority-policy-v1.json \
  --out-dir execution_gate_reports
```

## Declared task

```text
python tools/headless_cmd_runner.py \
  --task data/headless-tasks/execution-gate-check-v1.json \
  --arg request=data/gcat-bcat/execution-request-template-v1.json
```
