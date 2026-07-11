#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REPO = "master-records/orchestration"
SOURCE_WORKFLOW = "Runtime Evidence Validation"
ARTIFACT_NAME = "governed-transition-index-export"
INDEX_MEMBER = "reports/governed_transition_index.generated.json"
RECEIPT_MEMBER = "reports/governed_transition_index.export-receipt.json"
IMPORTER = ROOT / "scripts" / "import_governed_transition_index.py"
API_ROOT = "https://api.github.com"


class AcquisitionError(RuntimeError):
    pass


def _request_json(url: str, token: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "StegVerse-Site-artifact-acquisition",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
        raise AcquisitionError(f"GitHub API request failed: {exc}") from exc


def _download(url: str, token: str, destination: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "StegVerse-Site-artifact-acquisition",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            destination.write_bytes(response.read())
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        raise AcquisitionError(f"artifact download failed: {exc}") from exc


def select_run(payload: dict[str, Any]) -> dict[str, Any]:
    for run in payload.get("workflow_runs", []):
        if (
            run.get("name") == SOURCE_WORKFLOW
            and run.get("status") == "completed"
            and run.get("conclusion") == "success"
            and run.get("head_branch") == "main"
        ):
            return run
    raise AcquisitionError("no successful main-branch Runtime Evidence Validation run found")


def select_artifact(payload: dict[str, Any]) -> dict[str, Any]:
    for artifact in payload.get("artifacts", []):
        if artifact.get("name") == ARTIFACT_NAME and artifact.get("expired") is False:
            return artifact
    raise AcquisitionError("required governed-transition-index-export artifact not found")


def safe_extract(archive: Path, destination: Path) -> tuple[Path, Path]:
    with zipfile.ZipFile(archive) as bundle:
        names = set(bundle.namelist())
        missing = [name for name in (INDEX_MEMBER, RECEIPT_MEMBER) if name not in names]
        if missing:
            raise AcquisitionError(f"artifact missing required members: {missing}")
        for member in (INDEX_MEMBER, RECEIPT_MEMBER):
            target = (destination / member).resolve()
            if destination.resolve() not in target.parents:
                raise AcquisitionError("artifact contains unsafe member path")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(bundle.read(member))
    return destination / INDEX_MEMBER, destination / RECEIPT_MEMBER


def main() -> int:
    parser = argparse.ArgumentParser(description="Acquire and import a governed transition index artifact.")
    parser.add_argument("--token-env", default="STEGVERSE_REPO_SYNC_TOKEN")
    parser.add_argument("--run-id", type=int, help="Optional exact successful workflow run ID")
    args = parser.parse_args()

    token = os.environ.get(args.token_env, "").strip()
    if not token:
        print(f"GOVERNED TRANSITION ARTIFACT ACQUISITION: FAIL - {args.token_env} is not configured")
        return 1

    try:
        if args.run_id is None:
            runs = _request_json(
                f"{API_ROOT}/repos/{SOURCE_REPO}/actions/runs?branch=main&status=success&per_page=30",
                token,
            )
            run = select_run(runs)
            run_id = int(run["id"])
        else:
            run_id = args.run_id
            run = _request_json(f"{API_ROOT}/repos/{SOURCE_REPO}/actions/runs/{run_id}", token)
            if not (
                run.get("name") == SOURCE_WORKFLOW
                and run.get("conclusion") == "success"
                and run.get("head_branch") == "main"
            ):
                raise AcquisitionError("specified run does not match the successful main-branch source workflow")

        artifacts = _request_json(
            f"{API_ROOT}/repos/{SOURCE_REPO}/actions/runs/{run_id}/artifacts?per_page=100",
            token,
        )
        artifact = select_artifact(artifacts)

        with tempfile.TemporaryDirectory(prefix="site-governed-transition-") as temp_dir:
            temp = Path(temp_dir)
            archive = temp / "artifact.zip"
            _download(
                f"{API_ROOT}/repos/{SOURCE_REPO}/actions/artifacts/{artifact['id']}/zip",
                token,
                archive,
            )
            index_path, receipt_path = safe_extract(archive, temp / "extracted")
            result = subprocess.run(
                [
                    sys.executable,
                    str(IMPORTER),
                    "--index",
                    str(index_path),
                    "--receipt",
                    str(receipt_path),
                ],
                cwd=ROOT,
                check=False,
            )
            if result.returncode != 0:
                raise AcquisitionError("existing governed transition importer rejected the acquired artifact")

        print(
            "GOVERNED TRANSITION ARTIFACT ACQUISITION: PASS "
            f"(run={run_id}, artifact={artifact['id']})"
        )
        return 0
    except AcquisitionError as exc:
        print(f"GOVERNED TRANSITION ARTIFACT ACQUISITION: FAIL - {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
