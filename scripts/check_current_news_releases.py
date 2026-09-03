#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "news-releases.html"
ARTICLE = ROOT / "news-releases" / "ai-is-becoming-infrastructure-sovereignty-must-go-further.html"
DISCOVERY = ROOT / "Papers.html"

def require(condition, message, failures):
    if not condition:
        failures.append(message)

def main():
    failures = []
    require(INDEX.exists(), "missing news-releases.html", failures)
    require(ARTICLE.exists(), "missing inaugural news release", failures)
    require(DISCOVERY.exists(), "missing Papers.html discovery surface", failures)
    if failures:
        print("CURRENT_NEWS_RELEASES_FAIL")
        for f in failures: print(f)
        return 1

    index = INDEX.read_text(encoding="utf-8")
    article = ARTICLE.read_text(encoding="utf-8")
    discovery = DISCOVERY.read_text(encoding="utf-8")

    require("Current News Releases" in index, "landing title missing", failures)
    require('data-published="2026-09-03"' in index, "machine-readable publication date missing", failures)
    dates = re.findall(r'data-published="(\d{4}-\d{2}-\d{2})"', index)
    require(dates == sorted(dates, reverse=True), "news releases not reverse chronological", failures)
    require(len(dates) == len(set(dates)), "duplicate publication dates in current bounded index", failures)
    require("AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model." in article, "headline missing", failures)
    require("StegVerse LLC" in article, "company attribution missing", failures)
    require("sovereignty all the way down" in article, "key differentiator missing", failures)
    require("Ministry of Science and ICT" in article, "primary source reference missing", failures)
    require("TechSpot" in article, "secondary source reference missing", failures)
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
