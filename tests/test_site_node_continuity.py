from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
NODE=(ROOT/"assets/stegverse-node-continuity.js").read_text()
MYKV=(ROOT/"my-kv.html").read_text()
VA=(ROOT/"va-disability-claim-guide.html").read_text()
SIMPLE=(ROOT/"assets/ecosystem-chat-simple.js").read_text()
VARUNTIME=(ROOT/"assets/ecosystem-chat-va-runtime.js").read_text()

class NodeContinuityContractTests(unittest.TestCase):
    def test_unregistered_limit_is_ten(self):
        self.assertIn("MAX_UNREGISTERED_LLM = 10",NODE)
        self.assertIn("remaining: MAX_UNREGISTERED_LLM - used",NODE)
    def test_receipts_exclude_personal_values_and_credentials(self):
        self.assertIn("contains_personal_information: false",NODE)
        self.assertIn("contains_credentials: false",NODE)
        self.assertNotIn("email_address:",NODE)
        self.assertNotIn("password:",NODE)
    def test_personal_kv_sync_marker_is_privacy_bounded(self):
        self.assertIn('PERSONAL_KV_SYNC_KEY = "personal-kv-sync"', NODE)
        self.assertIn('function recordPersonalKvSync(input)', NODE)
        self.assertIn('schema: "stegos.node_personal_kv_sync_observation.v1"', NODE)
        self.assertIn('exact_readback_verified: true', NODE)
        self.assertIn('contains_personal_information: false', NODE)
        self.assertIn('contains_credentials: false', NODE)
        self.assertIn('recordPersonalKvSync: recordPersonalKvSync', NODE)
        self.assertIn('profile_class:"PERSONAL_FORM_PROFILE"', MYKV)
        self.assertIn('exact_readback_verified:true', MYKV)

    def test_my_kv_uses_five_node_backed_steps(self):
        self.assertEqual(MYKV.count("data-kv-step="),5)
        self.assertIn('node.capabilityProgress("my-kv-onboarding")',MYKV)
        self.assertIn('node.recordStep("my-kv-onboarding"',MYKV)

    def test_my_kv_registration_rechecks_before_mutation(self):
        self.assertIn('data-action="check">Check current registration</button>', MYKV)
        self.assertIn('function paintRegistrationControl(progress)', MYKV)
        self.assertIn('if(progress.registered)', MYKV)
        self.assertIn('registerButton.hidden=true', MYKV)
        self.assertIn('registrationRecheckConfirmedUnregistered', MYKV)
        self.assertIn('registerButton.dataset.action="register"', MYKV)
        self.assertIn('var current=await node.status();', MYKV)
        self.assertLess(
            MYKV.index('var current=await node.status();', MYKV.index('setStatus("kv-status-1","Registering…")')),
            MYKV.index('await node.registerDevice()', MYKV.index('setStatus("kv-status-1","Registering…")'))
        )
        self.assertIn('No new registration is required.', MYKV)
    def test_my_kv_portable_installation_bridge_fallback(self):
        bridge=(ROOT/"assets/my-kv-portable-installation-bridge.js").read_text()
        self.assertIn('if(!root || root.StegVerseKVInstallationBridge) return;', bridge)
        self.assertIn('input.addEventListener("cancel",onCancel)', bridge)
        self.assertIn('function onCancel(){', bridge)
        self.assertIn('returnedWithoutSelection();', bridge)
        self.assertIn('},2500);', bridge)
        self.assertIn('my-kv-portable-installation-bridge.js?v=20260902-device-local-receipt-r2', MYKV)
        self.assertIn('window.addEventListener("focus",onFocus)', bridge)
        self.assertIn('document.addEventListener("visibilitychange",onVisibility)', bridge)
        self.assertIn('existingInstallation:function()', bridge)
        self.assertIn('reused_prior_validated_proof:true', bridge)
        self.assertIn('current_cloud_observation:false', bridge)
        self.assertIn('stegverse.kv.portable-installation-proof.v1', bridge)
        self.assertIn('receipt.schema_version!=="1.1"', bridge)
        self.assertIn('full_template_parity!=="VALIDATED"', bridge)
        self.assertIn('receipt.authority_effect!=="NONE"||receipt.activation_effect!==false', bridge)
        self.assertIn('provider_specific_identifier_persisted:false', bridge)
        self.assertIn('credential_material_present:false', bridge)
        self.assertNotIn('destination_folder_id:', bridge)
        self.assertNotIn('localStorage.setItem(STORAGE_KEY,JSON.stringify(receipt))', bridge)
        self.assertIn('bridge_kind:"PORTABLE_OWNER_SELECTED_CANONICAL_RECEIPT"', bridge)
        self.assertIn('installAndVerify:function()', bridge)
        self.assertIn('verifyCloud:function()', bridge)
        self.assertIn('assets/my-kv-portable-installation-bridge.js', MYKV)
        self.assertIn('Connect / verify KV', MYKV)
        self.assertIn('_System/installation.receipt.json', MYKV)
        self.assertIn('installBridge.existingInstallation()', MYKV)
        self.assertIn('Live DEVICE_KV installation status was unavailable, so a previously validated installation proof was restored.', MYKV)
        self.assertIn('Current cloud state has not been reverified.', MYKV)
        self.assertIn('my-kv-portable-installation-bridge.js?v=', MYKV)
        self.assertIn('device_local_kv_materialization_observed', bridge)
        self.assertIn('var resident=await readLiveInstallationStatus();', MYKV)
        self.assertIn('KnowledgeVault installation receipt was admitted through DEVICE_KV and verified from the resident device-local KV.', MYKV)
        self.assertIn('function materializeReceipt(receipt)', bridge)
        self.assertIn('canonical_path:"_System"', bridge)
        self.assertIn('name:"installation.receipt.json"', bridge)
        self.assertIn('"inline://materialization_request.portable_payload"', bridge)
        self.assertIn('queueIntrMaterializationRequest(request)', bridge)
        self.assertIn('sync.synchronizeMaterialization(request.materialization_id)', bridge)
        self.assertIn('device_local_kv_materialization_observed', bridge)


    def test_my_kv_step2_prefers_live_device_kv_installation_status(self):
        query=(ROOT/"assets/my-kv-device-kv-query-bridge.js").read_text()
        self.assertIn('MY_KV_INSTALLATION_STATUS', query)
        self.assertIn('root.StegVerseKVInstallationStatusBridge', query)
        self.assertIn('getInstallationStatus:function()', query)
        self.assertIn('requester:{module:"Site",component:"MyKVOnboarding"}', query)
        self.assertIn('selector:{receipt_path:"_System/installation.receipt.json"}', query)
        self.assertIn('requested_scope:["installation_status"]', query)
        self.assertIn('installationStatusBridge=window.StegVerseKVInstallationStatusBridge||null', MYKV)
        self.assertIn('readLiveInstallationStatus()', MYKV)
        self.assertIn('KnowledgeVault installation verified from the current resident KV root over DEVICE_KV.', MYKV)
        click=MYKV.index('document.getElementById("kv-install").addEventListener')
        self.assertLess(MYKV.index('readLiveInstallationStatus()',click),MYKV.index('installBridge.installAndVerify()',click))
        self.assertIn('Cloud-provider revalidation remains Step 5.', MYKV)

    def test_va_node_is_optional(self):
        self.assertIn("Continue without Node",VA)
        self.assertIn("You can use the full VA Claims Guide without registering",VA)
        self.assertIn("vaClaimsNodeContinuityOptInV1",VA)
    def test_all_model_routes_check_entitlement(self):
        self.assertIn("beforeLlmRequest",SIMPLE)
        self.assertIn("recordLlmExecution",SIMPLE)
        self.assertIn("beforeLlmRequest",VARUNTIME)
        self.assertIn("recordLlmExecution",VARUNTIME)

if __name__=="__main__":
    unittest.main()
