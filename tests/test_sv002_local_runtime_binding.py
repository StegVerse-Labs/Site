from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class SV002LocalRuntimeBindingTests(unittest.TestCase):
    def test_observer_binds_queued_materialization_to_canonical_local_runtime(self):
        html=(ROOT/"sv002-observe/index.html").read_text(encoding="utf-8")
        obs=(ROOT/"assets/sv002-observe.js").read_text(encoding="utf-8")
        local=(ROOT/"assets/sv002-local-runtime-materializer.js").read_text(encoding="utf-8")
        self.assertIn("sv002-local-runtime-materializer.js",html)
        self.assertIn("StegVerseSV002LocalRuntime.materialize(queued)",obs)
        self.assertIn("BROWSER_WEB_WORKER_ON_VALID_STEGVERSE_NODE",local)
        self.assertIn("EVENT_EPHEMERAL",local)
        self.assertIn("SV002:PublicObservation",local)
        self.assertIn('credential_authority:"TV/TVC"',local)
        self.assertIn('github_token_runtime_authority:"NONE"',local)
        self.assertIn('principal_execution_state:"AWAITING_QUALIFYING_LOCAL_PRINCIPAL"',local)
        self.assertNotIn("GITHUB_TOKEN",local)
        self.assertNotIn("RENDER",local)
        self.assertNotIn("VERCEL",local)

if __name__=="__main__":
    unittest.main()
