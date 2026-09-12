from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "stegos-bootstrap" / "hil-resume.html"


def test_resume_router_exists_and_is_single_user_entry_contract():
    page = PAGE.read_text(encoding="utf-8")
    assert "canonical same-device HIL continuation surface" in page
    assert "You do not need to remember which HIL page was used previously" in page
    assert 'var LOCAL_READY_PAGE="./hil-activate.html"' in page
    assert 'var ESRL_PAGE="./hil-esrl-activate.html"' in page
    assert 'var CUSTODY_PAGE="./hil-custody-activate.html"' in page
    assert 'var SUBMISSION_PAGE="../humans-as-interoperability-layer.html#submit-response"' in page


def test_resume_router_canonicalizes_http_before_state_reads():
    page = PAGE.read_text(encoding="utf-8")
    redirect = page.index('if(canonicalizeSecureOrigin()){return;}')
    first_read = page.index('var CONTEXT_KEY="stegos-hil-browser-context-v1"')
    assert redirect < first_read
    assert 'location.replace(target);' in page
    assert '"https://stegverse.org"+location.pathname+location.search+location.hash' in page


def test_resume_router_discovers_all_durable_hil_stores():
    page = PAGE.read_text(encoding="utf-8")
    for marker in (
        'CONTEXT_KEY="stegos-hil-browser-context-v1"',
        'LOCAL_READY_KEY="stegos-hil-last-success-v1"',
        'ESRL_KEY="stegos-hil-esrl-last-success-v1"',
        'SUBMISSIONS_KEY="stegverse.hil.submissions.v1"',
        'CUSTODY_KEY="stegos-hil-custody-last-success-v1"',
        'DB_NAME="stegverse-hil-v3"',
        'STORE_NAME="response_files"',
    ):
        assert marker in page


def test_resume_router_cross_checks_pending_metadata_against_exact_indexeddb_bytes():
    page = PAGE.read_text(encoding="utf-8")
    assert 'row.state==="INTR_TRANSPORT_PENDING"' in page
    assert 'row.local_pretransport_staged===true' in page
    assert 'row.response_storage_verified===true' in page
    assert 'readStagedObject(row.response_object_key)' in page
    assert 'pending metadata/staged-object hash binding mismatch' in page
    assert 'pending staged exact-byte SHA-256 mismatch' in page
    assert 'digestBytes(staged.bytes)' in page


def test_resume_router_preserves_g25_and_non_overclaim_boundaries():
    page = PAGE.read_text(encoding="utf-8")
    assert 'CLAIM_ID="SHWP-SHWP-HIL-SOVEREIGN-RECEIVER-001-G25"' in page
    assert 'var FENCE=25' in page
    assert 'EXPECTED_LEASE="HIL-BROWSER-ESRL-7bafde4a280e847758da157e"' in page
    assert 'value.tvc_admission_completed===false' in page
    assert 'value.post_restart_exact_byte_proof_observed===false' in page
    assert 'value.broader_hil_lifecycle_complete===false' in page
    assert 'NEXT_PARENT_BOUNDARY: POST_RESTART_EXACT_BYTE_PROOF' in page


def test_resume_router_accepts_historical_v1_local_ready_without_execution_surface():
    page = PAGE.read_text(encoding="utf-8")
    assert 'var surfaceOk=!Object.prototype.hasOwnProperty.call(value,"execution_surface")||value.execution_surface==="CURRENT_USER_IPHONE";' in page
    assert 'value.second_claim_minted===false&&surfaceOk' in page
    assert 'value.execution_surface==="CURRENT_USER_IPHONE"&&value.second_claim_minted===false' not in page


def test_resume_router_routes_by_latest_admissible_state_without_tab_memory():
    page = PAGE.read_text(encoding="utf-8")
    custody = page.index('if(custody!==null)')
    lease = page.index('if(lease){')
    local_ready = page.index('if(localReady){route("RESUMING_ACCEPTED_HIL_LINEAGE_TO_ESRL"')
    activation = page.index('route("ESTABLISHING_OR_RECOVERING_LOCAL_HIL_READY_STATE"')
    assert custody < lease < local_ready < activation
    assert 'route("RESUMING_SAME_DEVICE_CUSTODY",CUSTODY_PAGE)' in page
    assert 'route("RESPONSE_PACKET_STAGING_REQUIRED",SUBMISSION_PAGE)' in page


def test_resume_router_fails_closed_on_true_storage_continuity_conflicts():
    page = PAGE.read_text(encoding="utf-8")
    assert 'FAIL_CLOSED_DEVICE_CONTINUITY:' in page
    assert 'stored custody result exists but fails canonical receipt validation' in page
    assert 'stored ESRL result exists but fails canonical lease validation' in page
    assert 'stored local-ready result exists but fails canonical HIL validation' in page
    assert 'persisted browser-context pointer conflicts with canonical local-ready evidence' in page
    assert 'location.replace(url)' in page
    assert 'localStorage.setItem(' not in page
