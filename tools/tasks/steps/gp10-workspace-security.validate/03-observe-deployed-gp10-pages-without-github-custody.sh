set -euo pipefail
ROOT="."
cd "$ROOT"
mkdir -p /tmp/gp10-validation
python3 scripts/check_gp10_workspace_deployment.py \
  --commit "$SOURCE_SHA" \
  --run-id "${GITHUB_RUN_ID}" \
  --attempts 18 \
  --delay-seconds 20 \
  --output /tmp/gp10-validation/gp10-workspace-deployment-receipt.json
python3 - <<'PY'
import json
from pathlib import Path
receipt = json.loads(Path('/tmp/gp10-validation/gp10-workspace-deployment-receipt.json').read_text(encoding='utf-8'))
if receipt.get('result') != 'PASS':
    raise SystemExit('GP10 deployed-page observation did not pass')
if receipt.get('execution_authority') not in (False, None):
    raise SystemExit('GP10 deployment observation attempted authority escalation')
print('GP10_DEPLOYMENT_OBSERVATION=PASS')
print('GP10_RECEIPT_CUSTODY=NONE')
PY
