#!/usr/bin/env python3
"""Render Site TT code-representation status from a propagated TT bundle.

This renderer is intentionally fail-closed for operational status. If the TT
bundle is not present, it writes a pending mirror page rather than inventing
canonical data.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = REPO_ROOT / "data/tt/transition-element-propagation-bundle.manifest.json"
OUTPUT_MD = REPO_ROOT / "docs/SITE_TT_CODE_REPRESENTATION_STATUS.md"
OUTPUT_JSON = REPO_ROOT / "docs/SITE_TT_CODE_REPRESENTATION_STATUS.json"


def load_bundle() -> dict[str, Any] | None:
    if not BUNDLE_PATH.exists():
        return None
    return json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))


def render_pending(generated_at: str) -> tuple[str, dict[str, Any]]:
    status = {
        "generated_at": generated_at,
        "status": "PENDING",
        "canonical_source": "Admissible-Existence/TT",
        "reason": "No propagated TT bundle found at data/tt/transition-element-propagation-bundle.manifest.json.",
        "fail_closed": True,
    }
    markdown = f"""# Site TT Code Representation Status

## Assumptions

1. `Admissible-Existence/TT` is the canonical source for TT code-representation artifacts.
2. Site may render mirrored status, but it must not infer canonical TT state.
3. Missing propagated bundle means Site status remains pending and downstream consumers should fail closed.

## Status

```text
Status: PENDING
Generated at: {generated_at}
Canonical source: Admissible-Existence/TT
Reason: No propagated TT bundle found at data/tt/transition-element-propagation-bundle.manifest.json.
Fail closed: true
```

## Next Required Input

```text
data/tt/transition-element-propagation-bundle.manifest.json
```

This page is displayed without asserting operational TT mirror completeness.
"""
    return markdown, status


def render_bundle(bundle: dict[str, Any], generated_at: str) -> tuple[str, dict[str, Any]]:
    artifacts = bundle.get("artifacts", [])
    missing = [artifact for artifact in artifacts if not artifact.get("exists")]
    status_name = "PASS" if not missing else "FAIL_CLOSED"
    status = {
        "generated_at": generated_at,
        "status": status_name,
        "canonical_source": bundle.get("canonical_source", "Admissible-Existence/TT"),
        "bundle_id": bundle.get("bundle_id"),
        "artifact_count": bundle.get("artifact_count", len(artifacts)),
        "missing_count": len(missing),
        "fail_closed": bool(missing),
    }

    rows = [
        "| Path | iOS Display Path | Exists | SHA-256 | Bytes |",
        "|---|---|---:|---|---:|",
    ]
    for artifact in artifacts:
        rows.append(
            "| {path} | {ios} | {exists} | `{sha}` | {bytes} |".format(
                path=artifact.get("path", ""),
                ios=artifact.get("ios_display_path", ""),
                exists=str(artifact.get("exists", False)).lower(),
                sha=artifact.get("sha256", ""),
                bytes=artifact.get("bytes", ""),
            )
        )

    markdown = "\n".join([
        "# Site TT Code Representation Status",
        "",
        "## Assumptions",
        "",
        "1. `Admissible-Existence/TT` is the canonical source for TT code-representation artifacts.",
        "2. Site renders a propagated bundle manifest and does not redefine TT semantics.",
        "3. Missing artifacts cause fail-closed mirror status.",
        "",
        "## Status",
        "",
        "```text",
        f"Status: {status_name}",
        f"Generated at: {generated_at}",
        f"Canonical source: {status['canonical_source']}",
        f"Bundle id: {status['bundle_id']}",
        f"Artifact count: {status['artifact_count']}",
        f"Missing count: {status['missing_count']}",
        f"Fail closed: {str(status['fail_closed']).lower()}",
        "```",
        "",
        "## Artifacts",
        "",
        *rows,
        "",
        "## Authority Boundary",
        "",
        "A rendered Site status page does not grant execution authority. SPE must still reconstruct current standing before any commit boundary is allowed.",
        "",
    ])
    return markdown, status


def main() -> int:
    generated_at = datetime.now(timezone.utc).isoformat()
    bundle = load_bundle()
    if bundle is None:
        markdown, status = render_pending(generated_at)
    else:
        markdown, status = render_bundle(bundle, generated_at)

    OUTPUT_MD.write_text(markdown, encoding="utf-8")
    OUTPUT_JSON.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status["status"], "markdown": str(OUTPUT_MD.relative_to(REPO_ROOT)), "json": str(OUTPUT_JSON.relative_to(REPO_ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
