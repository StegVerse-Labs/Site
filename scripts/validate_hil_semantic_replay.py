#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'data/fixtures/hil-semantic-transformation/semantic-event-replay-packet.json'


def main() -> int:
    packet = json.loads(PACKET.read_text(encoding='utf-8'))
    records = packet['ordered_records']
    by_kind = {record['kind']: record for record in records}
    failures = []
    required = {'source','output','receipt','event'}
    if set(by_kind) != required:
        failures.append('ordered record kinds differ from required replay chain')
    else:
        receipt = by_kind['receipt']
        event = by_kind['event']
        if event['source_record_id'] != by_kind['source']['id']:
            failures.append('source reference does not resolve')
        if event['output_record_id'] != by_kind['output']['id']:
            failures.append('output reference does not resolve')
        if event['receipt_ref'] != receipt['id']:
            failures.append('receipt reference does not resolve')
        expected = packet['expected_reconstruction']
        if sorted(receipt['transformations']) != sorted(['hypothesis_to_conclusion','confidence_inflation','constraint_removal','campaign_boundary_reduction']):
            failures.append('transformation set drifted')
        if any(record.get('authority_effect') is not False for record in (receipt,event)):
            failures.append('authority effect must remain false')
        if expected['result'] != 'PASS':
            failures.append('expected reconstruction must be PASS')
    result = {'packet_id': packet['packet_id'], 'validation': 'PASS' if not failures else 'FAIL', 'failures': failures, 'authority_effect': False}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1

if __name__ == '__main__':
    raise SystemExit(main())
