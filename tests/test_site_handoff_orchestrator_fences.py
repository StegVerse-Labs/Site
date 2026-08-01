#!/usr/bin/env python3
"""Regression checks for Site handoff workload extraction."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "site_handoff_orchestrator.py"

spec = importlib.util.spec_from_file_location("site_handoff_orchestrator", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_language_qualified_fences_are_parsed() -> None:
    handoff = """
# Handoff
## Remaining work
Destination `StegVerse-Labs/Site`:

```text
Add captured-versus-derived inspection and downstream projection permission controls
```

Destination `StegVerse-org/LLM-adapter`:

```text
Create canonical governed events before rendering
```

## Machine-owned continuation
"""
    observed = module.extract_remaining_work(handoff)
    assert observed == [
        {
            "destination": "StegVerse-Labs/Site",
            "workload": "Add captured-versus-derived inspection and downstream projection permission controls",
        },
        {
            "destination": "StegVerse-org/LLM-adapter",
            "workload": "Create canonical governed events before rendering",
        },
    ]


def test_branch_tokens_map_to_projection_workload() -> None:
    branch_tokens = module.normalized("goal/rtg-tt-downstream-projection".replace("/", " ").replace("-", " "))
    workload_tokens = module.normalized(
        "Add captured-versus-derived inspection and downstream projection permission controls"
    )
    assert branch_tokens & workload_tokens


if __name__ == "__main__":
    test_language_qualified_fences_are_parsed()
    test_branch_tokens_map_to_projection_workload()
    print("PASS: Site handoff fenced workload regression")
