import hashlib
import json
import os
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

targets = {
    "page": "https://stegverse.org/generic-login-test.html",
    "kv_client": "https://stegverse.org/assets/kv-ui/intr-kv-client.js",
}
markers = {
    "page": [
        "Create My KnowledgeVault",
        "Attach Existing KnowledgeVault",
        "Install on This Device",
        "assets/kv-ui/intr-kv-client.js",
        "stegverse.intr.kv-onboarding-transition/v1",
        "production_kv_custody:false",
    ],
    "kv_client": [
        "kv.interlock.request.v1",
        "kv.interlock.response.v1",
        "COMMIT_CANDIDATE",
        "KV_INTR_NOT_PROVISIONED",
        "candidate_only:true",
        "canonical_state_changed:false",
        "SCOPE_EXPANSION_REJECTED",
        "AUTHORITY_BINDING_REJECTED",
    ],
}

def fetch_exact(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "StegVerse-Site-Public-Observer/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        final = urlparse(response.geturl())
        expected = urlparse(url)
        if final.scheme != "https" or final.hostname != expected.hostname or final.path != expected.path:
            raise RuntimeError(f"unexpected final URL for {url}: {response.geturl()}")
        if response.status != 200:
            raise RuntimeError(f"unexpected HTTP status for {url}: {response.status}")
        return response.read().decode("utf-8")

last_error = None
bodies = None
for attempt in range(1, 13):
    try:
        candidate = {name: fetch_exact(url) for name, url in targets.items()}
        missing = {
            name: [marker for marker in markers[name] if marker not in candidate[name]]
            for name in targets
        }
        missing = {name: value for name, value in missing.items() if value}
        if missing:
            raise RuntimeError(f"public marker mismatch: {missing}")
        bodies = candidate
        break
    except Exception as exc:
        last_error = str(exc)
        if attempt < 12:
            time.sleep(10)

if bodies is None:
    raise SystemExit(f"public KV Interlock adapter observation failed: {last_error}")

combined = bodies["page"] + "\n" + bodies["kv_client"]
if "GITHUB_TOKEN" in combined or "TVC_EPHEMERAL_GITHUB_TOKEN" in combined or "document.cookie" in combined:
    raise SystemExit("forbidden authority/credential marker present in public projection")

report = "\n".join([
    "GENERIC_LOGIN_KV_INTERLOCK_PUBLIC_OBSERVATION_PASS",
    "KV_INTERLOCK_REQUEST_SCHEMA_PUBLIC_PASS",
    "KV_INTERLOCK_RESPONSE_SCHEMA_PUBLIC_PASS",
    "KV_INTERLOCK_COMMIT_CANDIDATE_PUBLIC_PASS",
    "KV_INTERLOCK_FAIL_CLOSED_PUBLIC_PASS",
    "PRODUCTION_KV_CUSTODY_CLAIMED=false",
    "PRODUCTION_KV_RUNTIME_ACTIVATION_CLAIMED=false",
    "CREDENTIAL_AUTHORITY=TV/TVC",
    "AUTHORITY_EFFECT=NONE",
]) + "\n"

receipt = {
    "schema": "stegverse.site.generic_login_kv_interlock_public_observation/v1",
    "page_url": targets["page"],
    "kv_client_url": targets["kv_client"],
    "source_sha": os.environ.get("GITHUB_SHA"),
    "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
    "event_name": os.environ.get("GITHUB_EVENT_NAME"),
    "observation_passed": True,
    "request_schema_observed": True,
    "response_schema_observed": True,
    "commit_candidate_observed": True,
    "fail_closed_not_provisioned_observed": True,
    "production_kv_custody_claimed": False,
    "production_kv_runtime_activation_claimed": False,
    "credential_authority": "TV/TVC",
    "credential_material_observed": False,
    "authority_effect": "NONE",
    "page_sha256": hashlib.sha256(bodies["page"].encode("utf-8")).hexdigest(),
    "kv_client_sha256": hashlib.sha256(bodies["kv_client"].encode("utf-8")).hexdigest(),
}

Path("reports").mkdir(exist_ok=True)
Path("reports/generic-login-kv-interlock-public-observation.txt").write_text(report, encoding="utf-8")
Path("reports/generic-login-kv-interlock-public-observation.json").write_text(
    json.dumps(receipt, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(report, end="")
