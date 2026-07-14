#!/usr/bin/env python3
"""Adversarial regression tests for the fail-closed Site activation ledger."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "SITE_ACTIVATION_LEDGER.json"
VALIDATOR = ROOT / "scripts" / "check_site_activation_ledger.py"

spec = importlib.util.spec_from_file_location("site_activation_ledger_validator", VALIDATOR)
if spec is None or spec.loader is None:
    raise SystemExit("site_activation_ledger_tests:validator_import_failed")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def expect_failure(base: dict[str, Any], label: str, mutate: Callable[[dict[str, Any]], None]) -> None:
    candidate = copy.deepcopy(base)
    mutate(candidate)
    try:
        module.validate_ledger(candidate)
    except module.ActivationLedgerError:
        return
    raise AssertionError(f"mutation unexpectedly passed: {label}")


def main() -> None:
    base = json.loads(LEDGER.read_text(encoding="utf-8"))
    module.validate_ledger(base)

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("activate", lambda d: d.__setitem__("activation_status", "ACTIVE")),
        ("enable_transport", lambda d: d.__setitem__("live_transport_enabled", True)),
        ("grant_authority", lambda d: d.__setitem__("authority_granted", True)),
        ("record_custody", lambda d: d.__setitem__("custody_recorded", True)),
        ("authorize_release", lambda d: d.__setitem__("release_authorized", True)),
        (
            "configure_live_api",
            lambda d: d["gates"]["same_origin_authenticated_deployment"].__setitem__(
                "usage_api_base", "https://example.invalid"
            ),
        ),
        (
            "expose_browser_secret",
            lambda d: d["gates"]["same_origin_authenticated_deployment"].__setitem__(
                "browser_secret_surface_allowed", True
            ),
        ),
        (
            "equate_local_persistence_with_custody",
            lambda d: d["gates"]["master_records_authenticated_custody"].__setitem__(
                "local_persistence_is_custody", True
            ),
        ),
        (
            "drop_same_run_requirement",
            lambda d: d["gates"]["site_same_run_artifact_set"].__setitem__(
                "same_run_required", False
            ),
        ),
        (
            "weaken_reconstructability",
            lambda d: d["gates"]["reconstructability"].__setitem__(
                "required_result", "PARTIAL"
            ),
        ),
        (
            "self_authorize_all_verified",
            lambda d: [gate.__setitem__("status", "VERIFIED") for gate in d["gates"].values()],
        ),
    ]

    for label, mutate in mutations:
        expect_failure(base, label, mutate)

    print(f"site_activation_ledger_tests:PASS:{len(mutations)}_mutations_rejected")


if __name__ == "__main__":
    main()
