import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_session_disposition_custody_packet import build_result, validate_packet


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "data/session-custody-outbox/SESSION-ORCHESTRATION-DESIGN-SUPERSEDED-2026-08-07.custody.json"
RECEIPT_PATH = ROOT / "data/session-disposition-receipts/SESSION-ORCHESTRATION-DESIGN-SUPERSEDED-2026-08-07.receipt.json"


class SessionDispositionCustodyPacketTests(unittest.TestCase):
    def setUp(self):
        self.packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        self.receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))

    def test_current_packet_is_intake_ready_but_not_custody_proof(self):
        result = build_result(PACKET_PATH)
        self.assertEqual(result["state"], "PASS")
        self.assertTrue(result["custody_intake_ready"])
        self.assertFalse(result["custody_established"])
        self.assertFalse(result["reconstruction_verified"])
        self.assertEqual(result["authority_effect"], "NONE")

    def test_receipt_hash_binding_mismatch_blocks(self):
        packet = dict(self.packet)
        packet["source_receipt"] = dict(self.packet["source_receipt"])
        packet["source_receipt"]["receipt_sha256"] = "0" * 64
        failures = validate_packet(packet, self.receipt)
        self.assertIn("source_receipt_mismatch:receipt_sha256", failures)

    def test_registry_lineage_mismatch_blocks(self):
        packet = dict(self.packet)
        packet["baseline_registry_commit"] = "0" * 40
        failures = validate_packet(packet, self.receipt)
        self.assertIn("receipt_binding_mismatch:baseline_registry_commit", failures)

    def test_authority_escalation_blocks(self):
        packet = dict(self.packet)
        packet["authority"] = dict(self.packet["authority"])
        packet["authority"]["publication_authority"] = True
        failures = validate_packet(packet, self.receipt)
        self.assertIn("authority_escalation:publication_authority", failures)

    def test_unadmitted_source_receipt_blocks(self):
        receipt = dict(self.receipt)
        receipt["admission_status"] = "PENDING"
        failures = validate_packet(self.packet, receipt)
        self.assertIn("source_receipt_not_admitted", failures)

    def test_missing_source_receipt_path_blocks_without_custody_claim(self):
        packet = dict(self.packet)
        packet["source_receipt"] = dict(self.packet["source_receipt"])
        packet["source_receipt"]["path"] = ""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "packet.json"
            path.write_text(json.dumps(packet), encoding="utf-8")
            result = build_result(path)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertFalse(result["custody_established"])
        self.assertFalse(result["reconstruction_verified"])


if __name__ == "__main__":
    unittest.main()
