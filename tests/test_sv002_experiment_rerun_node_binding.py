from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "assets" / "sv002-experiment-rerun.js"
SYNC = ROOT / "stegos-node" / "sv002-self-characterization-intr-sync.js"
TARGET = ROOT / "stegos-node" / "sv002-self-characterization-intr-sync-target.json"
PAGE = ROOT / "sv002-rerun" / "index.html"
HANDOFF = ROOT / "docs" / "SV002_EXPERIMENT_RERUN_NODE_BINDING_MIRROR_HANDOFF.md"
CONNECTOR = ROOT / "assets" / "generated" / "site-browser-intr-connectors.js"
MANIFEST = ROOT / "assets" / "generated" / "site-browser-intr-connectors.manifest.json"
PROJECTOR = ROOT / "scripts" / "project_sv002_self_characterization_intr_sync_target.py"

GOAL = "STEGVERSE-002-EXPERIMENT-RERUN-001"
COSV = "50000000107000"


def test_generated_connector_projects_canonical_self_characterization_profile():
    source = CONNECTOR.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert "sv002-self-characterization" in manifest["profiles"]
    assert "sv002-self-characterization" in manifest["profile_sha256"]
    assert '" + '"REQUEST_SELF_CHARACTERIZATION"' + "' in source
    assert '" + '"SV002:SelfCharacterization"' + "' in source
    assert '" + '"StegVerse-002/.github"' + "' in source
    assert '" + '"invocation_count"' + "' in source


def test_builder_is_exact_single_request_node_outbox_binding():
    source = BUILDER.read_text(encoding="utf-8")
    required = (
        GOAL, COSV,
        'var OPERATION="REQUEST_SELF_CHARACTERIZATION"',
        'var MANIFEST_ID="SDK-SV002-FIRST-SELF-CHARACTERIZATION-001"',
        'var SOURCE_ORG="StegVerse-SDK-Evaluator"',
        'var TARGET_ENTITY="StegVerse-002"',
        "queueIntrMaterializationRequest(materialization)",
        'invocation_count:1',
        '"REQUEST_BOUND"',
        "sameBefore.length<=1",
        "sameAfter.length===1",
        "request_grants_execution_authority===false",
        "claim_or_fence_minted===false",
        'github_token_runtime_authority==="NONE"',
    )
    for marker in required:
        assert marker in source
    forbidden = ("new Worker(", "setInterval(", "WebSocket(", "EventSource(", "Healer", "SHWP-SV002-FROZEN-CORPUS-MATERIALIZATION-001")
    for marker in forbidden:
        assert marker not in source


def test_sync_filters_only_exact_goal_cosv_and_single_invocation():
    source = SYNC.read_text(encoding="utf-8")
    for marker in (
        GOAL, COSV, 'var OPERATION="REQUEST_SELF_CHARACTERIZATION"',
        'subsystem:"SV002:SelfCharacterization"', 'var OWNER="StegVerse-002/.github"',
        "m.invocation_count!==1", "entries.length>1", "INTR_MATERIALIZATION_ADMITTED",
        "runtime_execution_attempted:false", "claim_or_fence_minted:false",
    ):
        assert marker in source


def test_target_starts_fail_closed_until_authentic_shared_profile_observation():
    target = json.loads(TARGET.read_text(encoding="utf-8"))
    assert target["state"] == "AWAITING_SOVEREIGN_INTR_INGRESS"
    assert target["ingress_url"] is None
    assert target["runtime_ingress_observed"] is False
    assert target["required_profile"] == "SV002:SelfCharacterization"
    assert target["execution_authority"] == "NONE"


def test_projector_requires_self_characterization_on_existing_shared_profile():
    spec = importlib.util.spec_from_file_location("projector", PROJECTOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    text = PROJECTOR.read_text(encoding="utf-8")
    assert "BASE.project_target(observation)" in text
    assert 'REQUIRED_PROFILE = "SV002:SelfCharacterization"' in text
    assert "profile_sv002_self_characterization_support_missing" in text
    assert '"request_bound_observed": False' in text
    assert '"origin_return_observed": False' in text


def test_rerun_page_loads_only_existing_node_intr_components_plus_bounded_builder():
    source = PAGE.read_text(encoding="utf-8")
    assert "../assets/stegverse-node-continuity.js" in source
    assert "../assets/hb-intr-carrier.js" in source
    assert "../assets/generated/site-browser-intr-connectors.js" in source
    assert "../assets/sv002-experiment-rerun.js" in source
    assert "../stegos-node/sv002-self-characterization-intr-sync.js" in source
    assert "bindOnce()" in source
    assert "registerDevice()" in source
    assert "sv002-local-runtime-materializer.js" not in source
    assert "sv002-principal-worker.js" not in source


def test_handoff_preserves_nonclaim_boundary():
    source = HANDOFF.read_text(encoding="utf-8")
    assert GOAL in source and COSV in source
    assert "Source/CI/merge alone is not" in source and "REQUEST_BOUND" in source
    assert "No new runtime, scheduler, host, Healer dependency, corpus prerequisite" in source
