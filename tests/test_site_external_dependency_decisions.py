"""Owner external-dependency decisions: each removal is prepared and selected by one flag.

Standard library only. Covers data/site-external-dependency-decisions.json, the Playwright gating
in four workflows, and scripts/apply_site_external_dependency_decisions.py for the paper page.
"""
from __future__ import annotations

import contextlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import apply_site_external_dependency_decisions as apply  # noqa: E402

CONFIG = ROOT / "data" / "site-external-dependency-decisions.json"
PAGE = "papers/single-lane-manifold-matrix-governance.html"
SIX_FIELDS = (
    "failure_code",
    "failed_predicate",
    "required_evidence_or_repair",
    "retry_entrypoint",
    "owning_existing_goal",
    "next_attempt",
)
GATE_OFF = "if: steps.dependency_decision.outputs.remove != 'true'"
GATE_ON = "if: steps.dependency_decision.outputs.remove == 'true'"
NOT_RUN = "Declare browser verification not run (owner removed Playwright)"
# Steps that need Playwright and must be skipped when the owner removes it.
GATED_STEPS = {
    "autonomy-telemetry.yml": ["Install browser runtime verifier"],
    "conectrr-live-verification.yml": ["Install remote-browser verifier", "Execute deployed Conectrr runtime in Chromium"],
    "entity-economy-volume-ii-public-observation.yml": [
        "Install established browser validation dependency",
        "Execute deployed bounded paper routes in Chromium",
    ],
    "stegmusic-browser-execution.yml": ["Install browser test dependencies", "Execute StegMusic browser runtime"],
}


def steps_of(path: Path) -> list[dict]:
    """Split a workflow's single job into steps (six-space '- ' items) without a YAML library."""
    steps, current = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("      - "):
            current = {"lines": [line]}
            steps.append(current)
        elif current is not None and (line.startswith("        ") or not line.strip()):
            current["lines"].append(line)
        elif current is not None:
            current = None
    for step in steps:
        text = "\n".join(step["lines"])
        step["text"] = text
        name = re.search(r"^      - name: (.+)$", text, re.M)
        step["name"] = name.group(1).strip() if name else None
        cond = re.search(r"^        (if: .+)$", text, re.M) or re.search(r"^      - (if: .+)$", text, re.M)
        step["if"] = cond.group(1).strip() if cond else None
        step["id"] = (re.search(r"^        id: (\S+)$", text, re.M) or [None, None])[1]
    return steps


def runs(step: dict, remove: bool) -> bool:
    """Whether a step runs for a flag value (only the decision gates matter here)."""
    if step["if"] == GATE_OFF:
        return not remove
    if step["if"] == GATE_ON:
        return remove
    return True


def heredoc(step: dict) -> str:
    match = re.search(r"python3 - <<'PY'\n(.*?)\n\s*PY", step["text"], re.S)
    assert match, step["name"]
    lines = match.group(1).splitlines()
    indent = min(len(l) - len(l.lstrip()) for l in lines if l.strip())
    return "\n".join(l[indent:] for l in lines) + "\n"


def decision_command(step: dict) -> str:
    match = re.search(r'run: python3 -c "(.*)" >> "\$GITHUB_OUTPUT"', step["text"])
    assert match, step["text"]
    return match.group(1)


class ConfigTest(unittest.TestCase):
    def test_schema_and_defaults(self):
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(config["schema"], "stegverse.site-external-dependency-decisions/v1")
        self.assertEqual(config["authority_effect"], "NONE")
        self.assertIn("Flip remove to true", config["note"])
        self.assertEqual(set(config["decisions"]), {"PLAYWRIGHT_BROWSER_VERIFICATION", "PAPER_MATHJAX_MARKED_CDN"})
        for decision in config["decisions"].values():
            self.assertIs(decision["remove"], False)
            self.assertTrue(decision["owner"].strip())
            self.assertTrue(decision["effect_when_removed"].strip())
        playwright = config["decisions"]["PLAYWRIGHT_BROWSER_VERIFICATION"]
        self.assertEqual(sorted(playwright["workflows"]), sorted(f".github/workflows/{n}" for n in GATED_STEPS))
        self.assertEqual(set(playwright["workflow_owners"]), set(playwright["workflows"]))
        for rel in playwright["workflows"] + playwright["scripts"]:
            self.assertTrue((ROOT / rel).is_file(), rel)
        self.assertEqual(config["decisions"]["PAPER_MATHJAX_MARKED_CDN"]["files"], [PAGE])
        apply.load_config(CONFIG)


class WorkflowGateTest(unittest.TestCase):
    def test_each_workflow_gates_playwright_on_the_flag(self):
        for name, gated in GATED_STEPS.items():
            with self.subTest(workflow=name):
                steps = steps_of(ROOT / ".github" / "workflows" / name)
                by_name = {s["name"]: s for s in steps}
                decision = [s for s in steps if s["id"] == "dependency_decision"]
                self.assertEqual(len(decision), 1)
                self.assertIsNone(decision[0]["if"])
                self.assertIn("data/site-external-dependency-decisions.json", decision[0]["text"])
                self.assertIn("PLAYWRIGHT_BROWSER_VERIFICATION", decision[0]["text"])
                self.assertLess(steps.index(decision[0]), min(steps.index(by_name[g]) for g in gated))
                for g in gated:
                    self.assertEqual(by_name[g]["if"], GATE_OFF, g)
                # Every step that installs or imports Playwright is gated off when removed.
                for step in steps:
                    if re.search(r"pip install[^\n]*playwright|playwright install", step["text"]):
                        self.assertEqual(step["if"], GATE_OFF, step["name"])
                not_run = by_name[NOT_RUN]
                self.assertEqual(not_run["if"], GATE_ON)
                self.assertNotIn("exit 1", not_run["text"])
                for field in SIX_FIELDS:
                    self.assertIn(f'"{field}":', not_run["text"])
                self.assertIn("EXTERNAL_DEPENDENCY_REMOVED_BROWSER_VERIFICATION_NOT_RUN", not_run["text"])
                self.assertIn(f'"retry_entrypoint": ".github/workflows/{name}"', not_run["text"])
                # remove=false: the Playwright steps run, the not-run declaration does not.
                for g in gated:
                    self.assertTrue(runs(by_name[g], remove=False))
                    self.assertFalse(runs(by_name[g], remove=True))
                self.assertFalse(runs(not_run, remove=False))
                self.assertTrue(runs(not_run, remove=True))
                # No other step is conditioned on the decision.
                touched = {s["name"] for s in steps if "dependency_decision" in (s["if"] or "")}
                self.assertEqual(touched, set(gated) | {NOT_RUN})

    def test_autonomy_runtime_verification_still_runs_and_fails_closed(self):
        steps = {s["name"]: s for s in steps_of(ROOT / ".github/workflows/autonomy-telemetry.yml")}
        runtime = steps["Execute runtime verification"]
        self.assertIsNone(runtime["if"])
        self.assertTrue(runs(runtime, remove=True))
        self.assertEqual(steps["Fail workflow when required runtime checks fail"]["if"], "if: steps.runtime.outcome == 'failure'")

    def test_decision_step_output_follows_the_flag(self):
        steps = [s for s in steps_of(ROOT / ".github/workflows/stegmusic-browser-execution.yml") if s["id"] == "dependency_decision"]
        command = decision_command(steps[0])
        for name in GATED_STEPS:
            other = [s for s in steps_of(ROOT / ".github" / "workflows" / name) if s["id"] == "dependency_decision"]
            self.assertEqual(decision_command(other[0]), command, name)
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "data").mkdir()
            config = json.loads(CONFIG.read_text(encoding="utf-8"))
            for flag, expected in ((False, "remove=false"), (True, "remove=true")):
                config["decisions"]["PLAYWRIGHT_BROWSER_VERIFICATION"]["remove"] = flag
                (Path(tmp) / "data/site-external-dependency-decisions.json").write_text(json.dumps(config), encoding="utf-8")
                out = subprocess.run([sys.executable, "-c", command], cwd=tmp, capture_output=True, text=True, check=True)
                self.assertEqual(out.stdout.strip(), expected)

    def test_not_run_step_writes_six_field_fail_closed_record(self):
        for name in GATED_STEPS:
            with self.subTest(workflow=name):
                step = {s["name"]: s for s in steps_of(ROOT / ".github" / "workflows" / name)}[NOT_RUN]
                with tempfile.TemporaryDirectory() as tmp:
                    out = subprocess.run([sys.executable, "-I", "-"], input=heredoc(step), cwd=tmp, capture_output=True, text=True)
                    self.assertEqual(out.returncode, 0, out.stderr)
                    record = json.loads(out.stdout)
                    files = list((Path(tmp) / "reports").glob("*.json"))
                    self.assertEqual(len(files), 1)
                    self.assertEqual(json.loads(files[0].read_text()), record)
                for field in SIX_FIELDS:
                    self.assertTrue(isinstance(record[field], str) and record[field].strip(), field)
                self.assertEqual(record["failure_code"], "EXTERNAL_DEPENDENCY_REMOVED_BROWSER_VERIFICATION_NOT_RUN")
                self.assertEqual(record["result"], "FAIL_CLOSED")
                self.assertIs(record["passed"], False)
                self.assertIs(record["browser_verification_performed"], False)
                self.assertIn("not performed", record["failed_predicate"])
                self.assertEqual(record["retry_entrypoint"], f".github/workflows/{name}")


class PaperDecisionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "papers").mkdir()
        (self.tmp / "data").mkdir()
        shutil.copy(ROOT / PAGE, self.tmp / PAGE)
        self.config = self.tmp / "data/site-external-dependency-decisions.json"
        self.write_flag(False)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write_flag(self, remove: bool):
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        config["decisions"]["PAPER_MATHJAX_MARKED_CDN"]["remove"] = remove
        self.config.write_text(json.dumps(config), encoding="utf-8")

    def run_script(self, *extra: str) -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return apply.main(["--root", str(self.tmp), "--config", str(self.config), *extra])

    def test_committed_page_matches_committed_flag(self):
        config = apply.load_config(CONFIG)
        remove = config["decisions"]["PAPER_MATHJAX_MARKED_CDN"]["remove"]
        text = (ROOT / PAGE).read_text(encoding="utf-8")
        self.assertEqual(apply.check_page(remove, text), [])
        if not remove:
            self.assertEqual(text.count("https://cdn.jsdelivr.net/npm/"), 2)

    def test_remove_false_leaves_page_unchanged(self):
        before = (self.tmp / PAGE).read_bytes()
        self.assertEqual(self.run_script(), 0)
        self.assertEqual((self.tmp / PAGE).read_bytes(), before)
        self.assertEqual(self.run_script("--check"), 0)

    def test_remove_true_rewrites_without_cdn_and_is_idempotent(self):
        self.write_flag(True)
        self.assertEqual(self.run_script("--check"), 1)  # guard: flag flipped, page not regenerated
        self.assertEqual(self.run_script(), 0)
        once = (self.tmp / PAGE).read_text(encoding="utf-8")
        self.assertNotIn("cdn.jsdelivr.net", once)
        self.assertNotRegex(once, r"<script[^>]*\bsrc=")
        self.assertIn(apply.MARKER, once)
        self.assertIn("pre.textContent=md", once)
        self.assertIn("removed by owner decision PAPER_MATHJAX_MARKED_CDN", once)
        self.assertNotIn("marked.parse", once.split("showUnformattedSource();")[0].split("function showUnformattedSource")[1])
        self.assertEqual(self.run_script(), 0)
        self.assertEqual((self.tmp / PAGE).read_text(encoding="utf-8"), once)
        self.assertEqual(self.run_script("--check"), 0)
        # Flipping back without restoring the page also fails closed.
        self.write_flag(False)
        self.assertEqual(self.run_script("--check"), 1)

    def test_guard_fails_closed_on_remove_true_with_jsdelivr(self):
        text = (ROOT / PAGE).read_text(encoding="utf-8")
        problems = apply.check_page(True, text)
        self.assertTrue(any("cdn.jsdelivr.net" in p for p in problems))
        tampered = apply.remove_dependencies(text).replace(apply.MARKER, apply.MARKER + '\n<script src="https://cdn.jsdelivr.net/npm/x"></script>')
        self.assertTrue(apply.check_page(True, tampered))
        with self.assertRaises(apply.DecisionError):
            apply.remove_dependencies(tampered)

    def test_unrecognised_page_fails_closed(self):
        self.write_flag(True)
        (self.tmp / PAGE).write_text("<html><script src=\"https://cdn.jsdelivr.net/npm/marked\"></script></html>", encoding="utf-8")
        self.assertEqual(self.run_script(), 1)


if __name__ == "__main__":
    unittest.main()
