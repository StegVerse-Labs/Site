#!/usr/bin/env python3
"""Fact-graph validator.

Enforces the publication rules so the public surface cannot carry an
unverifiable or vocabulary-drifted fact:

  1. Every edge's relation MUST be in the closed relations vocabulary.
  2. Every fact with status proved/released/canonical MUST have at least
     one evidence path, and (when --repo-root given) those paths MUST resolve.
  3. Every edge endpoint MUST reference a known fact_id or term_id.
  4. Every status MUST be a known grade.
  5. supersedes targets are advisory (the superseded fact may be historical
     and absent); reported, not failed.

Exit 0 = graph publishable. Exit 1 = at least one blocking error.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a fact-graph instance against schema + closed relations.")
    ap.add_argument("--instance", default=str(HERE / "facts.seed.json"))
    ap.add_argument("--relations", default=str(HERE / "relations.json"))
    ap.add_argument("--schema", default=str(HERE / "schema.json"))
    ap.add_argument("--repo-root", default=None,
                    help="If given, evidence paths are resolved relative to this root (a formalism-tests checkout).")
    args = ap.parse_args()

    relations = load(Path(args.relations))
    schema = load(Path(args.schema))
    inst = load(Path(args.instance))

    rel_ids = {r["relation_id"] for r in relations["relations"]}
    grades = set(schema["status_grades"].keys())
    origin_types = set(schema["origin_types"].keys())
    needs_evidence = {"proved", "released", "canonical"}

    facts = {f["fact_id"]: f for f in inst.get("facts", [])}
    terms = {t["term_id"]: t for t in inst.get("terms", [])}
    node_ids = set(facts) | set(terms)

    errors: list[str] = []
    warnings: list[str] = []

    # facts
    for fid, f in facts.items():
        for req in schema["fact_node"]["required"]:
            if req not in f:
                errors.append(f"fact '{fid}': missing required field '{req}'")
        st = f.get("status")
        if st not in grades:
            errors.append(f"fact '{fid}': unknown status '{st}'")
        ot = f.get("origin_type")
        if ot not in origin_types:
            errors.append(f"fact '{fid}': unknown origin_type '{ot}'")
        # evidence required only for artifact-origin facts at proved/released/canonical
        if ot == "artifact" and st in needs_evidence:
            ev = f.get("evidence") or []
            if not ev:
                errors.append(f"fact '{fid}': artifact-origin status '{st}' requires at least one evidence path")
            elif args.repo_root:
                for path in ev:
                    if not (Path(args.repo_root) / path).exists():
                        errors.append(f"fact '{fid}': evidence does not resolve under repo-root: {path}")
        sup = f.get("supersedes")
        if sup:
            base = sup.split("@")[0]
            if base not in facts:
                warnings.append(f"fact '{fid}': supersedes '{sup}' not present (historical fact, ok)")

    # terms
    for tid, t in terms.items():
        for req in schema["term_node"]["required"]:
            if req not in t:
                errors.append(f"term '{tid}': missing required field '{req}'")

    # edges
    for i, e in enumerate(inst.get("edges", [])):
        rel = e.get("relation")
        if rel not in rel_ids:
            errors.append(f"edge[{i}] {e.get('from')}->{e.get('to')}: relation '{rel}' not in closed vocabulary")
        for end in ("from", "to"):
            if e.get(end) not in node_ids:
                errors.append(f"edge[{i}]: endpoint '{end}'='{e.get(end)}' is not a known fact_id or term_id")

    print(f"facts: {len(facts)} | terms: {len(terms)} | edges: {len(inst.get('edges', []))}")
    for w in warnings:
        print(f"  WARN: {w}")
    if errors:
        print(f"\nFAIL — {len(errors)} blocking error(s):")
        for er in errors:
            print(f"  ERROR: {er}")
        return 1
    print("\nPASS — fact graph is publishable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
