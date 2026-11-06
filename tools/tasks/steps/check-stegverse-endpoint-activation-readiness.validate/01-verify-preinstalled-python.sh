python3 --version
python3 - <<'PY'
import sys
assert sys.version_info >= (3, 11), sys.version
print('ENDPOINT_READINESS_PYTHON=PASS')
PY
