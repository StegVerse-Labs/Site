from __future__ import annotations

import copy
import json
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
    assert all(site[field] == "NOT_GRANTED" for field in ("publication_authority", "release_authority", "execution_authority", "live_authority"))


def test_valid_publisher_status_is_accepted():
    source = publisher_from_site_status()
    assert validate(source) == []
    projected = project("PAPER_ACCESSIBLE", "validated", source)
    assert projected["paper_trading_accessible"] is True
    assert projected["live_trading_accessible"] is False


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


def test_fetch_source_requires_materialized_local_publisher(monkeypatch):
    monkeypatch.delenv("STEGVERSE_REPO_ROOTS_JSON", raising=False)
    with pytest.raises(ValueError, match="STEGVERSE_REPO_ROOTS_JSON_REQUIRED"):
        fetch_source()


def test_fetch_source_reads_materialized_publisher_without_network(monkeypatch, tmp_path):
    publisher_root = tmp_path / "Publisher"
    status_path = publisher_root / "data" / "marketplace-coinbase-release-evidence-status.json"
    status_path.parent.mkdir(parents=True)
    expected = publisher_from_site_status()
    status_path.write_text(json.dumps(expected), encoding="utf-8")
    monkeypatch.setenv("STEGVERSE_REPO_ROOTS_JSON", json.dumps({"GCAT-BCAT-Engine/Publisher": str(publisher_root)}))
    assert fetch_source() == expected


def test_fetch_source_refuses_non_tvtvc_credential_environment(monkeypatch, tmp_path):
    publisher_root = tmp_path / "Publisher"
    publisher_root.mkdir()
    monkeypatch.setenv("STEGVERSE_REPO_ROOTS_JSON", json.dumps({"GCAT-BCAT-Engine/Publisher": str(publisher_root)}))
    monkeypatch.setenv("GITHUB_TOKEN", "forbidden")
    with pytest.raises(ValueError, match="NON_TV_TVC_CREDENTIAL_ENV_PROHIBITED"):
        fetch_source()
