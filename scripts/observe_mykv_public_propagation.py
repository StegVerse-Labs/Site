#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TARGETS = {
    "install_shell": "https://stegverse.org/my-kv-install.html",
    "manifest": "https://stegverse.org/my-kv.webmanifest",
    "node_continuity_loader": "https://stegverse.org/assets/stegverse-node-continuity.js",
}

SHELL_MARKERS = (
    "20260915-unified-mykv-v1",
    "single owner-facing installation surface",
    "automatically establishes or reuses the minimal resident StegOS/Node substrate",
    "report.resident_install_health!=='HEALTHY'",
    "report.node.registered!==true",
    "Installation stopped before KV-host selection.",
    "There is no separate StegOS website or second owner installation step",
)

LOADER_MARKERS = (
    "/assets/stegos-node-idb-schema-compat.js",
    "/stegos-bootstrap/stegos-bootstrap-impl.js",
    "/stegos-bootstrap/device-local-autostart.js?v=20260915-unified-mykv-v1",
    "/assets/stegverse-node-continuity-impl.js",
    "/assets/stegos-resident-health.js?v=20260915-unified-mykv-v1",
)


def fetch(url: str, *, attempt: int) -> tuple[int, bytes, dict[str, str]]:
    separator = "&" if "?" in url else "?"
    target = f"{url}{separator}mykv_proof_attempt={attempt}&ts={int(time.time())}"
    request = urllib.request.Request(
        target,
        headers={
            "Accept": "text/html,application/manifest+json,application/javascript,*/*;q=0.8",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "StegVerse-MyKV-Public-Observer/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return (
            int(response.status),
            response.read(),
            {key.lower(): value for key, value in response.headers.items()},
        )


def validate(bodies: dict[str, bytes]) -> dict[str, bool]:
    shell = bodies["install_shell"].decode("utf-8", "replace")
    loader = bodies["node_continuity_loader"].decode("utf-8", "replace")
    try:
        manifest = json.loads(bodies["manifest"])
    except Exception:
        manifest = {}

    return {
        "shell_required_markers": all(marker in shell for marker in SHELL_MARKERS),
        "manifest_is_object": isinstance(manifest, dict),
        "manifest_standalone_display": manifest.get("display") == "standalone",
        "manifest_standalone_start_url": manifest.get("start_url")
        == "/my-kv-install.html?source=installed",
        "manifest_scope_root": manifest.get("scope") == "/",
        "loader_required_markers": all(marker in loader for marker in LOADER_MARKERS),
    }


def observe(
    output_dir: Path, *, attempts: int = 20, delay_seconds: int = 10
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    last_error = None

    for attempt in range(1, attempts + 1):
        try:
            statuses: dict[str, int] = {}
            bodies: dict[str, bytes] = {}
            headers: dict[str, dict[str, str]] = {}

            for name, url in TARGETS.items():
                code, body, response_headers = fetch(url, attempt=attempt)
                statuses[name] = code
                bodies[name] = body
                headers[name] = response_headers

            checks = validate(bodies)
            passed = all(code == 200 for code in statuses.values()) and all(checks.values())

            receipt = {
                "schema": "stegverse.mykv-public-propagation-proof/v1",
                "goal_task_id": "KV-ICLOUD-AUTOMATED-UPGRADE-001",
                "cosv_id": "40000100100000",
                "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "attempt": attempt,
                "targets": {
                    name: {
                        "url": TARGETS[name],
                        "http_status": statuses[name],
                        "sha256": hashlib.sha256(bodies[name]).hexdigest(),
                    }
                    for name in TARGETS
                },
                "checks": checks,
                "result": "PASS" if passed else "FAIL",
                "authority_effect": False,
                "activation_effect": False,
                "execution_authority": False,
                "github_actions_runtime_authority": False,
            }

            suffixes = {
                "install_shell": "html",
                "manifest": "webmanifest",
                "node_continuity_loader": "js",
            }
            for name, body in bodies.items():
                (output_dir / f"{name}.{suffixes[name]}").write_bytes(body)
                (output_dir / f"{name}-headers.json").write_text(
                    json.dumps(headers[name], indent=2, sort_keys=True) + "\n"
                )

            (output_dir / "receipt.json").write_text(
                json.dumps(receipt, indent=2, sort_keys=True) + "\n"
            )
            if passed:
                return receipt

            last_error = f"public content did not satisfy checks on attempt {attempt}"
        except Exception as exc:
            last_error = repr(exc)

        if attempt < attempts:
            time.sleep(delay_seconds)

    fail = {
        "schema": "stegverse.mykv-public-propagation-proof/v1",
        "goal_task_id": "KV-ICLOUD-AUTOMATED-UPGRADE-001",
        "cosv_id": "40000100100000",
        "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "result": "FAIL",
        "error": last_error,
        "authority_effect": False,
        "activation_effect": False,
        "execution_authority": False,
        "github_actions_runtime_authority": False,
    }
    (output_dir / "receipt.json").write_text(
        json.dumps(fail, indent=2, sort_keys=True) + "\n"
    )
    return fail


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("evidence/mykv-public-propagation"),
    )
    parser.add_argument("--attempts", type=int, default=20)
    parser.add_argument("--delay-seconds", type=int, default=10)
    args = parser.parse_args()

    receipt = observe(
        args.output_dir,
        attempts=args.attempts,
        delay_seconds=args.delay_seconds,
    )
    print("MYKV_PUBLIC_PROPAGATION_" + receipt["result"])
    return 0 if receipt["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
