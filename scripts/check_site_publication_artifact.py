#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "site-publication-artifact"
CONTRACT = ROOT / "data" / "publication-equivalence-contract.json"
SELECTION = ROOT / "data" / "publication-origin-selection-2026-09-09.json"


def die(message: str) -> None:
    raise SystemExit("SITE_PUBLICATION_ARTIFACT_FAIL: " + message)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "materialize_site_publication_artifact.py"), "--output", "build/site-publication-artifact"], cwd=ROOT, check=True)
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    manifest = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema") != "stegverse.site.static_publication_artifact.v1":
        die("unexpected manifest schema")
    if manifest.get("format") != "STEGVERSE_SITE_STATIC_PUBLICATION_V1":
        die("unexpected artifact format")
    if manifest.get("canonical_public_domain") != "stegverse.org":
        die("canonical public domain mismatch")
    entries = manifest.get("entries") or []
    if manifest.get("entry_count") != len(entries) or not entries:
        die("entry count mismatch or empty artifact")
    seen = set()
    expected_lines = []
    for entry in entries:
        rel = entry.get("path")
        if not isinstance(rel, str) or not rel or rel in seen:
            die("invalid or duplicate path")
        seen.add(rel)
        target = OUT / "public" / rel
        if not target.is_file():
            die(f"artifact file missing: {rel}")
        digest = sha256(target)
        if digest != entry.get("sha256"):
            die(f"artifact digest mismatch: {rel}")
        if target.stat().st_size != entry.get("bytes"):
            die(f"artifact byte count mismatch: {rel}")
        expected_lines.append(f"{digest}  public/{rel}\n")
    if (OUT / "SHA256SUMS").read_text(encoding="utf-8") != "".join(expected_lines):
        die("SHA256SUMS differs from manifest")
    if manifest.get("provider_selected") is not False:
        die("artifact incorrectly claims provider selection")
    if manifest.get("publication_observed") is not False:
        die("artifact incorrectly claims publication")
    if manifest.get("public_content_equivalence_observed") is not False:
        die("artifact incorrectly claims public equivalence")

    policy = contract.get("provider_selection", {})
    if policy.get("hosted_origin_allowed") is not False or policy.get("render_allowed") is not False:
        die("hosted provider or Render is allowed by publication contract")
    obs = contract.get("current_observation", {})
    if obs.get("hosted_origin_selected") is not False or obs.get("non_github_origin_selected") is not False:
        die("publication contract still claims a hosted/non-GitHub origin")
    if obs.get("selected_origin_provider") is not None or obs.get("selected_origin_materialized") is not False:
        die("publication contract still binds a provider origin")
    if obs.get("provider_live_state_observed") is not False or obs.get("provider_build_artifact_entries_observed") is not None:
        die("publication contract still carries hosted-provider live evidence")
    if obs.get("resident_rendezvous_contract_installed") is not True:
        die("resident rendezvous contract is not installed")
    if obs.get("resident_rendezvous_observed") is not False:
        die("resident rendezvous is prematurely claimed")
    if selection.get("selected_origin") is not None or selection.get("selection_state") != "NO_HOSTED_ORIGIN_SELECTED":
        die("origin selection is not provider-neutral/no-hosted")
    if "RENDER" not in selection.get("prohibited_providers_for_this_lane", []):
        die("Render is not explicitly prohibited")
    for key in ("independent_publication_observed", "non_github_publication_observed", "exact_public_content_equivalence_observed", "tls_equivalence_observed"):
        if obs.get(key) is not False:
            die(f"contract prematurely claims observation: {key}")

    print(f"SITE_PUBLICATION_ARTIFACT=PASS entries={len(entries)}")
    print("ARTIFACT_PROVIDER_SELECTED=false")
    print("HOSTED_ORIGIN_SELECTED=false")
    print("RENDER_ALLOWED=false")
    print("RESIDENT_RENDEZVOUS_CONTRACT_INSTALLED=true")
    print("RESIDENT_RENDEZVOUS_OBSERVED=false")
    print("INDEPENDENT_PUBLICATION_OBSERVED=false")
    print("EXACT_PUBLIC_CONTENT_EQUIVALENCE_OBSERVED=false")


if __name__ == "__main__":
    main()
