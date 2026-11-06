set -euo pipefail
python3 - <<'PY'
from pathlib import Path
page = Path('Physical-Economics.html').read_text(encoding='utf-8')
client = Path('js/physical-economics-report.js').read_text(encoding='utf-8')
assert 'name="physical-economics-report-endpoint" content=""' in page
assert "PERTINENCE_MATRIX_VERSION='0.1'" in client
assert "excluded_attributes:[]" in client
assert "BACKEND_NOT_CONFIGURED" in client
assert "UNVERIFIED_REPORT" in client
assert "GENERATED_NOT_PUBLICLY_ACTIVATED" in client
assert "VERIFIABLE" in client
assert page.index('physical-economics-report-form') < page.index('physical-economics-report-result')
print('PHYSICAL_ECONOMICS_UI_BACKEND_ENDPOINT=UNCONFIGURED_FAIL_CLOSED')
print('PHYSICAL_ECONOMICS_UI_AUTHORITY_EFFECT=NONE')
print('PHYSICAL_ECONOMICS_UI_ACTIVATION_EFFECT=NONE')
PY
