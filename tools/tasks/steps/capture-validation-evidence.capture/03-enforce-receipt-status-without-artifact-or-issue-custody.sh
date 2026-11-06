set -euo pipefail
python3 - <<'PY'
import json
from pathlib import Path
path = Path('reports/validation-execution-receipt.json')
if not path.exists(): raise SystemExit('Missing reports/validation-execution-receipt.json')
receipt = json.loads(path.read_text(encoding='utf-8'))
if receipt['status'] != 'PASS':
    raise SystemExit('Site ST-018 validation did not pass')
print('ST018_VALIDATION=PASS')
print('authority_effect=NONE')
print('custody_effect=NONE')
PY
