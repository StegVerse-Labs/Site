from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_generic_source_package_schema_is_platform_neutral():
    s=json.loads((ROOT/"stegos-node/source-package-v1.schema.json").read_text())
    assert s["properties"]["schema"]["const"]=="stegverse.source-package/v1"
    assert s["properties"]["package_version"]["const"]=="1.0.0"
    assert s["properties"]["source_identity"]["pattern"].startswith("^sha256:")
    assert s["properties"]["credential_material_included"]["const"] is False

def test_receiver_separates_integrity_from_admission():
    html=(ROOT/"stegos-node/source-package-bootstrap-v1.html").read_text()
    assert 'SOURCE_DB="stegos-source-packages-v1"' in html
    assert 'state:"MATERIALIZED_UNADMITTED"' in html
    assert 'admission_state:"UNADMITTED"' in html
    assert 'execution_authority:"NONE"' in html
    assert 'github_platform_required:false' in html
    assert 'specific_external_platform_required:false' in html
    assert "source identity mismatch" in html
    assert "source bundle digest mismatch" in html
    assert "file digest mismatch" in html
    assert "GITHUB_TOKEN" not in html
    assert "github.com/" not in html

def test_node_shell_exposes_and_caches_canonical_bootstrap():
    index=(ROOT/"stegos-node/index.html").read_text()
    sw=(ROOT/"stegos-node/service-worker.js").read_text()
    assert './source-package-bootstrap-v1.html' in index
    assert './source-package-bootstrap-v1.html' in sw
    assert './source-package-v1.schema.json' in sw

def test_handoff_forbids_platform_dependency():
    text=(ROOT/"docs/SOURCE_PACKAGE_BOOTSTRAP_V1_MIRROR_HANDOFF.md").read_text()
    assert "github_platform_required: false" in text
    assert "specific_external_platform_required: false" in text
    assert "package_integrity_confers_execution_authority: false" in text
