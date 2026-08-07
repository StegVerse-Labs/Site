import copy
import unittest

from scripts.check_heartbeat_response_network import DETAIL_CLASSES, LIFECYCLE, validate_outbox, validate_receipt


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
            "authority": {
                "execution": False,
                "activation": False,
                "publication": False,
                "custody": False,
                "release": False,
            },
        }

    def test_lifecycle_is_ordered(self):
        self.assertEqual(LIFECYCLE, ["SENT", "RECEIVED", "RESPONDED", "RECOVERED", "REPEAT"])

    def test_required_detail_classes_present(self):
        self.assertTrue({"MEMORY", "ACTION", "AWARENESS", "CAPABILITY", "BLOCKER"}.issubset(DETAIL_CLASSES))

    def test_receipt_accepts_registered_orgs(self):
        digest = validate_receipt(self.base, self.orgs)
        self.assertEqual(len(digest), 64)

    def test_receipt_rejects_unknown_org(self):
        item = copy.deepcopy(self.base)
        item["destination_org"] = "Unknown-Org"
        item["node_org"] = "Unknown-Org"
        with self.assertRaises(ValueError):
            validate_receipt(item, self.orgs)

    def test_receipt_rejects_node_destination_mismatch(self):
        item = copy.deepcopy(self.base)
        item["node_org"] = "StegVerse-Labs"
        with self.assertRaises(ValueError):
            validate_receipt(item, self.orgs)

    def test_transport_cannot_grant_authority(self):
        item = copy.deepcopy(self.base)
        item["authority"]["execution"] = True
        with self.assertRaises(ValueError):
            validate_receipt(item, self.orgs)

    def test_action_is_valid_class_but_not_authority(self):
        item = copy.deepcopy(self.base)
        item["detail_class"] = "ACTION"
        digest = validate_receipt(item, self.orgs)
        self.assertEqual(len(digest), 64)

    def test_outbox_requires_one_sent_message_per_org(self):
        authority = {"execution": False, "activation": False, "publication": False, "custody": False, "release": False}
        outbox = {
            "message_count": 2,
            "messages": [
                {"message_id":"msg-1-000","exchange_id":"ex-1-0000","source_org":"StegVerse-Labs","destination_org":"StegVerse-Labs","stage":"SENT","detail_class":"AWARENESS","authority":authority,"payload":{}},
                {"message_id":"msg-2-000","exchange_id":"ex-2-0000","source_org":"StegVerse-Labs","destination_org":"master-records","stage":"SENT","detail_class":"AWARENESS","authority":authority,"payload":{}},
            ],
        }
        validate_outbox(outbox, self.orgs)

    def test_outbox_rejects_duplicate_destination(self):
        authority = {"execution": False, "activation": False, "publication": False, "custody": False, "release": False}
        outbox = {
            "message_count": 2,
            "messages": [
                {"message_id":"msg-1-000","exchange_id":"ex-1-0000","source_org":"StegVerse-Labs","destination_org":"master-records","stage":"SENT","detail_class":"AWARENESS","authority":authority,"payload":{}},
                {"message_id":"msg-2-000","exchange_id":"ex-2-0000","source_org":"StegVerse-Labs","destination_org":"master-records","stage":"SENT","detail_class":"AWARENESS","authority":authority,"payload":{}},
            ],
        }
        with self.assertRaises(ValueError):
            validate_outbox(outbox, self.orgs)


if __name__ == "__main__":
    unittest.main()
