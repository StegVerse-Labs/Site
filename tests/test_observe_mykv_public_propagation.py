import importlib.util
import json
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "observe_mykv_public_propagation.py"
SPEC = importlib.util.spec_from_file_location("observe_mykv_public_propagation", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)

SHELL = b"""<script src=\"/assets/stegverse-node-continuity.js?v=20260915-unified-mykv-v1\"></script>
single owner-facing installation surface
automatically establishes or reuses the minimal resident StegOS/Node substrate
report.resident_install_health!=='HEALTHY'
report.node.registered!==true
Installation stopped before KV-host selection.
There is no separate StegOS website or second owner installation step
"""

MANIFEST = json.dumps(
    {
        "display": "standalone",
        "start_url": "/my-kv-install.html?source=installed",
        "scope": "/",
    }
).encode("utf-8")

LOADER = b"""
/assets/stegos-node-idb-schema-compat.js
/stegos-bootstrap/stegos-bootstrap-impl.js
/stegos-bootstrap/device-local-autostart.js?v=20260915-unified-mykv-v1
/assets/stegverse-node-continuity-impl.js
/assets/stegos-resident-health.js?v=20260915-unified-mykv-v1
"""


class MyKVPublicPropagationObserverTests(unittest.TestCase):
    def bodies(self):
        return {
            "install_shell": SHELL,
            "manifest": MANIFEST,
            "node_continuity_loader": LOADER,
        }

    def test_current_contract_passes(self):
        checks = MODULE.validate(self.bodies())
        self.assertTrue(all(checks.values()), checks)

    def test_missing_registered_node_gate_fails_closed(self):
        bodies = self.bodies()
        bodies["install_shell"] = bodies["install_shell"].replace(
            b"report.node.registered!==true", b"missing-node-gate"
        )
        checks = MODULE.validate(bodies)
        self.assertFalse(checks["shell_required_markers"])

    def test_wrong_standalone_start_url_fails(self):
        bodies = self.bodies()
        bodies["manifest"] = json.dumps(
            {"display": "standalone", "start_url": "/wrong", "scope": "/"}
        ).encode("utf-8")
        checks = MODULE.validate(bodies)
        self.assertFalse(checks["manifest_standalone_start_url"])

    def test_missing_unified_loader_marker_fails(self):
        bodies = self.bodies()
        bodies["node_continuity_loader"] = bodies["node_continuity_loader"].replace(
            b"/assets/stegos-resident-health.js?v=20260915-unified-mykv-v1",
            b"/assets/stegos-resident-health.js",
        )
        checks = MODULE.validate(bodies)
        self.assertFalse(checks["loader_required_markers"])


if __name__ == "__main__":
    unittest.main()
