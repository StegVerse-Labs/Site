#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "Papers.html"
PAPER = ROOT / "papers" / "knowledgevault" / "conversation-continuity.html"
DOC = ROOT / "docs" / "KNOWLEDGEVAULT_PAPER_PUBLICATION.md"


def require(path: Path, text: str) -> None:
    if not path.is_file():
        raise SystemExit(f"missing:{path.relative_to(ROOT)}")
    body = path.read_text(encoding="utf-8")
    if text not in body:
        raise SystemExit(f"missing_text:{path.relative_to(ROOT)}:{text}")


def main() -> int:
    require(PAPERS, "papers/knowledgevault/conversation-continuity.html")
    require(PAPERS, "What If We Stopped Storing Conversations")
    require(PAPER, "working local-first prototype")
    require(PAPER, "The larger production architecture")
    require(PAPER, "StegVerse-Labs/continuity-vault-kit")
    require(DOC, "Site role: public display and discovery surface only")
    require(DOC, "does not independently validate")
    print("OK: KnowledgeVault conversation continuity paper publication is bounded and linked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
