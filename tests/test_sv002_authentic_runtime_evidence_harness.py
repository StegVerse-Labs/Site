from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'sv002-observe/runtime-evidence-test.html').read_text()
JS=(ROOT/'assets/sv002-runtime-evidence-test.js').read_text()
NODE=(ROOT/'assets/stegverse-node-continuity.js').read_text()
SYNC=(ROOT/'stegos-node/sv002-intr-sync.js').read_text()
OBS=(ROOT/'assets/sv002-observe.js').read_text()
INVARIANTS=(ROOT/'data/sv002-viewer-evidence-invariants.v1.json').read_text()

class AuthenticRuntimeEvidenceHarnessTests(unittest.TestCase):
    def test_consumes_existing_node_instead_of_registering(self):
        self.assertIn('StegVerseNodeContinuity.status()',JS)
        self.assertIn('VALID_NODE_REQUIRED',JS)
        self.assertNotIn('registerDevice(',JS)
        self.assertIn('device_node_revalidation_performed:false',JS)
        self.assertIn('Receipt #1',HTML)

    def test_authentic_context_is_public_stegverse_https(self):
        self.assertIn('location.protocol==="https:"',JS)
        self.assertIn('location.hostname.toLowerCase()==="stegverse.org"',JS)
        self.assertIn('AUTHENTIC_EXTERNAL_CONTEXT_REQUIRED',JS)
        self.assertIn('credentials:"omit"',JS)

    def test_public_profile_must_explicitly_support_sv002(self):
        self.assertIn('SV002:PublicObservation',JS)
        self.assertIn('ACTIVE_SOVEREIGN_INTR_INGRESS',JS)
        self.assertIn('NONE_DISCOVERY_EVIDENCE_ONLY',JS)
        self.assertIn('/intr/profile',JS)
        self.assertIn('/intr/materialization',JS)

    def test_uses_production_node_and_intr_contracts(self):
        for marker in [
            'stegverse.universal-intr-materialization-request/v1',
            'DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION',
            'StegVerse-Labs/.github#493',
            'STEGOS_NODE_OUTBOX',
            'NONE_REQUEST_ONLY',
        ]:
            self.assertIn(marker,JS)
            self.assertTrue(marker in OBS or marker in SYNC or marker in NODE, marker)
        self.assertIn('StegVerseSV002InTrSync.buildTrigger',JS)
        self.assertIn('StegVerseSV002InTrSync.validateIngressReceipt',JS)
        self.assertIn('queueIntrMaterializationRequest',JS)

    def test_receiver_ready_is_observed_after_materialization(self):
        self.assertIn('/intr/sv002-observe/readiness',JS)
        self.assertIn('stegverse.sv002-public-observation-runtime-readiness/v1',JS)
        self.assertIn('j.state==="READY"',JS)
        self.assertIn('receiver_readiness:"NOT_OBSERVED"',JS)

    def test_round_trip_requires_received_then_forwarded(self):
        self.assertIn('dir==="ingress"?"RECEIVED":"FORWARDED"',JS)
        self.assertIn('egress.prior_receipt_hash===ingress.receipt_hash',JS)
        self.assertIn('AUTHENTIC_RUNTIME_ROUND_TRIP_OBSERVED',JS)
        self.assertIn('observation_ingress="OBSERVED_RECEIVED"',JS)
        self.assertIn('observation_egress="OBSERVED_FORWARDED"',JS)

    def test_does_not_overclaim_experiment_or_master_records(self):
        self.assertIn('master_records_reconstruction:"NOT_CLAIMED"',JS)
        self.assertIn('principal_experiment_execution:"NOT_CLAIMED"',JS)
        self.assertIn('authority_effect:"NONE"',JS)
        self.assertIn('This does not claim principal experiment execution or Master Records reconstruction.',JS)

    def test_observer_verifies_reconstructed_runtime_sequence(self):
        self.assertIn('verifyRuntimeEvidenceProjection',OBS)
        self.assertIn('ordered_transition_receipts',OBS)
        self.assertIn('repository_ledger_root',OBS)
        self.assertIn('organization_ledger_root',OBS)
        self.assertIn('repository ordered receipt root mismatch',OBS)
        self.assertIn('organization ledger does not include repository root',OBS)

    def test_viewer_invariant_profile_is_published(self):
        self.assertIn('/data/sv002-viewer-evidence-invariants.v1.json',OBS)
        self.assertIn('viewer_invariant_runtime_evidence',INVARIANTS)
        self.assertIn('viewer_bound_observation_evidence',INVARIANTS)
        self.assertIn('cross_viewer_reconstructed_runtime_evidence_equality_required',INVARIANTS)

    def test_evidence_is_phone_friendly(self):
        self.assertIn('Copy evidence',HTML)
        self.assertIn('Export JSON',HTML)
        self.assertIn('navigator.clipboard.writeText',JS)
        self.assertIn('application/json',JS)
        self.assertIn('condition_label:',JS)

if __name__=='__main__':
    unittest.main()
