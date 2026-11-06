set -euo pipefail
ROOT="."
cd "$ROOT"
python3 scripts/check_gp10_workspace.py
echo 'GP10_STATIC_VALIDATION=PASS'
echo 'GP10_EXECUTION_AUTHORITY=NONE'
echo 'GP10_CUSTODY_AUTHORITY=NONE'
