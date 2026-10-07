#!/usr/bin/env python3
"""Structural check for the StegBrowser llm.v1 conformance fixture page.

The page must keep its stable selectors and deterministic echo, and must not
gain network, storage or credential behavior.
"""
from pathlib import Path
import re
import sys

PAGE = Path(__file__).resolve().parents[1] / "integration/llm-browser-test/v1/index.html"
text = PAGE.read_text(encoding="utf-8")
failures = []
for needed in ('id="prompt"', 'id="submit"', 'id="response"', 'id="notice"',
               'content="stegverse.integration.llm-browser-test.v1"', 'content="PERMITTED_BY_OWNER"',
               '"STEGVERSE_CONFORMANCE_V1 "', "response.textContent = PREFIX + prompt.value"):
    if needed not in text:
        failures.append(f"missing: {needed}")
for forbidden in ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource", "sendBeacon", "localStorage",
                  "sessionStorage", "indexedDB", "document.cookie", "innerHTML", "<script src", "<link"):
    if forbidden in text:
        failures.append(f"forbidden: {forbidden}")
if len(re.findall(r"<script\b", text)) != 1:
    failures.append("exactly one inline script expected")
if failures:
    print("\n".join(failures), file=sys.stderr)
    sys.exit(1)
print("LLM_BROWSER_CONFORMANCE_PAGE_PASS")
