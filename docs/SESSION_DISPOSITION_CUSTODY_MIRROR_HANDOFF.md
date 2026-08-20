# Session Disposition Custody Mirror Handoff

## Goal

Define and validate the exact bounded packet Site may submit to the canonical `master-records/orchestration` custody lane for session-disposition receipts, without claiming that custody, reconstruction, publication, release, activation, or any ChatGPT UI archive action has occurred.

```text
goal_id: SOR-C-SESSION-DISPOSITION-CUSTODY-001
parent_goal: SESSION-ORCHESTRATION-ACTIVATION-0001
owner: StegVerse-Labs/Site issue #119
repository: StegVerse-Labs/Site
branch: main
state: SOURCE_PACKET_INTERFACE_INSTALLED_VALIDATION_PENDING
master_records_goal: MR-SESSION-DISPOSITION-CUSTODY-001
credential_authority: TV/TVC
```

## Installed Site surfaces

```text
schemas/session-disposition-custody-packet.schema.json
data/session-custody-outbox/SESSION-ORCHESTRATION-DESIGN-SUPERSEDED-2026-08-07.custody.json
scripts/check_session_disposition_custody_packet.py
tests/test_session_disposition_custody_packet.py
```

Commits:

```text
schema: 788a24e648c0e6620a0319cd113d2826bf067c78
packet: e4b6b5a6b28533bcd9e05d1dfb3c2dd5c43a5dd6
validator: c218ec6cebc25cc4f517be344181ed921a7ad1a9
tests: 468a16563b848c52142f4c5b193f6c7a60448835
```

The first packet is bound to admitted receipt:

`data/session-disposition-receipts/SESSION-ORCHESTRATION-DESIGN-SUPERSEDED-2026-08-07.receipt.json`

and preserves its receipt SHA-256, evidence/session/task identifiers, baseline registry commit, before hash, after hash, and `SUPERSEDED` disposition.

## Master Records counterpart

The canonical target repository now contains:

```text
docs/SESSION_DISPOSITION_CUSTODY_MIRROR_HANDOFF.md
scripts/check_session_disposition_custody_intake.py
data/session-disposition-custody-intake.example.json
tests/test_session_disposition_custody_intake.py
```

Master Records intake interface commits:

```text
handoff creation: cb05d208b1d081eb3907fd7afc2be9c2e0f75f0a
validator: 0f481263f72a3e7dfa0c97c9f5a21e4a3c94c987
bounded example: 752f71749df49a981fdb41dbfcf852298cd95aee
tests: 9accc88bc13d276c3e3929c79598d6992acd1745
handoff state update: ddb53c47baeb645a4107fb8f6108eaeeeeebccb9
```

A valid Master Records intake returns `PENDING_PERSISTENT_SERVICE_EVIDENCE`; packet validation alone can never set `custody_established` or `reconstruction_verified` true.

## Required terminal return evidence

Before issue #119 may satisfy the custody gate, the canonical persistent-service lane must directly prove all of:

1. accepted packet/source receipt identity;
2. custody write receipt;
3. exact payload readback;
4. distinct post-restart service instance;
5. post-restart exact readback;
6. reconstruction receipt;
7. matching source/readback/reconstruction hashes.

Only then may Master Records emit a sanitized immutable return receipt for Site import.

## Current blockers

`docs/HIL_MASTER_RECORDS_MIRROR_HANDOFF.md` currently records the canonical service lane as awaiting authorized endpoint/token bindings and live persistent-service evidence. This custody-interface work does not bypass or weaken that blocker.

## Collision and authority boundaries

- issue #119 remains SOR-C owner;
- `docs/HIL_MASTER_RECORDS_MIRROR_HANDOFF.md` remains persistent-service authority;
- no second custody service may be created;
- endpoint/token values must not be committed;
- packet readiness is not custody establishment;
- custody is not publication, release, activation, or UI archive authority;
- downstream Publisher/admissibility/Guardian projection remains blocked by the parent activation and custody gates.

## Remaining exact work

1. Validate both deterministic test suites through the strongest credential-clean available source path.
2. Observe authorized canonical Master Records service bindings.
3. Execute one bounded custody/write/readback/restart/reconstruction cycle.
4. Persist sanitized return evidence.
5. Import and verify that return in Site issue #119.
6. Reassess parent gate #9; gate #4 remains independently machine-observed and must not be fabricated.
