"""Every `uses:` in .github/workflows must be a local path or a full-SHA pin with a `# <tag>` comment."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"

USES_LINE = re.compile(r"^\s*(?:-\s+)?uses:\s*(?P<rest>.*)$")
PINNED = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.\-/]+@[0-9a-f]{40} # \S+\s*$")
LOCAL = re.compile(r"^\./\S+\s*(?:#.*)?$")


def workflow_files():
    return sorted(list(WORKFLOWS.glob("*.yml")) + list(WORKFLOWS.glob("*.yaml")))


def unpinned_uses():
    bad = []
    count = 0
    for path in workflow_files():
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = USES_LINE.match(line)
            if not match:
                continue
            rest = match.group("rest").strip()
            count += 1
            if LOCAL.match(rest) or PINNED.match(rest):
                continue
            bad.append(f"{path.relative_to(ROOT)}:{lineno}: {line.strip()}")
    return count, bad


class WorkflowActionsPinnedTest(unittest.TestCase):
    def test_workflows_exist(self):
        self.assertTrue(workflow_files(), "no workflow files found")

    def test_every_uses_is_local_or_sha_pinned_with_tag_comment(self):
        count, bad = unpinned_uses()
        self.assertGreater(count, 0, "no uses: lines found")
        self.assertEqual(bad, [], "unpinned uses: lines:\n" + "\n".join(bad[:50]))


if __name__ == "__main__":
    unittest.main()
