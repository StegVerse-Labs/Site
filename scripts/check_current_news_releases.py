#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "news-releases.html"
ARTICLE = ROOT / "news-releases" / "ai-is-becoming-infrastructure-sovereignty-must-go-further.html"
COHERENT_LIFE = ROOT / "papers" / "coherent-life-and-admissible-existence" / "index.html"
COMPANION = ROOT / "papers" / "coherent-life-companion" / "index.html"
EMPIRICAL_ADDENDUM = ROOT / "papers" / "coherent-life-and-admissible-existence" / "empirical-addendum-i.html"
ENTITY_ECONOMY = ROOT / "papers" / "stegverse-entity-economy" / "index.html"
ENTITY_ECONOMY_PDF = ROOT / "papers" / "stegverse-entity-economy" / "stegverse-entity-economy.pdf"
DISCOVERY = ROOT / "Papers.html"

PARENT_TITLE = "Coherent Life and Admissible Existence"
COMPANION_TITLE = "Coherent Life and Admissible Existence — Companion Extensions"
ADDENDUM_TITLE = "Empirical Addendum I — Unknown-Class Transformation at the Quantum-Gravitational Boundary"
ENTITY_TITLE = "The StegVerse Entity Economy"
SOUTH_KOREA_TITLE = "AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model."
PARENT_ROUTE = 'href="papers/coherent-life-and-admissible-existence/"'
COMPANION_ROUTE = 'href="papers/coherent-life-companion/"'
ADDENDUM_ROUTE = 'href="papers/coherent-life-and-admissible-existence/empirical-addendum-i.html"'


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def main():
    failures = []
    required_files = [
        (INDEX, "missing news-releases.html"),
        (ARTICLE, "missing inaugural news release"),
        (COHERENT_LIFE, "missing Coherent Life working-paper projection"),
        (COMPANION, "missing Coherent Life attached companion projection"),
        (EMPIRICAL_ADDENDUM, "missing legacy Empirical Addendum I deep-link projection"),
        (ENTITY_ECONOMY, "missing Entity Economy paper landing page"),
        (ENTITY_ECONOMY_PDF, "missing Entity Economy PDF"),
        (DISCOVERY, "missing Papers.html discovery surface"),
    ]
    for path, message in required_files:
        require(path.exists(), message, failures)
    if failures:
        print("CURRENT_NEWS_RELEASES_FAIL")
        for failure in failures:
            print(failure)
        return 1

    index = INDEX.read_text(encoding="utf-8")
    article = ARTICLE.read_text(encoding="utf-8")
    coherent_life = COHERENT_LIFE.read_text(encoding="utf-8")
    companion = COMPANION.read_text(encoding="utf-8")
    addendum = EMPIRICAL_ADDENDUM.read_text(encoding="utf-8")
    entity = ENTITY_ECONOMY.read_text(encoding="utf-8")
    discovery = DISCOVERY.read_text(encoding="utf-8")

    require("Current News Releases" in index, "landing title missing", failures)
    entries = re.findall(r'data-published="(\d{4}-\d{2}-\d{2})" data-sequence="(\d+)"', index)
    require(entries, "machine-readable publication ordering missing", failures)
    keys = [(date, int(sequence)) for date, sequence in entries]
    require(keys == sorted(keys, reverse=True), "news releases not reverse chronological/sequence order", failures)

    for title in (PARENT_TITLE, ENTITY_TITLE, SOUTH_KOREA_TITLE):
        require(title in index, f"news release entry missing: {title}", failures)
    require(PARENT_ROUTE in index, "Current News Releases must point to the Coherent Life parent paper", failures)
    require(COMPANION_ROUTE not in index, "Current News Releases must not promote the companion as a peer release", failures)
    require(ADDENDUM_ROUTE not in index, "Current News Releases must not expose a separate Empirical Addendum I release", failures)
    require(COMPANION_TITLE not in index, "Current News Releases must not present the companion as a second publication identity", failures)
    require(ADDENDUM_TITLE not in index, "Current News Releases must not expose the former standalone Empirical Addendum I title", failures)
    require("Working Formal Paper / Attached Companion Extensions" in index, "attached-companion release classification missing", failures)
    if all(title in index for title in (PARENT_TITLE, ENTITY_TITLE, SOUTH_KOREA_TITLE)):
        require(
            index.index(PARENT_TITLE) < index.index(ENTITY_TITLE) < index.index(SOUTH_KOREA_TITLE),
            "required Coherent Life -> Entity Economy -> South Korea ordering not preserved",
            failures,
        )

    require(PARENT_TITLE in coherent_life, "Coherent Life parent title missing", failures)
    require("Working Formal Paper" in coherent_life, "Coherent Life parent working-paper marker missing", failures)
    require("Conjoined Working Formal Paper" not in coherent_life, "Coherent Life parent must not remain over-integrated", failures)
    require("Empirical Application I" not in coherent_life, "Coherent Life parent must not embed Addendum I", failures)
    require("Attached companion materials" in coherent_life, "Coherent Life parent attached-companion section missing", failures)
    require('href="../coherent-life-companion/"' in coherent_life, "Coherent Life parent does not link its attached companion", failures)
    require("subordinate to and attached to this working paper" in coherent_life, "parent/companion hierarchy boundary missing", failures)

    require(COMPANION_TITLE in companion, "Coherent Life companion title missing", failures)
    require("does not replace or rewrite the original Coherent Life working paper" in companion, "companion parent-preservation boundary missing", failures)
    require("Notation Table and Theorem Witnesses" in companion, "companion notation/theorem component missing", failures)
    require("Unknown-Class Transformation at the Quantum-Gravitational Boundary" in companion, "companion Addendum I component missing", failures)
    require("Recoverable Capacity Across Representational Boundaries" in companion, "companion Addendum II component missing", failures)
    require("Observation ≠ Interpretation ≠ Established knowledge" in companion, "companion Addendum I preservation relation missing", failures)
    require("transition-then-project ≈ project-then-transition" in companion, "companion Addendum II representation-coherence relation missing", failures)

    require("Unknown-Class Transformation at the Quantum-Gravitational Boundary" in addendum, "legacy Empirical Addendum I deep link title missing", failures)

    require(SOUTH_KOREA_TITLE in article, "headline missing", failures)
    require("StegVerse LLC" in article, "company attribution missing", failures)
    require("sovereignty all the way down" in article, "key differentiator missing", failures)

    require(ENTITY_TITLE in entity, "Entity Economy title missing", failures)
    require('href="stegverse-entity-economy.pdf"' in entity, "Entity Economy PDF link missing", failures)

    require(PARENT_TITLE in discovery, "Coherent Life parent missing from Papers index", failures)
    require(PARENT_ROUTE in discovery, "Coherent Life parent Papers route missing", failures)
    require(COMPANION_ROUTE not in discovery, "Papers index must not promote companion to peer publication card", failures)
    require(COMPANION_TITLE not in discovery, "Papers index must expose one Coherent Life publication identity", failures)
    require(ADDENDUM_ROUTE not in discovery, "Papers index must not expose Addendum I as a peer publication", failures)
    require(ADDENDUM_TITLE not in discovery, "Papers index must not expose standalone Addendum I title", failures)
    require("Attached companion materials:" in discovery, "Papers index must describe attached companion under parent", failures)
    require("CURRENT FEATURED" in discovery, "Papers index featured publication marker missing", failures)
    require('href="news-releases.html"' in discovery, "public discovery link missing", failures)

    if failures:
        print("CURRENT_NEWS_RELEASES_FAIL")
        for failure in failures:
            print(failure)
        return 1
    print("CURRENT_NEWS_RELEASES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
