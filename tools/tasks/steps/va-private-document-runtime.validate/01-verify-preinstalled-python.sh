set -euo pipefail
python3 --version
python3 - <<'PY'
import sys
assert sys.version_info >= (3, 11), sys.version
print('VA_PRIVATE_DOCUMENT_FIXTURE_PYTHON=PASS')
PY
