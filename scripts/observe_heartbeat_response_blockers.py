#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "data" / "heartbeat-response-adapter-targets.json"
REPORT = ROOT / "data" / "heartbeat-response-blocker-observation.json"
API = "https://api.github.com"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def request_json(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "stegverse-heartbeat-blocker-observer/1.0"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=20) as response:
        return response.status, json.load(response)


def observe_target(target):
    org = target["organization"]
    state = target["state"]
    result = {
        "organization": org,
        "configured_state": state,
        "repository": target.get("repository"),
        "release_condition": target.get("release_condition"),
        "observed_state": state,
        "next_action": "retain blocker",
    }
    try:
        if state == "BLOCKED_NO_REPOSITORY":
            status, repos = request_json(f"{API}/orgs/{org}/repos?per_page=1&type=all")
            result["http_status"] = status
            result["repository_count_observed"] = len(repos)
            if repos:
                result["observed_state"] = "REVIEW_REQUIRED_REPOSITORY_AVAILABLE"
                result["candidate_repository"] = repos[0].get("full_name")
                result["next_action"] = "review candidate repository, create/read canonical handoff, and install node only if authority permits"
        elif state == "BLOCKED_CONNECTOR_WRITE_AUTHORITY":
            repo = target["repository"]
            status, metadata = request_json(f"{API}/repos/{repo}")
            permissions = metadata.get("permissions", {})
            result["http_status"] = status
            result["permissions_observed"] = permissions
            if permissions.get("push") is True:
                result["observed_state"] = "REVIEW_REQUIRED_WRITE_AUTHORITY_AVAILABLE"
                result["next_action"] = "read/create canonical handoff and install AaCT-E response node"
            else:
                result["observed_state"] = "BLOCKED_CONNECTOR_WRITE_AUTHORITY"
                result["next_action"] = "GitHub App installation/permission owner must grant repository write scope; observer will detect push=true afterward"
        elif target.get("receipt_mode") == "PRIVATE_RELAY_REQUIRED":
            repo = target["repository"]
            exchange = target["exchange_id"]
            path = f"data/heartbeat-response-receipts/{exchange}.responded.json"
            status, _ = request_json(f"{API}/repos/{repo}/contents/{path}")
            result["http_status"] = status
            result["observed_state"] = "REVIEW_REQUIRED_PRIVATE_RECEIPT_READABLE"
            result["next_action"] = "bind this authenticated read path into the Site collector without exposing credentials"
        else:
            result["observed_state"] = "NOT_A_BLOCKER_TARGET"
            result["next_action"] = "none"
    except HTTPError as exc:
        result["http_status"] = exc.code
        if target.get("receipt_mode") == "PRIVATE_RELAY_REQUIRED":
            result["observed_state"] = "BLOCKED_PRIVATE_RELAY_CREDENTIAL"
            result["next_action"] = "retain local destination receipts; GitHub integration owner must grant Site collector read authority or install an authorized relay"
        elif state == "BLOCKED_CONNECTOR_WRITE_AUTHORITY":
            result["observed_state"] = "BLOCKED_CONNECTOR_WRITE_AUTHORITY"
            result["next_action"] = "GitHub App installation/permission owner must grant repository visibility/write scope"
        else:
            result["observed_state"] = state
    except (URLError, TimeoutError) as exc:
        result["observed_state"] = "RETRY"
        result["error"] = str(exc)
        result["next_action"] = "retry on repository-native schedule"
    return result


def main():
    targets = load_json(TARGETS)["targets"]
    blocker_targets = [t for t in targets if t["state"].startswith("BLOCKED") or t.get("receipt_mode") == "PRIVATE_RELAY_REQUIRED"]
    observations = [observe_target(t) for t in blocker_targets]
    report = {
        "schema_version": "1.0.0",
        "owner": "StegVerse-Labs/Site issue #234",
        "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "observer": ".github/workflows/heartbeat-response-blocker-observer.yml",
        "observations": observations,
        "review_required": [x["organization"] for x in observations if x["observed_state"].startswith("REVIEW_REQUIRED")],
        "blocked": [x["organization"] for x in observations if x["observed_state"].startswith("BLOCKED")],
        "retry": [x["organization"] for x in observations if x["observed_state"] == "RETRY"],
        "authority_rule": "observation can release a blocker into REVIEW_REQUIRED but cannot grant repository mutation, execution, activation, publication, custody, or release authority",
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"HB_BLOCKER_OBSERVER_PASS:targets={len(observations)}:review={len(report['review_required'])}:blocked={len(report['blocked'])}:retry={len(report['retry'])}")


if __name__ == "__main__":
    main()
