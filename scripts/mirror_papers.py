#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PAPERS = REPO_ROOT / "_source" / "publisher" / "papers"
TARGET_PAPERS = REPO_ROOT / "papers"
PAPERS_HTML = REPO_ROOT / "Papers.html"
PAPERS_INDEX = TARGET_PAPERS / "index.html"
MANIFEST_PATH = TARGET_PAPERS / "papers_manifest.json"

ALLOWED_EXTENSIONS = {
    ".html", ".htm", ".pdf", ".md", ".txt", ".tex", ".bib",
    ".png", ".jpg", ".jpeg", ".svg", ".webp", ".json"
}


def is_allowed_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS


def clean_target() -> None:
    if TARGET_PAPERS.exists():
        shutil.rmtree(TARGET_PAPERS)
    TARGET_PAPERS.mkdir(parents=True, exist_ok=True)


def copy_papers() -> list[dict]:
    if not SOURCE_PAPERS.exists():
        raise SystemExit(f"source papers directory not found: {SOURCE_PAPERS}")

    clean_target()
    entries: list[dict] = []

    for source_file in sorted(SOURCE_PAPERS.rglob("*")):
        if not is_allowed_file(source_file):
            continue

        relative = source_file.relative_to(SOURCE_PAPERS)
        target_file = TARGET_PAPERS / relative
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)

        entries.append({
            "path": relative.as_posix(),
            "href": "papers/" + relative.as_posix(),
            "title": relative.stem.replace("_", " ").replace("-", " ").strip() or relative.name,
            "extension": relative.suffix.lower(),
            "bytes": target_file.stat().st_size,
        })

    return entries


def category(extension: str) -> str:
    if extension in {".html", ".htm"}:
        return "HTML papers"
    if extension == ".pdf":
        return "PDF papers"
    if extension == ".md":
        return "Markdown drafts"
    if extension in {".tex", ".bib"}:
        return "LaTeX and references"
    return "Other paper assets"


def render_page(entries: list[dict]) -> str:
    generated = datetime.now(timezone.utc).isoformat()
    grouped: dict[str, list[dict]] = {}
    for entry in entries:
        grouped.setdefault(category(entry["extension"]), []).append(entry)

    css = """
:root{--bg:#07111f;--panel:#0f1b2d;--text:#edf6ff;--muted:#a8b8cc;--line:rgba(255,255,255,.14);--accent:#6ee7ff;--accent2:#59f59b;}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.6}
a{color:inherit}.wrap{width:min(1080px,calc(100% - 32px));margin:0 auto;padding:24px 0}
header{border-bottom:1px solid var(--line);background:rgba(7,17,31,.92);position:sticky;top:0}
.nav{width:min(1080px,calc(100% - 32px));margin:0 auto;display:flex;gap:16px;justify-content:space-between;align-items:center;padding:18px 0;flex-wrap:wrap}
.brand{font-weight:900;letter-spacing:.15em;text-transform:uppercase;text-decoration:none}.links{display:flex;gap:14px;flex-wrap:wrap;color:var(--muted);font-weight:700}
.links a.active{color:var(--accent)}h1{font-size:clamp(2.1rem,6vw,3.45rem);line-height:1.08}.lead,.muted{color:var(--muted)}
.badge{display:inline-block;padding:6px 14px;border:1px solid var(--accent);border-radius:999px;color:var(--accent);font-weight:800}
.card{background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:24px;margin-top:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.paper{display:block;border:1px solid var(--line);border-radius:16px;padding:16px;background:rgba(255,255,255,.04);text-decoration:none}
.title{font-weight:900}.meta{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--muted);font-size:.82rem;word-break:break-word}
.tag{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:4px 9px;color:var(--accent);font-size:.72rem;font-weight:800;margin-top:10px}
pre{white-space:pre-wrap;background:rgba(0,0,0,.28);border:1px solid var(--line);border-radius:14px;padding:16px;color:#e5f6ff}
footer{padding:30px 0 50px;color:var(--muted);border-top:1px solid var(--line);margin-top:30px;text-align:center;font-size:.85rem}
"""

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8"/>',
        '<meta name="viewport" content="width=device-width,initial-scale=1"/>',
        "<title>StegVerse Papers</title>",
        '<meta name="description" content="Mirrored StegVerse papers from GCAT-BCAT-Engine publisher outputs."/>',
        "<style>" + css + "</style>",
        "</head>",
        "<body>",
        "<header><div class=\"nav\">",
        '<a class="brand" href="index.html">StegVerse</a>',
        '<nav class="links"><a href="index.html">Home</a><a href="demo.html">Demo</a><a href="stegfinco.html">FinCo</a><a href="support.html">Support</a><a href="product.html">Product</a><a href="pricing.html">Pricing</a><a href="methodology.html">Methodology</a><a href="about.html">About</a><a href="Papers.html" class="active">Papers</a></nav>',
        "</div></header>",
        '<main class="wrap">',
        '<section><div class="badge">Mirrored paper outputs</div><h1>StegVerse Papers</h1>',
        '<p class="lead">This page mirrors paper outputs from <strong>GCAT-BCAT-Engine/publisher/papers</strong> into the public Site repository. When new papers are pushed to that source path and the mirror workflow runs, they become visible here.</p></section>',
        '<section class="card"><h2>Mirror status</h2><pre>Source: StegVerse-Labs/GCAT-BCAT-Engine/publisher/papers\nTarget: StegVerse-Labs/Site/papers\nIndex: StegVerse-Labs/Site/Papers.html\nGenerated UTC: ' + html.escape(generated) + "\nMirrored files: " + str(len(entries)) + "</pre></section>",
    ]

    if not entries:
        parts.append('<section class="card"><h2>No mirrored papers yet</h2><p class="muted">No supported files were found in GCAT-BCAT-Engine/publisher/papers.</p></section>')
    else:
        for label, label_entries in grouped.items():
            parts.append('<section class="card"><h2>' + html.escape(label) + '</h2><div class="grid">')
            for entry in label_entries:
                title = html.escape(entry["title"])
                path = html.escape(entry["path"])
                href = html.escape(entry["href"])
                ext = html.escape(entry["extension"].lstrip(".").upper() or "FILE")
                size = str(entry["bytes"])
                parts.append('<a class="paper" href="' + href + '"><div class="title">' + title + '</div><div class="meta">' + path + '</div><span class="tag">' + ext + '</span> <span class="tag">' + size + ' bytes</span></a>')
            parts.append("</div></section>")

    parts.extend([
        "</main>",
        "<footer>StegVerse · Papers mirrored from GCAT-BCAT-Engine · Generated " + html.escape(generated) + "</footer>",
        "</body>",
        "</html>",
    ])

    return "\n".join(parts)


def main() -> int:
    entries = copy_papers()
    MANIFEST_PATH.write_text(json.dumps({
        "source": "StegVerse-Labs/GCAT-BCAT-Engine/publisher/papers",
        "target": "StegVerse-Labs/Site/papers",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "count": len(entries),
        "entries": entries,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    page = render_page(entries)
    PAPERS_HTML.write_text(page, encoding="utf-8")
    PAPERS_INDEX.write_text(page, encoding="utf-8")

    print(json.dumps({
        "ok": True,
        "mirrored_count": len(entries),
        "papers_html": str(PAPERS_HTML),
        "papers_index": str(PAPERS_INDEX),
        "manifest": str(MANIFEST_PATH),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
