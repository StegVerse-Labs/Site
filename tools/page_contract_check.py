#!/usr/bin/env python3
"""
StegVerse public page contract checker.

Standard-library only.

v1.2 behavior:
- Text checks are whitespace/punctuation/underscore/hyphen tolerant.
- Required link checks pass when the target is a real anchor href OR appears in embedded/fallback payload text.
- JSON checks remain strict.
"""

from __future__ import annotations

import argparse
import html
import html.parser
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class CheckResult:
    kind: str
    target: str
    check: str
    passed: bool
    detail: str


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.hrefs.append(value)


class TextParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "noscript"}:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.skip_depth == 0:
            self.parts.append(data)


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/") + "/"


def extract_visible_text(markup: str) -> str:
    parser = TextParser()
    parser.feed(markup)
    return " ".join(parser.parts)


def normalize_words(value: str) -> str:
    value = html.unescape(value).upper()
    value = re.sub(r"[_\-]+", " ", value)
    value = re.sub(r"[^A-Z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def compact_alnum(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "", html.unescape(value).upper())


def body_contains_marker(markup: str, marker: str) -> bool:
    visible = extract_visible_text(markup)
    marker_words = normalize_words(marker)
    marker_compact = compact_alnum(marker)

    candidates = [
        normalize_words(visible),
        normalize_words(markup),
        compact_alnum(visible),
        compact_alnum(markup),
    ]

    return any(marker_words in candidate or marker_compact in candidate for candidate in candidates)


def fetch_url(url: str, retries: int, timeout: int) -> tuple[int | None, str, str | None]:
    last_error: str | None = None
    for attempt in range(retries + 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "stegverse-page-contract-checker/1.2"})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                body = response.read().decode(charset, errors="replace")
                return response.status, body, None
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = str(exc)
            if attempt < retries:
                time.sleep(1 + attempt)
    return None, "", last_error


def get_json_path(value: Any, dotted_path: str) -> Any:
    current = value
    for part in dotted_path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def object_contains(container: Any, expected: dict[str, Any]) -> bool:
    if not isinstance(container, list):
        return False
    for item in container:
        if not isinstance(item, dict):
            continue
        if all(item.get(key) == expected_value for key, expected_value in expected.items()):
            return True
    return False


def page_links(html_text: str) -> set[str]:
    parser = LinkParser()
    parser.feed(html_text)
    normalized: set[str] = set()
    for href in parser.hrefs:
        clean = href.split("#", 1)[0].strip()
        if clean:
            normalized.add(clean)
    return normalized


def same_site_link(href: str) -> bool:
    if href.startswith(("mailto:", "tel:", "javascript:")):
        return False
    parsed = urllib.parse.urlparse(href)
    return parsed.scheme in ("", "http", "https")


def resolve_link(base_url: str, page_path: str, href: str) -> str:
    page_url = urllib.parse.urljoin(base_url, page_path)
    return urllib.parse.urljoin(page_url, href)


def required_link_present(markup: str, links: set[str], expected_link: str) -> bool:
    if expected_link in links:
        return True
    if expected_link in markup:
        return True
    escaped = expected_link.replace("/", r"\/")
    return escaped in markup


def run_checks(contract: dict[str, Any], base_url: str, strict_links: bool, retries: int, timeout: int) -> list[CheckResult]:
    results: list[CheckResult] = []
    base_url = normalize_base_url(base_url)

    for page in contract.get("pages", []):
        path = page["path"]
        url = urllib.parse.urljoin(base_url, path)
        status, body, error = fetch_url(url, retries=retries, timeout=timeout)

        results.append(CheckResult("page", path, "http_200", status == 200, f"status={status}" if error is None else f"error={error}"))
        if status != 200:
            continue

        for marker in page.get("required_substrings", []):
            found = body_contains_marker(body, marker)
            results.append(CheckResult("page", path, f"contains:{marker}", found, "found" if found else "missing"))

        links = page_links(body)
        for expected_link in page.get("required_links", []):
            found = required_link_present(body, links, expected_link)
            results.append(CheckResult(
                "page",
                path,
                f"link:{expected_link}",
                found,
                "found" if found else f"missing; found={sorted(links)}",
            ))

        if strict_links:
            for href in sorted(links):
                if not same_site_link(href):
                    continue
                if href.startswith(("http://", "https://")) and "stegverse-labs.github.io" not in href:
                    continue
                resolved = resolve_link(base_url, path, href)
                link_status, _, link_error = fetch_url(resolved, retries=1, timeout=timeout)
                results.append(CheckResult(
                    "link",
                    f"{path} -> {href}",
                    "http_200",
                    link_status == 200,
                    f"status={link_status}" if link_error is None else f"error={link_error}",
                ))

    for json_file in contract.get("json_files", []):
        path = json_file["path"]
        url = urllib.parse.urljoin(base_url, path)
        status, body, error = fetch_url(url, retries=retries, timeout=timeout)

        results.append(CheckResult("json", path, "http_200", status == 200, f"status={status}" if error is None else f"error={error}"))
        if status != 200:
            continue

        try:
            parsed = json.loads(body)
            results.append(CheckResult("json", path, "valid_json", True, "parsed"))
        except json.JSONDecodeError as exc:
            results.append(CheckResult("json", path, "valid_json", False, str(exc)))
            continue

        for check in json_file.get("required_values", []):
            actual = get_json_path(parsed, check["json_path"])
            expected = check["equals"]
            results.append(CheckResult(
                "json",
                path,
                f"{check['json_path']} == {expected}",
                actual == expected,
                f"actual={actual!r}",
            ))

        for check in json_file.get("required_contains", []):
            actual = get_json_path(parsed, check["json_path"])
            if "contains_object" in check:
                expected_obj = check["contains_object"]
                passed = object_contains(actual, expected_obj)
                detail = f"expected object={expected_obj!r}"
            else:
                expected_value = check["contains"]
                passed = isinstance(actual, list) and expected_value in actual
                detail = f"actual={actual!r}"
            results.append(CheckResult("json", path, f"{check['json_path']} contains", passed, detail))

    return results


def write_reports(results: list[CheckResult], out_dir: Path, base_url: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "base_url": base_url,
        "passed": all(result.passed for result in results),
        "total": len(results),
        "failures": sum(1 for result in results if not result.passed),
        "results": [result.__dict__ for result in results],
    }
    (out_dir / "page-contract-report.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Page Contract Report",
        "",
        f"Base URL: `{base_url}`",
        "",
        f"Result: **{'PASS' if payload['passed'] else 'FAIL'}**",
        "",
        f"Total checks: `{payload['total']}`",
        f"Failures: `{payload['failures']}`",
        "",
        "## Failures",
        "",
    ]

    failures = [result for result in results if not result.passed]
    if not failures:
        lines.append("No failures.")
    else:
        for result in failures:
            lines.append(f"- `{result.kind}` `{result.target}` `{result.check}` — {result.detail}")

    lines.extend(["", "## All Checks", ""])
    for result in results:
        icon = "✅" if result.passed else "❌"
        lines.append(f"- {icon} `{result.kind}` `{result.target}` `{result.check}` — {result.detail}")

    (out_dir / "page-contract-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify StegVerse public pages against a JSON contract.")
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--contracts", default="data/page-contracts-v1.json")
    parser.add_argument("--out-dir", default="page_contract_reports")
    parser.add_argument("--strict-links", action="store_true")
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()

    contract = json.loads(Path(args.contracts).read_text(encoding="utf-8"))
    base_url = args.base_url or contract.get("base_url_default")
    if not base_url:
        raise SystemExit("No base URL provided and no base_url_default found in contracts.")

    results = run_checks(contract, base_url, args.strict_links, args.retries, args.timeout)
    write_reports(results, Path(args.out_dir), base_url)

    failures = [result for result in results if not result.passed]
    if failures:
        print(f"FAIL: {len(failures)} page contract check(s) failed.")
        for failure in failures[:20]:
            print(f"- {failure.kind} {failure.target} {failure.check}: {failure.detail}")
        if len(failures) > 20:
            print(f"... plus {len(failures) - 20} more failure(s).")
        return 1

    print(f"PASS: {len(results)} page contract check(s) passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
