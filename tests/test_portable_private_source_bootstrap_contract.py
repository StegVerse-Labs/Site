from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_portable_private_source_bootstrap_contract():
    html=(ROOT/"stegos-node/portable-source-bootstrap-v1.html").read_text()
    schema=json.loads((ROOT/"stegos-node/private-source-portable-package-v1.schema.json").read_text())
    assert schema["properties"]["schema"]["const"]=="stegverse.private-source-portable-package/v1"
    assert schema["properties"]["package_version"]["const"]=="1.0.0"
    assert 'DB="stegos-web-bootstrap-v1"' in html
    assert 'SOURCE_DB="stegos-portable-source-v1"' in html
    assert 'credential_transport!=="SYSTEMD_LOADCREDENTIAL"' in html
    assert 'credential_material_included!==false' in html
    assert 'credential_material_observed:false' in html
    assert 'new_node_identity_minted:false' in html
    assert 'source bundle digest mismatch' in html
    assert 'file digest mismatch' in html
    assert "GITHUB_TOKEN" not in html
    assert "GH_TOKEN" not in html

def test_handoff_preserves_tvc_authority_and_first_profile():
    text=(ROOT/"docs/DEVICE_NODE_PORTABLE_PRIVATE_SOURCE_BOOTSTRAP_MIRROR_HANDOFF.md").read_text()
    assert "credential_authority: TV/TVC" in text
    assert "browser_credential_material_allowed: false" in text
    assert "b5288f9910ada26c6ab2e9bca3f7701afaae2cef" in text
    assert "0369ed677a014a99a983415a9094e6aaa0c570d163d9818d9a086fee6042dd6a" in text
