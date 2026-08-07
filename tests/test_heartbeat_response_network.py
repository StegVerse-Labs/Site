import copy
import unittest

from scripts.check_heartbeat_response_network import DETAIL_CLASSES, LIFECYCLE, validate_receipt


class HeartbeatResponseNetworkTests(unittest.TestCase):
    def setUp(self):
        self.orgs = {"StegVerse-Labs", "master-records"}
        self.base = {
            "message_id": "msg-00000001",
            "exchange_id": "ex-00000001",
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
        self.assertTrue({"MEMORY", "ACTION", "AWARENESS"}.issubset(DETAIL_CLASSES))

    def test_receipt_accepts_registered_orgs(self):
        digest = validate_receipt(self.base, self.orgs)
        self.assertEqual(len(digest), 64)

    def test_receipt_rejects_unknown_org(self):
        item = copy.deepcopy(self.base)
        item["destination_org"] = "Unknown-Org"
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


if __name__ == "__main__":
    unittest.main()
