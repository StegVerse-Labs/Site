python3 --version
python3 - <<'PY'
import sys
assert sys.version_info >= (3, 11), sys.version
print('HIL_PROTOCOL_PYTHON=PASS')
PY
