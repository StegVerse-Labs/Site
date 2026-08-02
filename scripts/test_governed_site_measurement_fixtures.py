#!/usr/bin/env python3
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/governed-site-measurement-event.schema.json").read_text())
VALID = json.loads((ROOT / "tests/governed-site-measurement/valid-events.json").read_text())
REJECTED = json.loads((ROOT / "tests/governed-site-measurement/rejected-events.json").read_text())
validator = Draft202012Validator(SCHEMA)

failures = []
for index, event in enumerate(VALID):
    errors = list(validator.iter_errors(event))
    if errors:
        failures.append(f"valid[{index}] rejected: {errors[0].message}")

for item in REJECTED:
    errors = list(validator.iter_errors(item["event"]))
    if not errors:
        failures.append(f"rejected case accepted: {item['case']}")

if failures:
    raise SystemExit("\n".join(failures))

print(f"GOVERNED_SITE_MEASUREMENT_FIXTURES_PASS valid={len(VALID)} rejected={len(REJECTED)}")
