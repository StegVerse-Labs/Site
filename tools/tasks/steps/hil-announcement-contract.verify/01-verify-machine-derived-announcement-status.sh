python scripts/derive_hil_announcement_status.py --check
python scripts/test_hil_announcement_status.py
python - <<'PY'
import json
from pathlib import Path
from scripts.stegverse_jsonschema import Draft202012Validator, FormatChecker

status = json.loads(Path('data/hil-announcement-status.json').read_text(encoding='utf-8'))
schema = json.loads(Path('data/schemas/hil-announcement-status.schema.json').read_text(encoding='utf-8'))
errors = sorted(
    Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(status),
    key=lambda error: list(error.path),
)
if errors:
    raise SystemExit('\n'.join(error.message for error in errors))
print('HIL_ANNOUNCEMENT_STATUS_SCHEMA=PASS')
PY
