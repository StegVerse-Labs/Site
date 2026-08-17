from __future__ import annotations

import copy
import json
import os
import tempfile
from pathlib import Path

import pytest

from scripts.import_marketplace_coinbase_accessibility import digest, fetch_source, project, validate

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "marketplace-coinbase-accessibility-status.json"


def publisher_from_site_status() -> dict:
    site = json.loads(STATUS.read_text(encoding="utf-8"))
    body = {
        "schema": "stegverse.publisher.marketplace_coinbase_release_evidence.v2",
        "status": site["publisher_status"],
        "sources": site["publisher_sources"],
        "evidence_bindings": site["evidence_bindings"],
        "paper_release_verified": site["paper_trading_accessible"],
        "publication_authorized": False,
        "release_authorized": False,
        "execution_authorized": False,
        "live_authority_granted": False,
        "failures": [],
    }
    return {**body, "status_digest": digest(body)}


def test_committed_site_projection_is_digest_valid_and_paper_only():
    site = json.loads(STATUS.read_text(encoding="utf-8"))
    body = {key: value for key, value in site.items() if key != "projection_digest"}
    assert site["projection_digest"] == digest(body)
    assert site["state"] == "PAPER_ACCESSIBLE"
    assert site["paper_trading_accessible"] is True
    assert site["live_trading_accessible"] is False
    assert all(site[field] == "NOT_GRANTED" for field in (
        "publication_authority", "release_authority", "execution_authority", "live_authority"
    ))


def test_valid_publisher_status_is_accepted():
    source = publisher_from_site_status()
    assert validate(source) == []
    projected = project("PAPER_ACCESSIBLE", "validated", source)
    assert projected["paper_trading_accessible"] is True
    assert projected["live_trading_accessible"] is False
    assert projected["source_transport"] == "LOCAL_MATERIALIZED_REPOSITORY"
    assert projected["credential_requirement"] == "NONE"
    assert projected["github_token_allowed"] is False
    assert projected["remote_source_fetch_allowed"] is False
    assert projected["financial_authority"] == "NOT_GRANTED"


def test_authority_escalation_is_rejected_even_after_resigning():
    source = publisher_from_site_status()
    tampered = copy.deepcopy(source)
    tampered["execution_authorized"] = True
    tampered["status_digest"] = digest({key: value for key, value in tampered.items() if key != "status_digest"})
    assert "publisher_execution_authorized_boundary_invalid" in validate(tampered)


def test_tampered_status_digest_is_rejected():
    source = publisher_from_site_status()
    source["status"] = "REJECTED"
    assert "publisher_status_digest_mismatch" in validate(source)


def test_fetch_source_requires_local_publisher_materialization(monkeypatch):
    monkeypatch.delenv("STEGVERSE_REPO_ROOTS_JSON", raising=False)
    with pytest.raises(ValueError, match="STEGVERSE_REPO_ROOTS_JSON_REQUIRED"):
        fetch_source()


def test_fetch_source_reads_exact_local_publisher_evidence(monkeypatch):
    source = publisher_from_site_status()
    with tempfile.TemporaryDirectory() as temp_dir:
        publisher = Path(temp_dir) / "publisher"
        evidence = publisher / "data" / "marketplace-coinbase-release-evidence-status.json"
        evidence.parent.mkdir(parents=True)
        evidence.write_text(json.dumps(source), encoding="utf-8")
        monkeypatch.setenv("STEGVERSE_REPO_ROOTS_JSON", json.dumps({"GCAT-BCAT-Engine/Publisher": str(publisher)}))
        assert fetch_source() == source


def test_fetch_source_refuses_github_or_marketplace_credentials(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_dir:
        monkeypatch.setenv("STEGVERSE_REPO_ROOTS_JSON", json.dumps({"GCAT-BCAT-Engine/Publisher": temp_dir}))
        monkeypatch.setenv("MARKETPLACE_COINBASE_EVIDENCE_TOKEN", "forbidden")
        with pytest.raises(RuntimeError, match="FORBIDDEN_CREDENTIAL_ENV"):
            fetch_source()
        monkeypatch.delenv("MARKETPLACE_COINBASE_EVIDENCE_TOKEN", raising=False)


def test_source_contains_no_remote_github_fetch_contract():
    source = (ROOT / "scripts" / "import_marketplace_coinbase_accessibility.py").read_text(encoding="utf-8")
    assert "raw.githubusercontent.com" not in source
    assert "urllib" not in source
    assert "Authorization" not in source
