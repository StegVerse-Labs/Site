#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "news-releases.html"
ARTICLE = ROOT / "news-releases" / "ai-is-becoming-infrastructure-sovereignty-must-go-further.html"
COHERENT_LIFE = ROOT / "papers" / "coherent-life-and-admissible-existence" / "index.html"
EMPIRICAL_ADDENDUM = ROOT / "papers" / "coherent-life-and-admissible-existence" / "empirical-addendum-i.html"
ENTITY_ECONOMY = ROOT / "papers" / "stegverse-entity-economy" / "index.html"
ENTITY_ECONOMY_PDF = ROOT / "papers" / "stegverse-entity-economy" / "stegverse-entity-economy.pdf"
DISCOVERY = ROOT / "Papers.html"

PARENT_TITLE = "Coherent Life and Admissible Existence"
ADDENDUM_TITLE = "Empirical Addendum I — Unknown-Class Transformation at the Quantum-Gravitational Boundary"
ENTITY_TITLE = "The StegVerse Entity Economy"
SOUTH_KOREA_TITLE = "AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model."
PARENT_ROUTE = 'href="papers/coherent-life-and-admissible-existence/"'
ADDENDUM_ROUTE = 'href="papers/coherent-life-and-admissible-existence/empirical-addendum-i.html"'


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def main():
    failures = []
    required_files = [
        (INDEX, "missing news-releases.html"),
        (ARTICLE, "missing inaugural news release"),
        (COHERENT_LIFE, "missing Coherent Life and Admissible Existence public projection"),
        (EMPIRICAL_ADDENDUM, "missing Empirical Addendum I public projection"),
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
    addendum = EMPIRICAL_ADDENDUM.read_text(encoding="utf-8")
    entity = ENTITY_ECONOMY.read_text(encoding="utf-8")
    discovery = DISCOVERY.read_text(encoding="utf-8")

    require("Current News Releases" in index, "landing title missing", failures)
    entries = re.findall(r'data-published="(\d{4}-\d{2}-\d{2})" data-sequence="(\d+)"', index)
    require(entries, "machine-readable publication ordering missing", failures)
    keys = [(date, int(sequence)) for date, sequence in entries]
    require(keys == sorted(keys, reverse=True), "news releases not reverse chronological/sequence order", failures)

    for title in (PARENT_TITLE, ADDENDUM_TITLE, ENTITY_TITLE, SOUTH_KOREA_TITLE):
        require(title in index, f"news release entry missing: {title}", failures)
    require(PARENT_ROUTE in index, "Coherent Life canonical Site route missing from Current News Releases", failures)
    require(ADDENDUM_ROUTE in index, "Empirical Addendum I route missing from Current News Releases", failures)
    if all(title in index for title in (PARENT_TITLE, ADDENDUM_TITLE, ENTITY_TITLE, SOUTH_KOREA_TITLE)):
        require(
            index.index(PARENT_TITLE)
            < index.index(ADDENDUM_TITLE)
            < index.index(ENTITY_TITLE)
            < index.index(SOUTH_KOREA_TITLE),
            "required parent -> addendum -> Entity Economy -> South Korea ordering not preserved",
            failures,
        )

    require(PARENT_TITLE in coherent_life, "Coherent Life public projection title missing", failures)
    require("Canonical research owner: <code>Admissible-Existence/AE</code>" in coherent_life, "Coherent Life canonical research ownership boundary missing", failures)
    require('href="empirical-addendum-i.html"' in coherent_life, "Coherent Life page does not link its empirical addendum", failures)
    require("Public display does not create empirical validation" in coherent_life, "Coherent Life authority/non-validation boundary missing", failures)

    require("Unknown-Class Transformation at the Quantum-Gravitational Boundary" in addendum, "Empirical Addendum I title missing", failures)
    require("does not claim that the cited experiment validates Admissible Existence" in addendum, "Empirical Addendum validation boundary missing", failures)
    require("10.1126/sciadv.aec8045" in addendum, "Empirical Addendum primary DOI missing", failures)
    require("Observation → Constraint → Unknown transformation → Admissible interpretation" in addendum, "Empirical Addendum transition relation missing", failures)
    require("Public display does not establish empirical validation of Admissible Existence" in addendum, "Empirical Addendum public authority boundary missing", failures)

    require(SOUTH_KOREA_TITLE in article, "headline missing", failures)
    require("StegVerse LLC" in article, "company attribution missing", failures)
    require("sovereignty all the way down" in article, "key differentiator missing", failures)
    require("Ministry of Science and ICT" in article, "primary source reference missing", failures)
    require("TechSpot" in article, "secondary source reference missing", failures)
    require("does not itself establish execution, activation, custody, certification, admissibility, or release authority" in article, "authority boundary missing", failures)

    require(ENTITY_TITLE in entity, "Entity Economy title missing", failures)
    require("VALUE SHOULD BE ATTRIBUTABLE" in entity, "Entity Economy design thesis missing", failures)
    require('href="stegverse-entity-economy.pdf"' in entity, "Entity Economy PDF link missing", failures)

    require(PARENT_TITLE in discovery, "Coherent Life missing from Papers index", failures)
    require(ADDENDUM_TITLE in discovery, "Empirical Addendum I missing from Papers index", failures)
    require(PARENT_ROUTE in discovery, "Coherent Life Papers index route missing", failures)
    require(ADDENDUM_ROUTE in discovery, "Empirical Addendum I Papers index route missing", failures)
    if PARENT_TITLE in discovery and ADDENDUM_TITLE in discovery:
        require(discovery.index(PARENT_TITLE) < discovery.index(ADDENDUM_TITLE), "Papers index must place parent paper before addendum", failures)
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
