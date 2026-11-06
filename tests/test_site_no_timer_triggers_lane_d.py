"""Lane D: timer-driven (cron) runs are not manifest-bound state transitions.

The heartbeat orchestration gate and the HIL live probe must not be started
by a `schedule:` trigger. Liveness/availability observations are never
authority, and an unavailable receiver is answered by durable queue or
event-ephemeral materialization, never by polling on a timer. Both
workflows remain runnable on demand through `workflow_dispatch`.

Stdlib only: the `on:` block is extracted and its top-level trigger keys are
read by indentation, so no YAML dependency is required.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
LANE_D_WORKFLOWS = (
    "ecosystem-heartbeat-orchestration.yml",
    "hil-live-probe.yml",
)


def trigger_keys(text: str) -> set:
    """Return the top-level trigger names declared under the `on:` key."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if re.match(r"^(on|['\"]on['\"]|true)\s*:\s*(#.*)?$", line):
            start = index
            break
        inline = re.match(r"^(on|['\"]on['\"])\s*:\s*(\S.*)$", line)
        if inline:
            value = inline.group(2).split("#", 1)[0].strip()
            return {item.strip(" '\"") for item in value.strip("[]").split(",") if item.strip()}
    if start is None:
        raise AssertionError("workflow has no top-level `on:` block")

    keys = set()
    child_indent = None
    for line in lines[start + 1:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0:
            break
        if child_indent is None:
            child_indent = indent
        if indent == child_indent:
            match = re.match(r"^\s*['\"]?([A-Za-z_][\w-]*)['\"]?\s*:", line)
            if match:
                keys.add(match.group(1))
    return keys


class NoTimerTriggersLaneDTest(unittest.TestCase):
    def test_parser_detects_schedule(self):
        sample = "name: x\non:\n  push:\n  schedule:\n    - cron: '1 * * * *'\njobs: {}\n"
        self.assertEqual(trigger_keys(sample), {"push", "schedule"})

    def test_lane_d_workflows_have_no_schedule_trigger(self):
        for name in LANE_D_WORKFLOWS:
            with self.subTest(workflow=name):
                text = (WORKFLOWS / name).read_text(encoding="utf-8")
                keys = trigger_keys(text)
                self.assertNotIn("schedule", keys)
                self.assertNotRegex(text, r"(?m)^\s*-?\s*cron\s*:")

    def test_lane_d_workflows_remain_dispatchable(self):
        for name in LANE_D_WORKFLOWS:
            with self.subTest(workflow=name):
                keys = trigger_keys((WORKFLOWS / name).read_text(encoding="utf-8"))
                self.assertIn("workflow_dispatch", keys)


if __name__ == "__main__":
    unittest.main()
