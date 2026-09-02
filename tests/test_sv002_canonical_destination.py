from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class SV002CanonicalDestinationTests(unittest.TestCase):
    def test_local_runtime_matches_generated_intr_profile_destination(self):
        generated=(ROOT/"assets/generated/site-browser-intr-connectors.js").read_text(encoding="utf-8")
        materializer=(ROOT/"assets/sv002-local-runtime-materializer.js").read_text(encoding="utf-8")
        worker=(ROOT/"assets/sv002-principal-worker.js").read_text(encoding="utf-8")
        expected='subsystem":"SV002:ObservationProjection"'
        self.assertIn(expected,generated)
        self.assertIn('SV002:ObservationProjection',materializer)
        self.assertIn('SV002:ObservationProjection',worker)
        self.assertNotIn('SV002:PublicObservation',materializer)
        self.assertNotIn('SV002:PublicObservation',worker)

if __name__=="__main__":
    unittest.main()
