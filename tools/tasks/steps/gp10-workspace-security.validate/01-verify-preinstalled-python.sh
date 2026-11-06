set -euo pipefail
python3 --version
python3 - <<'PY'
import sys
assert sys.version_info >= (3, 11), sys.version
print('GP10_PYTHON=PASS')
PY
