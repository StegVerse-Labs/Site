from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "run_sandbox_validation",
    ROOT / "scripts/run_sandbox_validation.py",
)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def test_sandbox_env_removes_parent_github_pr_and_runner_context() -> None:
    parent = {
        "PATH": "/usr/bin",
        "HOME": "/tmp/home",
        "GITHUB_EVENT_NAME": "pull_request",
        "GITHUB_HEAD_REF": "claim/release-example",
        "GITHUB_BASE_REF": "main",
        "GITHUB_SHA": "a" * 40,
        "GITHUB_TOKEN": "forbidden",
        "GITHUB_RUN_ID": "123",
        "ACTIONS_RUNTIME_TOKEN": "forbidden-runtime",
        "RUNNER_OS": "Linux",
        "RUNNER_TEMP": "/tmp/runner",
        "CI": "true",
        "CUSTOM_LOCAL_VALUE": "preserved",
    }
    child = mod.sandbox_env(parent)

    assert child["PATH"] == "/usr/bin"
    assert child["HOME"] == "/tmp/home"
    assert child["CUSTOM_LOCAL_VALUE"] == "preserved"
    assert child["STEGVERSE_SANDBOX_ISOLATION"] == "LOCAL_REPOSITORY_ONLY"
    assert child["STEGVERSE_GITHUB_RUNTIME_AUTHORITY"] == "NONE"
    assert child["STEGVERSE_CREDENTIAL_AUTHORITY"] == "TV/TVC"

    for key in (
        "GITHUB_EVENT_NAME",
        "GITHUB_HEAD_REF",
        "GITHUB_BASE_REF",
        "GITHUB_SHA",
        "GITHUB_TOKEN",
        "GITHUB_RUN_ID",
        "ACTIONS_RUNTIME_TOKEN",
        "RUNNER_OS",
        "RUNNER_TEMP",
        "CI",
    ):
        assert key not in child


def test_sandbox_env_does_not_strip_unrelated_local_environment() -> None:
    child = mod.sandbox_env({"PATH": "/bin", "LOCAL_MODEL_ROOT": "/srv/models"})
    assert child["PATH"] == "/bin"
    assert child["LOCAL_MODEL_ROOT"] == "/srv/models"
