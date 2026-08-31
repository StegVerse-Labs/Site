from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]

class DeviceKVInTrSyncTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sync=(ROOT/"stegos-node/device-kv-intr-sync.js").read_text()
        cls.page=(ROOT/"my-kv-directory.html").read_text()
        cls.portable=(ROOT/"assets/my-kv-portable-direct-source-bridge.js").read_text()
        cls.target=json.loads((ROOT/"stegos-node/device-kv-intr-sync-target.json").read_text())

    def test_exact_destination_owner_and_receipt(self):
        self.assertIn('subsystem: "KnowledgeVault:Interlock"',self.sync)
        self.assertIn('StegVerse-Labs/continuity-vault-kit#79',self.sync)
        self.assertIn('stegverse.device-kv-intr-materialization-ingress/v1',self.sync)

    def test_ingress_does_not_promote_runtime(self):
        self.assertIn("network_delivery_observed: true",self.sync)
        self.assertIn("runtime_materialization_observed: false",self.sync)
        self.assertIn("receiver_receipt_observed: false",self.sync)
        self.assertIn("tvc_receipt_observed: false",self.sync)

    def test_target_fails_closed_without_observed_route(self):
        self.assertEqual(self.target["state"],"AWAITING_SOVEREIGN_INTR_INGRESS")
        self.assertIsNone(self.target["ingress_url"])
        self.assertFalse(self.target["runtime_ingress_observed"])
        self.assertEqual(self.target["execution_authority"],"NONE")

    def test_directory_loads_node_before_portable_bridge(self):
        order=["assets/stegverse-node-continuity.js","stegos-node/device-kv-intr-sync.js","assets/my-kv-directory.js","assets/my-kv-portable-direct-source-bridge.js"]
        positions=[self.page.index(x) for x in order]
        self.assertEqual(positions,sorted(positions))

    def test_queue_attempts_existing_device_kv_sync(self):
        self.assertIn("StegVerseDeviceKVInTrSync.attempt()",self.portable)

if __name__=="__main__":
    unittest.main()
