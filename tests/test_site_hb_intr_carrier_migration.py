from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class SiteHBInTrCarrierMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sv=(ROOT/"assets/sv002-observe.js").read_text()
        cls.sv_page=(ROOT/"sv002-observe/index.html").read_text()
        cls.hil=(ROOT/"assets/hil-direct-upload-v1.js").read_text()
        cls.hil_page=(ROOT/"humans-as-interoperability-layer.html").read_text()
        cls.carrier=(ROOT/"assets/hb-intr-carrier.js").read_text()

    def test_sv002_uses_shared_carrier_before_request_hash(self):
        self.assertIn("StegVerseHBInTrCarrier.buildBinding",self.sv)
        self.assertIn("carrier_binding:binding",self.sv)
        self.assertIn('body.request_hash="sha256:"+await sha256(body)',self.sv)

    def test_hil_uses_shared_carrier_before_request_hash(self):
        self.assertIn("StegVerseHBInTrCarrier",self.hil)
        self.assertIn("carrier_binding: binding",self.hil)
        self.assertIn("body.request_hash = await digestJsonUri(body)",self.hil)

    def test_shared_carrier_validates_and_recovers_return_signals(self):
        for marker in (
            "function validateBinding(",
            "function recoverSignal(",
            "stegverse.heartbeat-intr-derived-carrier/v1",
            "packet_base64",
            "packet_sha256",
            "NONE_CARRIER_ONLY",
            "derived_carrier_grants_execution_authority",
            "HB carrier binding sha256 mismatch",
        ):
            self.assertIn(marker,self.carrier)

    def test_script_load_order(self):
        self.assertLess(self.sv_page.index("../assets/hb-intr-carrier.js"),self.sv_page.index("../assets/sv002-observe.js"))
        self.assertLess(self.hil_page.index("assets/hb-intr-carrier.js"),self.hil_page.index("assets/hil-direct-upload-v1.js"))

if __name__=="__main__":
    unittest.main()
