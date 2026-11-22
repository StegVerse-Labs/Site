#!/usr/bin/env python3
"""StegVM GEN 03 birth bootstrap (STEGVM-01) — cross-machine birth.

Run this on a fresh machine (reference target: a Raspberry Pi 4 with a
stock Raspberry Pi OS — Python 3 standard library only, nothing to
install, no sudo, no system changes). The machine is born as a StegVM
instance from the RECORD ALONE:

  1. PREFLIGHT  Python >= 3.9, the production read surfaces reachable,
                >= 1 GB free disk. Each check prints.
  2. DEFINITION the StegVM GEN 01 suite ZIP is fetched from its public
                KnowledgeVault location and verified against its filed
                SHA-256 pin BEFORE anything in it is trusted. A hash
                mismatch stops the birth; nothing proceeds on a bad
                hash.
  3. GATE       the suite's own birth_gate.py is imported from the
                extracted, hash-verified suite: its disposition
                grammar (deny()) and its failure codes judge this
                birth. The definition inside the suite must hash to
                the GEN 01 pin (6489752a...), and the suite must pass
                its own self_check.py.
  4. STATE      the production chain state is fetched over HTTPS from
                the live public read surfaces — the way any remote
                host obtains it. Nothing is copied from any local
                filesystem.
  5. JUDGMENT   each fetched chain is recomputed locally and compared
                against the anchor the production record states live:
                  - endpoint: verify_chain.py — the production chain
                    service's own standalone verifier, fetched from
                    its /chain/verifier.py route and checked against
                    the SHA-256 pin the production manifest publishes
                    (the same verifier the GEN 01 gate shells out to
                    for its chain-export leg);
                  - 4lph4: recomputed under chain4-rules/1 exactly as
                    published in the production chain manifest.
                Chains with no public recompute surface (router,
                skap-signing — localhost-only by the production
                proxy's own route table) are recorded NOT_JUDGED,
                never silently passed.
  6. SERVE      on ALLOW only: the instance serves the verified chain
                on its LAN address (/chain, /chain/manifest.json,
                /chain/export.ndjson) and proves its own surface by
                running the production verifier against itself. On
                DENY it prints the six-field disposition and serves
                nothing.

Footprint: everything the program writes lives under one directory
(default ~/stegvm-birth). `python3 birth.py --clean` removes it.

Usage:
  python3 birth.py [--port 8799] [--root DIR] [--clean]
                   [--self-test-tamper]

Exit codes: 0 = ALLOW and serving (until Ctrl-C) / clean done;
1 = DENY (a statement about the transition, not a defect);
2 = preflight failure; 3 = definition fetch/hash failure.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
import zipfile
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ---- The record's pins (filed; changing one is a new filing, never an
# ---- edit at the gate) ---------------------------------------------
SUITE_ZIP_URL = ("https://drive.google.com/uc?export=download&id="
                 "1JGRf8baYNfeTRWo-XZwWd8EB89AKLo3B")
SUITE_ZIP_SHA256 = ("f2ecbd5744bc8845ed75c03d6523a4ef103ab2290a8ed99353"
                    "5f66c3fd2f6864")
SUITE_ZIP_BYTES = 32598
SUITE_DIR_NAME = "STEGVM__SUITE__GEN__01"
DEFINITION_NAME = "STEGVM__FLEET__MANIFEST__01.json"
DEFINITION_SHA256 = ("6489752a3a66e6f2566bd976360b3e9b7e4a49eb16de43e09"
                     "d549440a880afd9")
VERIFIER_SHA256 = ("24669106d134b607dc7b707568c303e368ff99018d2c5ed7c4"
                   "5dab67a4dffe25")
CHAIN_ROOT = "https://8374.stegverse.org/chain"
# Mirror of the production verifier on the Site leg (a different,
# healthy transport). The bytes are judged against the production
# manifest's published pin either way — the pin is the judge, the
# leg is fungible.
SITE_VERIFIER_URL = "https://stegverse.org/stegvm/verify_chain.py"
LPH4_ROOT = "https://4lph4.stegverse.org"
UA = "stegvm-gen03-birth/1"
OWNING_GOAL = "Ephemeral Stack program (STEGVM-01)"


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def http_get(url, timeout=30):
    """One logical fetch over an unreliable transport. The algorithm
    is the production verifier's own (verify_chain.py's
    fetch_url_full, the transport the record already trusts on these
    legs): public legs truncate single responses for some client
    classes and occasionally reset connections, so every attempt's
    partial bytes are kept as the held prefix and the next attempt
    resumes from the exact byte count held (Range: bytes=N-);
    completion is judged against the stated Content-Length.
    Reassembly is transport only: every judgment downstream is made
    on hashes and recomputes over the assembled bytes, so no
    transport cure can admit anything a clean single fetch would
    not."""
    import http.client
    got = bytearray()
    total = None
    ctype = None
    last_err = None
    # Attempt ceiling is generous on purpose: on a sick leg the held
    # prefix ratchets upward in tranches across repeated requests
    # (observed from the coordinator VM's egress, 2026-11-22: one
    # 15,515-byte body completed at attempt 21 after long stalls at
    # 12,310 and 14,429 bytes). On a healthy leg the first attempt
    # completes and the ceiling never matters.
    for _attempt in range(90):
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", UA)
        req.add_header("Accept", "*/*")
        if got and total is not None:
            req.add_header("Range", "bytes=%d-" % len(got))
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                status = r.status
                stated = r.headers.get("Content-Length")
                crange = r.headers.get("Content-Range") or ""
                ctype = r.headers.get_content_type()
                if status == 200 and stated is not None:
                    total = int(stated)
                elif status == 206 and "/" in crange:
                    try:
                        total = int(crange.rsplit("/", 1)[1])
                    except ValueError:
                        pass
                try:
                    data = r.read()
                    complete = True
                except http.client.IncompleteRead as e:
                    data = e.partial or b""
                    complete = False
        except urllib.error.HTTPError:
            raise
        except Exception as e:  # noqa: BLE001 — dropped connection
            last_err = e
            time.sleep(0.7)
            continue
        if status == 206:
            got += data
        elif complete and stated is not None \
                and len(data) == int(stated):
            return bytes(data), ctype
        elif not complete:
            if len(data) > len(got):
                got = bytearray(data)
        else:
            return bytes(data), ctype
        if total is not None and len(got) == total:
            return bytes(got), ctype
        if total is not None and len(got) > total:
            raise ValueError("server sent more bytes than the "
                             "stated Content-Length")
        time.sleep(0.4)
    raise ValueError("could not fetch a complete body from %s in 90 "
                     "attempts (held %d of %s bytes; last error %r)"
                     % (url, len(got), total, last_err))


def http_get_json(url, timeout=30):
    data, _ = http_get(url, timeout=timeout)
    return json.loads(data.decode("utf-8", "replace"))


def fetch_suite_zip(url):
    """Drive anyone-reader download. Returns the ZIP bytes. Handles
    the confirm interstitial if Drive serves one (an HTML page instead
    of the file): the real download link is extracted and followed
    once. Route evidence: from the coordinator VM's egress on
    2026-11-22 the direct uc?export=download form returned the file
    itself, byte-exact against the filed pins."""
    data, ctype = http_get(url, timeout=60)
    if ctype == "text/html" or data[:1] == b"<":
        m = re.search(r'href="(/uc\?export=download[^"]+)"', data.decode(
            "utf-8", "replace"))
        if not m:
            m = re.search(r'href="(https://drive\.google\.com/uc\?export'
                          r'=download[^"]+)"', data.decode("utf-8",
                                                           "replace"))
        if not m:
            raise RuntimeError("Drive served an interstitial page and "
                               "no download link could be extracted")
        link = m.group(1).replace("&amp;", "&")
        if link.startswith("/"):
            link = "https://drive.google.com" + link
        data, _ = http_get(link, timeout=60)
    return data


def fetch_export(manifest):
    """The endpoint chain export, verbatim. Some public legs truncate
    large single responses; completeness is checked against the
    manifest's entry count and, when a single fetch comes back short,
    the export is reassembled from entry windows (transport only —
    the recompute judges the assembled stream)."""
    entries_expected = manifest["entries"]

    def count_lines(data):
        return sum(1 for ln in data.splitlines() if ln.strip())

    data, _ = http_get(manifest["export_url"], timeout=60)
    if count_lines(data) >= entries_expected:
        return data
    out = []
    offset = 0
    window = 32
    while offset < entries_expected:
        url = "%s?offset=%d&limit=%d" % (manifest["export_url"], offset,
                                         window)
        chunk, _ = http_get(url, timeout=60)
        lines = [ln for ln in chunk.splitlines() if ln.strip()]
        if not lines:
            break
        out.extend(lines)
        offset += len(lines)
    return b"\n".join(out) + b"\n"


def recompute_chain4(export_bytes, expected_anchor):
    """chain4-rules/1, exactly as published in the production chain
    manifest: entry hash = SHA-256 of the canonical JSON of the full
    entry excluding the hash field; every entry's prev is the previous
    entry's hash; the genesis entry's prev is 64 zero hex digits; the
    terminal anchor is the last entry's hash."""
    doc = json.loads(export_bytes.decode("utf-8"))
    ents = doc["segment"]
    prev = "0" * 64
    problems = []
    pairs = set()
    for i, e in enumerate(ents):
        if e.get("prev") != prev:
            problems.append("entry %d: prev linkage broken" % i)
            break
        body = {k: v for k, v in e.items() if k != "hash"}
        canon = json.dumps(body, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=False).encode("utf-8")
        h = hashlib.sha256(canon).hexdigest()
        if h != e.get("hash"):
            problems.append("entry %d: hash does not recompute" % i)
            break
        if e.get("pair_id"):
            pairs.add(e["pair_id"])
        prev = e["hash"]
    return {"verdict": "MATCH" if not problems and prev == expected_anchor
            else "MISMATCH",
            "entries": len(ents), "pairs": len(pairs),
            "anchor": prev, "problems": problems}


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8799)
    ap.add_argument("--root", default=os.path.expanduser("~/stegvm-birth"))
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--self-test-tamper", action="store_true",
                    help="TEST ONLY: flip one hex character in one "
                         "fetched endpoint entry hash before judgment; "
                         "a correct gate DENYs and serves nothing")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)

    if args.clean:
        if os.path.isdir(root):
            shutil.rmtree(root)
            print("removed %s" % root)
        else:
            print("nothing to remove at %s" % root)
        return 0

    print("=== StegVM GEN 03 birth — this machine, from the record "
          "alone ===")
    if args.self_test_tamper:
        print("*** SELF-TEST TAMPER MODE: one fetched entry will be "
              "corrupted on purpose. A correct gate DENYs. ***")

    # ---- 1. Preflight ------------------------------------------------
    print("-- preflight")
    ok = True
    v = sys.version_info
    print("   python %d.%d.%d (need >= 3.9): %s"
          % (v[0], v[1], v[2], "PASS" if v >= (3, 9) else "FAIL"))
    ok = ok and v >= (3, 9)
    print("   platform: %s / %s" % (os.uname().sysname, os.uname().machine))
    try:
        st = os.statvfs(os.path.expanduser("~"))
        free_gb = st.f_bavail * st.f_frsize / 1e9
    except Exception:
        free_gb = 0
    print("   free disk %.1f GB (need >= 1): %s"
          % (free_gb, "PASS" if free_gb >= 1 else "FAIL"))
    ok = ok and free_gb >= 1
    try:
        doc = http_get_json(CHAIN_ROOT, timeout=20)
        print("   production read surface %s reachable: PASS "
              "(%d entries live)" % (CHAIN_ROOT, doc.get("entries", -1)))
    except Exception as e:
        print("   production read surface %s reachable: FAIL (%r)"
              % (CHAIN_ROOT, e))
        ok = False
    if not ok:
        print("PREFLIGHT FAILED — the missing item is printed above; "
              "nothing was written.")
        return 2

    os.makedirs(os.path.join(root, "state", "endpoint"), exist_ok=True)
    os.makedirs(os.path.join(root, "state", "4lph4"), exist_ok=True)

    # ---- 2. Definition, by hash --------------------------------------
    print("-- definition (StegVM GEN 01 suite, fetched from the KV)")
    try:
        zdata = fetch_suite_zip(SUITE_ZIP_URL)
    except Exception as e:
        print("   suite fetch failed: %r" % (e,))
        return 3
    got = sha256_bytes(zdata)
    print("   suite ZIP: %d bytes (filed %d), sha256 %s"
          % (len(zdata), SUITE_ZIP_BYTES, got))
    if got != SUITE_ZIP_SHA256 or len(zdata) != SUITE_ZIP_BYTES:
        print("   DEFINITION HASH MISMATCH — expected %s. STOP: "
              "nothing proceeds on a bad hash." % SUITE_ZIP_SHA256)
        return 3
    print("   hash verifies against the filed pin: PASS")
    zpath = os.path.join(root, "suite.zip")
    with open(zpath, "wb") as f:
        f.write(zdata)
    suite_dir = os.path.join(root, "suite")
    with zipfile.ZipFile(zpath) as z:
        z.extractall(suite_dir)
    suite_root = os.path.join(suite_dir, SUITE_DIR_NAME)

    # ---- 3. The suite's own gate judges ------------------------------
    spec = importlib.util.spec_from_file_location(
        "birth_gate", os.path.join(suite_root, "birth_gate.py"))
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)

    def emit(result):
        text = json.dumps(result, indent=2)
        print(text)
        with open(os.path.join(root, "birth_record.json"), "w") as f:
            f.write(text + "\n")
        return 0 if result.get("gate_verdict") == "ALLOW" else 1

    definition = os.path.join(suite_root, DEFINITION_NAME)
    actual = gate.sha256_file(definition)
    if actual != DEFINITION_SHA256:
        return emit(gate.deny(
            "DEFINITION_HASH_MISMATCH",
            "the StegVM definition being instantiated must hash to its "
            "pinned SHA-256 before any replay counts (expected %s, "
            "recomputed %s)" % (DEFINITION_SHA256, actual),
            "present the definition at its pinned hash, or re-pin the "
            "hash through the record (a new filing), never by editing "
            "the pin at the gate",
            "birth.py with the suite at its filed hash",
            "re-run the birth once the definition verifies"))
    print("   definition %s hashes to the GEN 01 pin: PASS"
          % DEFINITION_NAME)
    r = subprocess.run([sys.executable,
                        os.path.join(suite_root, "self_check.py")],
                       capture_output=True, text=True, timeout=120)
    tail = (r.stdout or "").strip().splitlines()
    print("   suite self-check: %s" % (tail[-1] if tail else r.returncode))
    if r.returncode != 0:
        return emit(gate.deny(
            "SUITE_MEMBER_VERIFICATION_FAIL",
            "the extracted suite must pass its own self_check.py "
            "(every manifest member verifies) before its gate may "
            "judge a birth",
            "re-fetch the suite ZIP and verify its filed SHA-256; if "
            "the failure persists at the pinned hash, the suite itself "
            "is the defect — file it, do not work around it",
            "birth.py against a self-verifying suite",
            "re-run the birth once the suite self-verifies"))

    # ---- 4. State, over the network, from the live record ------------
    print("-- state (fetched over HTTPS from the production read "
          "surfaces)")
    try:
        manifest = http_get_json(CHAIN_ROOT + "/manifest.json")
        lph_replay = http_get_json(LPH4_ROOT + "/replay")
        lph_manifest = http_get_json(LPH4_ROOT + "/manifest")
    except Exception as e:
        return emit(gate.deny(
            "EXPECTED_RECORD_UNAVAILABLE",
            "the gate compares against the record at birth time; a "
            "production read surface did not answer (%r)" % (e,),
            "restore network reachability to the production read "
            "surfaces and re-run; the gate does not fall back to "
            "pinned anchors",
            "birth.py once every production replay surface answers",
            "re-run the birth when the record is reachable"))
    if lph_replay.get("verdict") != "MATCH":
        return emit(gate.deny(
            "PRODUCTION_REPLAY_NOT_MATCH",
            "the record itself does not replay to MATCH for: 4lph4 — "
            "an instance cannot be admitted against a record that "
            "does not verify",
            "repair the production chain state through its own "
            "governed route, then re-run",
            "birth.py once production replays MATCH on all judged "
            "chains",
            "re-run the birth after production repair"))
    exp_anchor = manifest["terminal_anchor"]
    lph_anchor = lph_replay["terminal_anchor"]
    if lph_manifest.get("terminal_anchor") != lph_anchor:
        return emit(gate.deny(
            "EXPECTED_RECORD_UNAVAILABLE",
            "the production 4lph4 surfaces disagree on the terminal "
            "anchor (manifest %s, replay %s); the gate does not choose "
            "between two statements of the record"
            % (lph_manifest.get("terminal_anchor"), lph_anchor),
            "reconcile the production 4lph4 surfaces through their "
            "own route, then re-run",
            "birth.py once the production surfaces agree",
            "re-run the birth after reconciliation"))
    print("   expected anchors (live): endpoint %s… (%d entries), "
          "4lph4 %s… (%d entries)"
          % (exp_anchor[:16], manifest["entries"], lph_anchor[:16],
             lph_replay["entries"]))

    verifier_pin = (manifest.get("verifier") or {}).get("sha256")
    vdata = None
    verr = None
    for vsrc in (CHAIN_ROOT + "/verifier.py", SITE_VERIFIER_URL):
        try:
            vdata, _ = http_get(vsrc, timeout=30)
            break
        except Exception as e:  # noqa: BLE001 — try the other leg
            verr = e
    if vdata is None:
        return emit(gate.deny(
            "EXPECTED_RECORD_UNAVAILABLE",
            "the production verifier could not be fetched from "
            "either of its legs (%r); without the record's own "
            "verifier at its published pin, the endpoint chain "
            "cannot be judged and the birth does not proceed"
            % (verr,),
            "restore network reachability to the production read "
            "surfaces and re-run; the gate does not substitute a "
            "local or unverified verifier",
            "birth.py once the verifier fetches from either leg",
            "re-run the birth when the record is reachable"))
    vhash = sha256_bytes(vdata)
    if vhash != VERIFIER_SHA256 or (verifier_pin and
                                    verifier_pin != VERIFIER_SHA256):
        return emit(gate.deny(
            "VERIFIER_PIN_MISMATCH",
            "the endpoint verifier fetched from the production chain "
            "service must hash to the SHA-256 the production manifest "
            "publishes (pin %s, recomputed %s, manifest states %s)"
            % (VERIFIER_SHA256, vhash, verifier_pin),
            "the verifier is part of the record: re-fetch it from the "
            "production service; if the mismatch persists, the "
            "record's pin has moved and the birth pins must be "
            "re-filed, never edited locally",
            "birth.py with the verifier at its published pin",
            "re-run the birth once the verifier verifies"))
    verifier_path = os.path.join(root, "verify_chain.py")
    with open(verifier_path, "wb") as f:
        f.write(vdata)
    print("   verify_chain.py: fetched from the production service, "
          "hashes to its published pin: PASS")

    try:
        exp_data = fetch_export(manifest)
        lph_data, _ = http_get(lph_replay["export_url"], timeout=30)
    except Exception as e:
        return emit(gate.deny(
            "EXPECTED_RECORD_UNAVAILABLE",
            "the chain state could not be fetched complete from "
            "the production read surfaces (%r); a birth judges "
            "fetched state, and incomplete state is not judged"
            % (e,),
            "restore network reachability and re-run; the "
            "transport completes bodies by held-prefix resumption "
            "and reports honestly when it cannot",
            "birth.py once the exports fetch complete",
            "re-run the birth when the record is reachable"))
    if args.self_test_tamper:
        txt = exp_data.decode("utf-8")
        m = re.search(r'"hash":\s*"([0-9a-f])', txt)
        if m:
            i = m.start(1)
            repl = "0" if txt[i] != "0" else "1"
            txt = txt[:i] + repl + txt[i + 1:]
            exp_data = txt.encode("utf-8")
            print("   *** TAMPER APPLIED (self-test): one hex "
                  "character flipped in one fetched entry hash ***")
    seg_path = os.path.join(root, "state", "endpoint", "segment-0001.jsonl")
    with open(seg_path, "wb") as f:
        f.write(exp_data)
    print("   endpoint export: %d bytes fetched" % len(exp_data))
    if sha256_bytes(lph_data) != lph_replay["export_sha256"]:
        return emit(gate.deny(
            "CHAIN_ANCHOR_MISMATCH",
            "chain '4lph4': the fetched export must be the export the "
            "production replay surface states (expected export sha256 "
            "%s, recomputed %s)"
            % (lph_replay["export_sha256"], sha256_bytes(lph_data)),
            "re-fetch the export from the production surface; if the "
            "mismatch persists, the surface changed mid-birth — "
            "re-fetch the record and re-run",
            "birth.py against freshly fetched state",
            "re-run the birth; mismatched chains: 4lph4"))
    with open(os.path.join(root, "state", "4lph4", "chain4.json"),
              "wb") as f:
        f.write(lph_data)
    print("   4lph4 export: %d bytes, sha256 matches the production "
          "replay statement: PASS" % len(lph_data))

    # ---- 5. Judgment ---------------------------------------------------
    print("-- judgment (the suite's gate predicates; the chains' own "
          "verifiers)")
    r = subprocess.run([sys.executable, verifier_path, seg_path,
                        "--anchor", exp_anchor],
                       capture_output=True, text=True, timeout=300)
    vout = r.stdout or ""
    rec = re.search(r"terminal_anchor_recomputed:\s*([0-9a-f]+)", vout)
    endpoint_res = {"verdict": "MATCH" if "verdict: MATCH" in vout
                    else "MISMATCH",
                    "anchor": rec.group(1) if rec else None,
                    "entries": manifest["entries"],
                    "pairs": manifest["pairs"]}
    lph_res = recompute_chain4(lph_data, lph_anchor)
    table = {
        "endpoint": {"target_verdict": endpoint_res["verdict"],
                     "target_anchor": endpoint_res["anchor"],
                     "expected_anchor": exp_anchor,
                     "pairs": endpoint_res["pairs"],
                     "entries": endpoint_res["entries"],
                     "anchor_match": bool(
                         endpoint_res["verdict"] == "MATCH"
                         and endpoint_res["anchor"] == exp_anchor)},
        "4lph4": {"target_verdict": lph_res["verdict"],
                  "target_anchor": lph_res["anchor"],
                  "expected_anchor": lph_anchor,
                  "pairs": lph_res["pairs"],
                  "entries": lph_res["entries"],
                  "anchor_match": bool(lph_res["verdict"] == "MATCH"
                                       and lph_res["anchor"]
                                       == lph_anchor)},
        "chain-export": {"target_verdict": endpoint_res["verdict"],
                         "target_anchor": endpoint_res["anchor"],
                         "expected_anchor": exp_anchor,
                         "pairs": endpoint_res["pairs"],
                         "entries": endpoint_res["entries"],
                         "anchor_match": table_anchor(endpoint_res,
                                                      exp_anchor),
                         "note": "the endpoint chain served as a read "
                                 "surface; judged by the same verifier "
                                 "over the same bytes"},
        "router": {"verdict": "NOT_JUDGED",
                   "note": "no public recompute surface: /router/replay "
                           "is localhost-only by the production proxy's "
                           "route table; the chain is neither passed "
                           "nor failed"},
        "skap-signing": {"verdict": "NOT_JUDGED",
                         "note": "no public recompute surface: the "
                                 "signing service is not proxied and "
                                 "remains localhost-only; the chain is "
                                 "neither passed nor failed"},
    }
    mismatches = [c for c in ("endpoint", "4lph4")
                  if not table[c]["anchor_match"]]
    if mismatches:
        first = mismatches[0]
        return emit(gate.deny(
            "CHAIN_ANCHOR_MISMATCH",
            "chain '%s': the target replay must recompute the "
            "production terminal anchor before the instance may serve "
            "(expected %s, recomputed %s, target verdict %s)"
            % (first, table[first]["expected_anchor"],
               table[first]["target_anchor"],
               table[first]["target_verdict"]),
            "re-fetch the chain state from the production read "
            "surfaces and re-run; if the mismatch persists, the "
            "production state changed mid-birth — re-fetch the record "
            "and re-run",
            "birth.py against freshly fetched state",
            "re-run the birth; mismatched chains: %s"
            % ", ".join(sorted(mismatches)),
            extra={"chains_compared": table}))

    instance_id = "stegvm-" + hashlib.sha256(
        (now_iso() + root).encode()).hexdigest()[:12]
    birth = {"gate_verdict": "ALLOW", "ts": now_iso(),
             "binding_record": {
                 "instance_id": instance_id,
                 "host_class": "cross-machine (GEN 03) — %s / %s, "
                               "born from the record alone"
                               % (os.uname().sysname,
                                  os.uname().machine),
                 "suite_generation": "STEGVM GEN 01",
                 "definition": DEFINITION_NAME,
                 "definition_sha256": actual,
                 "birth_ts": now_iso(),
                 "gate_verdict": "ALLOW",
                 "chains_compared": table,
                 "seat_binding": "remote — SEAT_URL of the standing "
                                 "production seat (GEN 01 default for "
                                 "short-lived instances, design D-2); "
                                 "no seat was instantiated",
                 "units_admitted": ["chain-export (read surface over "
                                    "the verified endpoint chain)"],
                 "admission_basis": "definition fetched from the KV "
                                    "and verified against its filed "
                                    "SHA-256; chain state fetched over "
                                    "HTTPS from the production read "
                                    "surfaces and recomputed locally "
                                    "to the live anchors by the "
                                    "chains' own verifiers (endpoint: "
                                    "the production verify_chain.py at "
                                    "its published pin; 4lph4: "
                                    "chain4-rules/1 as published). "
                                    "Router and skap-signing chains "
                                    "NOT_JUDGED — no public recompute "
                                    "surface exists; neither passed "
                                    "nor failed. Signing/settlement "
                                    "services were not booted "
                                    "(credentialess birth, design "
                                    "§2.4).",
                 "target_root": root}}
    with open(os.path.join(root, "birth_record.json"), "w") as f:
        f.write(json.dumps(birth, indent=2) + "\n")

    # ---- 6. Serve ------------------------------------------------------
    served_manifest = {
        "document": "8374 receipt-chain export manifest (StegVM GEN "
                    "03 instance %s)" % instance_id,
        "chain": "8374 endpoint receipt chain (production), served "
                 "by a cross-machine StegVM instance",
        "rules": "receipt-chain-rules/1",
        "format": manifest.get("format"),
        "entries": endpoint_res["entries"],
        "pairs": endpoint_res["pairs"],
        "terminal_anchor": endpoint_res["anchor"],
        "export_sha256": sha256_bytes(exp_data),
        "source": manifest.get("export_url"),
        "instance_id": instance_id,
        "verifier": {"name": "verify_chain.py",
                     "url": CHAIN_ROOT + "/verifier.py",
                     "sha256": VERIFIER_SHA256,
                     "usage": "python3 verify_chain.py http://<this "
                              "host>:%d/chain" % args.port}}
    service_doc = {
        "service": "8374 chain export (StegVM GEN 03 instance)",
        "instance_id": instance_id,
        "what": "the production receipt chain, fetched from the "
                "record and recomputed at birth by this instance; "
                "fetch the export, run the verifier, and the verdict "
                "is yours, not this server's",
        "rules": "receipt-chain-rules/1",
        "entries": endpoint_res["entries"],
        "pairs": endpoint_res["pairs"],
        "terminal_anchor": endpoint_res["anchor"],
        "export_url": "/chain/export.ndjson",
        "manifest_url": "/chain/manifest.json",
        "verifier": served_manifest["verifier"]}

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, body, ctype):
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/chain":
                self._send(json.dumps(service_doc, indent=1).encode(),
                           "application/json")
            elif self.path == "/chain/manifest.json":
                self._send(json.dumps(served_manifest,
                                      indent=1).encode(),
                           "application/json")
            elif self.path == "/chain/export.ndjson":
                self._send(exp_data, "application/x-ndjson")
            else:
                self.send_response(404)
                self.end_headers()

    server = ThreadingHTTPServer(("0.0.0.0", args.port), H)
    # Self-probe: the production verifier, against this instance.
    import threading
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    probe_ok = False
    try:
        r = subprocess.run([sys.executable, verifier_path,
                            "http://127.0.0.1:%d/chain" % args.port],
                           capture_output=True, text=True, timeout=300)
        probe_ok = "verdict: MATCH" in (r.stdout or "")
    except Exception:
        probe_ok = False
    if not probe_ok:
        server.shutdown()
        return emit(gate.deny(
            "INSTANCE_SURFACE_VERIFY_FAIL",
            "the born instance's own served surface must verify "
            "under the production verifier before the birth counts "
            "(self-probe against http://127.0.0.1:%d/chain did not "
            "return MATCH)" % args.port,
            "inspect the served manifest/export against the verified "
            "fetched bytes; the state judged ALLOW is not in question "
            "— the surface is",
            "birth.py once the served surface verifies",
            "re-run the birth; if the probe failure persists, file "
            "it against the GEN 03 bootstrap",
            extra={"chains_compared": table}))
    ip = lan_ip()
    print(json.dumps(birth, indent=2))
    print("")
    print("=== BORN — instance %s is serving the verified chain ==="
          % instance_id)
    print("   on this machine's LAN:  http://%s:%d/chain"
          % (ip, args.port))
    print("   verify it from any other machine:")
    print("     curl -O %s/verifier.py && python3 verify_chain.py "
          "http://%s:%d/chain" % (CHAIN_ROOT, ip, args.port))
    print("   birth record: %s" % os.path.join(root,
                                               "birth_record.json"))
    print("   stop it: Ctrl-C (a death writes nothing; the binding "
          "goes stale, and staleness is data)")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\nstopped — instance %s evaporates; the record holds."
              % instance_id)
    finally:
        server.shutdown()
    return 0


def table_anchor(res, expected):
    return bool(res["verdict"] == "MATCH" and res["anchor"] == expected)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
