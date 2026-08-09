from __future__ import annotations

import json
import pathlib
import urllib.request
from datetime import datetime, timezone

RECEIPT_URL = "https://raw.githubusercontent.com/StegVerse-org/LLM-adapter/main/receipts/math-solver-public-runtime.latest.json"
PUBLIC_PAGE = "https://stegverse-labs.github.io/Site/math-solver/"
STATUS_PATH = pathlib.Path("data/steggate-four-app-status.json")
OBS_PATH = pathlib.Path("data/math-solver-public-activation.latest.json")


def get_json(url: str):
    with urllib.request.urlopen(url, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def get_text(url: str):
    with urllib.request.urlopen(url, timeout=20) as response:
        return response.read().decode("utf-8")


def main() -> int:
    observed_at = datetime.now(timezone.utc).isoformat()
    try:
        receipt = get_json(RECEIPT_URL)
        if receipt.get("state") != "COMPLETE":
            observation = {
                "schema_version": "stegverse.site.math_solver_activation.v1",
                "state": "BLOCKED",
                "observed_at": observed_at,
                "source_receipt_state": receipt.get("state"),
                "source_receipt_observed_at": receipt.get("observed_at"),
                "blocker": receipt.get("blocker"),
                "next_executable_action": "Retry automatically after the LLM-adapter public-runtime receipt becomes COMPLETE.",
                "authority_effect": False,
            }
            OBS_PATH.write_text(json.dumps(observation, indent=2) + "\n")
            print(json.dumps(observation, indent=2))
            return 0

        page = get_text(PUBLIC_PAGE)
        required_markers = [
            "Governed Math Solver",
            "https://stegverse-ecosystem-chat-gateway.onrender.com",
            "/api/math-solver/v1/readiness",
            "/api/math-solver/v1/solve",
            "No local fallback",
        ]
        missing = [marker for marker in required_markers if marker not in page]
        if missing:
            raise RuntimeError("public_site_binding_missing:" + ",".join(missing))

        status = json.loads(STATUS_PATH.read_text())
        math = status["applications"]["math_solver"]
        math["state"] = "PUBLIC_GOVERNED_RUNTIME_VERIFIED"
        for key in math["gates"]:
            math["gates"][key] = True
        math["completed_gates"] = math["total_gates"]
        math["progress_percent"] = 100
        math["blockers"] = []

        completed = sum(app["completed_gates"] for app in status["applications"].values())
        total = sum(app["total_gates"] for app in status["applications"].values())
        functional = sum(1 for app in status["applications"].values() if app["completed_gates"] == app["total_gates"])
        status["aggregate"]["completed_gates"] = completed
        status["aggregate"]["total_gates"] = total
        status["aggregate"]["execution_progress_percent"] = int(round(completed * 100 / total))
        status["aggregate"]["fully_functional_public_apps"] = functional
        status["aggregate"]["goal_complete"] = functional == status["aggregate"]["required_fully_functional_public_apps"]
        status["updated_at"] = observed_at
        STATUS_PATH.write_text(json.dumps(status, indent=2) + "\n")

        observation = {
            "schema_version": "stegverse.site.math_solver_activation.v1",
            "state": "COMPLETE",
            "observed_at": observed_at,
            "source_receipt_observed_at": receipt.get("observed_at"),
            "public_page": PUBLIC_PAGE,
            "checks": {
                "runtime_receipt_complete": True,
                "public_site_reachable": True,
                "public_site_runtime_binding_present": True,
                "public_replay_verified": bool((receipt.get("checks") or {}).get("replay_match", True)),
            },
            "authority_effect": False,
        }
        OBS_PATH.write_text(json.dumps(observation, indent=2) + "\n")
        print(json.dumps(observation, indent=2))
        return 0
    except Exception as exc:
        observation = {
            "schema_version": "stegverse.site.math_solver_activation.v1",
            "state": "BLOCKED",
            "observed_at": observed_at,
            "blocker": {"type": type(exc).__name__, "reason": str(exc)},
            "next_executable_action": "Retry automatically; do not advance execution gates without complete source receipt and public Site binding.",
            "authority_effect": False,
        }
        OBS_PATH.write_text(json.dumps(observation, indent=2) + "\n")
        print(json.dumps(observation, indent=2))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
