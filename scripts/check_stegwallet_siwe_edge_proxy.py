#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKER_DIR = ROOT / "workers" / "stegwallet-siwe-edge"
WORKER = WORKER_DIR / "src" / "index.js"
TEST = WORKER_DIR / "test.mjs"
WRANGLER = WORKER_DIR / "wrangler.siwe.candidate.jsonc"
PACKAGE = WORKER_DIR / "package.json"
STATE = ROOT / "data" / "stegwallet-siwe-edge-deployment.json"


def require(text: str, marker: str, source: str) -> None:
    if marker not in text:
        raise SystemExit(f"STEGWALLET_SIWE_EDGE_FAIL: missing {marker!r} in {source}")


def prohibit(text: str, marker: str, source: str) -> None:
    if marker.lower() in text.lower():
        raise SystemExit(f"STEGWALLET_SIWE_EDGE_FAIL: prohibited {marker!r} in {source}")


def main() -> int:
    worker = WORKER.read_text(encoding="utf-8")
    test = TEST.read_text(encoding="utf-8")
    wrangler = WRANGLER.read_text(encoding="utf-8")
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8"))

    for path, method in (
        ("/api/stegwallet/siwe/health", "GET"),
        ("/api/stegwallet/siwe/challenge", "POST"),
        ("/api/stegwallet/siwe/verify", "POST"),
        ("/api/stegwallet/siwe/session", "GET"),
        ("/api/stegwallet/siwe/logout", "POST"),
    ):
        require(worker, f"'{path}': '{method}'", WORKER.name)

    for marker in (
        "incoming.hostname !== 'stegverse.org'",
        "query_or_fragment_prohibited",
        "method_not_allowed",
        "headers.delete('x-stegwallet-edge-token')",
        "headers.set('x-stegwallet-edge-token', env.SIWE_EDGE_TOKEN)",
        "headers.set('x-forwarded-host', incoming.host)",
        "headers.set('x-forwarded-proto', 'https')",
        "request.headers.get('cf-connecting-ip')",
        "redirect: 'manual'",
        "cache-control",
        "x-stegwallet-edge",
        "transaction_authority: false",
        "execution_authority: false",
        "delegation_authority: false",
        "custody_recorded: false",
    ):
        require(worker, marker, WORKER.name)

    for marker in (
        "client-forgery",
        "x-stegwallet-edge-token",
        "wrongHost.status, 403",
        "unknown.status, 404",
        "method.status, 405",
        "query.status, 400",
        "transaction_authority, false",
        "execution_authority, false",
    ):
        require(test, marker, TEST.name)

    for marker in (
        '"workers_dev": false',
        '"pattern": "stegverse.org/api/stegwallet/siwe/*"',
        '"zone_name": "stegverse.org"',
        '"SIWE_UPSTREAM_ORIGIN": "https://siwe-origin.invalid"',
    ):
        require(wrangler, marker, WRANGLER.name)

    combined = worker + "\n" + test + "\n" + wrangler + "\n" + json.dumps(package)
    for marker in (
        "private_key",
        "seed_phrase",
        "mnemonic",
        "eth_sendTransaction",
        "wallet_switchEthereumChain",
        "wallet_addEthereumChain",
        "eth_requestAccounts",
        "SIWE_EDGE_TOKEN\":",
        "CLOUDFLARE_API_TOKEN\":",
    ):
        prohibit(combined, marker, "SIWE edge package")

    if state["status"] != "AUTHORIZATION_REQUIRED":
        raise SystemExit("STEGWALLET_SIWE_EDGE_FAIL: deployment must remain authorization-required")
    if state["upstream_origin"] is not None or state["upstream_origin_verified"] is not False:
        raise SystemExit("STEGWALLET_SIWE_EDGE_FAIL: no upstream may be preclaimed")
    for field in (
        "edge_secret_provisioned",
        "edge_secret_matches_origin",
        "cloudflare_account_authorized",
        "worker_deployed",
        "route_observed",
        "site_configuration_promoted",
        "wallet_authenticated",
        "transaction_authority",
        "execution_authority",
        "delegation_authority",
        "custody_recorded",
    ):
        if state[field] is not False:
            raise SystemExit(f"STEGWALLET_SIWE_EDGE_FAIL: {field} must be false")
    if not state.get("activation_blockers"):
        raise SystemExit("STEGWALLET_SIWE_EDGE_FAIL: activation blockers required")

    completed = subprocess.run(
        ["node", str(TEST)],
        cwd=WORKER_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0 or "STEGWALLET_SIWE_EDGE_BEHAVIOR_PASS" not in completed.stdout:
        raise SystemExit(f"STEGWALLET_SIWE_EDGE_FAIL: behavior test failed\n{completed.stdout}")

    print("STEGWALLET_SIWE_EDGE_PROXY_PASS")
    print("worker_deployed=false")
    print("edge_secret_embedded=false")
    print("financial_authority=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
