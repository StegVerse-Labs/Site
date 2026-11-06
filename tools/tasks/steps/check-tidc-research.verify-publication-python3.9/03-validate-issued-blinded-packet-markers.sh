set -euo pipefail
packet='data/tidc/blinded-coding/BCP-2026-07-27-01.md'
manifest='data/tidc/blinded-coding/BCP-2026-07-27-01.manifest.json'
return_schema='data/tidc/blinded-coding/blinded-coder-return.schema.json'
receipt_schema='data/tidc/blinded-coding/blinded-return-receipt.schema.json'
test -s "$packet"
test -s "$manifest"
test -s "$return_schema"
test -s "$receipt_schema"
grep -F 'BCP-2026-07-27-01' "$packet"
grep -F 'ISSUED_FOR_BLINDED_SECOND_CODING' "$manifest"
grep -F 'exactly 10 records' "$packet"
grep -F 'RECEIVED_NOT_ADJUDICATED' "$receipt_schema"
