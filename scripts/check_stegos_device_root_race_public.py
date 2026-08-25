#!/usr/bin/env python3
"""Observe the deployed StegOS device-continuity root-race repair.

Credential-free validation only. This script does not activate a Node, mutate
browser state, or grant any StegOS authority.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request

EXPECTED_BLOB = "3927e2aa650f3267c53af73f3ef8bea2379805b9"
DEFAULT_URL = "https://stegverse.org/stegos-bootstrap/device-local-autostart.js"
MARKERS = (
    "function addMetaIfAbsent(db, key, value)",
    'objectStore(META_STORE).add({ key: key, value: value })',
    'req.error.name === "ConstraintError"',
    "then(function (wonCreate)",
    "if (!wonCreate)",
    "device continuity root race lost without persisted winner",
)


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def validate(data: bytes) -> list[str]:
    failures: list[str] = []
    observed = git_blob_sha(data)
    if observed != EXPECTED_BLOB:
        failures.append(f"public blob mismatch: {observed} != {EXPECTED_BLOB}")
    text = data.decode("utf-8")
    for marker in MARKERS:
        if marker not in text:
            failures.append(f"missing deployed repair marker: {marker}")
    try:
        losing = text.split("then(function (wonCreate)", 1)[1].split("return appendReceipt(db", 1)[0]
    except IndexError:
        failures.append("unable to isolate losing-context branch")
    else:
        if "appendReceipt" in losing:
            failures.append("losing-context branch may append a root-establishment receipt")
        if "getMeta(db, DEVICE_ROOT_KEY)" not in losing:
            failures.append("losing-context branch does not reuse persisted winner")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()
    request = urllib.request.Request(
        args.url,
        headers={"User-Agent": "StegVerse-Site-Deployment-Observer/1.0"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            status = int(response.status)
            body = response.read()
    except Exception as exc:
        print(f"STEGOS_DEVICE_ROOT_RACE_PUBLIC_OBSERVATION_FAIL\nfetch failed: {exc}")
        return 1
    failures = [] if status == 200 else [f"HTTP status {status} != 200"]
    failures.extend(validate(body))
    if failures:
        print("STEGOS_DEVICE_ROOT_RACE_PUBLIC_OBSERVATION_FAIL")
        for failure in failures:
            print(failure)
        return 1
    print("STEGOS_DEVICE_ROOT_RACE_PUBLIC_OBSERVATION_PASS")
    print(f"URL={args.url}")
    print(f"GIT_BLOB={git_blob_sha(body)}")
    print("AUTHORITY_EFFECT=NONE")
    print("PHYSICAL_NODE_ACTIVATION_CLAIMED=false")
    print("NETWORK_ACTIVATION_CLAIMED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
