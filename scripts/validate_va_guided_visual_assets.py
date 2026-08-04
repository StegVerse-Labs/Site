#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "va-claims-guided-workflow.html"
ASSET_DIR = ROOT / "assets/va-claims-guided"
OUT = ROOT / "data/va-claim-assistant/guided-visual-assets-validation.json"
EXPECTED = [
    "card-1-get-ready.svg",
    "card-2-choose-sign-in.svg",
    "card-3-create-account.svg",
    "card-4-sign-in-va.svg",
    "card-5-download-records.svg",
    "card-6-preserve-continue.svg",
]


def main() -> int:
    errors: list[str] = []
    page = PAGE.read_text(encoding="utf-8")
    for name in EXPECTED:
        path = ASSET_DIR / name
        if not path.is_file():
            errors.append(f"missing visual asset: {name}")
            continue
        svg = path.read_text(encoding="utf-8")
        for marker in ("<title", "<desc", 'role="img"', "aria-labelledby"):
            if marker not in svg:
                errors.append(f"{name}: missing accessible SVG marker {marker}")
        reference = f'assets/va-claims-guided/{name}'
        if reference not in page:
            errors.append(f"guided page does not reference {name}")
    figures = re.findall(r'<figure class="visual">(.*?)</figure>', page, re.S)
    if len(figures) != 6:
        errors.append(f"expected 6 visual figures, found {len(figures)}")
    for index, figure in enumerate(figures, 1):
        if not re.search(r'<img[^>]+alt="[^"]{12,}"', figure):
            errors.append(f"card {index}: descriptive img alt text missing")
        if "<figcaption>" not in figure:
            errors.append(f"card {index}: figcaption missing")
    for phrase in (
        "simplified illustrations, not exact screenshots",
        "official pages can change",
        "do not post sensitive records publicly",
    ):
        if phrase.lower() not in page.lower():
            errors.append(f"page boundary missing: {phrase}")

    assets = {}
    for name in EXPECTED:
        path = ASSET_DIR / name
        if path.is_file():
            assets[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    body = {
        "schema_version": "1.0.0",
        "state": "PASS" if not errors else "FAIL",
        "surface": PAGE.name,
        "asset_directory": str(ASSET_DIR.relative_to(ROOT)),
        "expected_assets": EXPECTED,
        "asset_sha256": assets,
        "page_sha256": hashlib.sha256(PAGE.read_bytes()).hexdigest(),
        "accessible_svg_markers_required": True,
        "descriptive_alt_text_required": True,
        "non_screenshot_boundary_required": True,
        "authority_effect": False,
        "activation_effect": False,
        "errors": errors,
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    body["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(body, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
