#!/usr/bin/env python3
"""Negative tests: Site source cannot award authenticated roadmap progress."""
import copy
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/project_economic_roadmap_subgoals.py"
spec = importlib.util.spec_from_file_location("economic_subgoals", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

DIGEST = "a" * 64


def trusted(evidence):
    """Stand-in for an authenticated Publisher custody verifier."""
    return True


def authoritative(benchmark_id, overrides=None):
    entry = {
        "evidence_class": "MASTER_RECORDS_VERIFIED",
        "evidence_ref": f"master-records://receipt/{benchmark_id}",
        "benchmark_id": benchmark_id,
        "synthetic": False,
        "master_records_state": "RECORDED",
        "reconstruction_status": "PASS",
        "required_evidence_validation_status": "PASS",
        "receipt_sha256": DIGEST,
        "reconstructed_receipt_sha256": DIGEST,
    }
    entry.update(overrides or {})
    return entry


class SubgoalProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((ROOT / "data/economy/public-release-benchmarks.v1.json").read_text())

    def gate(self, output, benchmark_id):
        return next(b for b in output["benchmarks"] if b["benchmark_id"] == benchmark_id)

    def predicates(self, benchmark_id):
        return self.gate(module.project(self.source), benchmark_id)["outstanding_subgoals_list"]

    def evidence(self, benchmark_id, make_entry, source="PUBLISHER_GOVERNED_PROJECTION"):
        return {
            "schema": "stegverse.economic-roadmap-evidence/v1",
            "source": source,
            "benchmarks": {benchmark_id: {p: make_entry(p) for p in self.predicates(benchmark_id)}},
        }

    def test_exact_sixteen_no_verified_subgoals(self):
        output = module.project(self.source)
        self.assertEqual(output["benchmark_count"], 16)
        self.assertEqual(len({b["benchmark_id"] for b in output["benchmarks"]}), 16)
        self.assertEqual(output["authority_effect"], "NONE")
        for b in output["benchmarks"]:
            self.assertEqual(b["verified_subgoals"], 0)
            self.assertEqual(b["completed_subgoals"], [])
            self.assertGreater(b["outstanding_subgoals"], 0)
            self.assertEqual(b["public_benchmark_status"], "NOT_VERIFIED")
            self.assertEqual(b["governed_completion_disposition"], "NOT_ELIGIBLE")
            self.assertTrue(b["stage_name"] and b["criterion"] and b["next_executable_repair"])
            self.assertTrue(all(p["evidence_ref"] is None for p in b["acceptance_predicates"]))

    def test_non_authoritative_evidence_classes_cannot_satisfy(self):
        for evidence_class in ("SOURCE_VALIDATED", "CI_VALIDATED", "PR_MERGED", "ISSUE_CLOSED",
                               "SYNTHETIC_FIXTURE", "RUNTIME_OBSERVED"):
            with self.subTest(evidence_class=evidence_class):
                evidence = self.evidence("S1_CHATGPT", lambda p: authoritative("S1_CHATGPT", {"evidence_class": evidence_class}))
                gate = self.gate(module.project(self.source, evidence), "S1_CHATGPT")
                self.assertEqual(gate["verified_subgoals"], 0)
                self.assertEqual(gate["governed_completion_disposition"], "NOT_ELIGIBLE")
                self.assertTrue(all(p["status"] == "OBSERVED_NOT_AUTHORITATIVE" for p in gate["acceptance_predicates"]))

    def test_each_missing_closure_predicate_fails_closed(self):
        cases = {
            "correct_benchmark_identity": {"benchmark_id": "S1_CLAUDE"},
            "master_records_state_RECORDED": {"master_records_state": "PENDING"},
            "reconstruction_PASS": {"reconstruction_status": "FAIL"},
            "required_evidence_validation_PASS": {"required_evidence_validation_status": None},
            "exact_receipt_digest_equality": {"reconstructed_receipt_sha256": "b" * 64},
            "evidence_not_declared_non_synthetic": {"synthetic": True},
            "evidence_ref_missing": {"evidence_ref": ""},
        }
        for expected, overrides in cases.items():
            with self.subTest(expected=expected):
                evidence = self.evidence("S1_CHATGPT", lambda p: authoritative("S1_CHATGPT", overrides))
                gate = self.gate(module.project(self.source, evidence), "S1_CHATGPT")
                self.assertEqual(gate["verified_subgoals"], 0)
                self.assertEqual(gate["governed_completion_disposition"], "FAIL_CLOSED")
                self.assertEqual(gate["failed_predicate"], expected)

    def test_missing_digest_is_not_equality(self):
        evidence = self.evidence("S1_CHATGPT", lambda p: authoritative(
            "S1_CHATGPT", {"receipt_sha256": None, "reconstructed_receipt_sha256": None}))
        gate = self.gate(module.project(self.source, evidence), "S1_CHATGPT")
        self.assertEqual(gate["failed_predicate"], "exact_receipt_digest_equality")

    def test_evidence_outside_publisher_projection_is_refused(self):
        evidence = self.evidence("S1_CHATGPT", lambda p: authoritative("S1_CHATGPT"), source="SITE_LOCAL")
        gate = self.gate(module.project(self.source, evidence), "S1_CHATGPT")
        self.assertEqual(gate["failed_predicate"], "evidence_not_from_publisher_governed_projection")

    def test_non_allow_disposition_is_preserved_as_failure(self):
        evidence = self.evidence("S1_CHATGPT", lambda p: {"disposition": "DENY", "failed_predicate": "exact_external_intr_ingress_allow"})
        gate = self.gate(module.project(self.source, evidence), "S1_CHATGPT")
        self.assertEqual(gate["governed_completion_disposition"], "FAIL_CLOSED")
        self.assertEqual(gate["failed_predicate"], "exact_external_intr_ingress_allow")

    def test_full_proof_is_only_eligible_for_review_never_verified(self):
        evidence = self.evidence("S1_CHATGPT", lambda p: authoritative("S1_CHATGPT"))
        output = module.project(self.source, evidence, provenance_verifier=trusted)
        self.assertEqual(output["evidence_provenance"], "AUTHENTICATED_BY_INJECTED_VERIFIER")
        gate = self.gate(output, "S1_CHATGPT")
        self.assertEqual(gate["outstanding_subgoals"], 0)
        self.assertEqual(gate["governed_completion_disposition"], "ELIGIBLE_FOR_PUBLISHER_GOVERNED_REVIEW")
        self.assertEqual(gate["public_benchmark_status"], "NOT_VERIFIED")

    def test_unbound_benchmark_never_eligible(self):
        evidence = self.evidence("S1_MYKV_AI", lambda p: authoritative("S1_MYKV_AI"))
        gate = self.gate(module.project(self.source, evidence, provenance_verifier=trusted), "S1_MYKV_AI")
        self.assertEqual(gate["outstanding_subgoals"], 0)
        self.assertEqual(gate["governed_completion_disposition"], "NOT_ELIGIBLE")
        self.assertIn("Register a canonical Task Registry binding", gate["next_executable_repair"])

    def test_self_declared_publisher_source_cannot_satisfy(self):
        evidence = self.evidence("S1_CHATGPT", lambda p: authoritative("S1_CHATGPT"))
        output = module.project(self.source, evidence)
        self.assertEqual(output["evidence_provenance"], "SELF_DECLARED_UNAUTHENTICATED")
        gate = self.gate(output, "S1_CHATGPT")
        self.assertEqual(gate["verified_subgoals"], 0)
        self.assertEqual(gate["governed_completion_disposition"], "NOT_ELIGIBLE")
        self.assertTrue(all(p["status"] == "OBSERVED_UNAUTHENTICATED_PROVENANCE" for p in gate["acceptance_predicates"]))

    def test_rejected_provenance_fails_closed(self):
        evidence = self.evidence("S1_CHATGPT", lambda p: authoritative("S1_CHATGPT"))
        output = module.project(self.source, evidence, provenance_verifier=lambda doc: False)
        self.assertEqual(output["evidence_provenance"], "VERIFIER_REJECTED")
        gate = self.gate(output, "S1_CHATGPT")
        self.assertEqual(gate["governed_completion_disposition"], "FAIL_CLOSED")
        self.assertEqual(gate["failed_predicate"], "publisher_provenance_unauthenticated")

    def test_verifier_must_return_exactly_true(self):
        evidence = self.evidence("S1_CHATGPT", lambda p: authoritative("S1_CHATGPT"))
        gate = self.gate(module.project(self.source, evidence, provenance_verifier=lambda doc: "yes"), "S1_CHATGPT")
        self.assertEqual(gate["failed_predicate"], "publisher_provenance_unauthenticated")

    def test_cli_with_full_evidence_is_never_eligible(self):
        evidence = self.evidence("S1_CHATGPT", lambda p: authoritative("S1_CHATGPT"))
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(evidence, handle)
        try:
            result = subprocess.run([sys.executable, str(SCRIPT), "--evidence", handle.name],
                                    capture_output=True, text=True, check=True)
        finally:
            Path(handle.name).unlink()
        gate = self.gate(json.loads(result.stdout), "S1_CHATGPT")
        self.assertEqual(gate["governed_completion_disposition"], "NOT_ELIGIBLE")
        self.assertEqual(gate["verified_subgoals"], 0)

    def test_tampered_public_status_fails_closed(self):
        source = copy.deepcopy(self.source)
        source["stages"][0]["benchmarks"][2]["status"] = "VERIFIED_COMPLETE"
        source["ci_checks"] = "SUCCESS"
        source["issue_closed"] = True
        gate = self.gate(module.project(source), "S1_CHATGPT")
        self.assertEqual(gate["governed_completion_disposition"], "FAIL_CLOSED")
        self.assertEqual(gate["failed_predicate"], "public_status_without_governed_proof")

    def test_identity_and_invariant_drift_raise(self):
        dropped = copy.deepcopy(self.source)
        dropped["authority_boundary"]["required_for_complete"].remove("exact_receipt_digest_equality")
        with self.assertRaises(ValueError):
            module.project(dropped)
        duplicate = copy.deepcopy(self.source)
        duplicate["stages"][1]["benchmarks"].append(copy.deepcopy(duplicate["stages"][0]["benchmarks"][0]))
        with self.assertRaises(ValueError):
            module.project(duplicate)
        with self.assertRaises(ValueError):
            module.project(self.source, {"schema": "stegverse.economic-roadmap-evidence/v1",
                                         "source": "PUBLISHER_GOVERNED_PROJECTION",
                                         "benchmarks": {"S9_UNKNOWN": {}}})
        with self.assertRaises(ValueError):
            module.project(self.source, {"schema": "other", "benchmarks": {}})

    def test_binding_not_promoted_to_authority(self):
        output = module.project(self.source)
        bound = self.gate(output, "S1_CHATGPT")
        unbound = self.gate(output, "S1_MYKV_AI")
        self.assertEqual(bound["binding_state"], "OBSERVED_NOT_AUTHORIZING")
        self.assertEqual(bound["binding_provenance"], "REGISTRY_ASSERTED")
        self.assertEqual(unbound["binding_state"], "UNRESOLVED")
        self.assertIsNone(unbound["canonical_task_id"])

    def test_ephemeral_runtime_predicates_independent(self):
        output = module.project(self.source)
        for bid in ("S1_CHATGPT", "S1_CLAUDE"):
            names = {p["predicate"] for p in self.gate(output, bid)["acceptance_predicates"]}
            self.assertIn("real_provider_request_and_usable_response", names)
            self.assertIn("terminal_ephemeral_session_destruction", names)
            self.assertIn("governed_publication_closure", names)


    def test_verifier_exception_fails_closed_without_escape(self):
        evidence = self.evidence("S1_CHATGPT", lambda p: authoritative("S1_CHATGPT"))
        def broken_verifier(_):
            raise RuntimeError("custody service unavailable")
        output = module.project(self.source, evidence, provenance_verifier=broken_verifier)
        gate = self.gate(output, "S1_CHATGPT")
        self.assertEqual(output["evidence_provenance"], "VERIFIER_REJECTED")
        self.assertEqual(gate["governed_completion_disposition"], "FAIL_CLOSED")
        self.assertEqual(gate["failed_predicate"], "publisher_provenance_unauthenticated")

    def test_malformed_evidence_maps_rejected(self):
        for invalid in ([], "untrusted", 7):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    module.project(self.source, invalid)
        for malformed in ([], "not-a-map", 17):
            with self.subTest(malformed=malformed):
                with self.assertRaises(ValueError):
                    module.project(self.source, {"schema": module.EVIDENCE_SCHEMA,
                                                 "benchmarks": malformed})
                with self.assertRaises(ValueError):
                    module.project(self.source, {"schema": module.EVIDENCE_SCHEMA,
                                                 "benchmarks": {"S1_CHATGPT": malformed}})

    def test_cli_emits_read_only_projection(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=True)
        output = json.loads(result.stdout)
        self.assertEqual(output["benchmark_count"], 16)
        self.assertEqual(output["authority_effect"], "NONE")


class PublishedSubgoalViewTests(unittest.TestCase):
    """The Site view renders the committed projection of a pinned Publisher export copy."""

    def setUp(self):
        self.economy = ROOT / "data/economy"
        self.record = json.loads((self.economy / "economic-roadmap-evidence.mirror.json").read_text())

    def test_mirror_is_byte_exact_publisher_copy(self):
        raw = (ROOT / self.record["target_path"]).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        self.assertEqual(self.record["source_repository"], "GCAT-BCAT-Engine/Publisher")
        self.assertRegex(self.record["source_commit_sha"], r"^[0-9a-f]{40}$")
        self.assertEqual(blob, self.record["source_git_blob_sha"])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), self.record["target_sha256"])
        self.assertIs(self.record["provenance_authenticated"], False)
        self.assertEqual(self.record["authority_effect"], "NONE")

    def test_committed_projection_matches_projector(self):
        source = json.loads((self.economy / "public-release-benchmarks.v1.json").read_text())
        evidence = json.loads((ROOT / self.record["target_path"]).read_text())
        committed = json.loads((self.economy / "economic-roadmap-subgoals.v1.json").read_text())
        self.assertEqual(committed, module.project(source, evidence))
        self.assertEqual(committed["evidence_provenance"], "SELF_DECLARED_UNAUTHENTICATED")
        self.assertTrue(all(b["governed_completion_disposition"] != "ELIGIBLE_FOR_PUBLISHER_GOVERNED_REVIEW"
                            for b in committed["benchmarks"]))

    def test_page_reads_only_local_projections_and_never_sets_check_marks_from_subgoals(self):
        page = (ROOT / "economic-roadmap.html").read_text()
        fetched = re.findall(r"fetch\('([^']+)'", page)
        self.assertEqual(sorted(fetched), ["data/economy/economic-roadmap-subgoals.v1.json",
                                           "data/economy/public-release-benchmarks.v1.json"])
        subgoal_code = page[page.index("function showSubgoals"):page.index("function loadSubgoals")]
        self.assertNotIn("VERIFIED_COMPLETE", subgoal_code)
        self.assertNotIn("accepted", subgoal_code)

    @unittest.skipUnless(shutil.which("node"), "node is required to syntax-check the page script")
    def test_page_script_parses(self):
        page = (ROOT / "economic-roadmap.html").read_text()
        script = page[page.rindex("<script>") + len("<script>"):page.rindex("</script>")]
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
            handle.write(script)
        try:
            subprocess.run(["node", "--check", handle.name], check=True, capture_output=True, text=True)
        finally:
            Path(handle.name).unlink()

if __name__ == "__main__":
    unittest.main()
