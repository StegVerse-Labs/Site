import unittest
from scripts.project_device_kv_intr_sync_target import project_target,sha256_hex,ProjectionError

def profile():
    return {
      "schema":"stegverse.universal-intr-profiled-ingress/v1",
      "state":"ACTIVE_SOVEREIGN_INTR_INGRESS","protocol":"InTr",
      "profile_path":"/intr/profile","materialization_path":"/intr/materialization",
      "profiles":["HIL:Ingress","KV:KnowledgeVaultInterlock"],
      "supported_origins":["STEGOS_NODE_OUTBOX"],
      "event_triggered":True,"always_on_application_receiver_required":False,
      "second_user_device_required":False,"g18_required":False,"tls_enabled":True,
      "credential_authority":"TV/TVC","github_token_runtime_authority":"NONE",
      "execution_authority":"NONE","authority_effect":"NONE_DISCOVERY_EVIDENCE_ONLY"
    }

def observation():
    p=profile()
    return {
      "schema":"stegverse.universal-intr-ingress-observation/v1",
      "observation_state":"OBSERVED_HTTPS_PROFILE","https_observed":True,"http_status":200,
      "credential_used":False,"github_token_runtime_authority":"NONE","execution_authority":"NONE",
      "authority_effect":"NONE_OBSERVATION_ONLY","observed_at":"2026-08-31T12:00:00Z",
      "evidence_ref":"receipts/runtime/profile.json","observed_profile_url":"https://node.example/intr/profile",
      "profile":p,"profile_sha256":sha256_hex(p)
    }

class Tests(unittest.TestCase):
    def test_projects_device_kv_target(self):
        out=project_target(observation())
        self.assertEqual(out["state"],"CONFORMING_SOVEREIGN_INTR_INGRESS")
        self.assertEqual(out["ingress_url"],"https://node.example/intr/materialization")
        self.assertTrue(out["device_kv_materialization_profile_observed"])
        self.assertFalse(out["runtime_materialization_observed"])
        self.assertFalse(out["canonical_kv_staging_observed"])

    def test_missing_device_kv_profile_fails(self):
        o=observation(); o["profile"]["profiles"]=["HIL:Ingress"]; o["profile_sha256"]=sha256_hex(o["profile"])
        with self.assertRaises(ProjectionError): project_target(o)

    def test_http_and_credentials_fail(self):
        o=observation(); o["https_observed"]=False
        with self.assertRaises(ProjectionError): project_target(o)
        o=observation(); o["credential_used"]=True
        with self.assertRaises(ProjectionError): project_target(o)

    def test_profile_hash_drift_fails(self):
        o=observation(); o["profile_sha256"]="0"*64
        with self.assertRaises(ProjectionError): project_target(o)

if __name__=="__main__": unittest.main()
