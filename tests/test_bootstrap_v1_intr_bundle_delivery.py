from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "stegos-node/bootstrap-bundle-intr-delivery-v1.html"
CANONICAL = ROOT / "stegos-node/bootstrap-bundle-materialization-v1.html"
SW = ROOT / "stegos-node/service-worker.js"
HANDOFF = ROOT / "docs/BOOTSTRAP_V1_BUNDLE_MATERIALIZATION_MIRROR_HANDOFF.md"


def test_delivery_companion_reuses_canonical_materializer():
    html = PAGE.read_text()
    assert 'src="./bootstrap-bundle-materialization-v1.html"' in html
    assert 'document.getElementById("bundle-file")' in html
    assert 'input.dispatchEvent(new Event("change",{bubbles:true}))' in html
    assert 'button.click()' in html
    assert 'stegos.web_source_package_materialization_receipt.v1' not in html
    assert 'stegos.web_bootstrap_bundle_materialization_receipt.v1' not in html
    assert CANONICAL.is_file()


def test_delivery_companion_uses_same_origin_universal_intr():
    html = PAGE.read_text()
    assert 'var ENDPOINT="/intr/bootstrap-v1/bundle"' in html
    assert '"X-StegVerse-Transport":"InTr"' in html
    assert 'credentials:"omit"' in html
    assert 'mode:"same-origin"' in html
    assert 'STEGVERSE-UNIVERSAL-INTR-TRANSPORT-001' in html
    assert 'stegverse.universal-intr.adjacent-hop/v1' in html
    assert 'DEVICE_SYSTEM' in html
    assert 'STEGOS_ECOSYSTEM' in html


def test_delivery_companion_validates_receipt_chain_and_zero_authority():
    html = PAGE.read_text()
    assert 'receipt.schema!=="stegverse.intr.hop_receipt/v1"' in html
    assert 'receipt.secret_plaintext_present!==false' in html
    assert 'receipt.authority_transfer!==false' in html
    assert 'egress.prior_receipt_hash!==ingress.receipt_hash' in html
    assert 'response.execution_authority!=="NONE"' in html
    assert 'response.release_activated!==false' in html
    assert 'response.publication_performed!==false' in html
    assert 'response.authority_effect!=="NONE_BUNDLE_DELIVERY_ONLY"' in html
    assert 'request_grants_execution_authority:false' in html
    assert 'credential_required:false' in html


def test_delivery_does_not_fetch_from_repository_or_registry():
    html = PAGE.read_text()
    assert 'github.com' not in html.lower()
    assert 'api.github.com' not in html.lower()
    assert 'npmjs' not in html.lower()
    assert 'pypi' not in html.lower()
    assert 'unpkg' not in html.lower()


def test_offline_shell_caches_delivery_companion():
    sw = SW.read_text()
    assert 'stegos-node-shell-v9-bootstrap-intr-delivery-v1' in sw
    assert './bootstrap-bundle-intr-delivery-v1.html' in sw
    assert './bootstrap-bundle-materialization-v1.html' in sw


def test_handoff_records_implemented_canonical_receiver_and_separate_delivery_gate():
    handoff = HANDOFF.read_text()
    assert 'bundle-level browser receiver: IMPLEMENTED / MERGED (Site PR #693)' in handoff
    assert 'bundle materialization implementation claim: RELEASED (Site PR #694)' in handoff
    assert '/intr/bootstrap-v1/bundle' in handoff
    assert 'Delivery success is not materialization success.' in handoff
    assert 'first authentic InTr bundle delivery: NOT YET OBSERVED' in handoff
