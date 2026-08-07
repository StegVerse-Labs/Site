import copy
import unittest

from scripts.collect_heartbeat_response_receipts import authority_false, canonical_sha256, make_recovered, validate_pair


class HeartbeatResponseCollectorTests(unittest.TestCase):
    def setUp(self):
        self.authority = {"execution": False, "activation": False, "publication": False, "custody": False, "release": False}
        self.message = {
            "message_id": "hb-bootstrap-test",
            "exchange_id": "hb-exchange-test",
            "source_org": "StegVerse-Labs",
            "destination_org": "AdmittedCode",
            "stage": "SENT",
            "detail_class": "AWARENESS",
            "authority": self.authority,
        }
        observed = canonical_sha256(self.message)
        self.received = {
            "schema_version": "1.0.0",
            "message_id": "hb-bootstrap-test-received",
            "exchange_id": "hb-exchange-test",
            "node_org": "AdmittedCode",
            "source_org": "StegVerse-Labs",
            "destination_org": "AdmittedCode",
            "stage": "RECEIVED",
            "detail_class": "AWARENESS",
            "observed_message_sha256": observed,
            "authority": self.authority,
        }
        self.responded = {
            "schema_version": "1.0.0",
            "message_id": "hb-bootstrap-test-responded",
            "exchange_id": "hb-exchange-test",
            "node_org": "AdmittedCode",
            "source_org": "StegVerse-Labs",
            "destination_org": "AdmittedCode",
            "stage": "RESPONDED",
            "detail_class": "CAPABILITY",
            "observed_message_sha256": observed,
            "authority": self.authority,
            "classification": {"node_state": "RESPONSIVE"},
            "parent_receipt_sha256": canonical_sha256(self.received),
        }

    def test_pair_accepts_hash_bound_response(self):
        validate_pair("AdmittedCode", "hb-exchange-test", self.message, self.received, self.responded)

    def test_pair_rejects_observed_message_hash_drift(self):
        item = copy.deepcopy(self.responded)
        item["observed_message_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            validate_pair("AdmittedCode", "hb-exchange-test", self.message, self.received, item)

    def test_pair_rejects_parent_receipt_hash_drift(self):
        item = copy.deepcopy(self.responded)
        item["parent_receipt_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            validate_pair("AdmittedCode", "hb-exchange-test", self.message, self.received, item)

    def test_transport_authority_escalation_rejected(self):
        item = copy.deepcopy(self.responded)
        item["authority"]["execution"] = True
        with self.assertRaises(ValueError):
            validate_pair("AdmittedCode", "hb-exchange-test", self.message, self.received, item)

    def test_recovered_receipt_links_to_response_and_grants_no_authority(self):
        recovered = make_recovered("AdmittedCode", "hb-exchange-test", self.responded)
        self.assertEqual(recovered["stage"], "RECOVERED")
        self.assertEqual(recovered["parent_receipt_sha256"], canonical_sha256(self.responded))
        self.assertTrue(authority_false(recovered["authority"]))
        self.assertFalse(recovered["classification"]["action_admitted"])


if __name__ == "__main__":
    unittest.main()
