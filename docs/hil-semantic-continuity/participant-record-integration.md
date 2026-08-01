# HIL Semantic Transformation Receipt Integration

## Goal

Bind semantic-transformation receipts into canonical HIL participant records without altering the source participant submission, granting authority, or conflating semantic analysis with truth determination.

## Owning repository and paths

```text
Repository: StegVerse-Labs/Site
Task state: data/hil-semantic-continuity-task-state.json
Receipt schema: data/schemas/hil-semantic-transformation.schema.json
Source validator: scripts/validate_hil_semantic_transformation.py
Activation receipt: data/hil-semantic-continuity-activation-receipt.json
Integration specification: docs/hil-semantic-continuity/participant-record-integration.md
Future integration fixture: data/fixtures/hil-semantic-transformation/participant-record-with-receipt.json
Future integration validator: scripts/validate_hil_participant_semantic_receipt.py
```

All tasks are repository-owned and `external: false`.

## Canonical relationship

A participant record remains the authoritative source submission record. A semantic-transformation receipt is an immutable linked analysis record.

```text
participant source record
  -> source_record_id
semantic transformation receipt
  -> source_record_id
  -> output_record_id
  -> evidence_refs
  -> authority_effect=false
```

The receipt must never replace, rewrite, summarize over, or become the source record.

## Minimum participant-record extension

```json
{
  "semantic_continuity": {
    "source_record_preserved": true,
    "receipt_refs": [],
    "latest_receipt_state": "NONE|PASS|FAIL|DISPUTED",
    "reconstruction_available": false,
    "authority_effect": false
  }
}
```

## Admission rules

A semantic receipt may be linked only when:

1. `source_record_id` resolves to the exact preserved participant record;
2. `output_record_id` resolves to the transformed record being evaluated;
3. the receipt validates against `data/schemas/hil-semantic-transformation.schema.json`;
4. all evidence references resolve;
5. the source record bytes remain unchanged;
6. motive is not inferred unless separately evidenced and declared;
7. `authority_effect` remains false;
8. disagreement creates a competing receipt or dispute record rather than overwriting the original receipt.

## Anti-halt continuation

The next internal tasks are:

```text
HIL-SC-NEXT-002
Repository: StegVerse-Labs/Site
Location: data/fixtures/hil-semantic-transformation/participant-record-with-receipt.json
Purpose: create a canonical participant record linked to one valid semantic receipt.

HIL-SC-NEXT-003
Repository: StegVerse-Labs/Site
Location: scripts/validate_hil_participant_semantic_receipt.py
Purpose: validate source preservation, receipt linkage, schema posture, evidence references, and authority_effect=false.

HIL-SC-NEXT-004
Repository: StegVerse-Labs/Site
Location: data/fixtures/hil-semantic-transformation/participant-record-dispute.json
Purpose: prove that competing interpretations coexist without source mutation or receipt overwrite.
```

Failure at any step creates a repair task at the exact failing repository path. No unavailable destination or unobserved external status halts this workstream.

## Current posture

```text
foundational semantic-continuity layer: ACTIVE
participant-record integration: STARTED
source mutation authorized: false
truth determination authorized: false
scientific claim authority: false
publication authority: false
```
