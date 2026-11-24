"""Q-67 source build. Python standard library only; no financial transactions.

LOCATED means a verbatim claim and its three evidence locations were fetched.
It does not mean the truth of an arbitrary framework claim was established.
"""
from __future__ import annotations

import hashlib
import http.client
import ipaddress
import json
import os
from pathlib import Path
import re
import secrets
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import zipfile

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "template"
TEMPLATE_SHA = "f63d612c15e2ee364f3df651da8c11948846c61c897899aa45f8e9f6324bcc4e"
PROTOCOL = (ROOT / "protocol.html").read_text()
MAX_BODY = 1024 * 1024
RAILS = {
    "8374": {"offer": "https://8374.stegverse.org/offer", "replay": "https://8374.stegverse.org/chain/manifest.json"},
    "4LPH4": {"offer": "https://4lph4.stegverse.org/offer", "replay": "https://4lph4.stegverse.org/replay"},
}


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def nonallow(code, predicate, repair, entry="/api/intakes"):
    return {"failure_code": code, "failed_predicate": predicate,
            "required_evidence_or_repair": repair, "retry_entrypoint": entry,
            "owning_goal": "Q-67 (native registration UNBOUND)",
            "next_attempt": "After the named repair; observations confer no authority."}


class Refused(ValueError):
    def __init__(self, code, predicate, repair):
        super().__init__(code)
        self.disposition = nonallow(code, predicate, repair)


def public_url(url):
    if not isinstance(url, str) or len(url) > 2048:
        raise Refused("URL_INVALID", "bounded HTTPS URL", "Supply an HTTPS public URL.")
    p = urllib.parse.urlsplit(url)
    if (p.scheme != "https" or not p.hostname or p.username or p.password
            or p.port not in (None, 443) or p.fragment):
        raise Refused("URL_INVALID", "HTTPS, no credentials/fragment, port 443", "Supply a public HTTPS evidence URL without credentials or fragment.")
    if p.hostname.endswith(".") or p.hostname.lower() in ("localhost",):
        raise Refused("URL_NOT_PUBLIC", "public host", "Use a public host.")
    return p


class PublicFetcher:
    """No redirects/proxy/cookies. DNS checked and socket pinned to checked IP.

    This bypasses proxy environment variables deliberately: public intake must
    never turn an operator's private network or authenticated proxy into evidence.
    """
    def __call__(self, url):
        p = public_url(url)
        addresses = socket.getaddrinfo(p.hostname, 443, type=socket.SOCK_STREAM)
        if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
            raise Refused("URL_NOT_PUBLIC", "all resolved addresses globally routable", "Publish evidence on public Internet addresses.")
        family, socktype, proto, _, address = addresses[0]
        raw = socket.socket(family, socktype, proto)
        raw.settimeout(5)
        try:
            raw.connect(address)
            secure = ssl.create_default_context().wrap_socket(raw, server_hostname=p.hostname)
            def stop_read():
                try:
                    secure.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
            timer = threading.Timer(10, stop_read)
            timer.daemon = True
            timer.start()
            conn = http.client.HTTPSConnection(p.hostname, timeout=5)
            conn.sock = secure
            path = urllib.parse.urlunsplit(("", "", p.path or "/", p.query, ""))
            conn.request("GET", path, headers={"User-Agent": "StegVerse-Q67-Evidence-Locator/1", "Accept-Encoding": "identity"})
            response = conn.getresponse()
            data = response.read(MAX_BODY + 1)
            if len(data) > MAX_BODY:
                raise Refused("EVIDENCE_TOO_LARGE", "evidence <= 1 MiB", "Provide a bounded public evidence resource.")
            if response.status != 200:
                raise Refused("EVIDENCE_HTTP_NON_200", "direct GET 200 without redirects", "Use the final public evidence URL returning 200.")
            return {"url": url, "status": response.status, "body": data,
                    "sha256": sha(data), "bytes": len(data),
                    "content_type": response.getheader("Content-Type", "")}
        finally:
            if "timer" in locals():
                timer.cancel()
            raw.close()
            if "conn" in locals():
                conn.close()


def validate_intake(data):
    if not isinstance(data, dict):
        raise Refused("INTAKE_INVALID", "JSON object", "Submit a framework intake object.")
    required = ("framework", "operator", "project_id", "funding", "funder", "arrangement")
    for field in required:
        v = data.get(field)
        if not isinstance(v, str) or not v.strip() or len(v) > 1000 or "{{" in v or "\x00" in v:
            raise Refused("INTAKE_INVALID", "bounded nonempty " + field, "Supply " + field + " as plain text without template tokens.")
    surfaces = data.get("public_surfaces")
    claims = data.get("claims")
    if not isinstance(surfaces, list) or not 1 <= len(surfaces) <= 8:
        raise Refused("INTAKE_INVALID", "1..8 public surfaces", "List the framework's public HTTPS surfaces.")
    for u in surfaces:
        public_url(u)
    if not isinstance(claims, list) or not 1 <= len(claims) <= 12:
        raise Refused("INTAKE_INVALID", "1..12 submitted claims", "Supply at most twelve verbatim claims per intake.")
    for c in claims:
        if not isinstance(c, dict) or not isinstance(c.get("text"), str) or not 1 <= len(c["text"]) <= 4000:
            raise Refused("INTAKE_INVALID", "bounded verbatim claim text", "Supply each claim as text plus optional evidence URLs.")
        for k in ("lives_at", "receipted_by", "replay"):
            if k in c and (not isinstance(c[k], str) or len(c[k]) > 2048):
                raise Refused("INTAKE_INVALID", "bounded evidence pointers", "Use HTTPS evidence pointers as text.")
    # Roundtrip preserves original strings, order, and submitter claims verbatim.
    return json.loads(json.dumps(data))


def analyze(data, fetch):
    results = []
    cache = {}
    deadline = time.monotonic() + 30
    def get(u):
        if u not in cache:
            if time.monotonic() > deadline:
                raise Refused("EVIDENCE_TIME_BUDGET", "analysis within 30 seconds", "Use bounded reachable evidence and retry the intake.")
            cache[u] = fetch(u)
        return cache[u]
    for n, claim in enumerate(data["claims"], 1):
        row = {"id": "C" + str(n), "submitted_claim": claim,
               "status": "EVIDENCE_NOT_FOUND", "truth_verdict": "NOT_DETERMINED"}
        try:
            for field in ("lives_at", "receipted_by", "replay"):
                public_url(claim.get(field, ""))
            lives_url = public_url(claim["lives_at"])
            declared = [public_url(u) for u in data["public_surfaces"]]
            if not any(lives_url.hostname == p.hostname and
                       (lives_url.path == p.path or lives_url.path.startswith(p.path.rstrip("/") + "/"))
                       for p in declared):
                raise Refused("CLAIM_SURFACE_UNDECLARED", "lives_at within a declared framework surface", "Declare the exact public framework surface before locating a claim there.")
            lives = get(claim["lives_at"])
            if claim["text"] not in lives["body"].decode("utf-8", errors="replace"):
                raise Refused("CLAIM_TEXT_NOT_LOCATED", "verbatim submitted claim on lives_at", "Provide a public surface containing the exact submitted text.")
            evidence = {field: get(claim[field]) for field in ("lives_at", "receipted_by", "replay")}
            row["evidence"] = {k: {a: v[a] for a in ("url", "status", "sha256", "bytes")} for k, v in evidence.items()}
            row["status"] = "LOCATED"
            row["scope"] = "Claim text located verbatim; receipt and replay URLs reachable. Receipt semantics and claim truth are NOT verified."
        except (ValueError, OSError, http.client.HTTPException) as error:
            row["disposition"] = error.disposition if isinstance(error, Refused) else nonallow("EVIDENCE_UNAVAILABLE", "public evidence fetch", "Provide reachable public evidence; retry after reachability is restored.")
        results.append(row)
    return {"claims": results, "located": sum(r["status"] == "LOCATED" for r in results),
            "evidence_not_found": sum(r["status"] == "EVIDENCE_NOT_FOUND" for r in results),
            "method": "Literal evidence-location check, not a proof of arbitrary claim semantics."}


def verify_template(path=None):
    path = TEMPLATE if path is None else path
    raw = (path / "TEMPLATE__MANIFEST__01.json").read_bytes()
    if sha(raw) != TEMPLATE_SHA:
        raise Refused("TEMPLATE_HASH_MISMATCH", "canonical template manifest pin", "Restore exact canonical GEN 01 template bytes.")
    manifest = json.loads(raw)
    for m in manifest["components"]:
        b = (path / m["file"]).read_bytes()
        if len(b) != m["bytes"] or sha(b) != m["sha256"]:
            raise Refused("TEMPLATE_COMPONENT_MISMATCH", m["file"], "Restore the canonical component before deriving any output.")
    return manifest


def rebind(suite):
    path = suite / "PACKAGE__MANIFEST__01.json"
    manifest = json.loads(path.read_bytes())
    manifest["members"] = [{"file": p.name, "bytes": p.stat().st_size, "sha256": sha(p.read_bytes())}
                           for p in sorted(suite.iterdir()) if p.is_file() and p != path]
    path.write_bytes(encoded(manifest))


def run_python(script, *args):
    result = subprocess.run([sys.executable, "-B", str(script), *map(str, args)],
                            cwd=ROOT, capture_output=True, text=True, timeout=30,
                            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    if result.returncode:
        raise Refused("NON_CONFORMANT", "canonical conformance instrument passes", result.stdout + result.stderr)
    return result.stdout


class Pipeline:
    def __init__(self, storage, fetch=None):
        self.storage = Path(storage)
        self.storage.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.fetch = fetch or PublicFetcher()
        self.lock = threading.Lock()

    def intake(self, data):
        data = validate_intake(data)
        with self.lock:
            if sum(p.is_dir() for p in self.storage.iterdir()) >= 1000:
                raise Refused("CAPACITY_UNAVAILABLE", "retained intake count below 1000", "Existing operator applies the declared retention policy before accepting more intakes.")
            identifier = "INTAKE-" + secrets.token_hex(16)
            path = self.storage / identifier
            path.mkdir(mode=0o700)
        receipt = {"id": identifier, "kind": "INTAKE", "input_sha256": sha(encoded(data)),
                   "authority_effect": "NONE", "grade": "LOCAL_SERVICE_RECEIPT",
                   "observation_time": time.time(), "retention": "Operator-managed; downloadable bundle is the submitter's copy."}
        (path / "intake.json").write_bytes(encoded(data))
        (path / "receipt.json").write_bytes(encoded(receipt))
        return receipt

    def directory_for(self, identifier):
        if not re.fullmatch(r"INTAKE-[a-f0-9]{32}", identifier):
            raise FileNotFoundError(identifier)
        p = self.storage / identifier
        if not p.is_dir():
            raise FileNotFoundError(identifier)
        return p

    def run(self, identifier):
        # Single writer, repeated build requests return the same retained result.
        with self.lock:
            p = self.directory_for(identifier)
            if (p / "result.json").exists():
                return json.loads((p / "result.json").read_bytes())
            data = json.loads((p / "intake.json").read_bytes())
            verify_template()  # includes instantiator + prover, before subprocesses.
            analysis = analyze(data, self.fetch)
            (p / "analysis.json").write_bytes(encoded(analysis))
            # Build in a disposable tree. Failed conformance never leaks partial downloads.
            with tempfile.TemporaryDirectory(prefix=".q67-", dir=self.storage) as temp:
                suite = Path(temp) / "suite"
                run_python(TEMPLATE / "instantiate.py", "--name", data["framework"], "--generation", "GEN 01",
                           "--project-id", data["project_id"], "--funding-line", data["funding"],
                           "--funder", data["funder"], "--arrangement", data["arrangement"],
                           "--source", "Q-67 intake " + identifier, "--out", suite)
                located = [r for r in analysis["claims"] if r["status"] == "LOCATED"]
                gaps = [r for r in analysis["claims"] if r["status"] != "LOCATED"]
                # Claims and gaps occupy distinct data members, never silent upgrades.
                (suite / "CLAIMS__01.json").write_bytes(encoded({"scope": "LOCATED, truth NOT_DETERMINED", "claims": located}))
                (suite / "GAPS__01.json").write_bytes(encoded({"gaps": gaps}))
                (suite / "ANALYSIS__01.json").write_bytes(encoded(analysis))
                (suite / "INTAKE__RECEIPT__01.json").write_bytes((p / "receipt.json").read_bytes())
                (suite / "PROTOCOL__01.html").write_text(PROTOCOL)
                # Canonical instantiator deliberately emits author slots. Supply instance
                # content as derived members, retain template bytes and derivation pin.
                (suite / "SUITE__CHARTER__01.md").write_text("# Framework evidence determination\n\n" +
                    "ProjectID: " + data["project_id"] + "\nFunding: " + data["funding"] + "\n\n" +
                    "Submitted claims, evidence location, claim truth and rail acceptance are distinct.\n" +
                    "See CLAIMS__01.json, GAPS__01.json and ANALYSIS__01.json.\n")
                (suite / "SPEC__MEMBER__01.md").write_text("# Evidence boundary\n\n" +
                    "Only LOCATED claims enter CLAIMS__01.json. Reachability is not semantic validation.\n" +
                    "No automatic funds transfer, wallet custody or sovereign admission is performed.\n")
                (suite / "REFERENCES__01.md").write_text("# Public surfaces (submitter declarations)\n\n" + "\n".join(data["public_surfaces"]) + "\n")
                connection = {"state": "IN_BUILD", "rail_acceptance": "NOT_OBSERVED", "rails": RAILS,
                    "protocol": "PROTOCOL__01.html", "client": "rail_client.py",
                    "registration": "NOT_PERFORMED", "badge": "NOT_DECLARED", "pass_through": "NOT_TAKEN",
                    "disposition": nonallow("CONNECTION_NOT_INSTALLED", "verified hosted rail connection adapter and live instance",
                        "Existing runtime owner must install the on-ramp and bind its verified rail registration/receipt-pair adapter; non-author lane replays V1–V5 before offering full service.")}
                (suite / "CONNECTION__01.json").write_bytes(encoded(connection))
                (suite / "rail_client.py").write_bytes((ROOT / "rail_client.py").read_bytes())
                face = (suite / "README.md").read_text()
                face += ("\n## Actual instance state\n\nSPECIMEN ONLY — full connected product is not offered today.\n" +
                    "LOCATED means evidence locations found; it is not a truth verdict.\n" +
                    "Analysis: ANALYSIS__01.json. In-suite proof: CONFORMANCE__PROOF__01.json.\n" +
                    "Connection state and exact repair: CONNECTION__01.json.\n" +
                    "Rail client is read-only and transfers no value. It reads current offers rather than hardcoding prices.\n")
                (suite / "README.md").write_text(face)
                rebind(suite)
                proof_output = run_python(TEMPLATE / "prove_conformance.py", suite, "--install")
                diagnostic = run_python(TEMPLATE / "prove_conformance.py", suite)
                (p / "conformance.txt").write_text(proof_output + diagnostic)
                proof = json.loads((suite / "CONFORMANCE__PROOF__01.json").read_bytes())
                manifest_sha = sha((suite / "PACKAGE__MANIFEST__01.json").read_bytes())
                archive = Path(temp) / "suite.zip"
                with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
                    for member in sorted(suite.iterdir()):
                        if member.is_file():
                            z.write(member, "suite/" + member.name)
                archive.replace(p / "suite.zip")
            result = {"id": identifier, "state": "SPECIMEN_ONLY", "analysis": analysis,
                "conformance": proof, "manifest_sha256": manifest_sha,
                "bundle_sha256": sha((p / "suite.zip").read_bytes()),
                "download": "/api/intakes/" + identifier + "/bundle",
                "connection": connection, "independent_validation": "NOT_PERFORMED"}
            (p / "result.json").write_bytes(encoded(result))
            return result

    def status(self):
        try:
            verify_template()
            template_state = "AVAILABLE"
        except (OSError, ValueError):
            template_state = "UNAVAILABLE"
        return {"service": "q67-onramp", "mode": "SPECIMEN_ONLY", "authority_effect": "NONE",
                "observation_time": time.time(), "stages": {
                    "S1-INTAKE": "AVAILABLE" if os.access(self.storage, os.W_OK) else "UNAVAILABLE",
                    "S2-ANALYZE": "IMPLEMENTED_NOT_LIVE_PROBED", "S3-GENERATE": template_state,
                    "S4-CONNECT": "IN_BUILD", "S5-DELIVER": "SPECIMEN_ONLY"},
                "stage_check_scope": "local handler/storage/template checks; not a production V1–V5 acceptance test",
                "full_pipeline_offered": False, "independent_validation": "REQUIRED"}
