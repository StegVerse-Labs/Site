from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HEALTH = (ROOT / "assets/stegos-resident-health.js").read_text(encoding="utf-8")
NODE_LOADER = (ROOT / "assets/stegverse-node-continuity.js").read_text(encoding="utf-8")
BOOT_LOADER = (ROOT / "stegos-bootstrap/stegos-bootstrap.js").read_text(encoding="utf-8")


class ResidentStegOSHealthTests(unittest.TestCase):
    def test_one_canonical_client_is_loaded_by_mykv_node_and_stegos_bootstrap(self):
        marker = '/assets/stegos-resident-health.js?v=20260915-v1'
        self.assertIn(marker, NODE_LOADER)
        self.assertIn(marker, BOOT_LOADER)
        self.assertIn('root.StegOSResidentHealth=Object.freeze', HEALTH)
        self.assertIn('DOMContentLoaded', HEALTH)
        self.assertIn('diagnose:diagnose', HEALTH)
        self.assertIn('repair:repair', HEALTH)

    def test_diagnostic_reports_required_health_dimensions(self):
        for marker in (
            'resident_install_health',
            'device_continuity',
            'schema_freshness',
            'service_worker',
            'governed_transition',
            'kv_host_relationship',
            'device_kv_query_emitted:false',
            'provider_operation_authorized:false',
            'kv_mutation_authorized:false',
            'authority_effect:"NONE"',
        ):
            self.assertIn(marker, HEALTH)

    def test_diagnostic_does_not_emit_device_kv_or_provider_operations(self):
        forbidden = (
            '.getInstallationStatus(',
            '.getDomainHealth(',
            '.listDirectory(',
            'synchronizeMaterialization(',
            'queueIntrMaterializationRequest(',
            'provider_operation_authorized:true',
        )
        for marker in forbidden:
            self.assertNotIn(marker, HEALTH)
        self.assertIn('diagnostic_emits_device_kv_query:false', HEALTH)

    def test_repair_preserves_valid_node_and_has_no_kv_mutation_surface(self):
        self.assertIn('if(baseline&&baseline.node_id)return Promise.resolve({state:"EXISTING_NODE_PRESERVED"', HEALTH)
        self.assertIn('if(!nodePreserved)throw new Error("FAIL_CLOSED: resident repair changed valid Node identity")', HEALTH)
        self.assertIn('if(!kvPreserved)throw new Error("FAIL_CLOSED: resident repair changed visible KV relationship state")', HEALTH)
        self.assertIn('kv_create_called:false', HEALTH)
        self.assertIn('kv_replace_called:false', HEALTH)
        self.assertIn('kv_renumber_called:false', HEALTH)
        self.assertIn('kv_migrate_called:false', HEALTH)
        self.assertIn('kv_rehost_called:false', HEALTH)
        self.assertNotIn('registerDevice(', HEALTH)

    def test_repair_uses_existing_stegos_bootstrap_and_same_origin_handoff(self):
        self.assertIn('registerOfflineShell', HEALTH)
        self.assertIn('reg.update()', HEALTH)
        self.assertIn('STEGOS_BOOTSTRAP_REQUIRED', HEALTH)
        self.assertIn('new URL(STEGOS_ENTRY_PATH+"?resident_repair=1",root.location.origin)', HEALTH)
        self.assertIn('repair_can_create_replace_renumber_migrate_rehost_kv:false', HEALTH)


if __name__ == "__main__":
    unittest.main()
