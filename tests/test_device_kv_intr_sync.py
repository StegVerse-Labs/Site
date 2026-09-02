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
        cls.local_runtime=(ROOT/"intr-service-worker.js").read_text()

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
        self.assertIsNone(self.target["result_url"])
        self.assertFalse(self.target["runtime_ingress_observed"])
        self.assertEqual(self.target["execution_authority"],"NONE")

    def test_directory_loads_node_before_portable_bridge(self):
        order=["assets/stegverse-node-continuity.js","assets/generated/site-browser-intr-connectors.js","assets/hb-intr-carrier.js","stegos-node/device-kv-intr-sync.js","assets/my-kv-directory.js","assets/my-kv-device-kv-query-bridge.js","assets/my-kv-portable-direct-source-bridge.js"]
        positions=[self.page.index(x) for x in order]
        self.assertEqual(positions,sorted(positions))

    def test_sync_exports_target_and_delivery_for_query_bridge(self):
        self.assertIn("loadTarget: loadTarget",self.sync)
        self.assertIn("getDeliveryReceipt: getDeliveryReceipt",self.sync)
        self.assertIn("synchronizeMaterialization: synchronizeMaterialization",self.sync)
        self.assertIn("DEVICE_KV materialization not present in Node outbox",self.sync)
        self.assertIn("/intr/device-kv/result",self.sync)
        self.assertIn("ingress/result origin mismatch",self.sync)

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


    def test_device_local_runtime_precedes_static_awaiting_target(self):
        self.assertIn('navigator.serviceWorker.register("/intr-service-worker.js", { scope: "/" })',self.sync)
        self.assertIn('fetch("/intr/profile"',self.sync)
        self.assertIn('loadDeviceLocalTarget().catch(function ()',self.sync)
        self.assertIn('"CONFORMING_SOVEREIGN_INTR_INGRESS"',self.sync)
        self.assertIn('runtime_surface: profile.runtime_surface',self.sync)
        self.assertIn('"CURRENT_USER_IPHONE_SERVICE_WORKER"',self.local_runtime)
        self.assertIn('"REGISTERED_STEGVERSE_NODE"',self.local_runtime)

    def test_device_local_service_worker_refresh_precedes_profile_read(self):
        self.assertIn('function refreshLocalServiceWorker(registration)', self.sync)
        self.assertIn('registration.update()', self.sync)
        self.assertIn('registration.installing||registration.waiting', self.sync)
        self.assertIn('return refreshLocalServiceWorker(registration);', self.sync)
        self.assertLess(self.sync.index('registration.update()'), self.sync.index('fetch("/intr/profile"'))

    def test_installation_status_uses_device_local_target(self):
        self.assertIn('"MY_KV_INSTALLATION_STATUS":true', self.sync)
        self.assertIn('return loadTarget(recordClass);', self.sync)
        self.assertIn('if (recordClass && LOCAL_QUERY_CLASSES[recordClass] !== true) return loadRemoteTarget();', self.sync)

    def test_device_local_profile_is_non_authorizing_and_kv_scoped(self):
        for marker in (
            'state:"ACTIVE_SOVEREIGN_INTR_INGRESS"',
            'profiles:["KV:KnowledgeVaultInterlock"]',
            'event_triggered:true',
            'always_on_application_receiver_required:false',
            'second_user_device_required:false',
            'credential_authority:"TV/TVC"',
            'github_token_runtime_authority:"NONE"',
            'execution_authority:"NONE"',
            'authority_effect:"NONE_DISCOVERY_EVIDENCE_ONLY"',
        ):
            self.assertIn(marker,self.local_runtime)
        self.assertNotIn('profiles:["KV:KnowledgeVaultInterlock","SKAP_VAULT',self.local_runtime)

    def test_device_local_materialization_validates_exact_node_trigger_and_write_once(self):
        for marker in (
            'node_trigger_hash_mismatch',
            'node_outbox_entry_hash_mismatch',
            'materialization_request_hash_mismatch',
            'device_kv_destination_owner_mismatch',
            'write_once_collision:',
            'portable_file_sha256_mismatch',
            'runtime_execution_attempted:false',
            'consumer_dispatch_attempted:false',
            'claim_or_fence_minted:false',
            'g18_required:false',
            'authority_effect:"NONE_INGRESS_ONLY"',
        ):
            self.assertIn(marker,self.local_runtime)

    def test_device_local_installation_status_query_is_supported(self):
        for marker in (
            '"MY_KV_INSTALLATION_STATUS":true',
            'INSTALLATION_PROJECTION_SCHEMA="stegverse.kv.installation-status-projection/v1"',
            'query.selector.receipt_path==="_System/installation.receipt.json"',
            'state:"KV_INSTALLATION_NOT_VERIFIED"',
            'state:"KV_INSTALLATION_VERIFIED"',
            'resident_kv_root_observed:true',
            'installation_receipt_present:true',
            'current_cloud_provider_observation:false',
            'full_template_parity:"VALIDATED"',
            'response.receipt_path=q.selector.receipt_path',
            'response.selector={receipt_path:q.selector.receipt_path}',
            'directory_id:installation?null:q.selector.directory_id',
            'canonical_path:installation?null:q.selector.canonical_path',
        ):
            self.assertIn(marker,self.local_runtime)

    def test_device_local_personal_profile_read_write_is_supported(self):
        for marker in (
            '"PERSONAL_CONTACT_PROFILE":true',
            'PERSONAL_PROFILE_PATH="_Entities/Self/Personal_Contact_Profile.json"',
            'PERSONAL_PROFILE_READ_SCHEMA="stegverse.device-kv.personal-profile-response/v1"',
            'PERSONAL_PROFILE_WRITE_SCHEMA="stegverse.device-kv.profile-update-response/v1"',
            'q.operation==="REQUEST"',
            'q.operation==="COMMIT_CANDIDATE"',
            'candidate.candidate_type==="PERSONAL_CONTACT_PROFILE_REPLACE"',
            'candidate.requested_destination===PERSONAL_PROFILE_PATH',
            'state:"PROFILE_READ"',
            'state:"PROFILE_PERSISTED"',
            'exact_readback_verified:true',
            'personal_profile_exact_readback_failed',
            'personal_profile_secret_field_forbidden:',
        ):
            self.assertIn(marker, self.local_runtime)
        self.assertIn('"PERSONAL_CONTACT_PROFILE":true', self.sync)

    def test_device_local_query_return_preserves_hb_carrier_validation_contract(self):
        for marker in (
            'stegverse.heartbeat-intr-derived-carrier/v1',
            'stegverse.intr.hb-derived-carrier-binding/v1',
            'HB_ANCHOR_EPOCH=32',
            'HB_ANCHOR_UNIX_MS=1787511600000',
            'HB_PERIOD_MS=10',
            'HB_CHANNEL_COUNT=16',
            'response_transported_on_hb_derived_carrier:true',
            'exact_response_packet_recovered:true',
            'authority_effect:"NONE_CARRIER_ONLY"',
        ):
            self.assertIn(marker,self.local_runtime)

if __name__=="__main__":
    unittest.main()
