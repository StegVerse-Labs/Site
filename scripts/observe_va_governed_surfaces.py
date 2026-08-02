#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/va-claim-assistant/governed-surfaces-deployment.json"
BASE_URL = "https://site.rigelrandolph.workers.dev"
SURFACES = {
    "guide": "va-disability-claim-guide.html",
    "chat": "va-claims-chat.html",
    "capability": "data/va-claim-assistant/chat-capability-state.json",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str) -> tuple[int | None, bytes, str | None]:
    request = urllib.request.Request(url, headers={"User-Agent": "StegVerse-VA-Surface-Observer/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read(), None
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), f"HTTPError:{exc.code}"
    except Exception as exc:  # fail closed and preserve exact error
        return None, b"", f"{type(exc).__name__}:{exc}"


def main() -> int:
    results: dict[str, object] = {}
    blockers: list[str] = []

    for name, relative_path in SURFACES.items():
        repository_path = ROOT / relative_path
        repository_bytes = repository_path.read_bytes()
        url = f"{BASE_URL}/{relative_path}"
        http_status, deployed_bytes, error = fetch(url)
        repository_hash = sha256(repository_bytes)
        deployed_hash = sha256(deployed_bytes) if deployed_bytes else None
        equal = http_status == 200 and deployed_hash == repository_hash
        if http_status != 200:
            blockers.append(f"{name}:http_status_not_200:{http_status}")
        elif not equal:
            blockers.append(f"{name}:deployed_repository_hash_mismatch")
        results[name] = {
            "url": url,
            "repository_path": relative_path,
            "http_status": http_status,
            "error": error,
            "repository_sha256": repository_hash,
            "deployed_sha256": deployed_hash,
            "byte_equal": equal,
        }

    state = "VERIFIED" if not blockers else "BLOCKED"
    body = {
        "schema_version": "1.0.0",
        "observer_id": "SV-VA-GOVERNED-SURFACES-DEPLOYMENT-001",
        "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "state": state,
        "base_url": BASE_URL,
        "surfaces": results,
        "blockers": blockers,
        "private_document_upload_enabled": False,
        "automated_filing_enabled": False,
        "authority_effect": False,
        "activation_effect": False,
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    body["receipt_sha256"] = sha256(canonical)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(body, indent=2, sort_keys=True))
    return 0 if state == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
