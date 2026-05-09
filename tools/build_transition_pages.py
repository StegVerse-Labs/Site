#!/usr/bin/env python3
from pathlib import Path
import json, html

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data"
OUT = ROOT / "transition-elements"
OUT.mkdir(exist_ok=True)
SUPPORT = "https://buy.stripe.com/aFadRb99q0lu0Oa7RSdby00"

def read_json(name, default):
    p = D / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

def read_jsonl(name):
    p = D / name
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []

def esc(x):
    return html.escape(str(x), quote=True)

def render_page(e, ev, rows, eruns, deltas):
    eid = e["id"]
    c = e.get("coordinates", {})
    rel = e.get("relations", {})
    rows_html = "".join(
        f"<li><code>{esc(r.get('run_id',''))}</code> · invariant={esc(r.get('invariant',''))} · <strong>{esc(r.get('verdict',''))}</strong></li>"
        for r in rows[-20:]
    ) or "<li>No ledger rows yet.</li>"
    runs_html = "".join(
        f"<li><code>{esc(r.get('run_id',''))}</code> · {esc(r.get('experiment',''))} · <strong>{esc(r.get('status',''))}</strong></li>"
        for r in eruns[-10:]
    ) or "<li>No run manifests yet.</li>"
    deltas_html = "".join(
        f"<li><code>{esc(d.get('delta_id',''))}</code> · {esc(d.get('delta_type',''))} · {esc(d.get('summary',''))}</li>"
        for d in deltas[-10:]
    ) or "<li>No knowledge deltas yet.</li>"

    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>__EID__ | Transition Periodic Table</title>
<style>
body{margin:0;background:#080b12;color:#eef4ff;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.55}
main{width:min(980px,calc(100% - 28px));margin:0 auto;padding:24px 0 44px}
a{color:#43d694}
nav{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
nav a{border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:7px 11px;text-decoration:none;color:#eef4ff;background:rgba(255,255,255,.05)}
section{border:1px solid rgba(255,255,255,.14);border-radius:18px;background:rgba(16,24,39,.78);padding:18px;margin-top:14px}
h1{font-size:clamp(2rem,7vw,4rem);line-height:.95;margin:0;letter-spacing:-.06em}
h2{margin:0 0 8px;color:#43d694;text-transform:uppercase;letter-spacing:.12em;font-size:.85rem}
p{color:#dbe7f7}
code{color:#f5fbff}
.muted{color:#a9b7cc}
.formula{overflow-x:auto;white-space:nowrap;border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:10px;background:rgba(0,0,0,.28)}
li{margin:0 0 8px}
</style>
</head>
<body>
<main>
<nav>
  <a href="../index.html">Home</a>
  <a href="../demo.html">Demo</a>
  <a href="../transition-periodic-table.html">Research Landing</a>
  <a href="../transition-table.html">Transition Table</a>
  <a href="__SUPPORT__">Support StegVerse Research</a>
</nav>
<h1>__EID__ — __NAME__</h1>
<p class="muted">__QUESTION__</p>
<section><h2>Evidence State</h2>
  <p>Level: <strong>__LEVEL__/5 · __LABEL__</strong></p>
  <p>Runtime state: <strong>__RUNTIME__</strong></p>
  <p>Brightness: <strong>__BRIGHTNESS__</strong></p>
</section>
<section><h2>3D Lattice Coordinates</h2>
  <p>Composition: <strong>__COMPOSITION__</strong></p>
  <p>Reality-binding: <strong>__REALITY__</strong></p>
  <p>Observability gap: <strong>__OBS__</strong></p>
</section>
<section><h2>Relations</h2>
  <p>Requires: <strong>__REQUIRES__</strong></p>
  <p>Informs: <strong>__INFORMS__</strong></p>
</section>
<section><h2>Expected Behavior</h2>
  <p>__EXPECTED__</p>
  <div class="formula"><code>__FORMULA__</code></div>
</section>
<section><h2>Confirmed Behavior</h2><p>__SUMMARY__</p></section>
<section><h2>Run Manifests</h2><ul>__RUNS__</ul></section>
<section><h2>Knowledge Deltas</h2><ul>__DELTAS__</ul></section>
<section><h2>Recent Ledger Rows</h2><ul>__ROWS__</ul></section>
</main>
</body>
</html>
""".replace("__EID__", esc(eid)).replace("__NAME__", esc(e["name"])).replace("__QUESTION__", esc(e["question"])).replace("__SUPPORT__", SUPPORT).replace("__LEVEL__", esc(ev.get("evidence_level", e.get("evidence_level", 0)))).replace("__LABEL__", esc(ev.get("evidence_label", "Unknown"))).replace("__RUNTIME__", esc(ev.get("runtime_state", "idle"))).replace("__BRIGHTNESS__", esc(ev.get("brightness", 0))).replace("__COMPOSITION__", esc(c.get("composition", 0))).replace("__REALITY__", esc(c.get("reality_binding", 0))).replace("__OBS__", esc(c.get("observability_gap", 0))).replace("__REQUIRES__", esc(", ".join(rel.get("requires", [])) or "none")).replace("__INFORMS__", esc(", ".join(rel.get("informs", [])) or "none")).replace("__EXPECTED__", esc(e["expected_behavior"])).replace("__FORMULA__", esc(e["formula"])).replace("__SUMMARY__", esc(ev.get("latest_result_summary", e.get("confirmed_behavior", "")))).replace("__RUNS__", runs_html).replace("__DELTAS__", deltas_html).replace("__ROWS__", rows_html)

elements = read_json("transition-elements.json", [])
evidence = read_json("transition-evidence.json", {"elements": {}})
ledger = read_jsonl("transition-ledger.jsonl")
runs = read_json("transition-runs.json", {"runs": []})
kd = read_json("transition-knowledge-deltas.json", {"knowledge_deltas": []})

for e in elements:
    eid = e["id"]
    ev = evidence.get("elements", {}).get(eid, {})
    rows = [r for r in ledger if r.get("element_id") == eid]
    eruns = [r for r in runs.get("runs", []) if r.get("element_id") == eid]
    deltas = [d for d in kd.get("knowledge_deltas", []) if d.get("source_element") == eid or eid in d.get("informs", [])]
    (OUT / f"{eid}.html").write_text(render_page(e, ev, rows, eruns, deltas), encoding="utf-8")
    print(f"Wrote {OUT / (eid + '.html')}")
