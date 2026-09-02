from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class SV002SelfContainedRuntimeTests(unittest.TestCase):
    def test_local_runtime_has_no_secondary_http_fetch_dependency(self):
        src=(ROOT/"assets/sv002-local-runtime-materializer.js").read_text(encoding="utf-8")
        self.assertIn("EMBEDDED_PRINCIPAL_SOURCE",src)
        self.assertIn("EMBEDDED_WORKER_SOURCE",src)
        self.assertIn("EMBEDDED_MODEL_MANIFEST_TEXT",src)
        self.assertIn("URL.createObjectURL(new Blob([source]",src)
        self.assertNotIn('fetch("/data/sv002-principal/',src)
        self.assertNotIn('new Worker("/assets/sv002-principal-worker.js',src)
        self.assertIn('model_id==="stegverse-sv002-evidence-principal-v1"',src)

if __name__=="__main__":
    unittest.main()
