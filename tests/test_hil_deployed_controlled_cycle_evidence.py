from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts" / "check_hil_deployed_controlled_cycle_evidence.py"
PACKET = ROOT / "data" / "hil-deployed-controlled-cycle-evidence.json"
ACTIVATION = ROOT / "data" / "hil-activation-state.json"
RUNBOOK = ROOT / "docs" / "HIL_DEPLOYED_CONTROLLED_CYCLE_RUNBOOK.md"


def build_fixture(tmp_path: Path) -> Path:
    fixture = tmp_path / "site"
    (fixture / "scripts").mkdir(parents=True)
    (fixture / "data").mkdir()
    (fixture / "docs").mkdir()
    shutil.copy2(VERIFIER, fixture / "scripts" / VERIFIER.name)
    shutil.copy2(PACKET, fixture / "data" / PACKET.name)
    shutil.copy2(ACTIVATION, fixture / "data" / ACTIVATION.name)
    shutil.copy2(RUNBOOK, fixture / "docs" / RUNBOOK.name)
    return fixture


def run_verifier(fixture: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(fixture / "scripts" / VERIFIER.name)],
        cwd=fixture,
        text=True,
        capture_output=True,
        check=False,
    )


def load_packet(fixture: Path) -> dict:
    return json.loads((fixture / "data" / PACKET.name).read_text(encoding="utf-8"))


def write_packet(fixture: Path, packet: dict) -> None:
    (fixture / "data" / PACKET.name).write_text(
        json.dumps(packet, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_current_incomplete_packet_is_valid_and_non_authorizing(tmp_path: Path) -> None:
    fixture = build_fixture(tmp_path)
    result = run_verifier(fixture)
    assert result.returncode == 0, result.stderr
    assert "HIL_EVIDENCE_PACKET_STATE=INCOMPLETE" in result.stdout
    assert "HIL_PUBLIC_ACQUISITION_AUTHORIZED=false" in result.stdout
    assert "HIL_AUTHORITY=NONE" in result.stdout


def test_retired_v05_contract_is_rejected(tmp_path: Path) -> None:
    fixture = build_fixture(tmp_path)
    packet = load_packet(fixture)
    packet["contract"]["primary_version"] = "v0.5"
    write_packet(fixture, packet)
    result = run_verifier(fixture)
    assert result.returncode != 0
    assert "contract mismatch for primary_version" in result.stderr


def test_incomplete_packet_cannot_authorize_public_acquisition(tmp_path: Path) -> None:
    fixture = build_fixture(tmp_path)
    packet = load_packet(fixture)
    packet["public_acquisition"]["authorized"] = True
    packet["public_acquisition"]["authorization_ref"] = "invalid-early-authorization"
    write_packet(fixture, packet)
    result = run_verifier(fixture)
    assert result.returncode != 0
    assert "incomplete packet cannot authorize public acquisition" in result.stderr


def test_complete_packet_requires_every_live_section(tmp_path: Path) -> None:
    fixture = build_fixture(tmp_path)
    packet = load_packet(fixture)
    packet["packet_state"] = "COMPLETE"
    write_packet(fixture, packet)
    result = run_verifier(fixture)
    assert result.returncode != 0
    assert "packet marked complete before every evidence section is established" in result.stderr


def test_established_deployment_rejects_non_https_origin(tmp_path: Path) -> None:
    fixture = build_fixture(tmp_path)
    packet = load_packet(fixture)
    packet["deployment"].update(
        {
            "state": "ESTABLISHED",
            "deployed_commit": "a" * 40,
            "base_url": "http://receiver.example",
            "evidence_refs": ["deployment-receipt"],
        }
    )
    write_packet(fixture, packet)
    result = run_verifier(fixture)
    assert result.returncode != 0
    assert "deployment base URL must be a globally routable HTTPS origin" in result.stderr
