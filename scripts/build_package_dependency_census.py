#!/usr/bin/env python3
"""Build a local, registry-free census of package-install dependencies."""
from __future__ import annotations

import argparse
import json
import re
import shlex
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "package-dependency-census.json"

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
TEXT_SUFFIXES = {".yml", ".yaml", ".sh", ".py", ".md", ".txt", ".json", ".toml"}

PIP_RE = re.compile(r"(?:python(?:3)?\s+-m\s+pip|pip3?|uv\s+pip)\s+install\s+(.+)", re.I)
NPM_RE = re.compile(r"\bnpm\s+(install|ci)\b\s*(.*)", re.I)

MANIFESTS = [
    "requirements.txt", "requirements-dev.txt", "pyproject.toml", "setup.py", "setup.cfg",
    "Pipfile", "Pipfile.lock", "package.json", "package-lock.json", "pnpm-lock.yaml",
    "yarn.lock",
]


def iter_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in MANIFESTS:
            yield path


def clean_shell_tail(value: str) -> str:
    for marker in ("&&", "||", ";", "|"):
        if marker in value:
            value = value.split(marker, 1)[0]
    return value.strip().rstrip("\\")


def parse_pip_args(value: str):
    try:
        tokens = shlex.split(clean_shell_tail(value))
    except ValueError:
        tokens = clean_shell_tail(value).split()

    packages, requirement_files, constraints = [], [], []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in {"-r", "--requirement"} and i + 1 < len(tokens):
            requirement_files.append(tokens[i + 1])
            i += 2
            continue
        if token in {"-c", "--constraint"} and i + 1 < len(tokens):
            constraints.append(tokens[i + 1])
            i += 2
            continue
        if token in {"-e", "--editable"} and i + 1 < len(tokens):
            packages.append(tokens[i + 1])
            i += 2
            continue
        if token.startswith("-"):
            i += 1
            continue
        packages.append(token)
        i += 1
    return packages, requirement_files, constraints


def scan():
    records = []
    for path in iter_files():
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        try:
            body = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(body.splitlines(), 1):
            pip_match = PIP_RE.search(line)
            if pip_match:
                packages, requirements, constraints = parse_pip_args(pip_match.group(1))
                records.append({
                    "ecosystem": "python",
                    "path": rel,
                    "line": lineno,
                    "command": line.strip(),
                    "packages": packages,
                    "requirement_files": requirements,
                    "constraint_files": constraints,
                })
            npm_match = NPM_RE.search(line)
            if npm_match:
                tail = clean_shell_tail(npm_match.group(2))
                try:
                    tokens = shlex.split(tail)
                except ValueError:
                    tokens = tail.split()
                packages = [t for t in tokens if t and not t.startswith("-")]
                records.append({
                    "ecosystem": "npm",
                    "path": rel,
                    "line": lineno,
                    "command": line.strip(),
                    "mode": npm_match.group(1).lower(),
                    "packages": packages,
                })
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUT.relative_to(ROOT)))
    args = parser.parse_args()

    records = scan()
    manifests = {
        name: (ROOT / name).exists()
        for name in MANIFESTS
    }
    python_packages = sorted({
        pkg for rec in records if rec["ecosystem"] == "python"
        for pkg in rec.get("packages", [])
        if pkg and "$" not in pkg and not pkg.startswith(".")
    })
    npm_packages = sorted({
        pkg for rec in records if rec["ecosystem"] == "npm"
        for pkg in rec.get("packages", [])
        if pkg and "$" not in pkg and not pkg.startswith(".")
    })
    req_files = sorted({
        req for rec in records if rec["ecosystem"] == "python"
        for req in rec.get("requirement_files", [])
    })

    report = {
        "schema": "stegverse.site.package_dependency_census.v1",
        "goal_id": "SITE-497-THIRD-PARTY-DEPENDENCY-ERADICATION",
        "repository": "StegVerse-Labs/Site",
        "network_contacted": False,
        "manifest_presence": manifests,
        "install_command_count": len(records),
        "python_direct_package_tokens": python_packages,
        "npm_direct_package_tokens": npm_packages,
        "referenced_requirement_files": req_files,
        "install_records": records,
        "assessment": {
            "python_public_registry_independence_proven": False,
            "npm_public_registry_independence_proven": False,
            "exact_hash_pinning_proven": False,
            "offline_clean_install_proven": False,
            "state": "PACKAGE_SUPPLY_INVENTORY_READY",
        },
    }

    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
