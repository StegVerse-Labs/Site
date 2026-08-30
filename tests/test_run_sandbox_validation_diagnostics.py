#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "run_sandbox_validation", ROOT / "scripts" / "run_sandbox_validation.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def main() -> int:
    diagnostic = MODULE.failure_diagnostic(
        {
            "id": "validate-application",
            "stdout_tail": "before\nSITE_APPLICATION_CHECK_FAIL: exact-check\nafter",
            "stderr_tail": (
                "Authorization: Bearer super-secret\n"
                "GITHUB_TOKEN=also-secret\n"
                "safe error"
            ),
        }
    )
    assert "ST017_FAILED_COMMAND=validate-application" in diagnostic
    assert "SITE_APPLICATION_CHECK_FAIL: exact-check" in diagnostic
    assert "safe error" in diagnostic
    assert "super-secret" not in diagnostic
    assert "also-secret" not in diagnostic
    assert diagnostic.count("[REDACTED]") == 2
    assert len(MODULE.redact_diagnostic("x" * 6000)) == 5000
    print("ST017_SANDBOX_DIAGNOSTICS_TEST_PASS")
    print("AUTHORITY_EFFECT=NONE")
    print("ACTIVATION_EFFECT=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
