#!/usr/bin/env python3
"""Render the public Build Trajectory from its sole canonical record."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "build-trajectory.json"
OUTPUT = ROOT / "build-trajectory.html"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def evidence_links(rows: list[dict]) -> str:
    return " · ".join(
        f'<a href="{esc(row["url"])}">{esc(row["label"])}</a> '
        f'<span class="meta" title="Full observed Git blob: {esc(row["observed_blob_sha"])}">'
        f'(observed blob <code>{esc(row["observed_blob_sha"][:12])}…</code>, {esc(row["verified_at"])})</span>'
        for row in rows
    )


def render_report(report: dict, stage_map: dict[str, dict]) -> str:
    completed = []
    for outcome in report["completed_outcomes"]:
        badges = "".join(f'<span class="stage">{esc(stage_map[stage]["label"])}</span>' for stage in outcome["stages"])
        if outcome.get("stage_qualifier"):
            badges += f'<span class="stage">{esc(outcome["stage_qualifier"].replace("_", " ").title())}</span>'
        completed.append(
            f'<li>{badges}<strong>{esc(outcome["outcome"])}</strong> {esc(outcome["proof"])} '
            f'<em>{esc(outcome["boundary"])}</em> {evidence_links(outcome["evidence"])}.</li>'
        )
    incomplete = "\n".join(f'<li><strong>{esc(row["subject"])}:</strong> {esc(row["detail"])}</li>' for row in report["not_completed"])
    unproven = "\n".join(
        f'<li>“{esc(row["claim"])}” is unsupported. {esc(row["reason"])} '
        f'<strong>Missing proof:</strong> {esc(row["missing_proof"])}</li>'
        for row in report["unproven_completion_claims"]
    )
    remaining = "\n".join(
        f'<li><code>{esc(" + ".join(row["destinations"]))}</code>: {esc(row["work"])}</li>'
        for row in report["remaining_installation_or_integration"]
    )
    corrections = ""
    if report["corrections"]:
        correction_items = "\n".join(
            f'<li><time datetime="{esc(row["corrected_at"])}">{esc(row["corrected_at"])}</time>: '
            f'{esc(row["reason"])} — {esc(row["replacement"])}</li>'
            for row in report["corrections"]
        )
        corrections = f"<h3>Corrections</h3>\n<ul>{correction_items}</ul>"
    return f"""<article class="week" data-report-id="{esc(report["report_id"])}" data-period-end="{esc(report["period_end"])}">
<header>
<p class="eyebrow">Weekly accomplishment log</p>
<h2>{esc(report["title"])}</h2>
<p class="meta">{esc(report["summary"])}</p>
</header>
<h3>Completed outcomes</h3>
<ul class="outcomes">
{chr(10).join(completed)}
</ul>
<h3>Not completed</h3>
<ul>
{incomplete}
</ul>
<h3>Unproven completion claims</h3>
<ul class="claim">
{unproven}
</ul>
<h3>Remaining installation or integration</h3>
<ul>
{remaining}
</ul>
{corrections}
</article>"""


def render(record: dict) -> str:
    stage_map = {row["id"]: row for row in record["evidence_stages"]}
    stage_cards = "\n".join(
        f'<li><strong>{esc(row["label"])}</strong><br><span class="meta">{esc(row["meaning"])}</span></li>'
        for row in record["evidence_stages"]
    )
    reports = "\n".join(render_report(report, stage_map) for report in record["reports"])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Evidence-backed weekly StegVerse accomplishment reports showing implementation, validation, release or deployment, runtime proof, and governed activation as distinct stages.">
<title>Build Trajectory — StegVerse</title>
<link rel="stylesheet" href="sv-shared.css">
<style>
.wrap{{max-width:960px;margin:0 auto;padding:24px 16px 64px}}.top{{display:flex;justify-content:space-between;gap:16px;align-items:center;padding:8px 0 28px}}.top a{{text-decoration:none}}.intro,.week{{border:1px solid var(--border);border-radius:18px;background:var(--surface);padding:22px;margin:18px 0}}.eyebrow,.meta,.boundary{{color:var(--muted);font-size:.9rem}}.stages{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;padding:0;list-style:none}}.stages li{{border:1px solid var(--border);border-radius:12px;padding:10px}}.stage{{display:inline-block;border:1px solid var(--border2);border-radius:999px;padding:2px 8px;margin:0 6px 6px 0;font-size:.78rem;font-weight:700}}.outcomes{{padding-left:1.2rem}}.outcomes li{{margin:1rem 0}}.week h3{{margin-top:1.6rem}}.week h3:first-of-type{{margin-top:1rem}}.claim{{border-left:3px solid var(--border2);padding-left:28px}}.boundary{{margin-top:30px}}
</style>
</head>
<body>
<main class="wrap">
<nav class="top" aria-label="StegVerse"><a href="index.html"><strong>StegVerse</strong></a><a href="news-releases.html">Current News Releases</a></nav>
<header>
<p class="eyebrow">StegVerse LLC · Public build record</p>
<h1>{esc(record["title"])}</h1>
<p>Weekly, evidence-backed reports of what the StegVerse ecosystem actually reached—not merely what was proposed, assigned, or described.</p>
</header>
<section class="intro" aria-labelledby="why-this-exists">
<h2 id="why-this-exists">Why this log exists</h2>
<p>StegVerse is a multi-repository system whose progress occurs at different evidence stages. This log makes that trajectory legible while resisting a common failure in technical reporting: treating code, tests, releases, deployments, runtime events, and activation as interchangeable.</p>
<ul class="stages" aria-label="Evidence stages">
{stage_cards}
</ul>
<p class="meta">Newest reports appear first. Every completion is linked to inspectable evidence; missing proof is named. Corrections are dated and appended rather than silently replacing history.</p>
</section>
{reports}
<p class="boundary">This page is a deterministic projection of <code>{esc(record["source_of_truth"])}</code>. Site publication does not establish execution, deployment, custody, certification, admissibility, release authority, or governed activation.</p>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    projected = render(json.loads(SOURCE.read_text(encoding="utf-8")))
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != projected:
            raise SystemExit("FAIL: build-trajectory.html is not the exact canonical projection")
        print("PASS: build-trajectory.html exactly reconstructs from data/build-trajectory.json")
        return 0
    OUTPUT.write_text(projected, encoding="utf-8")
    print(f"WROTE: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
