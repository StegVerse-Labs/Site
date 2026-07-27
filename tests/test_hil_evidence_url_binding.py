from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_hil_evidence_url_binding.py"


def load_module():
    spec = importlib.util.spec_from_file_location("hil_evidence_url_binding", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_public_https_origin_and_lookup_are_accepted() -> None:
    module = load_module()
    assert module.clean_https_origin("https://receiver.example")
    assert module.clean_https_lookup("https://receiver.example/api/hil/publications/HIL-RESP-0001")
    assert module.origin("https://receiver.example") == module.origin(
        "https://receiver.example/api/hil/publications/HIL-RESP-0001"
    )


@pytest.mark.parametrize(
    "value",
    [
        "http://receiver.example",
        "https://localhost",
        "https://127.0.0.1",
        "https://10.0.0.1",
        "https://169.254.169.254",
        "https://[::1]",
        "https://user:secret@receiver.example",
        "https://receiver.example/path",
        "https://receiver.example?next=elsewhere",
        "https://receiver.example#fragment",
    ],
)
def test_unsafe_deployment_origins_are_rejected(value: str) -> None:
    module = load_module()
    assert not module.clean_https_origin(value)


@pytest.mark.parametrize(
    "value",
    [
        "http://receiver.example/api/hil/publications/HIL-RESP-0001",
        "https://localhost/api/hil/publications/HIL-RESP-0001",
        "https://user:secret@receiver.example/api/hil/publications/HIL-RESP-0001",
        "https://receiver.example",
        "https://receiver.example/",
        "https://receiver.example/api/hil/publications/HIL-RESP-0001?download=1",
        "https://receiver.example/api/hil/publications/HIL-RESP-0001#receipt",
    ],
)
def test_unsafe_publication_lookup_urls_are_rejected(value: str) -> None:
    module = load_module()
    assert not module.clean_https_lookup(value)


def test_different_publication_origin_is_rejected_by_binding() -> None:
    module = load_module()
    deployment = "https://receiver.example"
    lookup = "https://other.example/api/hil/publications/HIL-RESP-0001"
    assert module.clean_https_origin(deployment)
    assert module.clean_https_lookup(lookup)
    assert module.origin(deployment) != module.origin(lookup)


def test_current_incomplete_packet_passes_without_claiming_urls(monkeypatch, tmp_path: Path, capsys) -> None:
    module = load_module()
    packet = {
        "deployment": {"state": "NOT_ESTABLISHED", "base_url": None},
        "publication": {"state": "NOT_ESTABLISHED", "stable_lookup_url": None},
    }
    packet_path = tmp_path / "packet.json"
    packet_path.write_text(json.dumps(packet), encoding="utf-8")
    monkeypatch.setattr(module, "PACKET", packet_path)
    module.main()
    output = capsys.readouterr().out
    assert "HIL_DEPLOYMENT_URL_ESTABLISHED=false" in output
    assert "HIL_PUBLICATION_URL_ESTABLISHED=false" in output
    assert "HIL_AUTHORITY=NONE" in output
