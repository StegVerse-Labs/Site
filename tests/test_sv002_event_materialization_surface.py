from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SV002EventMaterializationSurfaceTests(unittest.TestCase):
    def test_page_provisions_materialization_before_observation(self):
        html = (ROOT / "sv002-observe/index.html").read_text(encoding="utf-8")
        self.assertIn('materialization_endpoint: "/intr/materialization"', html)
        self.assertIn('../assets/sv002-materialization.js', html)
        self.assertLess(html.index('../assets/sv002-materialization.js'), html.index('../assets/sv002-observe.js'))

    def test_materialization_is_node_bound_non_authorizing_and_g18_independent(self):
        js = (ROOT / "assets/sv002-materialization.js").read_text(encoding="utf-8")
        for required in (
            'stegverse.universal-intr-transport/v1',
            'stegverse.universal-intr-materialization-request/v1',
            'STEGOS_NODE_OUTBOX',
            'SV002:PublicObservation',
            'always_on_receiver_required:false',
            'second_user_device_required:false',
            'request_grants_execution_authority:false',
            'claim_or_fence_minted:false',
            'credential_authority:"TV/TVC"',
            'github_token_runtime_authority:"NONE"',
            'observer_direct_relation_to_stegverse_002!==false',
        ):
            self.assertIn(required, js)
        self.assertNotIn('authorization', js.lower())

    def test_observation_materializes_then_retries_same_read_only_request(self):
        js = (ROOT / "assets/sv002-observe.js").read_text(encoding="utf-8")
        materialize = 'StegVerseSV002Materialization.ensure(node,request)'
        transact = 'transactExactReadOnly(connector,request)'
        self.assertIn(materialize, js)
        self.assertIn(transact, js)
        self.assertLess(js.index(materialize), js.index(transact))
        self.assertIn('operation:"READ_OBSERVATION"', js)
        self.assertIn('authority_transfer:false', js)
        self.assertIn('materialization_ingress', js)


if __name__ == "__main__":
    unittest.main()
