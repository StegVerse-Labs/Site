#!/usr/bin/env python3
"""StegVM GEN 04 birth bootstrap (STEGVM-01) — cross-machine birth.

Run this on a fresh machine (reference target: a Raspberry Pi 4 with a
stock Raspberry Pi OS — Python 3 standard library only, nothing to
install, no sudo, no system changes). The machine is born as a StegVM
instance from the RECORD ALONE:

  1. PREFLIGHT  Python >= 3.9, the production read surfaces reachable,
                >= 1 GB free disk. Each check prints.
  2. DEFINITION the StegVM suite ZIPs are fetched from their public
                KnowledgeVault locations and verified against their
                filed SHA-256 pins BEFORE anything in them is
                trusted: the GEN 04 suite (the definition being
                instantiated; filed, #3443 comment 7090130522) and
                the GEN 02 suite (the GEN 04 gate's provenance and
                carried-member continuity predicates require it;
                filed, #3443 comment 7076007769). A hash mismatch
                stops the birth; nothing proceeds on a bad hash.
  3. GATE       the GEN 04 suite's own birth_gate.py judges this
                birth, run as the suite's GEN 04 driver runs it:
                this bootstrap extracts the gate binary from the
                hash-verified GEN 04 ZIP, hands it a birth record,
                and the gate verifies the ZIPs again inside its own
                run, re-executes itself from the verified tree,
                fetches its expected anchors and the chain state
                itself from the record's live public projections,
                replays, and issues ALLOW or a six-field DENY. The
                definition inside the GEN 04 suite must hash to the
                GEN 04 pin (cd538cd6...), and the extracted GEN 04
                suite must pass its own self_check.py before the
                gate is invoked.
  4. JUDGMENT   the gate's, over state it fetched itself — all
                four chains, the record now publishing each in full:
                  - endpoint: the gate's recompute per
                    receipt-chain-rules/1, and independently the
                    record's own published verifier (verify_chain.py,
                    fetched by the gate and hash-verified against the
                    pin inside the production export manifest);
                  - router, skap-signing: the gate's recompute per
                    receipt-chain-rules/1 over their published
                    exports;
                  - 4lph4: the gate's recompute per chain4-rules/1;
                  - and the record's portable verifier
                    (verify_all_chains.py), run by the gate over all
                    four chains with the birth-time anchors as pins.
                The GEN 02 record gap stands CLOSED in the binding
                record (closed 2026-11-22 by the portable-verifier
                cure); no scoped ALLOW exists at GEN 04.
  5. SERVE      on ALLOW only: the suite's own serve_instance.py
                (from the gate's verified tree) serves the instance's
                fetched state on loopback, and this bootstrap — the
                host-side driver, as in GEN 02 — answers external
                queries by relaying them to that server, so what
                the LAN receives is the instance server's own answer.
                The birth counts only after the production verifier,
                run externally against the born instance's surface,
                returns MATCH. On DENY the gate's disposition is
                printed and nothing serves.

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
import http.client
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
# GEN 04 suite — the definition being instantiated (GEN 04
# discharge #3443 comment 7090130522).
SUITE_ZIP_URL = ("https://drive.google.com/uc?export=download&id="
                 "1pL_zL9pb_F9zr_UMGyLVeakKP1e_50zb")
SUITE_ZIP_SHA256 = ("db30ec83b61f2b314148413e4adcc8e114ed512692584ad479d2b"
                    "c5653b55fd9")
SUITE_ZIP_BYTES = 68295
GEN04_DRIVE_ID = "1pL_zL9pb_F9zr_UMGyLVeakKP1e_50zb"
SUITE_DIR_NAME = "STEGVM__SUITE__GEN__04"
# GEN 02 suite — required by the GEN 04 gate's provenance step (the
# definition's predecessor, against which carried-member continuity
# is checked inside the gate). Filed, #3443 comment 7076007769.
GEN02_ZIP_URL = ("https://drive.google.com/uc?export=download&id="
                 "1s9pxZHhOmVD7b7SwcdhReRyqHKLe8giq")
GEN02_ZIP_SHA256 = ("24abc0857df875d521811ec533cab97fc17653a80776c92d768fb"
                    "996769c815c")
GEN02_ZIP_BYTES = 193566
GEN02_DRIVE_ID = "1s9pxZHhOmVD7b7SwcdhReRyqHKLe8giq"
GEN02_DIR_NAME = "STEGVM__SUITE__GEN__02"
DEFINITION_NAME = "STEGVM__FLEET__MANIFEST__01.json"
DEFINITION_SHA256 = ("cd538cd62c6d170f67c1290d585d2a8de526210beac6e953ae11e473ff16a412")
CONTINUITY_MEMBERS = ["fleet_restore.py", "self_check.py"]
VERIFIER_SHA256 = ("24669106d134b607dc7b707568c303e368ff99018d2c5ed7c4"
                   "5dab67a4dffe25")
CHAIN_ROOT = "https://8374.stegverse.org/chain"
UA = "stegvm-gen04-birth/1"
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
                    help="TEST ONLY: ask the gate for its tamper "
                         "variant (one hex character flipped in entry "
                         "i=3 of the fetched endpoint export, inside "
                         "the gate); a correct gate DENYs and serves "
                         "nothing")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    # the instance's own server binds loopback here (serve_instance.py
    # is loopback-only by design); the bootstrap's relay binds the
    # public --port and answers external queries from it, GEN 02
    # driver-style.
    internal_port = args.port + 1000 if args.port <= 64535 \
        else args.port - 1000

    if args.clean:
        if os.path.isdir(root):
            shutil.rmtree(root)
            print("removed %s" % root)
        else:
            print("nothing to remove at %s" % root)
        return 0

    print("=== StegVM GEN 04 birth — this machine, from the record "
          "alone ===")
    if args.self_test_tamper:
        print("*** SELF-TEST TAMPER MODE: the gate will corrupt one "
              "fetched entry on purpose. A correct gate DENYs. ***")

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

    for sub in ("suites", "bootstrap", "gate-work", "gate-state"):
        os.makedirs(os.path.join(root, sub), exist_ok=True)

    # ---- 2. Definition, by hash --------------------------------------
    print("-- definition (StegVM GEN 04 + GEN 02 suites, fetched "
          "from the KV)")
    pins = ((SUITE_ZIP_URL, SUITE_ZIP_SHA256, SUITE_ZIP_BYTES,
             SUITE_DIR_NAME, "GEN 04"),
            (GEN02_ZIP_URL, GEN02_ZIP_SHA256, GEN02_ZIP_BYTES,
             GEN02_DIR_NAME, "GEN 02"))
    zip_paths = {}
    for url, pin, nbytes, dir_name, tag in pins:
        try:
            zdata = fetch_suite_zip(url)
        except Exception as e:
            print("   %s suite fetch failed: %r" % (tag, e))
            return 3
        got = sha256_bytes(zdata)
        print("   %s suite ZIP: %d bytes (filed %d), sha256 %s"
              % (tag, len(zdata), nbytes, got))
        if got != pin or len(zdata) != nbytes:
            print("   DEFINITION HASH MISMATCH (%s) — expected %s. "
                  "STOP: nothing proceeds on a bad hash." % (tag, pin))
            return 3
        print("   %s hash verifies against the filed pin: PASS" % tag)
        zpath = os.path.join(root, "suites", dir_name + ".zip")
        with open(zpath, "wb") as f:
            f.write(zdata)
        zip_paths[tag] = zpath

    # ---- 3. The suite's own gate judges ------------------------------
    # Bootstrap extraction, GEN 04 driver-style: only the gate binary
    # is taken from the verified GEN 04 ZIP; the gate verifies the
    # ZIP against the birth record and re-executes itself from the
    # verified tree before trusting anything (birth_gate.py step 0).
    with zipfile.ZipFile(zip_paths["GEN 04"]) as z:
        gate_name = [n for n in z.namelist()
                     if n.endswith("/birth_gate.py")
                     or n == "birth_gate.py"][0]
        with z.open(gate_name) as src, open(
                os.path.join(root, "bootstrap", "birth_gate.py"),
                "wb") as out:
            out.write(src.read())
    gate_path = os.path.join(root, "bootstrap", "birth_gate.py")
    spec = importlib.util.spec_from_file_location("birth_gate", gate_path)
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)

    def emit(result):
        text = json.dumps(result, indent=2)
        print(text)
        with open(os.path.join(root, "birth_record.json"), "w") as f:
            f.write(text + "\n")
        return 0 if result.get("gate_verdict") == "ALLOW" else 1

    suite_extract = os.path.join(root, "suite")
    with zipfile.ZipFile(zip_paths["GEN 04"]) as z:
        z.extractall(suite_extract)
    suite_root = os.path.join(suite_extract, SUITE_DIR_NAME)

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
    print("   definition %s hashes to the GEN 04 pin: PASS"
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

    # ---- 4. The birth record, handed to the gate ---------------------
    birth_input = {
        "suite": SUITE_DIR_NAME,
        "variant": "tamper" if args.self_test_tamper else "clean",
        "provenance": {
            "gen02_suite_zip": {
                "path": zip_paths["GEN 02"],
                "sha256": GEN02_ZIP_SHA256,
                "drive_id": GEN02_DRIVE_ID,
                "verification": "fetched from the Ecosystem KV by "
                                "Drive id; SHA-256 verified by this "
                                "bootstrap against the filed GEN 02 "
                                "pin before the gate runs and "
                                "re-verified by the gate inside before "
                                "use"},
            "gen04_candidate_zip": {
                "path": zip_paths["GEN 04"],
                "sha256": SUITE_ZIP_SHA256,
                "drive_id": GEN04_DRIVE_ID,
                "verification": "fetched from the Ecosystem KV by "
                                "Drive id; SHA-256 verified by this "
                                "bootstrap against the filed GEN 04 "
                                "pin (GEN 04 discharge, #3443 comment "
                                "7090130522) before the gate runs and "
                                "re-verified by the gate inside before "
                                "use; the announcement is record-issued "
                                "(a filed suite ZIP), not builder-issued"},
        },
        "definition": {"file": DEFINITION_NAME,
                       "sha256": DEFINITION_SHA256},
        "continuity_members": CONTINUITY_MEMBERS,
        "isolation": "cross-machine (GEN 04) — %s / %s, born from "
                     "the record alone" % (os.uname().sysname,
                                            os.uname().machine),
        "isolation_detail": (
            "a separate physical machine (GEN 04 target: the "
            "principal's Raspberry Pi 4); the machine received "
            "nothing from any other host's filesystem — its "
            "definition crossed as the two filed suite ZIPs from the "
            "Ecosystem KV, hash-verified before use, and its chain "
            "state was fetched by the gate itself over HTTPS from "
            "the record's public projections; no credentials exist "
            "in the birth (credentialess birth, design §2.4)"),
        "issued_by": "StegVM GEN 04 birth bootstrap (birth.py)",
        "issued_at": now_iso(),
    }
    birth_input_path = os.path.join(root, "birth_input.json")
    with open(birth_input_path, "w") as f:
        f.write(json.dumps(birth_input, indent=2) + "\n")

    # ---- 5. Judgment — the gate's, over state it fetches itself ------
    print("-- judgment (the GEN 04 gate, run from the verified tree; "
          "it fetches its own anchors and state from the record)")
    gate_out = os.path.join(root, "gate_result.json")
    if os.path.exists(gate_out):
        os.remove(gate_out)
    gate_cmd = [sys.executable, gate_path,
                "--birth-record", birth_input_path,
                "--work", os.path.join(root, "gate-work"),
                "--state", os.path.join(root, "gate-state"),
                "--out", gate_out]
    if args.self_test_tamper:
        gate_cmd.append("--tamper")
    try:
        r = subprocess.run(gate_cmd, capture_output=True, text=True,
                           timeout=1200)
    except subprocess.TimeoutExpired:
        return emit(gate.deny(
            "GATE_EXECUTION_FAIL",
            "the suite's birth gate must run to a verdict (ALLOW or "
            "a six-field DENY) before a birth counts; this run "
            "exceeded the 1200-second ceiling without one",
            "read the gate's fetch behaviour against the public "
            "projections (the measured fragile leg) and re-run",
            "birth.py once the gate runs to a verdict",
            "re-run the birth after the gate's preconditions hold"))
    if not os.path.exists(gate_out):
        print("   the gate produced no result file; exit %d" % r.returncode)
        print("   gate stdout tail: %s" % (r.stdout or "")[-1500:])
        print("   gate stderr tail: %s" % (r.stderr or "")[-1500:])
        return emit(gate.deny(
            "GATE_EXECUTION_FAIL",
            "the suite's birth gate must run to a verdict (ALLOW or "
            "a six-field DENY) before a birth counts; this run ended "
            "with exit %d and no result file" % r.returncode,
            "read the gate output above; repair the run's own "
            "preconditions (network reachability of the public "
            "projections is the measured fragile leg) and re-run",
            "birth.py once the gate runs to a verdict",
            "re-run the birth after the gate's preconditions hold"))
    result = json.load(open(gate_out))
    if result.get("gate_verdict") != "ALLOW":
        print("   gate verdict: DENY — the disposition follows; "
              "nothing serves.")
        return emit(result)
    binding = result["binding_record"]
    table = binding["chains_compared"]
    instance_id = binding["instance_id"]
    for chain in ("endpoint", "chain-export", "router",
                  "skap-signing", "4lph4", "portable-verifier"):
        row = table[chain]
        print("   %-18s %s (anchor %s…)"
              % (chain, row.get("target_verdict"),
                 (row.get("target_anchor") or "")[:16]))
    with open(os.path.join(root, "birth_record.json"), "w") as f:
        f.write(json.dumps(result, indent=2) + "\n")

    # ---- 6. Serve ------------------------------------------------------
    # The suite's own read surface, from the gate's verified tree,
    # over the gate's fetched state. serve_instance.py binds
    # loopback; the relay below is the host-side driver surface.
    serve_py = os.path.join(root, "gate-work", "gen04",
                            "serve_instance.py")
    srv = subprocess.Popen(
        [sys.executable, serve_py,
         "--state", os.path.join(root, "gate-state"),
         "--gate-result", gate_out,
         "--port", str(internal_port)])
    deadline = time.time() + 60
    while True:
        try:
            probe = socket.create_connection(("127.0.0.1",
                                              internal_port),
                                             timeout=2)
            probe.close()
            break
        except OSError:
            if srv.poll() is not None or time.time() > deadline:
                srv.terminate()
                return emit(gate.deny(
                    "INSTANCE_SURFACE_VERIFY_FAIL",
                    "the born instance's read surface "
                    "(serve_instance.py, from the gate's verified "
                    "tree) must start and listen before the birth "
                    "counts as serving",
                    "read the instance server's output; the state "
                    "judged ALLOW is not in question — the surface is",
                    "birth.py once the instance surface starts",
                    "re-run the birth; if the failure persists, file "
                    "it against the GEN 04 suite's serve_instance.py",
                    extra={"chains_compared": table}))
            time.sleep(0.2)

    class Relay(BaseHTTPRequestHandler):
        """GEN 02 driver pattern: external queries are executed
        against the instance's own server and its answers relayed
        verbatim — the LAN receives the instance's own words."""
        def log_message(self, *a):
            pass

        def do_GET(self):
            try:
                conn = http.client.HTTPConnection(
                    "127.0.0.1", internal_port, timeout=30)
                conn.request("GET", self.path)
                resp = conn.getresponse()
                body = resp.read()
                status = resp.status
                ctype = resp.getheader("Content-Type") \
                    or "application/octet-stream"
                conn.close()
            except Exception as e:  # noqa: BLE001
                body = json.dumps(
                    {"error": "instance surface unreachable: %r"
                              % (e,)}).encode()
                status, ctype = 502, "application/json"
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer(("0.0.0.0", args.port), Relay)
    import threading
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    # Self-probe: the production verifier, externally, against this
    # instance's own surface. The copy used is the one the gate
    # fetched from the record and hash-verified against the pin
    # inside the production export manifest; it must also match
    # this bootstrap's filed pin for the probe to count.
    verifier_path = os.path.join(root, "gate-work", "verify_chain.py")
    probe_ok = False
    if os.path.exists(verifier_path) \
            and gate.sha256_file(verifier_path) == VERIFIER_SHA256:
        try:
            r = subprocess.run(
                [sys.executable, verifier_path,
                 "http://127.0.0.1:%d/chain" % args.port],
                capture_output=True, text=True, timeout=300)
            probe_ok = "verdict: MATCH" in (r.stdout or "")
        except Exception:
            probe_ok = False
    if not probe_ok:
        server.shutdown()
        srv.terminate()
        return emit(gate.deny(
            "INSTANCE_SURFACE_VERIFY_FAIL",
            "the born instance's own served surface must verify "
            "under the production verifier before the birth counts "
            "(external probe against http://127.0.0.1:%d/chain did "
            "not return MATCH)" % args.port,
            "inspect the served manifest/export against the state "
            "the gate fetched and judged; the ALLOW is not in "
            "question — the surface is",
            "birth.py once the served surface verifies",
            "re-run the birth; if the probe failure persists, file "
            "it against the GEN 04 bootstrap",
            extra={"chains_compared": table}))
    ip = lan_ip()
    # flush throughout: the verdict banner is the operator's signal
    # to act, and stdout is block-buffered when piped — an unflushed
    # banner would sit in the buffer for the whole serve (observed
    # in the GEN 03 pin-advance script test, 2026-11-22).
    print(json.dumps(result, indent=2), flush=True)
    print("", flush=True)
    print("=== BORN — instance %s is serving the verified chains ==="
          % instance_id, flush=True)
    print("   on this machine's LAN:  http://%s:%d/chain"
          % (ip, args.port), flush=True)
    print("   surfaces: /chain/manifest.json /chain/export.ndjson "
          "/chain/router/export.ndjson /chain/skap/export.ndjson "
          "/chain4.json /verify /bindings /health", flush=True)
    print("   verify it from any other machine:", flush=True)
    print("     curl -O %s/verifier.py && python3 verify_chain.py "
          "http://%s:%d/chain" % (CHAIN_ROOT, ip, args.port),
          flush=True)
    print("   birth record: %s" % os.path.join(root,
                                               "birth_record.json"),
          flush=True)
    print("   stop it: Ctrl-C (a death writes nothing; the binding "
          "goes stale, and staleness is data)", flush=True)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\nstopped — instance %s evaporates; the record holds."
              % instance_id)
    finally:
        server.shutdown()
        srv.terminate()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
