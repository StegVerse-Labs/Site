python3 --version
python3 - <<'PY'
import sys
assert sys.version_info >= (3, 12), sys.version
print('TVC_RECEIPT_IMPORT_PYTHON=PASS')
PY
