#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/governed-site-measurement-policy.json"
SCHEMA = ROOT / "schemas/governed-site-measurement-event.schema.json"
TASK = ROOT / "data/tasks/SITE-0001-GOVERNED-MEASUREMENT.json"

REQUIRED_PROHIBITED = {
    "name", "email", "phone", "address", "ssn", "ip", "user_id",
    "session_id", "cookie_id", "fingerprint", "question", "message",
    "diagnosis", "condition", "claim", "claim_status", "document",
    "filename", "medical_record", "free_text", "url_query", "referrer_url"
}


def load(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    failures = []
    for path in (POLICY, SCHEMA, TASK):
        if not path.exists():
            failures.append(f"missing:{path.relative_to(ROOT)}")
    if failures:
        print("GOVERNED_SITE_MEASUREMENT: FAIL")
        print("\n".join(failures))
        return 1

    policy = load(POLICY)
    schema = load(SCHEMA)
    task = load(TASK)

    if schema.get("additionalProperties") is not False:
        failures.append("schema must reject unknown fields")
    if schema.get("properties", {}).get("content_recorded", {}).get("const") is not False:
        failures.append("content_recorded must be false")
    missing = REQUIRED_PROHIBITED - set(policy.get("prohibited_fields", []))
    if missing:
        failures.append("missing prohibited fields: " + ",".join(sorted(missing)))
    identity = policy.get("identity_policy", {})
    for key in ("persistent_identity", "cross_site_tracking", "device_fingerprinting", "exact_location", "session_replay"):
        if identity.get(key) is not False:
            failures.append(f"identity policy must disable {key}")
    retention = policy.get("retention", {})
    if retention.get("raw_event_max_seconds", 999999) > 300:
        failures.append("raw event retention exceeds 300 seconds")
    if retention.get("minimum_report_group_size", 0) < 10:
        failures.append("minimum report group size below 10")
    if task.get("external_tasks_allowed") is not False or task.get("external_session_ownership_allowed") is not False:
        failures.append("task must remain repository-machine-owned")

    if failures:
        print("GOVERNED_SITE_MEASUREMENT: FAIL")
        print("\n".join(failures))
        return 1

    print("GOVERNED_SITE_MEASUREMENT: PASS")
    print("state=IMPLEMENTATION_IN_PROGRESS")
    print("activation_effect=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
