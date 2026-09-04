#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "news-releases.html"
ARTICLE = ROOT / "news-releases" / "ai-is-becoming-infrastructure-sovereignty-must-go-further.html"
ENTITY_ECONOMY = ROOT / "papers" / "stegverse-entity-economy" / "index.html"
ENTITY_ECONOMY_PDF = ROOT / "papers" / "stegverse-entity-economy" / "stegverse-entity-economy.pdf"
DISCOVERY = ROOT / "Papers.html"

def require(condition, message, failures):
    if not condition:
        failures.append(message)

def main():
    failures = []
    require(INDEX.exists(), "missing news-releases.html", failures)
    require(ARTICLE.exists(), "missing inaugural news release", failures)
    require(ENTITY_ECONOMY.exists(), "missing Entity Economy paper landing page", failures)
    require(ENTITY_ECONOMY_PDF.exists(), "missing Entity Economy PDF", failures)
    require(DISCOVERY.exists(), "missing Papers.html discovery surface", failures)
    if failures:
        print("CURRENT_NEWS_RELEASES_FAIL")
        for f in failures: print(f)
        return 1

    index = INDEX.read_text(encoding="utf-8")
    article = ARTICLE.read_text(encoding="utf-8")
    entity = ENTITY_ECONOMY.read_text(encoding="utf-8")
    discovery = DISCOVERY.read_text(encoding="utf-8")

    require("Current News Releases" in index, "landing title missing", failures)
    entries = re.findall(r'data-published="(\d{4}-\d{2}-\d{2})" data-sequence="(\d+)"', index)
    require(entries, "machine-readable publication ordering missing", failures)
    keys = [(d, int(seq)) for d, seq in entries]
    require(keys == sorted(keys, reverse=True), "news releases not reverse chronological/sequence order", failures)
    require("The StegVerse Entity Economy" in index, "Entity Economy not surfaced in news releases", failures)
    require(index.index("The StegVerse Entity Economy") < index.index("AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model."), "Entity Economy must precede South Korea statement", failures)
    require("AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model." in article, "headline missing", failures)
    require("StegVerse LLC" in article, "company attribution missing", failures)
    require("sovereignty all the way down" in article, "key differentiator missing", failures)
    require("Ministry of Science and ICT" in article, "primary source reference missing", failures)
    require("TechSpot" in article, "secondary source reference missing", failures)
    require("The StegVerse Entity Economy" in entity, "Entity Economy title missing", failures)
    require("VALUE SHOULD BE ATTRIBUTABLE" in entity, "Entity Economy design thesis missing", failures)
    require('href="stegverse-entity-economy.pdf"' in entity, "Entity Economy PDF link missing", failures)
    require("The StegVerse Entity Economy" in discovery, "Entity Economy missing from Papers index", failures)
    require('href="papers/stegverse-entity-economy/"' in discovery, "Entity Economy Papers index route missing", failures)
    require("Site-native bounded publications: 6" in discovery, "Papers index publication count not updated", failures)
    require("does not itself establish execution, activation, custody, certification, admissibility, or release authority" in article, "authority boundary missing", failures)
    require('href="news-releases.html"' in discovery, "public discovery link missing", failures)

    if failures:
        print("CURRENT_NEWS_RELEASES_FAIL")
        for f in failures: print(f)
        return 1
    print("CURRENT_NEWS_RELEASES_PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
