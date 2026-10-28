python - <<'PY'
import json
import subprocess
from pathlib import Path

root = Path(".")
task_paths = sorted(Path("data/tasks").glob("tidc-source-expansion-*.json"))
validated = 0

for task_path in task_paths:
    task = json.loads(task_path.read_text(encoding="utf-8"))
    task_id = task.get("task_id", "")
    if not task_id.startswith("TIDC-SRC-"):
        continue
    event_id = task_id.removeprefix("TIDC-SRC-")
    record = root / task["task_location"]
    if not record.is_file():
        print(f"TIDC_SOURCE_RECORD=SKIP:{event_id}:record_missing")
        continue
    subprocess.run(
        ["python", "scripts/reconcile_tidc_source_expansion.py", "--check", event_id],
        check=True,
    )
    validated += 1

if validated == 0:
    raise SystemExit("TIDC_SOURCE_RECORD_VALIDATION=FAIL:no_materialized_records")
print(f"TIDC_SOURCE_RECORD_VALIDATION=PASS:validated={validated}")
PY
