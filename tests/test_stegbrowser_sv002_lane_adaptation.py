from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class StegBrowserSV002LaneAdaptationTests(unittest.TestCase):
    def setUp(self):
        self.src = (ROOT / "assets/stegbrowser-manifest-runtime-materializer.js").read_text(encoding="utf-8")
        self.binding = json.loads((ROOT / "data/stegbrowser-manifest-runtime-binding.v1.json").read_text(encoding="utf-8"))

    def test_exact_goal_cosv_manifest_and_destination_bindings(self):
        self.assertEqual(self.binding["schema"], "stegverse.stegbrowser-universal-intr-invocation-binding/v1")
        self.assertEqual(self.binding["goal_task_id"], "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001")
        self.assertEqual(self.binding["cosv_task_vector"], "40000100100000")
        self.assertEqual(self.binding["manifest_task_id"], "STEG-BROWSER-RUNTIME-MATERIALIZATION-REMEDIATION-001")
        self.assertEqual(self.binding["route_owner"], "STEGVERSE")
        self.assertEqual(self.binding["outbound_interlock_intr_endpoint"], "STEGVERSE_OWNED_INTR_EGRESS_ENDPOINT")
        self.assertEqual(self.binding["far_end_receiver"], "STEGVERSE_OWNED_MIRROR_REFLECTOR")
        self.assertEqual(self.binding["far_end_receiver_role"], "OWNED_MIRROR_REFLECTOR")
        self.assertEqual(self.binding["expected_action"], "REFLECT_DECLARED_RECORDS_PACKET")
        self.assertEqual(self.binding["authority_effect"], "NONE_ROUTE_BINDING_ONLY")
        self.assertIn('var DESTINATION="StegBrowser:ManifestInvocation"', self.src)

    def test_preserves_validated_event_ephemeral_browser_mechanics(self):
        self.assertIn('BROWSER_WEB_WORKER_ON_VALID_STEGVERSE_NODE', self.src)
        self.assertIn('EVENT_EPHEMERAL', self.src)
        self.assertIn('URL.createObjectURL(new Blob([WORKER_SOURCE]', self.src)
        self.assertIn('new Worker(', self.src)
        self.assertNotIn('fetch(', self.src)
        self.assertNotIn('XMLHttpRequest', self.src)
        self.assertNotIn('WebSocket', self.src)

    def test_node_interlock_and_universal_intr_are_fail_closed(self):
        self.assertIn('stegos.node_intr_outbox_entry.v1', self.src)
        self.assertIn('stegverse.universal-intr-materialization-request/v1', self.src)
        self.assertIn('STEGOS_ECOSYSTEM', self.src)
        self.assertIn('node.node_id&&node.interlock_id&&node.registration_receipt_sha256', self.src)
        self.assertIn('destination_subsystem_mismatch', self.src)
        self.assertIn('request_authority_forbidden', self.src)
        self.assertIn('claim_fence_forbidden', self.src)

    def test_authority_boundaries_are_not_promoted(self):
        self.assertIn('claim_or_fence_minted:false', self.src)
        self.assertIn('request_grants_execution_authority:false', self.src)
        self.assertIn('r.github_token_runtime_authority==="NONE"', self.src)
        self.assertIn('r.credential_authority==="TV/TVC"', self.src)
        self.assertIn('NONE_RUNTIME_MATERIALIZATION_ONLY', self.src)
        self.assertNotIn('claim_or_fence_minted:true', self.src)
        self.assertNotIn('request_grants_execution_authority:true', self.src)

    def test_manifest_digest_is_exact_sha256_shape(self):
        value = self.binding["manifest_sha256"]
        self.assertRegex(value, r"^sha256:[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
