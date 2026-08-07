#!/usr/bin/env python3
"""Compare governed session-orchestration authority across canonical repository handoffs."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "data" / "session-orchestration-cross-repository-targets.json"
REPORT = ROOT / "data" / "session-orchestration-cross-repository.report.json"

Fetcher = Callable[[dict[str, Any], str], dict[str, str]]


def load_targets(path: Path = TARGETS) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("targets"), list):
        raise ValueError("cross-repository target manifest must contain targets[]")
    return value


def local_file(path_value: str) -> dict[str, str]:
    path = ROOT / path_value
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(path_value)
    content = path.read_text(encoding="utf-8")
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return {"sha": f"sha256:{digest}", "content": content}


def github_file(repository: str, path_value: str, branch: str) -> dict[str, str]:
    encoded_path = quote(path_value, safe="/")
    encoded_ref = quote(branch, safe="")
    url = f"https://api.github.com/repos/{repository}/contents/{encoded_path}?ref={encoded_ref}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "stegverse-session-orchestration",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"GitHub fetch failed for {repository}:{path_value}@{branch}: {exc}") from exc
    if payload.get("type") != "file" or not isinstance(payload.get("content"), str):
        raise RuntimeError(f"GitHub path is not a file: {repository}:{path_value}@{branch}")
    try:
        content = base64.b64decode(payload["content"]).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        raise RuntimeError(f"GitHub file content is not UTF-8 text: {repository}:{path_value}") from exc
    sha = payload.get("sha")
    if not isinstance(sha, str) or not sha:
        raise RuntimeError(f"GitHub file response lacks blob sha: {repository}:{path_value}")
    return {"sha": sha, "content": content}


def default_fetcher(target: dict[str, Any], path_value: str) -> dict[str, str]:
    mode = target.get("mode")
    if mode == "local":
        return local_file(path_value)
    if mode == "github":
        return github_file(str(target.get("repository")), path_value, str(target.get("branch")))
    raise RuntimeError(f"unsupported target mode: {mode}")


def evaluate(config: dict[str, Any], fetcher: Fetcher = default_fetcher) -> dict[str, Any]:
    failures: list[str] = []
    target_rows: list[dict[str, Any]] = []
    targets = config.get("targets", [])
    delegated_dependencies = config.get("delegated_dependencies", [])
    if len(targets) < 2:
        failures.append("INSUFFICIENT_TARGETS: comparison requires at least two governed repositories")
    if not isinstance(delegated_dependencies, list):
        failures.append("INVALID_DELEGATED_DEPENDENCIES: delegated_dependencies must be a list")
        delegated_dependencies = []

    seen_repositories: set[str] = set()
    active_scopes: dict[str, list[tuple[str, str]]] = {}

    for index, target in enumerate(targets):
        if not isinstance(target, dict):
            failures.append(f"INVALID_TARGET: targets[{index}] must be an object")
            continue
        repository = str(target.get("repository", ""))
        branch = str(target.get("branch", ""))
        handoff = str(target.get("canonical_handoff", ""))
        successor = str(target.get("successor_execution_source", ""))
        claim_scope = str(target.get("claim_scope", ""))
        owner = str(target.get("canonical_owner", ""))
        task_id = str(target.get("task_id", ""))
        row_failures: list[str] = []

        required_scalars = {
            "repository": repository,
            "branch": branch,
            "canonical_handoff": handoff,
            "successor_execution_source": successor,
            "claim_scope": claim_scope,
            "canonical_owner": owner,
            "task_id": task_id,
        }
        for field, value in required_scalars.items():
            if not value:
                row_failures.append(f"MISSING_AUTHORITY_FIELD:{field}")

        if repository in seen_repositories:
            row_failures.append("AMBIGUOUS_REPOSITORY_TARGET:duplicate repository entry")
        seen_repositories.add(repository)

        observed_handoff_sha: str | None = None
        successor_sha: str | None = None
        matched_markers: list[str] = []
        missing_markers: list[str] = []

        if handoff:
            try:
                handoff_value = fetcher(target, handoff)
                observed_handoff_sha = handoff_value["sha"]
                content = handoff_value["content"]
                expected_sha = target.get("expected_handoff_sha")
                if expected_sha and observed_handoff_sha != expected_sha:
                    row_failures.append(
                        f"STALE_HANDOFF:expected {expected_sha} observed {observed_handoff_sha}"
                    )
                markers = target.get("required_markers", [])
                if not isinstance(markers, list) or not markers:
                    row_failures.append("MISSING_AUTHORITY:required_markers must be non-empty")
                    markers = []
                for marker in markers:
                    if isinstance(marker, str) and marker and marker in content:
                        matched_markers.append(marker)
                    else:
                        missing_markers.append(str(marker))
                if missing_markers:
                    row_failures.append(
                        "MISSING_AUTHORITY:handoff markers absent: " + "; ".join(missing_markers)
                    )
            except Exception as exc:  # fail closed on all retrieval/parsing boundaries
                row_failures.append(f"MISSING_HANDOFF_OR_BRANCH:{exc}")

        if successor:
            try:
                successor_value = fetcher(target, successor)
                successor_sha = successor_value["sha"]
            except Exception as exc:  # fail closed on unresolved continuation source
                row_failures.append(f"UNRESOLVED_SUCCESSOR:{exc}")

        claim_active = target.get("claim_active") is True
        if claim_active and claim_scope:
            active_scopes.setdefault(claim_scope, []).append((repository, owner))

        target_rows.append(
            {
                "repository": repository,
                "branch": branch,
                "canonical_handoff": handoff,
                "expected_handoff_sha": target.get("expected_handoff_sha"),
                "observed_handoff_sha": observed_handoff_sha,
                "required_markers": target.get("required_markers", []),
                "matched_markers": matched_markers,
                "missing_markers": missing_markers,
                "task_id": task_id,
                "claim_scope": claim_scope,
                "claim_active": claim_active,
                "canonical_owner": owner,
                "successor_execution_source": successor,
                "successor_sha": successor_sha,
                "status": "FAIL" if row_failures else "PASS",
                "failures": row_failures,
            }
        )
        failures.extend(f"{repository}:{value}" for value in row_failures)

    collisions: list[dict[str, Any]] = []
    for scope, owners in sorted(active_scopes.items()):
        unique_owners = sorted(set(owners))
        if len(unique_owners) > 1:
            collision = {
                "claim_scope": scope,
                "owners": [
                    {"repository": repository, "canonical_owner": owner}
                    for repository, owner in unique_owners
                ],
            }
            collisions.append(collision)
            failures.append(
                "CONFLICTING_OWNER:"
                + scope
                + ":"
                + ",".join(f"{repository}={owner}" for repository, owner in unique_owners)
            )

    stale_count = sum(
        1
        for row in target_rows
        if any(str(value).startswith("STALE_HANDOFF") for value in row.get("failures", []))
    )
    missing_authority_count = sum(
        1
        for row in target_rows
        if any("MISSING_AUTHORITY" in str(value) for value in row.get("failures", []))
    )
    unresolved_successor_count = sum(
        1
        for row in target_rows
        if any(str(value).startswith("UNRESOLVED_SUCCESSOR") for value in row.get("failures", []))
    )

    return {
        "schema_version": "1.0.0",
        "state_type": "session_orchestration_cross_repository_report",
        "status": "FAIL" if failures else "PASS",
        "source_targets": "data/session-orchestration-cross-repository-targets.json",
        "policy": config.get("policy", {}),
        "targets": target_rows,
        "delegated_dependencies": delegated_dependencies,
        "owner_collisions": collisions,
        "summary": {
            "target_count": len(target_rows),
            "passing_targets": sum(1 for row in target_rows if row.get("status") == "PASS"),
            "active_claim_scope_count": len(active_scopes),
            "delegated_dependency_count": len(delegated_dependencies),
            "stale_handoff_count": stale_count,
            "missing_authority_count": missing_authority_count,
            "unresolved_successor_count": unresolved_successor_count,
            "owner_collision_count": len(collisions),
        },
        "next_action": (
            "use the verified handoff and owner comparison as bounded succession evidence while preserving delegated dependency boundaries"
            if not failures
            else "review stale, missing, unresolved, or conflicting authority before succession or archival"
        ),
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when live comparison differs from committed report")
    args = parser.parse_args()
    report = evaluate(load_targets())
    rendered = json.dumps(report, indent=2) + "\n"
    if args.check:
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != rendered:
            print("SESSION_CROSS_REPOSITORY_REPORT_STALE")
            return 1
    else:
        REPORT.write_text(rendered, encoding="utf-8")
    print(f"SESSION_CROSS_REPOSITORY_{report['status']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
