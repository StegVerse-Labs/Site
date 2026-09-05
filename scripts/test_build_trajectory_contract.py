#!/usr/bin/env python3
"""Adversarial checks for the single-source Build Trajectory contract."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "data/build-trajectory.json",
    "build-trajectory.html",
    "news-releases.html",
    "scripts/render_build_trajectory.py",
    "scripts/check_build_trajectory.py",
)


def prepare() -> Path:
    root = Path(tempfile.mkdtemp(prefix="build-trajectory-contract-"))
    for relative in FILES:
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)
    return root


def run(root: Path, script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(root / script)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def mutate_record(root: Path, callback) -> None:
    path = root / "data/build-trajectory.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    callback(value)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    rendered = run(root, "scripts/render_build_trajectory.py")
    if rendered.returncode != 0:
        raise AssertionError(rendered.stdout + rendered.stderr)


def require_failure(root: Path, label: str) -> None:
    result = run(root, "scripts/check_build_trajectory.py")
    if result.returncode == 0:
        raise AssertionError(f"{label}: invalid state was accepted")


baseline = prepare()
try:
    result = run(baseline, "scripts/check_build_trajectory.py")
    if result.returncode != 0:
        raise AssertionError("baseline failed: " + result.stdout + result.stderr)
finally:
    shutil.rmtree(baseline)

manual_projection = prepare()
try:
    page = manual_projection / "build-trajectory.html"
    page.write_text(page.read_text(encoding="utf-8").replace("Build Trajectory", "Independent Interpretation", 1), encoding="utf-8")
    require_failure(manual_projection, "manual projection divergence")
finally:
    shutil.rmtree(manual_projection)

direct_publication = prepare()
try:
    mutate_record(direct_publication, lambda value: value["publication_policy"].update({"direct_publication_allowed": True}))
    require_failure(direct_publication, "direct publication")
finally:
    shutil.rmtree(direct_publication)

duplicate_evidence = prepare()
try:
    def duplicate(value: dict) -> None:
        evidence = value["reports"][0]["completed_outcomes"][0]["evidence"][0]
        value["reports"][0]["completed_outcomes"][1]["evidence"].append(dict(evidence))
    mutate_record(duplicate_evidence, duplicate)
    require_failure(duplicate_evidence, "duplicate evidence")
finally:
    shutil.rmtree(duplicate_evidence)

unknown_stage = prepare()
try:
    path = unknown_stage / "data/build-trajectory.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    value["reports"][0]["completed_outcomes"][0]["stages"] = ["UNDECLARED_STAGE"]
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    require_failure(unknown_stage, "unknown stage")
finally:
    shutil.rmtree(unknown_stage)

invalid_correction = prepare()
try:
    def correction(value: dict) -> None:
        value["reports"][0]["corrections"].append({
            "corrected_at": "silently",
            "reason": "invalid undated mutation",
            "replacement": "must fail"
        })
    mutate_record(invalid_correction, correction)
    require_failure(invalid_correction, "invalid correction")
finally:
    shutil.rmtree(invalid_correction)

print("PASS: 1 baseline and 5 incoherency mutations handled correctly")
