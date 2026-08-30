from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class CanonicalRuntimeProofSurfaceTests(unittest.TestCase):
    def setUp(self):
        self.js=(ROOT/"assets/canonical-runtime-proof.js").read_text(encoding="utf-8")
        self.html=(ROOT/"canonical-runtime-proof/index.html").read_text(encoding="utf-8")

    def test_consumes_existing_node_and_never_registers(self):
        self.assertIn("StegVerseNodeContinuity.status",self.js)
        self.assertIn("VALID_NODE_REQUIRED",self.js)
        self.assertNotIn("registerDevice(",self.js)

    def test_accepts_existing_web_bootstrap_continuity(self):
        self.assertIn('"stegos-web-bootstrap-v1"',self.js)
        self.assertIn('"stegos.web_node.v1"',self.js)
        self.assertIn('"stegos.web_device_node_binding_receipt.v1"',self.js)
        self.assertIn('"LIVE_EXISTING_WEB_BOOTSTRAP"',self.js)
        self.assertIn('"stegos.web_canonical_runtime_closure_receipt.v1"',self.js)

    def test_real_isolated_runtime_is_materialized(self):
        self.assertIn("new Worker(",self.js)
        self.assertIn('type:"READY"',self.js)
        self.assertIn("worker.terminate()",self.js)
        self.assertIn('"LEASE_CLOSED"',self.js)

    def test_canonical_receipt_sequence_is_strict(self):
        self.assertIn('"RECEIVED"',self.js)
        self.assertIn('"FORWARDED"',self.js)
        self.assertIn("egress.prior_receipt_hash===ingress.receipt_hash",self.js)
        self.assertIn("bounded_operations_executed===1",self.js)

    def test_evidence_retained_before_release_and_node_receipt_appended(self):
        self.assertIn("EVIDENCE_RETAINED_PRE_RELEASE",self.js)
        self.assertIn("evidence_retained_before_release:true",self.js)
        self.assertIn('recordStep(CAPABILITY,"lease-closed","OBSERVED"',self.js)

    def test_authentic_origin_is_stegverse_org_only(self):
        self.assertIn('location.protocol==="https:"&&location.hostname==="stegverse.org"',self.js)

    def test_page_autoruns_and_exposes_evidence_controls(self):
        self.assertIn("canonical-runtime-proof.js",self.html)
        self.assertIn('id="copyBtn"',self.html)
        self.assertIn('id="exportBtn"',self.html)
        self.assertIn("run().catch",self.js)

if __name__=="__main__":
    unittest.main()
