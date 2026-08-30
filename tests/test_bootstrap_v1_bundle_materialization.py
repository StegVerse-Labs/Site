from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "stegos-node/bootstrap-bundle-materialization-v1.html"
SCHEMA = ROOT / "stegos-node/bootstrap-bundle-v1.schema.json"
SW = ROOT / "stegos-node/service-worker.js"
HANDOFF = ROOT / "docs/BOOTSTRAP_V1_BUNDLE_MATERIALIZATION_MIRROR_HANDOFF.md"
CLAIM = ROOT / "data/session-work-claims.d/site-bootstrap-v1-bundle-materialization-20260829.json"

COMPONENTS = [
    "stegverse.sdk",
    "stegverse.stegcore",
    "stegverse.core-lite",
    "stegverse.master-records",
]


def test_receiver_requires_exact_bundle_and_component_order():
    html = PAGE.read_text()
    assert 'stegverse.bootstrap.bundle/v1' in html
    assert 'bundle_version!=="1.0.0-rc.1"' in html
    assert 'var COMPONENTS=["stegverse.sdk","stegverse.stegcore","stegverse.core-lite","stegverse.master-records"]' in html
    assert 'canon(b.component_order)!==canon(COMPONENTS)' in html
    assert 'b.packages.length!==4' in html
    assert 'item.component_id!==component' in html


def test_receiver_verifies_bundle_candidate_catalog_and_package_identities():
    html = PAGE.read_text()
    assert 'sha(without(b,"bundle_identity"))' in html
    assert 'bundle identity mismatch' in html
    assert 'sha(without(c,"candidate_identity"))' in html
    assert 'candidate identity mismatch' in html
    assert 'candidate/catalog binding mismatch' in html
    assert 'sha(c.components)' in html
    assert 'catalog identity-set digest mismatch' in html
    assert 'file digest mismatch' in html
    assert 'source bundle identity mismatch' in html
    assert 'p.source_identity!==identity' in html


def test_receiver_appends_four_package_receipts_plus_aggregate_and_replays():
    html = PAGE.read_text()
    assert 'stegos.web_source_package_materialization_receipt.v1' in html
    assert 'stegos.web_bootstrap_bundle_materialization_receipt.v1' in html
    assert 'packageEntries.push(entry)' in html
    assert 'component_count:4' in html
    assert 'all_components_materialized:true' in html
    assert 'return replay(continuity.rows)' in html
    assert 'stegverse.device-node-bootstrap-bundle-evidence/v1' in html
    assert 'state:"MATERIALIZED_UNADMITTED"' in html
    assert 'new_node_identity_minted:false' in html
    assert 'execution_authority:"NONE"' in html
    assert 'release_activated:false' in html
    assert 'publication_performed:false' in html


def test_receiver_reuses_existing_continuity_and_does_not_auto_register():
    html = PAGE.read_text()
    assert 'CONTINUITY_DB="stegos-web-bootstrap-v1"' in html
    assert 'LIVE_EXISTING_WEB_BOOTSTRAP' in html
    assert 'VERIFIED_IMPORTED_WEB_BOOTSTRAP_EVIDENCE' in html
    assert 'stegos.web_device_node_binding_receipt.v1' in html
    assert 'registerDevice(' not in html
    assert 'new_node_identity_minted:false' in html


def test_receiver_is_platform_and_credential_neutral():
    html = PAGE.read_text()
    assert 'github_platform_required:false' in html
    assert 'specific_external_platform_required:false' in html
    assert 'credential_material_observed:false' in html
    assert 'GITHUB_TOKEN' not in html
    assert 'github.com/' not in html
    assert 'release_activated:true' not in html
    assert 'execution_authority:"ALLOW"' not in html


def test_bundle_schema_fixes_order_and_zero_authority():
    schema = json.loads(SCHEMA.read_text())
    props = schema["properties"]
    assert props["schema"]["const"] == "stegverse.bootstrap.bundle/v1"
    assert props["bundle_version"]["const"] == "1.0.0-rc.1"
    assert props["component_order"]["const"] == COMPONENTS
    assert props["component_count"]["const"] == 4
    assert props["github_platform_required"]["const"] is False
    assert props["specific_external_platform_required"]["const"] is False
    assert props["network_locator_required"]["const"] is False
    assert props["transport_implementation_required"]["const"] is False
    assert props["credential_required"]["const"] is False
    assert props["bundle_integrity_confers_execution_authority"]["const"] is False
    assert props["release_activated"]["const"] is False
    assert props["publication_performed"]["const"] is False
    assert props["execution_authority"]["const"] == "NONE"


def test_offline_shell_caches_bundle_receiver_without_changing_validated_lineage():
    sw = SW.read_text()
    assert 'stegos-node-shell-v8-source-package-bootstrap-v1' in sw
    assert './bootstrap-bundle-materialization-v1.html' in sw
    assert './bootstrap-bundle-v1.schema.json' in sw


def test_handoff_and_claim_preserve_release_boundary():
    handoff = HANDOFF.read_text()
    claim = json.loads(CLAIM.read_text())["claims"][0]
    assert 'bundle_state: MATERIALIZED_UNADMITTED' in handoff
    assert 'execution_authority: NONE' in handoff
    assert 'release_activated: false' in handoff
    assert 'Bootstrap v1 release activation: NOT YET AUTHORIZED' in handoff
    assert claim["state"] == "CLAIMED_FOR_IMPLEMENTATION"
    assert claim["authority_effect"] is False
    assert claim["activation_effect"] is False
    assert claim["github_token_runtime_authority"] == "NONE"
