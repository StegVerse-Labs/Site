#!/usr/bin/env python3
"""Validate and promote a HIL live-readiness observation without granting authority."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "data" / "hil-observation-promotion-policy.json"
OUT_DIR = ROOT / "data" / "hil-observations"
HEX64 = re.compile(r"^[a-f0-9]{64}$")


def fail(message: str) -> None:
    raise SystemExit(f"HIL observation import failed: {message}")


def canonical_hash(payload: dict) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read valid JSON from {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON root must be an object: {path}")
    return value


def validate_readiness_block(block: object, *, label: str, policy: dict) -> None:
    if not isinstance(block, dict):
        fail(f"{label} must be an object")
    if block.get("state") != "READY":
        fail(f"{label} is not READY")
    if block.get("primary_sha256") != policy["required_primary_sha256"]:
        fail(f"{label} Primary hash mismatch")
    if block.get("prompt_sha256") != policy["required_prompt_sha256"]:
        fail(f"{label} prompt hash mismatch")
    for field in ("execution_authority", "publication_authority", "master_record_append_authority"):
        if block.get(field) is True:
            fail(f"{label} improperly grants {field}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("observation", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    policy = load_json(POLICY_PATH)
    observation = load_json(args.observation)

    if observation.get("schema_version") != policy["accepted_observation_schema"]:
        fail("unsupported observation schema")
    scope = observation.get("observation_scope")
    scope_policy = policy.get("accepted_scopes", {}).get(scope)
    if not isinstance(scope_policy, dict):
        fail(f"unaccepted observation scope: {scope}")
    if observation.get("observed_state") != "CONTROLLED_CYCLE_READY":
        fail("observation did not reach CONTROLLED_CYCLE_READY")
    if observation.get("authority_granted") is not False:
        fail("observation must explicitly grant no authority")
    if observation.get("external_production_deployment_claimed") is True and scope != "AUTHORIZED_EXTERNAL_DEPLOYMENT":
        fail("scope cannot claim external production deployment")
    if observation.get("credential_separation_verified") is not True:
        fail("credential separation was not verified")
    if observation.get("durable_path_reused_across_process_restart") is not True:
        fail("process restart did not reuse the durable path")

    validate_readiness_block(observation.get("intake_before_restart"), label="intake_before_restart", policy=policy)
    validate_readiness_block(observation.get("intake_after_restart"), label="intake_after_restart", policy=policy)
    validate_readiness_block(observation.get("publication_after_restart"), label="publication_after_restart", policy=policy)

    stated_hash = observation.get("observation_sha256")
    if not isinstance(stated_hash, str) or not HEX64.fullmatch(stated_hash):
        fail("invalid observation_sha256")
    unhashed = dict(observation)
    unhashed.pop("observation_sha256", None)
    if canonical_hash(unhashed) != stated_hash:
        fail("observation_sha256 mismatch")

    if scope == "AUTHORIZED_EXTERNAL_DEPLOYMENT":
        missing = [field for field in scope_policy.get("requires", []) if not observation.get(field)]
        if missing:
            fail("external deployment observation missing: " + ", ".join(missing))

    promoted = {
        "schema_version": "HIL-PROMOTED-READINESS-OBSERVATION-v1",
        "promoted_at": datetime.now(timezone.utc).isoformat(),
        "source_schema_version": observation["schema_version"],
        "source_scope": scope,
        "source_observation_sha256": stated_hash,
        "source_commit_sha": observation.get("commit_sha"),
        "source_run_id": observation.get("run_id"),
        "observed_state": observation["observed_state"],
        "established_gates": scope_policy.get("may_establish", []),
        "non_established_gates": scope_policy.get("may_not_establish", []),
        "public_acquisition_authorized": False,
        "publication_authority": False,
        "master_record_append_authority": False,
        "authority_effect": "NONE",
    }
    promoted["promotion_sha256"] = canonical_hash(promoted)

    destination = OUT_DIR / f"{stated_hash}.json"
    print(json.dumps(promoted, indent=2, sort_keys=True))
    if not args.apply:
        print("HIL_OBSERVATION_IMPORT=DRY_RUN")
        return
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        existing = load_json(destination)
        if existing != promoted:
            fail("append-only destination already exists with different content")
        print(f"HIL_OBSERVATION_IMPORT=ALREADY_PRESENT:{destination.relative_to(ROOT)}")
        return
    destination.write_text(json.dumps(promoted, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"HIL_OBSERVATION_IMPORT=APPLIED:{destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
