#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "publication-manifest" / "media-pipeline.json"
PAGE = ROOT / "docs" / "media" / "media-pipeline-overview.md"
CHECKER = ROOT / "scripts" / "check_site_media_pipeline_mirror.py"
REQUIRED_KEYS = {
    "manifest_id",
    "manual_actions_required",
    "source_repo",
    "target_repo",
    "status",
    "artifacts",
    "downstream_repositories",
    "blocked_capabilities",
}
BLOCKED = {
    "live_camera_use",
    "live_microphone_use",
    "public_broadcast",
    "external_platform_streaming",
    "provider_execution",
}


def fail(message):
    print(f"FAIL {message}")
    return 1


def main():
    for path in [MANIFEST, PAGE, CHECKER]:
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")
        print(f"PASS {path.relative_to(ROOT)}")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    missing = sorted(REQUIRED_KEYS - set(data))
    if missing:
        return fail("missing manifest keys: " + ", ".join(missing))
    if data.get("manual_actions_required") is not False:
        return fail("manual_actions_required must be false")
    if data.get("source_repo") != "StegVerse-Labs/collective-environment-engine":
        return fail("unexpected source_repo")
    if data.get("target_repo") != "StegVerse-Labs/Site":
        return fail("unexpected target_repo")
    blocked = set(data.get("blocked_capabilities", []))
    if not BLOCKED.issubset(blocked):
        return fail("blocked capabilities incomplete")
    artifacts = data.get("artifacts", [])
    if len(artifacts) != 1:
        return fail("expected exactly one artifact")
    artifact = artifacts[0]
    if artifact.get("target_path") != "docs/media/media-pipeline-overview.md":
        return fail("unexpected artifact target_path")
    if artifact.get("publication_status") != "mirrored":
        return fail("artifact must be mirrored")
    if artifact.get("mirror_permitted") is not True:
        return fail("mirror_permitted must be true")
    if "scripts/check_site_media_pipeline_mirror.py" not in artifact.get("required_checks", []):
        return fail("required media pipeline checker missing")
    if artifact.get("boundary") != "planning_and_replay_only":
        return fail("boundary must be planning_and_replay_only")
    print("PASS publication manifest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
