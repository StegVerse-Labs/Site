from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class SV002ExperimentRerunBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension = (ROOT / "intr-sv002-rerun-extension.js").read_text(encoding="utf-8")
        cls.worker = (ROOT / "intr-service-worker.js").read_text(encoding="utf-8")
        cls.launcher = (ROOT / "stegos-bootstrap/sv002-experiment-rerun.js").read_text(encoding="utf-8")
        cls.page = (ROOT / "sv002-rerun/index.html").read_text(encoding="utf-8")
        cls.handoff = (ROOT / "docs/STEGVERSE_002_EXPERIMENT_RERUN_MIRROR_HANDOFF.md").read_text(encoding="utf-8")
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_exact_invocation_identity(self):
        markers = (
            "STEGVERSE-002-EXPERIMENT-RERUN-001",
            "50000000107000",
            "STEGVERSE-002-EXPERIMENT-RERUN-001-REQUEST-001",
            "REQUEST_SELF_CHARACTERIZATION",
        )
        for marker in markers:
            self.assertIn(marker, self.extension)
            self.assertIn(marker, self.launcher)
            self.assertIn(marker, self.handoff)

    def test_existing_root_worker_and_node_outbox_are_reused(self):
        self.assertIn('importScripts("/intr-sv002-rerun-extension.js")', self.worker)
        self.assertIn("StegVerseNodeContinuity.status()", self.launcher)
        self.assertIn("StegVerseNodeContinuity.queueIntrMaterializationRequest(materialization)", self.launcher)

    def test_sdk_manifest_contract_is_bound(self):
        for marker in (
            "SDK-SV002-FIRST-SELF-CHARACTERIZATION-001",
            "StegVerse-SDK-Evaluator",
            "stegverse.external_organization.interlock_request.v1",
            "stegverse.external_organization.interaction_manifest.v1",
            "prescribe_self_ontology:false",
            "prescribe_formalism:false",
            "prescribe_transition_elements:false",
            "sdk_mints_intr_receipt:false",
            "sdk_claims_delivery:false",
        ):
            self.assertIn(marker, self.launcher)

    def test_request_binding_does_not_promote_downstream_state(self):
        for marker in (
            "request_bound_observed:true",
            "registered_stegverse_node_bound_to_invocation:true",
            "interlock_bound_to_node_and_manifest:true",
            "intr_materialization_admitted:true",
            "event_ephemeral_runtime_materialized:false",
            "workercoordinator_claim_observed:false",
            "principal_execution_transitions_retained:false",
            "egress_emitted:false",
            "master_records_custody_observed:false",
            "master_records_reconstruction_pass:false",
            "origin_return_observed:false",
        ):
            self.assertIn(marker, self.extension)

    def test_surface_and_docs_are_wired(self):
        self.assertIn("../assets/stegverse-node-continuity.js", self.page)
        self.assertIn("../stegos-bootstrap/sv002-experiment-rerun.js", self.page)
        self.assertIn("sv002-rerun/index.html", self.readme)

if __name__ == "__main__":
    unittest.main()
