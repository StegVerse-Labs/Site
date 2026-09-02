from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class SV002UniqueObservationAttemptTests(unittest.TestCase):
    def test_each_observation_attempt_has_unique_identity_before_hashing(self):
        src=(ROOT/"assets/sv002-observe.js").read_text(encoding="utf-8")
        self.assertIn('attempt_id:"SV002-OBS-"+crypto.randomUUID()',src)
        self.assertIn('created_at:new Date().toISOString()',src)
        self.assertLess(src.index('attempt_id:"SV002-OBS-"+crypto.randomUUID()'),src.index('request.request_sha256=await sha256(request)'))

if __name__=="__main__":
    unittest.main()
