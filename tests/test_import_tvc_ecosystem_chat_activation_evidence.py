from __future__ import annotations
import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("site_tvc_import",ROOT/"scripts/import_tvc_ecosystem_chat_activation_evidence.py")
assert SPEC and SPEC.loader
mod=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(mod)

class SiteTvcImportTests(unittest.TestCase):
    def packet(self):
        p={
            "schema":"stegverse.tvc.ecosystem-chat-activation-evidence/v1",
            "state":"READY_FOR_SITE_IMPORT","source_projection_sha256":"projection","source_task_id":"SHWP-ECOSYSTEM-CHAT-INFERENCE-001","fencing_token":23,
            "same_execution":True,"persistent_conversational_runtime_ready":True,
            "credential_authority":"TV/TVC","credential_requirement":"NONE","credential_material_present":False,
            "github_token_required":False,"github_runtime_authority":"NONE",
            "route_authority_granted":False,"execution_authority_granted":False,"custody_authority_granted":False,
            "publication_authority_granted":False,"site_mutation_authority_granted":False,"site_mutation_performed":False,
            "publication_performed":False,"third_party_runtime_required":False,"authority_effect":"NONE_EVIDENCE_PERSISTENCE_ONLY"
        }
        p["packet_sha256"]=mod.canonical_hash(p)
        return p
    def test_imports_idempotently(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); src=root/"packet.json"; src.write_text(json.dumps(self.packet()))
            a=mod.import_packet(src,root); b=mod.import_packet(src,root)
            self.assertEqual(a["write_result"],"CREATED"); self.assertEqual(b["write_result"],"UNCHANGED")
            record=json.loads((root/mod.OUTPUT_REL).read_text())
            self.assertFalse(record["activation_authority_granted"]); self.assertEqual(record["github_runtime_authority"],"NONE")
            self.assertEqual(record["record_sha256"],mod.canonical_hash(record,"record_sha256"))
    def test_rejects_tamper(self):
        p=self.packet(); p["fencing_token"]=24
        with self.assertRaisesRegex(ValueError,"packet_hash"): mod.verify(p)
    def test_rejects_authority_escalation(self):
        p=self.packet(); p["publication_authority_granted"]=True; p["packet_sha256"]=mod.canonical_hash(p,"packet_sha256")
        with self.assertRaisesRegex(ValueError,"publication_authority_granted"): mod.verify(p)
if __name__=="__main__": unittest.main()
