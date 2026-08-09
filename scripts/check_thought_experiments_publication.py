#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORY = ROOT / "Thought-Experiments.html"
ARTICLE = ROOT / "thought-experiments" / "continuity-as-reconstructable-manifold-transition.html"
PDF = ROOT / "thought-experiments" / "continuity-as-reconstructable-manifold-transition.pdf"
INDEX = ROOT / "index.html"
REPORT = ROOT / "thought-experiments-publication.report.json"

REQUIRED_ARTICLE_MARKERS = [
    "Continuity as Reconstructable Manifold Transition",
    "Collapse(A<sub>N</sub>, G<sub>N</sub>, X<sub>A</sub>)",
    "single eigenvalue",
    "Residual multiplicity",
    "Continuity is not permission for a trajectory to continue",
    "Scaling the manifold",
    "Observation does not choose among completed solutions",
    "Working-formalism boundary",
]


def main() -> int:
    failures: list[str] = []
    for path in (CATEGORY, ARTICLE, PDF, INDEX):
        if not path.exists():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")

    if CATEGORY.exists():
        category = CATEGORY.read_text(encoding="utf-8")
        for marker in (
            "Thought Experiments",
            "thought-experiments/continuity-as-reconstructable-manifold-transition.html",
            "thought-experiments/continuity-as-reconstructable-manifold-transition.pdf",
        ):
            if marker not in category:
                failures.append(f"category missing marker: {marker}")

    if ARTICLE.exists():
        article = ARTICLE.read_text(encoding="utf-8")
        for marker in REQUIRED_ARTICLE_MARKERS:
            if marker not in article:
                failures.append(f"article missing marker: {marker}")

    if PDF.exists():
        raw = PDF.read_bytes()
        if not raw.startswith(b"%PDF-"):
            failures.append("PDF artifact lacks PDF header")
        if len(raw) < 2048:
            failures.append("PDF artifact unexpectedly small")

    if INDEX.exists() and "Thought-Experiments.html" not in INDEX.read_text(encoding="utf-8"):
        failures.append("index missing Thought Experiments navigation entry")

    report = {
        "schema_version": "1.0.0",
        "publication": "Continuity as Reconstructable Manifold Transition",
        "category": "Thought Experiments",
        "files_checked": [
            "Thought-Experiments.html",
            "thought-experiments/continuity-as-reconstructable-manifold-transition.html",
            "thought-experiments/continuity-as-reconstructable-manifold-transition.pdf",
            "index.html",
        ],
        "state": "PASS" if not failures else "FAIL",
        "failures": failures,
        "authority_effect": False,
        "activation_effect": False,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        print("THOUGHT_EXPERIMENTS_PUBLICATION=FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("THOUGHT_EXPERIMENTS_PUBLICATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
