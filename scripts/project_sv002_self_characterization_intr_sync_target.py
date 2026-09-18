#!/usr/bin/env python3
"""Project the SV002 self-characterization Node sync target from shared InTr profile evidence.

This is a non-authorizing projection over the already-existing shared Universal
InTr listener. It creates no listener, runtime, route authority, or credential
path. The shared profile must independently advertise both the existing SV002
public-observation route and the self-characterization route before this target
can become conforming.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "scripts" / "project_sv002_intr_sync_target.py"
SPEC = importlib.util.spec_from_file_location("sv002_public_target_projector", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("base_sv002_projector_import_failed")
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)

TARGET_SCHEMA = "stegos.site.sv002_self_characterization_intr_sync_target.v1"
REQUIRED_PROFILE = "SV002:SelfCharacterization"


class ProjectionError(ValueError):
    pass


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ProjectionError(reason)


def project_target(observation: Mapping[str, Any]) -> dict[str, Any]:
    base = BASE.project_target(observation)
    profile = observation.get("profile")
    require(isinstance(profile, Mapping), "profile_object_required")
    schema = profile.get("schema")
    if schema == BASE.UNIVERSAL_PROFILE_SCHEMA:
        profiles = profile.get("profiles")
    else:
        profiles = profile.get("additional_materialization_profiles")
    require(isinstance(profiles, list) and REQUIRED_PROFILE in profiles, "profile_sv002_self_characterization_support_missing")
    return {
        **base,
        "schema": TARGET_SCHEMA,
        "required_profile": REQUIRED_PROFILE,
        "sv002_self_characterization_materialization_profile_observed": True,
        "request_bound_observed": False,
        "intr_materialization_admitted": False,
        "event_ephemeral_runtime_observed": False,
        "workercoordinator_claim_fence_observed": False,
        "principal_experiment_observed": False,
        "governed_return_observed": False,
        "master_records_reconstruction_observed": False,
        "origin_return_observed": False,
        "authority_effect": "NONE_DISCOVERY_ONLY",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("observation", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    value = json.loads(args.observation.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "observation_object_required")
    target = project_target(value)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(target, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(target, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
