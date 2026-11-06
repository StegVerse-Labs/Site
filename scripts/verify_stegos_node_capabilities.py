#!/usr/bin/env python3
"""Observe exact published bytes only; never register, repair or admit a Node."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PATHS = (
    "stegos-node/capabilities.json",
    "stegos-node/resident-health.schema.json",
    "assets/stegos-resident-health.js",
    "stegos-node/index.html",
)


def observe(base_url, source_root=ROOT, opener=urlopen):
    results = []
    for path in PATHS:
        url = urljoin(base_url.rstrip("/") + "/", path)
        expected = (source_root / path).read_bytes()
        row = {"path": path, "url": url, "expected_sha256": hashlib.sha256(expected).hexdigest(), "match": False}
        try:
            request = Request(url, headers={"Cache-Control": "no-cache", "Accept": "application/json" if path.endswith(".json") else "*/*"})
            with opener(request, timeout=30) as response:
                body = response.read(len(expected) + 1)
                row.update(status=response.status, observed_sha256=hashlib.sha256(body).hexdigest(), observed_bytes=len(body))
                row["match"] = response.status == 200 and response.geturl() == url and body == expected
                if path.endswith(".json"):
                    row["match"] = row["match"] and response.headers.get_content_type() == "application/json"
        except Exception as error:
            row["error"] = str(error)
        results.append(row)
    return {"schema": "stegos.node_discovery_publication_observation.v1", "result": "PASS" if all(row["match"] for row in results) else "FAIL", "authority_effect": "NONE", "node_registration_performed": False, "runtime_health_verified": False, "routes": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="https://stegverse.org/")
    args = parser.parse_args()
    report = observe(args.base_url)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["result"] == "PASS" else 1)
