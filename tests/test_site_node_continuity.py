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
    def test_my_kv_uses_five_node_backed_steps(self):
        self.assertEqual(MYKV.count("data-kv-step="),5)
        self.assertIn('node.capabilityProgress("my-kv-onboarding")',MYKV)
        self.assertIn('node.recordStep("my-kv-onboarding"',MYKV)
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
