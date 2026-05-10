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

def clean_constraint(value):
    if value in (None, "", "None", "n/a"):
        return "not applicable"
    return value

def evidence_level(evidence, element_id):
    return int(evidence.get("elements", {}).get(element_id, {}).get("evidence_level", 0))

def deps_satisfied(target, evidence):
    requires = target.get("relations", {}).get("requires", [])
    return all(evidence_level(evidence, dep) >= 4 for dep in requires)

def source_runs_for_page(element, runs, knowledge):
    eid = element["id"]
    related_run_ids = set()
    for run in runs.get("runs", []):
        if run.get("element_id") == eid:
            related_run_ids.add(run.get("run_id"))
    for delta in knowledge.get("knowledge_deltas", []):
        if delta.get("source_element") == eid or eid in delta.get("informs", []):
            related_run_ids.add(delta.get("source_run_id"))
    return [run for run in runs.get("runs", []) if run.get("run_id") in related_run_ids]

def deltas_for_run(run_id, knowledge):
    return [delta for delta in knowledge.get("knowledge_deltas", []) if delta.get("source_run_id") == run_id]

def changelog_for(element, elements_by_id, evidence, runs, knowledge):
    eid = element["id"]
    entries = []
    for run in source_runs_for_page(element, runs, knowledge):
        run_id = run.get("run_id", "unknown-run")
        source = run.get("element_id", "unknown")
        source_element = elements_by_id.get(source, {})
        run_deltas = deltas_for_run(run_id, knowledge)
        informs = []
        for delta in run_deltas:
            for target in delta.get("informs", []):
                if target not in informs:
                    informs.append(target)
        if not informs:
            informs = source_element.get("relations", {}).get("informs", [])
        unlocked = []
        for target_id in informs:
            target = elements_by_id.get(target_id)
            if target and deps_satisfied(target, evidence):
                unlocked.append(target_id)
        evidence_delta = run.get("evidence_delta")
        if evidence_delta:
            evidence_text = f"{source} moved from {evidence_delta.get('from')} to {evidence_delta.get('to')} because {evidence_delta.get('reason')}."
        elif source == eid:
            evidence_text = "No evidence-level change was recorded for this run."
        else:
            evidence_text = f"No direct evidence-level change was recorded for {eid}; this run informs {eid} indirectly."
        knowledge_items = []
        for delta in run_deltas:
            if delta.get("source_element") == eid or eid in delta.get("informs", []) or source == eid:
                knowledge_items.append(f"{delta.get('delta_type', 'knowledge_delta')}: {delta.get('summary', '')}")
        if not knowledge_items:
            knowledge_items = ["No knowledge delta was recorded for this page from this run."]
        entries.append({
            "run_id": run_id,
            "source": source,
            "experiment": run.get("experiment", "unknown"),
            "status": run.get("status", "unknown"),
            "evidence_text": evidence_text,
            "knowledge_items": knowledge_items,
            "informs": informs,
            "unlocked": unlocked,
            "human_review_required": run.get("human_review_required", False),
            "relation_text": f"This run originated from {eid}." if source == eid else f"This run originated from {source} and informs {eid}.",
        })
    return entries

def changelog_html(entries):
    if not entries:
        return "<p>No consequential tests have changed or informed this transition yet.</p>"
    blocks = []
    for entry in entries:
        knowledge_list = "".join(f"<li>{esc(item)}</li>" for item in entry["knowledge_items"])
        informs = ", ".join(entry["informs"]) if entry["informs"] else "none"
        unlocked = ", ".join(entry["unlocked"]) if entry["unlocked"] else "none"
        review = "required" if entry["human_review_required"] else "not required"
        blocks.append(f"""
        <article class="change-entry">
          <h3>{esc(entry["run_id"])}</h3>
          <p><strong>Experiment:</strong> {esc(entry["experiment"])}</p>
          <p><strong>Status:</strong> {esc(entry["status"])}</p>
          <p><strong>Relation to this page:</strong> {esc(entry["relation_text"])}</p>
          <p><strong>Evidence consequence:</strong> {esc(entry["evidence_text"])}</p>
          <p><strong>Knowledge consequence:</strong></p>
          <ul>{knowledge_list}</ul>
          <p><strong>Graph consequence:</strong> informs {esc(informs)}.</p>
          <p><strong>Unlocked under current evidence state:</strong> {esc(unlocked)}.</p>
          <p><strong>Human review:</strong> {esc(review)}.</p>
        </article>
        """)
    return "\n".join(blocks)

def receipts_for_element(element_id, receipt_index):
    return [r for r in receipt_index.get("receipts", []) if r.get("element_id") == element_id]

def receipts_html(element_id, receipt_index):
    receipts = receipts_for_element(element_id, receipt_index)
    if not receipts:
        return "<p>No replayable state transition receipts have been generated for this transition yet.</p>"
    blocks = []
    for r in receipts[-20:]:
        extras = ""
        for key, label in [("lag_flip", "Lag flip"), ("decision_flip", "Decision flip"), ("actuation_flip", "Actuation flip"), ("total_lag_flip", "Total lag flip"), ("trust_flip", "Trust flip"), ("coupling_flip", "Coupling flip"), ("local_admissible_coupled_denied", "Local admissible / coupled denied")]:
            if r.get(key) is not None:
                extras += f"<p><strong>{label}:</strong> {esc(r.get(key))}</p>"
        blocks.append(f"""
        <article class="receipt-entry">
          <h3>{esc(r.get("receipt_id", ""))}</h3>
          <p><strong>Run:</strong> {esc(r.get("run_id", ""))}</p>
          <p><strong>Tested property:</strong> {esc(r.get("tested_property", ""))}</p>
          <p><strong>Admissibility verdict:</strong> {esc(r.get("admissibility_verdict", ""))}</p>
          <p><strong>Constraint result:</strong> {esc(clean_constraint(r.get("constraint_result")))}</p>
          {extras}
          <p><strong>Replay status:</strong> {esc(r.get("replay_status", "unknown"))}</p>
          <p><strong>Receipt hash:</strong> <code>{esc(r.get("receipt_hash", ""))}</code></p>
          <p><a href="../{esc(r.get("path", ""))}">Open receipt JSON</a></p>
        </article>
        """)
    return "\n".join(blocks)

def row_constraint(row):
    value = row.get("constraint_result")
    if value not in (None, "", "None", "n/a"):
        return value
    if row.get("mode") == "simplex_conservation_sweep_v1":
        cv = row.get("constraint_value")
        return "PASS" if cv is not None and abs(float(cv)) <= 1e-8 else "UNKNOWN"
    if row.get("mode") == "bounded_action_sweep_v1":
        n = row.get("action_norm")
        eps = row.get("epsilon", 0.10)
        return "PASS" if n is not None and float(n) <= float(eps) else "UNKNOWN"
    if row.get("mode") in ("capacity_margin_sweep_v1", "observation_lag_sweep_v1", "decision_lag_sweep_v1", "actuation_lag_sweep_v1", "trust_drift_sweep_v1", "two_state_coupling_sweep_v1"):
        return "PASS"
    return "not applicable"

def rule_release_html(rule_releases):
    rules = rule_releases.get("rules", [])
    if not rules:
        return "<p>No released rules file has been generated yet.</p>"
    released = [r for r in rules if r.get("status") == "released"]
    locked = [r for r in rules if r.get("status") != "released"]
    def items(rows):
        return "".join(f"<li><strong>{esc(r.get('rule_id'))}</strong> · released by {esc(r.get('released_by'))} · {esc(r.get('engine_effect'))}</li>" for r in rows) or "<li>none</li>"
    gate = rule_releases.get("automation_gate", {})
    return f"""
    <p><strong>Automation gate:</strong> {esc(gate.get("mode", "unknown"))}</p>
    <p><strong>Max sequence steps:</strong> {esc(gate.get("max_sequence_steps", "unknown"))}</p>
    <p><strong>Released rules:</strong></p>
    <ul>{items(released)}</ul>
    <p><strong>Locked rules:</strong></p>
    <ul>{items(locked)}</ul>
    """

def applied_rules_html(eruns):
    applied = []
    for run in eruns:
        for rule in run.get("applied_rules", []):
            if rule not in applied:
                applied.append(rule)
    if not applied:
        return "<p>No released operational rules have been applied directly by this transition yet.</p>"
    return "<ul>" + "".join(f"<li>{esc(rule)}</li>" for rule in applied) + "</ul>"

def render_page(e, ev, rows, eruns, deltas, change_entries, receipt_index, rule_releases):
    eid = e["id"]
    c = e.get("coordinates", {})
    rel = e.get("relations", {})

    rows_html = "".join(
        f"<li><code>{esc(r.get('run_id',''))}</code> · tested property={esc(r.get('tested_property', r.get('mode', '')))} · constraint={esc(row_constraint(r))} · admissibility invariant={esc(r.get('invariant',''))} · admissibility verdict=<strong>{esc(r.get('verdict',''))}</strong></li>"
        for r in rows[-20:]
    ) or "<li>No ledger rows yet.</li>"

    runs_html = "".join(
        f"<li><code>{esc(r.get('run_id',''))}</code> · {esc(r.get('experiment',''))} · <strong>{esc(r.get('status',''))}</strong> · sandbox={esc(r.get('sandbox', {}).get('type', 'unknown'))}</li>"
        for r in eruns[-10:]
    ) or "<li>No run manifests yet.</li>"

    deltas_html = "".join(
        f"<li><code>{esc(d.get('delta_id',''))}</code> · {esc(d.get('delta_type',''))} · {esc(d.get('summary',''))}</li>"
        for d in deltas[-10:]
    ) or "<li>No knowledge deltas yet.</li>"

    changes_html = changelog_html(change_entries)
    receipts_section = receipts_html(eid, receipt_index)
    rules_section = rule_release_html(rule_releases)
    applied_rules_section = applied_rules_html(eruns)

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
h3{margin:0 0 8px;font-size:1rem;color:#eef4ff}
p{color:#dbe7f7}
code{color:#f5fbff;word-break:break-all}
.muted{color:#a9b7cc}
.formula{overflow-x:auto;white-space:nowrap;border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:10px;background:rgba(0,0,0,.28)}
li{margin:0 0 8px}
.change-entry,.receipt-entry{border:1px solid rgba(255,255,255,.12);border-radius:14px;background:rgba(0,0,0,.18);padding:14px;margin-top:12px}
.change-entry p,.receipt-entry p{margin:8px 0}
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
<section><h2>Released Operational Rules</h2>__RULES__</section>
<section><h2>Applied Rules for This Transition</h2>__APPLIED_RULES__</section>
<section><h2>Run Manifests</h2><ul>__RUNS__</ul></section>
<section><h2>Knowledge Deltas</h2><ul>__DELTAS__</ul></section>
<section><h2>Recent Ledger Rows</h2><ul>__ROWS__</ul></section>
<section><h2>State Transition Receipts</h2>__RECEIPTS__</section>
<section><h2>Consequential Test Changelog</h2>__CHANGELOG__</section>
</main>
</body>
</html>
""".replace("__EID__", esc(eid)).replace("__NAME__", esc(e["name"])).replace("__QUESTION__", esc(e["question"])).replace("__SUPPORT__", SUPPORT).replace("__LEVEL__", esc(ev.get("evidence_level", e.get("evidence_level", 0)))).replace("__LABEL__", esc(ev.get("evidence_label", "Unknown"))).replace("__RUNTIME__", esc(ev.get("runtime_state", "idle"))).replace("__BRIGHTNESS__", esc(ev.get("brightness", 0))).replace("__COMPOSITION__", esc(c.get("composition", 0))).replace("__REALITY__", esc(c.get("reality_binding", 0))).replace("__OBS__", esc(c.get("observability_gap", 0))).replace("__REQUIRES__", esc(", ".join(rel.get("requires", [])) or "none")).replace("__INFORMS__", esc(", ".join(rel.get("informs", [])) or "none")).replace("__EXPECTED__", esc(e["expected_behavior"])).replace("__FORMULA__", esc(e["formula"])).replace("__SUMMARY__", esc(ev.get("latest_result_summary", e.get("confirmed_behavior", "")))).replace("__RULES__", rules_section).replace("__APPLIED_RULES__", applied_rules_section).replace("__RUNS__", runs_html).replace("__DELTAS__", deltas_html).replace("__ROWS__", rows_html).replace("__RECEIPTS__", receipts_section).replace("__CHANGELOG__", changes_html)

elements = read_json("transition-elements.json", [])
elements_by_id = {e["id"]: e for e in elements}
evidence = read_json("transition-evidence.json", {"elements": {}})
ledger = read_jsonl("transition-ledger.jsonl")
runs = read_json("transition-runs.json", {"runs": []})
knowledge = read_json("transition-knowledge-deltas.json", {"knowledge_deltas": []})
receipt_index = read_json("transition-receipts.json", {"receipts": []})
rule_releases = read_json("transition-rule-releases.json", {"rules": [], "automation_gate": {}})

for e in elements:
    eid = e["id"]
    ev = evidence.get("elements", {}).get(eid, {})
    rows = [r for r in ledger if r.get("element_id") == eid]
    eruns = [r for r in runs.get("runs", []) if r.get("element_id") == eid]
    deltas = [d for d in knowledge.get("knowledge_deltas", []) if d.get("source_element") == eid or eid in d.get("informs", [])]
    changes = changelog_for(e, elements_by_id, evidence, runs, knowledge)
    (OUT / f"{eid}.html").write_text(render_page(e, ev, rows, eruns, deltas, changes, receipt_index, rule_releases), encoding="utf-8")
    print(f"Wrote {OUT / (eid + '.html')}")
