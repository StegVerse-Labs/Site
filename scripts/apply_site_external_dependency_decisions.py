#!/usr/bin/env python3
"""Apply owner decisions from data/site-external-dependency-decisions.json to static pages.

Only PAPER_MATHJAX_MARKED_CDN needs a source rewrite (a static page cannot read repository
configuration). PLAYWRIGHT_BROWSER_VERIFICATION is read directly by the four workflows.

  python3 scripts/apply_site_external_dependency_decisions.py          # apply (idempotent)
  python3 scripts/apply_site_external_dependency_decisions.py --check  # guard, fails closed

With remove=false nothing is written. With remove=true the page is rewritten to the
dependency-free version; running it again changes nothing. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "site-external-dependency-decisions.json"
SCHEMA = "stegverse.site-external-dependency-decisions/v1"
PAPER_DECISION = "PAPER_MATHJAX_MARKED_CDN"
CDN_HOST = "cdn.jsdelivr.net"
MARKER = "<!-- site-external-dependency-decision: PAPER_MATHJAX_MARKED_CDN removed -->"

HEAD_DEPENDENCIES = """<script>
window.MathJax={
  tex:{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']],processEscapes:true},
  options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']},
  chtml:{scale:1.02}
};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
"""

LOADING = '<p class="loading">Loading and typesetting canonical Publisher paper…</p>'
LOADING_REMOVED = '<p class="loading">Loading canonical Publisher paper source…</p>'

ENTRY_CALL = "waitForDependencies();\n</script>"
ENTRY_CALL_REMOVED = """function showUnformattedSource(){
  const paper=document.getElementById('paper');
  fetch(canonical,{cache:'no-store'})
    .then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.text()})
    .then(md=>{
      const note=document.createElement('div');
      note.className='status';
      note.textContent='Rendering note: Markdown and TeX typesetting were removed by owner decision PAPER_MATHJAX_MARKED_CDN (no external libraries are loaded). The canonical Publisher source is shown below unformatted.';
      const pre=document.createElement('pre');
      pre.className='code-block';
      pre.style.whiteSpace='pre-wrap';
      pre.textContent=md;
      paper.replaceChildren(note,pre);
    })
    .catch(e=>{
      paper.innerHTML='<div class="error"><strong>The canonical paper source could not be loaded in this reader.</strong><br/>Use the Canonical Publisher source link above.<br/><br/>'+String(e.message).replace(/[<>&]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;'}[c]))+'</div>';
    });
}
showUnformattedSource();
</script>"""

REWRITES = (
    (HEAD_DEPENDENCIES, MARKER + "\n"),
    (LOADING, LOADING_REMOVED),
    (ENTRY_CALL, ENTRY_CALL_REMOVED),
)


class DecisionError(Exception):
    pass


def load_config(path: Path = CONFIG) -> dict:
    config = json.loads(path.read_text(encoding="utf-8"))
    if config.get("schema") != SCHEMA:
        raise DecisionError(f"{path}: schema is not {SCHEMA}")
    decision = config.get("decisions", {}).get(PAPER_DECISION)
    if not isinstance(decision, dict) or not isinstance(decision.get("remove"), bool):
        raise DecisionError(f"{path}: {PAPER_DECISION}.remove must be a boolean")
    if not decision.get("files"):
        raise DecisionError(f"{path}: {PAPER_DECISION}.files is empty")
    return config


def remove_dependencies(text: str) -> str:
    """Return the dependency-free page. Idempotent; fails closed on unrecognised source."""
    if MARKER in text:
        if CDN_HOST in text:
            raise DecisionError("page carries the removal marker but still references " + CDN_HOST)
        return text
    for old, new in REWRITES:
        if text.count(old) != 1:
            raise DecisionError("page source no longer matches the prepared removal: " + old.splitlines()[0])
        text = text.replace(old, new)
    if CDN_HOST in text:
        raise DecisionError("rewritten page still references " + CDN_HOST)
    return text


def check_page(remove: bool, text: str) -> list[str]:
    problems = []
    if remove:
        if CDN_HOST in text:
            problems.append(f"{PAPER_DECISION}.remove=true but the page still references {CDN_HOST}; run scripts/apply_site_external_dependency_decisions.py in the same change")
        if MARKER not in text:
            problems.append(f"{PAPER_DECISION}.remove=true but the page lacks the removal marker")
    else:
        if MARKER in text:
            problems.append(f"{PAPER_DECISION}.remove=false but the page carries the removal marker")
        for old, _ in REWRITES:
            if text.count(old) != 1:
                problems.append(f"{PAPER_DECISION}.remove=false but the page changed where the prepared removal applies: {old.splitlines()[0]}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="verify the page matches the decision; write nothing")
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--root", type=Path, default=ROOT, help="directory the decision's files are relative to")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
    except (OSError, ValueError, DecisionError) as exc:
        print(f"FAIL_CLOSED: {exc}", file=sys.stderr)
        return 1
    decision = config["decisions"][PAPER_DECISION]
    remove = decision["remove"]
    status = 0
    for rel in decision["files"]:
        page = args.root / rel
        text = page.read_text(encoding="utf-8")
        if args.check:
            for problem in check_page(remove, text):
                print(f"FAIL_CLOSED: {rel}: {problem}", file=sys.stderr)
                status = 1
            continue
        if not remove:
            print(f"{PAPER_DECISION}=KEEP {rel} unchanged")
            continue
        try:
            new = remove_dependencies(text)
        except DecisionError as exc:
            print(f"FAIL_CLOSED: {rel}: {exc}", file=sys.stderr)
            status = 1
            continue
        if new != text:
            page.write_text(new, encoding="utf-8")
            print(f"{PAPER_DECISION}=REMOVED {rel} rewritten")
        else:
            print(f"{PAPER_DECISION}=REMOVED {rel} already dependency-free")
    if args.check and status == 0:
        print(f"{PAPER_DECISION} remove={str(remove).lower()} page consistent")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
