#!/usr/bin/env python3
"""Finalize the SV-COST five-lane handoff from a successful public receipt."""
from __future__ import annotations

import json
from pathlib import Path

RECEIPT = Path("papers/sv-cost-five-lane-public-verification.json")
HANDOFF = Path("papers/SV_COST_FIVE_LANE_MIRROR_HANDOFF.md")
START = "<!-- SV_COST_FIVE_LANE_PUBLIC_RECEIPT:BEGIN -->"
END = "<!-- SV_COST_FIVE_LANE_PUBLIC_RECEIPT:END -->"


def main() -> int:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if receipt.get("state") != "COMPLETE":
        raise SystemExit("public verification receipt is not COMPLETE")
    if receipt.get("http_status") != 200:
        raise SystemExit("public verification did not return HTTP 200")
    if receipt.get("all_required_markers_present") is not True:
        raise SystemExit("required public markers are incomplete")

    text = HANDOFF.read_text(encoding="utf-8")
    replacements = {
        "- Role: `CLAIMED_FOR_VALIDATION`": "- Role: `COMPLETE — CLAIM RELEASED`",
        "public_paper_body_verification: BLOCKED_RETRY_ISSUE_173": "public_paper_body_verification: PASS",
        "- Task completion: 7/8; terminal public-body verification is owned by issue `#173`.": "- Task completion: 8/8.",
        "- Validation: 5/6.": "- Validation: 6/6.",
        "- Propagation: 3/4; public index is verified, direct paper body remains unverified.": "- Propagation: 4/4.",
        "- Goal activation: 7/8.": "- Goal activation: 8/8.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    block = f"""{START}
## Terminal public-body verification

```text
state: COMPLETE
observed_at: {receipt['observed_at']}
http_status: {receipt['http_status']}
content_sha256: {receipt['content_sha256']}
workflow_run_id: {receipt.get('workflow_run_id')}
workflow_run_attempt: {receipt.get('workflow_run_attempt')}
all_required_markers_present: true
claim_released: SV-COST-FIVE-LANE-PUBLIC-BODY-VERIFY-001
issue_closure: StegVerse-Labs/Site#173
```

The deployed paper body returned HTTP 200 and contained every required lane value and bounded-claim marker. The validation claim is released. No unique implementation, publication, propagation, or observation work remains in the originating session.
{END}"""

    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()
        text = before + "\n\n" + block + ("\n\n" + after if after else "\n")
    else:
        text = text.rstrip() + "\n\n" + block + "\n"

    HANDOFF.write_text(text, encoding="utf-8")
    print("SV_COST_FIVE_LANE_HANDOFF_FINALIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
