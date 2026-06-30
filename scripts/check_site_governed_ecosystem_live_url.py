from __future__ import annotations

from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

URL = "https://stegverse-labs.github.io/Site/governed-ecosystem.html"
REQUIRED_TEXT = [
    "StegVerse Governed Ecosystem Mirror",
    "StegVerse-Labs/admissibility-wiki",
    "Site is display-only",
    "Governed Ecosystem Index",
    "Ecosystem Capability Status",
]


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return "\n".join(self.parts)


def main() -> int:
    errors: list[str] = []
    try:
        request = Request(URL, headers={"User-Agent": "StegVerse-Site-Verification/1.0"})
        with urlopen(request, timeout=20) as response:
            status = getattr(response, "status", None)
            body = response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        print(f"SITE GOVERNED ECOSYSTEM LIVE URL: FAIL - http_{exc.code}")
        return 1
    except URLError as exc:
        print(f"SITE GOVERNED ECOSYSTEM LIVE URL: FAIL - url_error:{exc.reason}")
        return 1

    if status != 200:
        errors.append(f"status:{status}")

    parser = TextExtractor()
    parser.feed(body)
    text = parser.text()
    for item in REQUIRED_TEXT:
        if item not in text:
            errors.append("missing:" + item)

    if errors:
        print("SITE GOVERNED ECOSYSTEM LIVE URL: FAIL - " + ", ".join(errors))
        return 1
    print("SITE GOVERNED ECOSYSTEM LIVE URL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
