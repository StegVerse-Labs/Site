import copy
import unittest

from scripts.check_heartbeat_response_network import DETAIL_CLASSES, LIFECYCLE, canonical_sha256, validate_outbox, validate_receipt, validate_recovery_link


class HeartbeatResponseNetworkTests(unittest.TestCase):
    def setUp(self):
        self.orgs = {"StegVerse-Labs", "master-records"}
        self.base = {
            "message_id": "msg-00000001",
            "exchange_id": "ex-00000001",
            "node_org": "master-records",
            "source_org": "StegVerse-Labs",
            "destination_org": "master-records",
            "stage": "RECEIVED",
            "detail_class": "AWARENESS",
            "authority": {"execution": False, "activation": False, "publication": False, "custody": False, "release": False},
        }

    def test_lifecycle_is_ordered(self):
        self.assertEqual(LIFECYCLE, ["SENT", "RECEIVED", "RESPONDED", "RECOVERED", "REPEAT"])

    def test_required_detail_classes_present(self):
        self.assertTrue({"MEMORY", "ACTION", "AWARENESS", "CAPABILITY", "BLOCKER"}.issubset(DETAIL_CLASSES))

    def test_receipt_accepts_registered_orgs(self):
        digest = validate_receipt(self.base, self.orgs)
        self.assertEqual(len(digest), 64)

    def test_receipt_rejects_unknown_org(self):
        item = copy.deepcopy(self.base); item["destination_org"] = "Unknown-Org"; item["node_org"] = "Unknown-Org"
        with self.assertRaises(ValueError): validate_receipt(item, self.orgs)

    def test_receipt_rejects_node_destination_mismatch(self):
        item = copy.deepcopy(self.base); item["node_org"] = "StegVerse-Labs"
        with self.assertRaises(ValueError): validate_receipt(item, self.orgs)

    def test_transport_cannot_grant_authority(self):
        item = copy.deepcopy(self.base); item["authority"]["execution"] = True
        with self.assertRaises(ValueError): validate_receipt(item, self.orgs)

    def test_action_is_valid_class_but_not_authority(self):
        item = copy.deepcopy(self.base); item["detail_class"] = "ACTION"
        self.assertEqual(len(validate_receipt(item, self.orgs)), 64)

    def test_recovery_requires_hash_bound_responded_parent(self):
        responded = copy.deepcopy(self.base); responded["stage"] = "RESPONDED"; responded["detail_class"] = "CAPABILITY"
        recovered = copy.deepcopy(self.base); recovered["stage"] = "RECOVERED"; recovered["detail_class"] = "EVIDENCE"; recovered["parent_receipt_sha256"] = canonical_sha256(responded)
        validate_recovery_link(recovered, responded)
        recovered["parent_receipt_sha256"] = "0" * 64
        with self.assertRaises(ValueError): validate_recovery_link(recovered, responded)

    def test_outbox_requires_one_sent_message_per_org(self):
        authority = {"execution": False, "activation": False, "publication": False, "custody": False, "release": False}
        outbox = {"message_count": 2, "messages": [
            {"message_id":"msg-1-000","exchange_id":"ex-1-0000","source_org":"StegVerse-Labs","destination_org":"StegVerse-Labs","stage":"SENT","detail_class":"AWARENESS","authority":authority,"payload":{}},
            {"message_id":"msg-2-000","exchange_id":"ex-2-0000","source_org":"StegVerse-Labs","destination_org":"master-records","stage":"SENT","detail_class":"AWARENESS","authority":authority,"payload":{}},
        ]}
        validate_outbox(outbox, self.orgs)

    def test_outbox_rejects_duplicate_destination(self):
        authority = {"execution": False, "activation": False, "publication": False, "custody": False, "release": False}
        outbox = {"message_count": 2, "messages": [
            {"message_id":"msg-1-000","exchange_id":"ex-1-0000","source_org":"StegVerse-Labs","destination_org":"master-records","stage":"SENT","detail_class":"AWARENESS","authority":authority,"payload":{}},
            {"message_id":"msg-2-000","exchange_id":"ex-2-0000","source_org":"StegVerse-Labs","destination_org":"master-records","stage":"SENT","detail_class":"AWARENESS","authority":authority,"payload":{}},
        ]}
        with self.assertRaises(ValueError): validate_outbox(outbox, self.orgs)


if __name__ == "__main__":
    unittest.main()
