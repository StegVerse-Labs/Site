#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "MEDIA_PIPELINE_DOWNSTREAM_PUBLICATION.md"
MANIFEST = ROOT / "data" / "publication-manifest" / "media-pipeline.json"
PAGE = ROOT / "docs" / "media" / "media-pipeline-overview.md"
REQUIRED_TARGETS = {
    "GCAT-BCAT-Engine/Publisher",
    "StegVerse-Labs/admissibility-wiki",
    "StegVerse-Labs/stegguardian-wiki",
}
REQUIRED_PACKET_MARKERS = [
    "packet_id: media_pipeline_downstream_publication_001",
    "manual_actions_required: false",
    "state: READY_FOR_DOWNSTREAM_SUMMARY",
    "source_manifest: data/publication-manifest/media-pipeline.json",
    "source_page: docs/media/media-pipeline-overview.md",
    "planning-and-replay only",
    "broadcast-engine",
    "live media execution remains out of scope",
]


def fail(message):
    print(f"FAIL {message}")
    return 1


def main():
    for path in [PACKET, MANIFEST, PAGE]:
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")
        print(f"PASS {path.relative_to(ROOT)}")
    packet_text = PACKET.read_text(encoding="utf-8")
    for marker in REQUIRED_PACKET_MARKERS:
        if marker not in packet_text:
            return fail(f"packet missing {marker}")
        print(f"PASS packet contains {marker}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    targets = set(manifest.get("downstream_repositories", []))
    if not REQUIRED_TARGETS.issubset(targets):
        return fail("manifest downstream target list incomplete")
    page_text = PAGE.read_text(encoding="utf-8")
    for blocked in ["does not claim live camera use", "does not claim live microphone use", "public broadcast"]:
        if blocked not in page_text:
            return fail(f"page missing boundary {blocked}")
        print(f"PASS page boundary {blocked}")
    print("PASS media pipeline downstream publication")
    return 0


if __name__ == "__main__":
    sys.exit(main())
