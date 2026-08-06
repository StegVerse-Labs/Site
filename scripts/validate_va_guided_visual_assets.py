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


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[.-][A-Za-z0-9]+)*", text))


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
        if f"assets/va-claims-guided/{name}" not in page:
            errors.append(f"guided page does not reference {name}")

    cards = re.findall(r'<section class="card(?: active)?" data-card="(\d+)">(.*?)</section>', page, re.S)
    if len(cards) != 6:
        errors.append(f"expected 6 guided cards, found {len(cards)}")

    for expected_number, (number, card) in enumerate(cards, 1):
        if int(number) != expected_number:
            errors.append(f"card order mismatch at {expected_number}")
        heading = re.search(r"<h1>(.*?)</h1>", card, re.S)
        if not heading:
            errors.append(f"card {number}: missing h1")
        elif words(re.sub(r"<.*?>", "", heading.group(1))) > 7:
            errors.append(f"card {number}: heading exceeds 7 words")
        images = re.findall(r'<img[^>]+alt="([^"]+)"', card)
        if len(images) != 1 or len(images[0].strip()) < 12:
            errors.append(f"card {number}: requires one descriptive image")
        boxes = re.findall(r'<input type="checkbox"', card)
        if len(boxes) != 1:
            errors.append(f"card {number}: requires exactly one confirmation checkbox")
        if '<details class="help">' not in card or '<summary>Need help?</summary>' not in card:
            errors.append(f"card {number}: optional help must remain collapsed")
        if number != "1" and 'class="back"' not in card:
            errors.append(f"card {number}: missing Back button")
        if number != "6" and 'class="next"' not in card:
            errors.append(f"card {number}: missing Next button")
        if number == "6" and 'class="finish"' not in card:
            errors.append("card 6: missing Done button")
        if "<figcaption" in card:
            errors.append(f"card {number}: visible image caption adds main-path text")

    required_phrases = (
        "Email · Phone · Photo ID",
        "Use Login.gov or ID.me",
        "Follow the screen prompts",
        "Open VA records",
        "All time · Select all · Download",
        "Original stays unchanged",
    )
    for phrase in required_phrases:
        if phrase not in page:
            errors.append(f"missing short action phrase: {phrase}")

    if "Verified capability state" in page or "SOURCE_GROUNDED_ASSISTANT" in page:
        errors.append("internal capability language exposed in guided workflow")

    assets = {}
    for name in EXPECTED:
        path = ASSET_DIR / name
        if path.is_file():
            assets[name] = hashlib.sha256(path.read_bytes()).hexdigest()

    body = {
        "schema_version": "2.0.0",
        "state": "PASS" if not errors else "FAIL",
        "surface": PAGE.name,
        "design_contract": "SEE_DO_CONFIRM",
        "maximum_heading_words": 7,
        "one_visual_per_card": True,
        "one_confirmation_per_card": True,
        "optional_help_collapsed": True,
        "expected_assets": EXPECTED,
        "asset_sha256": assets,
        "page_sha256": hashlib.sha256(PAGE.read_bytes()).hexdigest(),
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
