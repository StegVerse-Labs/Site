#!/usr/bin/env python3
"""Projection regressions; these tests establish local source behavior only."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("roadmap",ROOT/"scripts/check_economic_roadmap_projection.py")
MOD=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

class PublicEconomicRoadmapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline=json.loads((ROOT/"data/economy/public-release-benchmarks.v1.json").read_text())
    def test_initial_projection_pending(self):
        self.assertEqual(MOD.validate(self.baseline), [])
        self.assertEqual(sum(b["status"]=="VERIFIED_COMPLETE" for s in self.baseline["stages"] for b in s["benchmarks"]), 0)
    def test_premature_completion_denied(self):
        data=copy.deepcopy(self.baseline)
        data["stages"][0]["benchmarks"][0]["status"]="VERIFIED_COMPLETE"
        errors=MOD.validate(data)
        self.assertTrue(any("completed without" in x for x in errors))
    def test_stage_cannot_precede_previous_stage(self):
        data=copy.deepcopy(self.baseline)
        data["publication_posture"]="GOVERNED_PUBLISHED"
        data["generated_at"]="2026-09-22T00:00:00Z"
        second=data["stages"][1]
        second["status"]="VERIFIED_COMPLETE"
        for b in second["benchmarks"]:
            b.update(status="VERIFIED_COMPLETE",evidence_ref="public:synthetic-test-only",verified_at="2026-09-22T00:00:00Z")
        errors=MOD.validate(data)
        self.assertTrue(any("predecessor is not complete" in x for x in errors))
    def test_mutable_authority_prohibited(self):
        data=copy.deepcopy(self.baseline)
        data["authority_boundary"]["site_display_grants_completion"]=True
        self.assertTrue(any("site_display" in x for x in MOD.validate(data)))

    def test_ephemeral_external_ai_independent_of_native_mykv(self):
        data=self.baseline
        lanes=data["stage1_execution_lanes"]
        self.assertFalse(lanes["external_ai"]["requires_native_mykv_installation"])
        self.assertTrue(lanes["private_workspace"]["requires_native_mykv_installation"])
        b={x["id"]:x for x in data["stages"][0]["benchmarks"]}
        for bid in ("S1_CHATGPT","S1_CLAUDE"):
            gate=b[bid]
            self.assertFalse(gate["native_mykv_installation_prerequisite"])
            self.assertEqual(gate["execution_mode"],"EPHEMERAL_STEGBROWSER_WITH_GOVERNED_EXTERNAL_PROVIDER")
            self.assertIn("terminal_ephemeral_session_destruction",gate["required_proof"])
            self.assertIn("real_provider_request_and_usable_response",gate["required_proof"])
            self.assertEqual(gate["status"],"NOT_VERIFIED")
        self.assertEqual(len(data["stages"]),6)
        self.assertEqual(sum(len(s["benchmarks"]) for s in data["stages"]),16)
        self.assertEqual(MOD.validate(data), [])

    def test_source_only_provider_response_does_not_complete(self):
        data=copy.deepcopy(self.baseline)
        chat=data["stages"][0]["benchmarks"][2]
        chat.update(status="VERIFIED_COMPLETE",evidence_ref=None,verified_at=None)
        self.assertTrue(any("completed without" in x for x in MOD.validate(data)))

if __name__=="__main__":
    unittest.main()
