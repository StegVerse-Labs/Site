"""Folded groups keep the push / pull_request path filters their workflows had.

A group whose original filter does not match the event's changed files records
NOT_SELECTED (a run, never a skipped job); a group whose filter matches runs its steps.
"""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_catalog", ROOT / "tools/tasks/run_catalog.py")
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)
CATALOG = json.loads((ROOT / "tools/tasks/task_catalog.json").read_text(encoding="utf-8"))
GROUPS = {g["id"]: g for g in CATALOG["groups"]}


def cell(event, files, gid):
    return [c for c in rc.matrix(event, files)["include"] if c["group"] == gid][0]["selected"]


class GlobTests(unittest.TestCase):
    def test_star_stops_at_slash_and_double_star_does_not(self):
        self.assertTrue(rc.glob_regex("data/*.json").match("data/a.json"))
        self.assertFalse(rc.glob_regex("data/*.json").match("data/x/a.json"))
        self.assertTrue(rc.glob_regex("data/**").match("data/x/y/a.json"))
        self.assertTrue(rc.glob_regex("**/a.json").match("a.json"))
        self.assertTrue(rc.glob_regex("**/a.json").match("x/y/a.json"))

    def test_later_negation_removes_an_earlier_match(self):
        self.assertTrue(rc.path_matches(["docs/**", "!docs/skip.md"], "docs/a.md"))
        self.assertFalse(rc.path_matches(["docs/**", "!docs/skip.md"], "docs/skip.md"))

    def test_paths_ignore_runs_unless_every_file_is_ignored(self):
        filt = {"paths_ignore": ["docs/**"]}
        self.assertFalse(rc.filter_selects(filt, ["docs/a.md"]))
        self.assertTrue(rc.filter_selects(filt, ["docs/a.md", "src/a.py"]))

    def test_unknown_changed_files_select_everything(self):
        self.assertTrue(rc.filter_selects({"paths": ["only/this"]}, None))


class GroupSelectionTests(unittest.TestCase):
    def test_evaluator_group_runs_only_when_its_original_paths_change(self):
        gid = "evaluator-review-public-verification.verify"
        for event in ("push", "pull_request"):
            self.assertEqual(cell(event, ["README.md"], gid), "false")
            self.assertEqual(cell(event, ["data/session-orchestration-registry.json"], gid), "false")
            self.assertEqual(cell(event, ["scripts/check_evaluator_review_public.py"], gid), "true")
            self.assertEqual(cell(event, ["assets/evaluator-review.js"], gid), "true")
            self.assertEqual(cell(event, None, gid), "true")

    def test_a_change_to_the_folded_copy_or_its_steps_selects_the_group(self):
        gid = "evaluator-review-public-verification.verify"
        self.assertEqual(cell("push", ["tools/tasks/folded/evaluator-review-public-verification.yml"], gid), "true")
        self.assertEqual(cell("push", [f"tools/tasks/steps/{gid}/02-observe.sh"], gid), "true")

    def test_every_filtered_group_is_selected_by_each_of_its_own_literal_paths(self):
        for gid, group in GROUPS.items():
            for event, filt in (group.get("path_filters") or {}).items():
                for pattern in filt.get("paths", []):
                    if pattern.startswith("!") or any(ch in pattern for ch in "*?+["):
                        continue
                    self.assertEqual(cell(event, [pattern], gid), "true", (gid, event, pattern))

    def test_filters_match_the_folded_originals(self):
        try:
            import yaml
        except ImportError:
            return
        for gid, group in GROUPS.items():
            wf = Path((group.get("source") or {}).get("workflow", "")).name
            original = ROOT / "tools/tasks/folded" / wf
            if not wf or not original.is_file():
                continue
            doc = yaml.safe_load(original.read_text(encoding="utf-8"))
            on = doc.get(True, doc.get("on")) or {}
            for event in group["events"]:
                cfg = on.get(event) if isinstance(on, dict) else None
                has = bool(isinstance(cfg, dict) and (cfg.get("paths") or cfg.get("paths-ignore")))
                self.assertEqual(has, event in (group.get("path_filters") or {}), (gid, event))


if __name__ == "__main__":
    unittest.main()
