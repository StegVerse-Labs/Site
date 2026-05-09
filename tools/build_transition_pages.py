#!/usr/bin/env python3
"""Generate static detail pages for transition elements."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "transition-elements"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def page_for(element: dict[str, Any], evidence: dict[str, Any], ledger: list[dict[str, Any]]) -> str:
    element_id = element["id"]
    ev = evidence.get("elements", {}).get(element_id, {})
    rows = [row for row in ledger if row.get("element_id") == element_id]
    ledger_html = "\n".join(
        f"<li><code>{html.escape(row['timestamp'])}</code> · "
        f"{html.escape(row['mode'])} · invariant={html.escape(str(row['invariant']))} · "
        f"<strong>{html.escape(row['verdict'])}</strong></li>"
        for row in rows[-20:]
    ) or "<li>No ledger rows have been generated for this element yet.</li>"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(element_id)} | Transition Periodic Table</title>
  <style>
    :root {{ color-scheme: dark; --bg:#080b12; --panel:#101827; --text:#eef4ff; --muted:#a9b7cc; --line:rgba(255,255,255,.14); --green:#43d694; }}
    body {{ margin:0; background:var(--bg); color:var(--text); font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; line-height:1.55; }}
    main {{ width:min(980px,calc(100% - 28px)); margin:0 auto; padding:28px 0 44px; }}
    a {{ color:var(--green); }}
    section {{ border:1px solid var(--line); border-radius:18px; background:rgba(16,24,39,.78); padding:18px; margin-top:14px; }}
    h1 {{ font-size:clamp(2rem,7vw,4rem); line-height:.95; margin:0; letter-spacing:-.06em; }}
    h2 {{ margin:0 0 8px; color:var(--green); text-transform:uppercase; letter-spacing:.12em; font-size:.85rem; }}
    p {{ color:#dbe7f7; }}
    code {{ color:#f5fbff; }}
    .muted {{ color:var(--muted); }}
    .formula {{ overflow-x:auto; white-space:nowrap; border:1px solid var(--line); border-radius:12px; padding:10px; background:rgba(0,0,0,.28); }}
    li {{ margin:0 0 8px; }}
  </style>
</head>
<body>
  <main>
    <p><a href="../transition-table.html">← Back to Transition Table</a></p>
    <h1>{html.escape(element_id)} — {html.escape(element["name"])}</h1>
    <p class="muted">{html.escape(element["question"])}</p>

    <section>
      <h2>Evidence State</h2>
      <p>Level: <strong>{html.escape(str(ev.get("evidence_level", element.get("evidence_level", 0))))}/5 · {html.escape(ev.get("evidence_label", "Unknown"))}</strong></p>
      <p>Brightness: <strong>{html.escape(str(ev.get("brightness", 0)))}</strong></p>
      <p>Receipt-backed: <strong>{html.escape(str(ev.get("receipt_backed", False)))}</strong></p>
    </section>

    <section>
      <h2>Expected Behavior</h2>
      <p>{html.escape(element["expected_behavior"])}</p>
      <div class="formula"><code>{html.escape(element["formula"])}</code></div>
    </section>

    <section>
      <h2>Confirmed Behavior</h2>
      <p>{html.escape(ev.get("latest_result_summary", element["confirmed_behavior"]))}</p>
    </section>

    <section>
      <h2>Recent Ledger Rows</h2>
      <ul>{ledger_html}</ul>
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    elements = load_json(DATA_DIR / "transition-elements.json")
    evidence = load_json(DATA_DIR / "transition-evidence.json")
    ledger = load_jsonl(DATA_DIR / "transition-ledger.jsonl")

    for element in elements:
        output = OUT_DIR / f"{element['id']}.html"
        output.write_text(page_for(element, evidence, ledger), encoding="utf-8")
        print(f"Wrote {output}")


if __name__ == "__main__":
    main()
