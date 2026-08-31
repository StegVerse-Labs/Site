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
        cls.carrier=(ROOT/"assets/hb-intr-carrier.js").read_text()
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
        order=["assets/stegverse-node-continuity.js","assets/hb-intr-carrier.js","stegos-node/device-kv-intr-sync.js","assets/my-kv-directory.js","assets/my-kv-portable-direct-source-bridge.js"]
        positions=[self.page.index(x) for x in order]
        self.assertEqual(positions,sorted(positions))

    def test_queue_attempts_existing_device_kv_sync(self):
        self.assertIn("StegVerseDeviceKVInTrSync.attempt()",self.portable)

    def test_portable_packet_uses_shared_canonical_hb_carrier(self):
        self.assertIn("StegVerseHBInTrCarrier.buildBinding",self.portable)
        self.assertIn("canonical HB-derived InTr carrier client unavailable",self.portable)
        self.assertIn("StegVerseGeneratedInTr",self.portable)
        self.assertIn('buildIntent("device-kv"',self.portable)
        self.assertIn("buildMaterializationRequest(",self.portable)
        self.assertIn("{portable_payload:inlinePayload}",self.portable)
        for marker in (
            "HB_ANCHOR_EPOCH=32",
            "HB_ANCHOR_UNIX_MS=1787511600000",
            "HB_PERIOD_MS=10",
            "HB_CHANNEL_COUNT=16",
            "stegverse.intr.hb-derived-carrier-binding/v1",
            "stegverse.intr.hb-derived-carrier-profile/v1",
            "PAYLOAD_SHA256_FIRST64_MOD_16",
            "payloadHash.charAt(22)",
            'authority_effect:"NONE_CARRIER_ONLY"',
        ):
            self.assertIn(marker,self.carrier)
        for marker in (
            "carrier_grants_admission_authority:false",
            "carrier_grants_execution_authority:false",
            "carrier_grants_credential_authority:false",
            "carrier_grants_routing_authority:false",
            "carrier_grants_transition_authority:false",
            "carrier_grants_receiving_authority:false",
        ):
            self.assertIn(marker,self.carrier)
        self.assertNotIn("HB_ANCHOR_EPOCH=32",self.portable)
        self.assertNotIn("PAYLOAD_SHA256_FIRST64_MOD_16",self.portable)
        self.assertNotIn("var intent={",self.portable)
        self.assertNotIn("var matBasis=",self.portable)
        self.assertNotIn("var materializationId=",self.portable)
        self.assertNotIn("var body={",self.portable)

    def test_device_kv_sync_requires_carrier_receipt_binding_when_present(self):
        for marker in (
            "carrier_binding_present: true",
            "carrier_binding_validated: true",
            "heartbeat_reference_epoch: carrier.heartbeat_reference.heartbeat_epoch",
            "carrier_channel_id: carrier.channel.channel_id",
            "carrier_binding_sha256: carrier.binding_sha256",
            "carrier_binding_grants_authority: false",
        ):
            self.assertIn(marker,self.sync)

if __name__=="__main__":
    unittest.main()
