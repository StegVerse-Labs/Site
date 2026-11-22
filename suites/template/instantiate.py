#!/usr/bin/env python3
"""Instantiate a suite from SUITE__TEMPLATE GEN 01.
Verifies every template component against TEMPLATE__MANIFEST__01.json
(SHA-256 + size) BEFORE deriving anything; aborts on any mismatch.
Fills the slots, copies the checker verbatim, generates the derived
suite's PACKAGE__MANIFEST__01.json (recording the derivation), and runs
the derived self-check."""
import argparse, hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def sha(b): return hashlib.sha256(b).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    for a in ["name", "generation", "project-id", "funding-line", "funder",
              "arrangement", "source", "out"]:
        ap.add_argument("--" + a, required=True)
    args = ap.parse_args()

    tman = json.load(open(os.path.join(HERE, "TEMPLATE__MANIFEST__01.json")))
    for m in tman["components"]:
        p = os.path.join(HERE, m["file"])
        if not os.path.exists(p):
            print(f"TEMPLATE INVALID: {m['file']} missing"); return 1
        data = open(p, "rb").read()
        if len(data) != m["bytes"] or sha(data) != m["sha256"]:
            print(f"TEMPLATE INVALID: {m['file']} hash/size mismatch"); return 1
    print(f"template verified: {len(tman['components'])} components, "
          f"manifest sha256 {sha(open(os.path.join(HERE, 'TEMPLATE__MANIFEST__01.json'), 'rb').read())}")

    slots = {"{{SUITE_NAME}}": args.name, "{{GENERATION}}": args.generation,
             "{{PROJECT_ID}}": args.project_id, "{{FUNDING_LINE}}": args.funding_line,
             "{{FUNDER}}": args.funder, "{{ARRANGEMENT}}": args.arrangement,
             "{{SOURCE_LINE}}": args.source,
             "{{STATUS_LINE}}": "FILED AS GEN 01 MEMBER (template instantiation).",
             "{{PURPOSE}}": "TODO — the suite's purpose, stated by its author.",
             "{{LEVELS}}": "TODO — the levels this suite holds apart.",
             "{{MEMBER_TITLE}}": "Spec Member",
             "{{BODY}}": "TODO — member content.",
             "{{POINTERS}}": "TODO — pointers to the surrounding record."}
    os.makedirs(args.out, exist_ok=True)
    mapping = {"README.md.tmpl": "README.md",
               "SUITE__CHARTER__01.md.tmpl": "SUITE__CHARTER__01.md",
               "FUNDING__STATEMENT__01.md.tmpl": "FUNDING__STATEMENT__01.md",
               "SPEC__MEMBER__01.md.tmpl": "SPEC__MEMBER__01.md",
               "REFERENCES__01.md.tmpl": "REFERENCES__01.md",
               "self_check.py.tmpl": "self_check.py"}
    for tmpl, out_name in mapping.items():
        text = open(os.path.join(HERE, tmpl), encoding="utf-8").read()
        if tmpl != "self_check.py.tmpl":
            for k, v in slots.items(): text = text.replace(k, v)
        with open(os.path.join(args.out, out_name), "w", encoding="utf-8") as f: f.write(text)

    sc_hash = sha(open(os.path.join(args.out, "self_check.py"), "rb").read())
    members = []
    for name in sorted(os.listdir(args.out)):
        if name == "PACKAGE__MANIFEST__01.json": continue
        data = open(os.path.join(args.out, name), "rb").read()
        members.append({"file": name, "bytes": len(data), "sha256": sha(data)})
    manifest = {"suite": args.name, "generation": args.generation,
                "project_id": args.project_id, "funding": args.funding_line,
                "source": args.source,
                "derived_from": {"template": "SUITE__TEMPLATE GEN 01",
                                 "template_manifest_sha256": sha(open(os.path.join(HERE, "TEMPLATE__MANIFEST__01.json"), "rb").read()),
                                 "self_check_sha256": sc_hash},
                "manifest_excludes": "PACKAGE__MANIFEST__01.json (this file)",
                "members": members}
    with open(os.path.join(args.out, "PACKAGE__MANIFEST__01.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    # The suite is born with its proof inside it: the prover installs
    # CONFORMANCE__PROOF__01.json as a hashed member and rebinds the manifest.
    r = subprocess.run([sys.executable, os.path.join(HERE, "prove_conformance.py"),
                        args.out, "--install"], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0: print(r.stderr.strip()); return r.returncode
    final = json.load(open(os.path.join(args.out, "PACKAGE__MANIFEST__01.json")))
    print(f"instantiated: {args.out} ({len(final['members'])} members incl. in-suite proof + manifest)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
