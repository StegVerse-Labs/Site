#!/usr/bin/env python3
"""Prove a suite's conformance to SUITE__TEMPLATE GEN 01.
Usage:
  prove_conformance.py <suite_dir> [proof_out.json]   assess (diagnostic)
  prove_conformance.py <suite_dir> --install          install the proof
The conformance instrument is the proof INSIDE the suite it proves:
CONFORMANCE__PROOF__01.json, a member of the suite, bound by the suite
manifest's hash like every other member. A proof outside the suite is a
diagnostic, not conformance. --install computes the elements, writes the
proof in, regenerates the suite manifest to bind it (template-dialect
manifests only; other dialects take their proof at their next generation),
and re-runs the suite's self-check over the final bytes.
Elements:
  E1 manifest present; every member verifies (size + SHA-256)
  E2 a self-check exists and passes when run
  E2b the suite's checker itself carries the template conformance checks
  E3 suite face (README) carries ProjectID + Funding lines
  E4 a FUNDING__STATEMENT member (or equivalent funding data) carries
     ProjectID / Funding / commercial-arrangement lines
  E5 an in-suite CONFORMANCE__PROOF__01.json exists, is bound by the
     manifest, and names the current template manifest hash"""
import hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TMAN_PATH = os.path.join(HERE, "TEMPLATE__MANIFEST__01.json")
PROOF_NAME = "CONFORMANCE__PROOF__01.json"
ORDER = ["E1_manifest_members_verify", "E2_self_check_passes",
         "E2b_checker_carries_template_checks", "E3_face_carries_projectid_funding",
         "E4_funding_statement", "E5_proof_in_suite"]

def sha(b): return hashlib.sha256(b).hexdigest()
def tman_sha(): return sha(open(TMAN_PATH, "rb").read())

def find_manifest(suite):
    for n in sorted(os.listdir(suite)):
        if "MANIFEST" in n.upper() and n.endswith(".json"):
            try: return n, json.load(open(os.path.join(suite, n)))
            except Exception: return n, None
    return None, None

def member_entries(manifest):
    if not manifest: return None
    for key in ("members", "files", "inventory", "entries"):
        v = manifest.get(key)
        if isinstance(v, list): return v
        if isinstance(v, dict):
            return [dict({"file": k}, **(val if isinstance(val, dict) else {}))
                    for k, val in v.items()]
    return None

def norm(m):
    return (m.get("file") or m.get("path") or m.get("name"),
            m.get("bytes", m.get("size")), m.get("sha256") or m.get("sha"))

def find_checker(suite):
    for n in sorted(os.listdir(suite)):
        if "self" in n.lower() and "check" in n.lower() and n.endswith(".py"): return n
    return None

def run_checker(suite, checker):
    r = subprocess.run([sys.executable, os.path.join(suite, checker)],
                       capture_output=True, text=True, cwd=suite)
    return r.returncode == 0, (r.stdout.strip().splitlines() or [""])[-1]

def assess(suite, tsha, skip_proof_member=False):
    el = {}
    man_name, manifest = find_manifest(suite)
    entries = member_entries(manifest)
    listed = set()
    if entries:
        bad = []
        for m in entries:
            rel, wb, ws = norm(m); listed.add(rel)
            if skip_proof_member and rel == PROOF_NAME: continue
            if not rel: bad.append("entry without a path"); continue
            p = os.path.join(suite, rel)
            if not os.path.exists(p): bad.append(rel + " missing"); continue
            d = open(p, "rb").read()
            if wb is not None and len(d) != wb: bad.append(rel + " size mismatch")
            elif ws and sha(d) != ws: bad.append(rel + " hash mismatch")
        el["E1_manifest_members_verify"] = {"pass": not bad,
            "detail": f"{len(entries)} members, {len(bad)} bad", "bad": bad[:5]}
    else:
        el["E1_manifest_members_verify"] = {"pass": False, "detail": "no manifest with member entries found"}

    checker = find_checker(suite)
    if checker:
        src = open(os.path.join(suite, checker), encoding="utf-8", errors="replace").read()
        el["E2b_checker_carries_template_checks"] = {
            "pass": ("FUNDING" in src and "ProjectID" in src),
            "detail": "checker source names FUNDING + ProjectID" if ("FUNDING" in src and "ProjectID" in src)
                      else "checker predates the template conformance checks"}
    else:
        el["E2b_checker_carries_template_checks"] = {"pass": False, "detail": "no self-check file"}

    readme = ""
    for n in sorted(os.listdir(suite)):
        if n.upper().startswith("README") and n.endswith(".md"):
            readme = open(os.path.join(suite, n), encoding="utf-8", errors="replace").read(); break
    el["E3_face_carries_projectid_funding"] = {
        "pass": ("ProjectID" in readme and "Funding" in readme),
        "detail": "README names ProjectID + Funding" if ("ProjectID" in readme and "Funding" in readme)
                  else "README lacks ProjectID and/or Funding lines"}

    e4 = {"pass": False, "detail": "no funding statement found"}
    cand = [n for n in os.listdir(suite) if "FUNDING" in n.upper() and n.endswith(".md")]
    if cand:
        t = open(os.path.join(suite, cand[0]), encoding="utf-8", errors="replace").read()
        ok = "ProjectID" in t and "Funding" in t and "commercial arrangement" in t.lower()
        e4 = {"pass": ok, "detail": f"{cand[0]} " + ("carries the three lines" if ok else "lacks required lines")}
    elif manifest and manifest.get("funding") and (manifest.get("project_id") or manifest.get("package")):
        e4 = {"pass": True, "detail": "funding carried as manifest data (funding block + package/ProjectID field)"}
    el["E4_funding_statement"] = e4

    ppath = os.path.join(suite, PROOF_NAME)
    if os.path.exists(ppath) and PROOF_NAME in listed:
        try:
            pj = json.load(open(ppath))
            match = pj.get("template_manifest_sha256") == tsha
            el["E5_proof_in_suite"] = {"pass": match,
                "detail": "in-suite proof bound by manifest, names the current template hash"
                          if match else "in-suite proof names a superseded template hash — re-proof required"}
        except Exception:
            el["E5_proof_in_suite"] = {"pass": False, "detail": "in-suite proof file unreadable"}
    else:
        el["E5_proof_in_suite"] = {"pass": False,
            "detail": "no in-suite proof (install: prove_conformance.py <suite> --install)"}
    return el

def public(el): return {k: el[k] for k in ORDER if k in el}
def verdict_of(el): return all(v["pass"] for v in public(el).values())

def regen_manifest(suite, man_name, manifest):
    members = []
    for name in sorted(os.listdir(suite)):
        if name == man_name or name.startswith("."): continue
        p = os.path.join(suite, name)
        if os.path.isfile(p):
            d = open(p, "rb").read()
            members.append({"file": name, "bytes": len(d), "sha256": sha(d)})
    manifest["members"] = members
    with open(os.path.join(suite, man_name), "w") as f: json.dump(manifest, f, indent=2)
    return members

def build_proof(suite, manifest, tsha, el):
    els = public(el)
    els["E5_proof_in_suite"] = {"pass": True,
        "detail": "this file — a member of the suite it proves, bound by the manifest hash"}
    ordered = {k: els[k] for k in ORDER if k in els}
    return {"proof_of": manifest.get("suite") or os.path.basename(os.path.abspath(suite)),
            "template": "SUITE__TEMPLATE GEN 01", "template_manifest_sha256": tsha,
            "convention": "This proof lives inside the suite it proves, as a hashed member "
                          "of the suite manifest. It is excluded from its own E1 enumeration; "
                          "the manifest binds its bytes.",
            "elements": ordered,
            "verdict": "CONFORMANT" if all(v["pass"] for v in ordered.values()) else "NON_CONFORMANT"}

def write_proof(suite, proof):
    with open(os.path.join(suite, PROOF_NAME), "w") as f: json.dump(proof, f, indent=2)

def install(suite):
    tsha = tman_sha()
    man_name, manifest = find_manifest(suite)
    if not manifest or not isinstance(manifest.get("members"), list):
        print("NON-ALLOW: suite manifest is not the template dialect ('members' list).")
        print("Its in-suite proof is installed at its next generation, by its own builder.")
        return 2
    checker = find_checker(suite)
    el = assess(suite, tsha, skip_proof_member=True)
    if checker:
        ok, last = run_checker(suite, checker)
        el["E2_self_check_passes"] = {"pass": ok, "detail": last + " (pre-install run)"}
    write_proof(suite, build_proof(suite, manifest, tsha, el))
    regen_manifest(suite, man_name, manifest)
    if checker:
        ok, last = run_checker(suite, checker)
        el["E2_self_check_passes"] = {"pass": ok, "detail": last}
        write_proof(suite, build_proof(suite, manifest, tsha, el))
        regen_manifest(suite, man_name, manifest)
        ok2, last2 = run_checker(suite, checker)
        print(f"final self-check over installed bytes: {'PASS' if ok2 else 'FAIL'} — {last2}")
        if not ok2: return 1
    final = build_proof(suite, manifest, tsha, el)
    v = final["verdict"] == "CONFORMANT"
    print(f"proof installed in suite: {PROOF_NAME} — verdict {final['verdict']}")
    for k, val in final["elements"].items():
        print(f"  {k}: {'PASS' if val['pass'] else 'FAIL'} — {val['detail']}")
    return 0 if v else 1

def main():
    suite = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--install":
        return install(suite)
    tsha = tman_sha()
    el = assess(suite, tsha)
    checker = find_checker(suite)
    if checker:
        ok, last = run_checker(suite, checker)
        el["E2_self_check_passes"] = {"pass": ok, "detail": last}
    else:
        el["E2_self_check_passes"] = {"pass": False, "detail": "no self-check file"}
    v = verdict_of(el)
    print(f"{os.path.basename(os.path.abspath(suite))}: {'CONFORMANT' if v else 'NON_CONFORMANT'}")
    for k in ORDER:
        if k in el: print(f"  {k}: {'PASS' if el[k]['pass'] else 'FAIL'} — {el[k]['detail']}")
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    if out_path:
        man_name, manifest = find_manifest(suite)
        proof = {"suite_dir": os.path.abspath(suite), "manifest": man_name,
                 "template": "SUITE__TEMPLATE GEN 01", "template_manifest_sha256": tsha,
                 "elements": public(el), "verdict": "CONFORMANT" if v else "NON_CONFORMANT",
                 "note": "Diagnostic printout. Conformance itself is the in-suite proof."}
        with open(out_path, "w") as f: json.dump(proof, f, indent=2)
        print(f"  diagnostic: {out_path}")
    return 0 if v else 1

if __name__ == "__main__":
    sys.exit(main())
