#!/usr/bin/env python3
"""
StegVerse public page contract checker.

This script verifies the public GitHub Pages surface against a JSON contract.
It uses only the Python standard library so it can run in GitHub Actions without extra dependencies.
"""

from __future__ import annotations

import argparse
import html.parser
import json
import sys
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


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/") + "/"


def fetch_url(url: str, retries: int, timeout: int) -> tuple[int | None, str, str | None]:
    last_error: str | None = None
    for attempt in range(retries + 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "stegverse-page-contract-checker/1.0"})
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


def run_checks(contract: dict[str, Any], base_url: str, strict_links: bool, retries: int, timeout: int) -> list[CheckResult]:
    results: list[CheckResult] = []
    base_url = normalize_base_url(base_url)
    fetched_pages: dict[str, str] = {}

    for page in contract.get("pages", []):
        path = page["path"]
        url = urllib.parse.urljoin(base_url, path)
        status, body, error = fetch_url(url, retries=retries, timeout=timeout)

        results.append(CheckResult(
            kind="page",
            target=path,
            check="http_200",
            passed=status == 200,
            detail=f"status={status}" if error is None else f"error={error}",
        ))

        if status != 200:
            continue

        fetched_pages[path] = body

        for marker in page.get("required_substrings", []):
            results.append(CheckResult(
                kind="page",
                target=path,
                check=f"contains:{marker}",
                passed=marker in body,
                detail="found" if marker in body else "missing",
            ))

        links = page_links(body)
        for expected_link in page.get("required_links", []):
            results.append(CheckResult(
                kind="page",
                target=path,
                check=f"link:{expected_link}",
                passed=expected_link in links,
                detail="found" if expected_link in links else f"missing; found={sorted(links)}",
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
                    kind="link",
                    target=f"{path} -> {href}",
                    check="http_200",
                    passed=link_status == 200,
                    detail=f"status={link_status}" if link_error is None else f"error={link_error}",
                ))

    for json_file in contract.get("json_files", []):
        path = json_file["path"]
        url = urllib.parse.urljoin(base_url, path)
        status, body, error = fetch_url(url, retries=retries, timeout=timeout)

        results.append(CheckResult(
            kind="json",
            target=path,
            check="http_200",
            passed=status == 200,
            detail=f"status={status}" if error is None else f"error={error}",
        ))

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
                kind="json",
                target=path,
                check=f"{check['json_path']} == {expected}",
                passed=actual == expected,
                detail=f"actual={actual!r}",
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
            results.append(CheckResult(
                kind="json",
                target=path,
                check=f"{check['json_path']} contains",
                passed=passed,
                detail=detail,
            ))

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
    parser.add_argument("--base-url", default=None, help="Base URL for the deployed site.")
    parser.add_argument("--contracts", default="data/page-contracts-v1.json", help="Path to contract JSON.")
    parser.add_argument("--out-dir", default="page_contract_reports", help="Directory for reports.")
    parser.add_argument("--strict-links", action="store_true", help="Also fetch and verify discovered same-site links.")
    parser.add_argument("--retries", type=int, default=2, help="Fetch retries per target.")
    parser.add_argument("--timeout", type=int, default=20, help="Fetch timeout in seconds.")
    args = parser.parse_args()

    contract_path = Path(args.contracts)
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    base_url = args.base_url or contract.get("base_url_default")
    if not base_url:
        raise SystemExit("No base URL provided and no base_url_default found in contracts.")

    results = run_checks(
        contract=contract,
        base_url=base_url,
        strict_links=args.strict_links,
        retries=args.retries,
        timeout=args.timeout,
    )

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
