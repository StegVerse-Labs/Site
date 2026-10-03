import importlib.util
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "observe_site_homepage_chat_assets.py"
SPEC = importlib.util.spec_from_file_location("observer", MODULE_PATH)
observer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(observer)

class HomepageChatAssetObserverTests(unittest.TestCase):
    def test_repository_assets_have_required_markers(self):
        for name, target in observer.TARGETS.items():
            body = (observer.ROOT / target["path"]).read_bytes()
            checks = observer.validate_body(name, body)
            self.assertTrue(checks["exact_repository_bytes"])
            self.assertTrue(checks["required_markers_present"])

    def test_changed_public_bytes_fail_exact_digest(self):
        name = "ecosystem_chat_simple"
        body = (observer.ROOT / observer.TARGETS[name]["path"]).read_bytes() + b"\n// changed"
        checks = observer.validate_body(name, body)
        self.assertFalse(checks["exact_repository_bytes"])

    def test_observation_is_non_authorizing_propagation_only(self):
        def fake_fetch(url, attempt):
            for target in observer.TARGETS.values():
                if target["url"] == url:
                    return 200, (observer.ROOT / target["path"]).read_bytes()
            raise AssertionError(url)
        with mock.patch.object(observer, "fetch", side_effect=fake_fetch):
            receipt = observer.observe(Path("/tmp/site-homepage-chat-observer-test"), attempts=1, delay_seconds=0)
        self.assertEqual(receipt["result"], "PASS")
        self.assertEqual(receipt["observation_class"], "PUBLIC_ASSET_PROPAGATION_ONLY")
        self.assertFalse(receipt["registered_node_execution_observed"])
        self.assertFalse(receipt["receipt_1_bound_browser_execution_observed"])
        self.assertEqual(receipt["authority_effect"], "NONE")
        self.assertEqual(receipt["credential_requirement"], "NONE")

if __name__ == "__main__":
    unittest.main()
