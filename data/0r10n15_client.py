#!/usr/bin/env python3
"""0R10N15 reference client — StegVerse LLC.

Implements the published crossing contract (0R10N15-CROSSING-SCHEMA/1)
for both live instances:

  8374   Base / USDC, x402 exact (EIP-3009), dual-stack v1 + v2
  4LPH4  Tron / USDT (TRC-20), transfer-then-present

What this client does:
  * fetch an instance's /offer
  * fetch an 8374 payment challenge (unpaid POST /crossing) and check
    the challenge's receptor, asset, network, and tier against the
    instance's published constants — refusing to proceed on mismatch
  * present a 4LPH4 payment txid for its disposition
  * verify a receipt pair against an instance's public chain export,
    recomputing the hash chain from GENESIS (receipt-chain-rules/1)
  * verify a RETENTION_BUNDLE/1 file offline

What it deliberately does not do: sign. Producing the x402 payment
header requires an EIP-3009 signature from the payer's own wallet;
use any conformant x402 signer with the challenge this client
returns. The challenge is the complete input to that signature:
payTo, asset, network, and the total in maxAmountRequired (v1) /
accepts[0].amount (v2). Keeping keys out of a reference client is
the point.

Stdlib only. Python 3.9+.
"""

import argparse
import base64
import hashlib
import http.client
import json
import os
import ssl
import sys
import urllib.parse

UA = "StegVerse-Builder-Client/1.0 (0R10N15-CROSSING-SCHEMA/1)"

INSTANCES = {
    "8374": {
        "base_url": "https://8374.stegverse.org",
        "payTo": "0x7721aB66161e60fCcA59CCe2A86817cbdd9b16Be",
        "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "network": "eip155:8453",
        "tiers": {"receipt-only": 500, "full-evaluation": 15000},
        "export_path": "/chain/export.ndjson",
        "export_format": "ndjson-content",
    },
    "4LPH4": {
        "base_url": "https://4lph4.stegverse.org",
        "receptor": "TAfcR4NLCgBFWUC4AjY4kEZShWJWRrmPWv",
        "asset_contract": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
        "tiers": {"receipt": 500, "full-eval": 15000},
        "export_path": "/chain4.json",
        "export_format": "chain4-doc",
    },
}


def _proxy_for(scheme):
    raw = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY") \
        if scheme == "https" else \
        os.environ.get("http_proxy") or os.environ.get("HTTP_PROXY")
    return urllib.parse.urlparse(raw) if raw else None


def _request(url, method="GET", body=None, headers=None, timeout=40):
    """One HTTP request, stdlib http.client.

    Deliberately not urllib: urllib sends `Connection: close` by
    default, and some proxy/tunnel paths answer that by truncating
    response bodies (observed live against these surfaces:
    IncompleteRead at varying offsets, while the identical request
    without the header completes). http.client sends no such header.
    Honors http_proxy/https_proxy env (CONNECT for https), as an
    agent on an arbitrary network may sit behind one.
    """
    parts = urllib.parse.urlparse(url)
    hdrs = {"User-Agent": UA, "Accept": "application/json"}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        hdrs["Content-Type"] = "application/json"
    if headers:
        hdrs.update(headers)
    proxy = _proxy_for(parts.scheme)
    target = parts.path or "/"
    if parts.query:
        target += "?" + parts.query
    if parts.scheme == "https":
        ctx = ssl.create_default_context()
        if proxy is not None:
            conn = http.client.HTTPSConnection(
                proxy.hostname, proxy.port or 3128, timeout=timeout,
                context=ctx)
            tunnel_hdrs = {}
            if proxy.username:
                cred = f"{urllib.parse.unquote(proxy.username)}:" \
                       f"{urllib.parse.unquote(proxy.password or '')}"
                tunnel_hdrs["Proxy-Authorization"] = "Basic " + \
                    base64.b64encode(cred.encode()).decode()
            conn.set_tunnel(parts.hostname, parts.port or 443,
                            headers=tunnel_hdrs)
        else:
            conn = http.client.HTTPSConnection(
                parts.hostname, parts.port or 443, timeout=timeout,
                context=ctx)
    else:
        if proxy is not None:
            conn = http.client.HTTPConnection(
                proxy.hostname, proxy.port or 3128, timeout=timeout)
            target = url
            if proxy.username:
                cred = f"{urllib.parse.unquote(proxy.username)}:" \
                       f"{urllib.parse.unquote(proxy.password or '')}"
                hdrs["Proxy-Authorization"] = "Basic " + \
                    base64.b64encode(cred.encode()).decode()
        else:
            conn = http.client.HTTPConnection(
                parts.hostname, parts.port or 80, timeout=timeout)
    try:
        conn.request(method, target, body=data, headers=hdrs)
        r = conn.getresponse()
        raw = r.read()
        return r.status, {k: v for k, v in r.getheaders()}, raw
    finally:
        conn.close()


def _json(raw):
    return json.loads(raw.decode())


# ---------------- offers and challenges ----------------

def fetch_offer(instance):
    base = INSTANCES[instance]["base_url"]
    status, _h, raw = _request(base + "/offer")
    if status != 200:
        raise SystemExit(f"offer fetch failed: HTTP {status}")
    return _json(raw)


def fetch_challenge(instance="8374", tier="receipt-only",
                    counterparty="reference-client", action="evaluate",
                    scope_ref="specimen", resource="governed-evaluation"):
    """Unpaid POST /crossing. Returns (v1_challenge, v2_challenge).

    Validates the challenge against the instance's published
    constants; raises SystemExit on any mismatch — never sign a
    challenge whose receptor differs from the published one.
    """
    if instance != "8374":
        raise SystemExit("challenges are an 8374 (x402) form; "
                         "4LPH4 is transfer-then-present")
    spec = INSTANCES[instance]
    body = {"counterparty": counterparty, "action": action,
            "scope_ref": scope_ref, "resource": resource, "tier": tier}
    status, headers, raw = _request(spec["base_url"] + "/crossing",
                                    method="POST", body=body)
    if status == 503:
        raise SystemExit(
            "endpoint failed closed (503): no live settlement-charge "
            "quote, no challenge issued. Nothing was consumed; "
            "retry later. Body: " + raw.decode()[:400])
    if status != 402:
        raise SystemExit(f"expected 402 challenge, got HTTP {status}: "
                         + raw.decode()[:400])
    v1 = _json(raw)
    accepts = (v1.get("accepts") or [{}])[0]
    problems = []
    if accepts.get("payTo") != spec["payTo"]:
        problems.append(f"payTo {accepts.get('payTo')} != published "
                        f"{spec['payTo']}")
    if accepts.get("asset") != spec["asset"]:
        problems.append(f"asset {accepts.get('asset')} != published "
                        f"{spec['asset']}")
    if accepts.get("network") != spec["network"]:
        problems.append(f"network {accepts.get('network')} != "
                        f"published {spec['network']}")
    if accepts.get("tier") != tier:
        problems.append(f"tier {accepts.get('tier')} != requested "
                        f"{tier}")
    fee = accepts.get("governance_fee_micro_usdc")
    if fee != spec["tiers"][tier]:
        problems.append(f"governance fee {fee} != published tier fee "
                        f"{spec['tiers'][tier]}")
    total = int(accepts.get("maxAmountRequired", -1))
    if total != accepts.get("total_micro_usdc"):
        problems.append("maxAmountRequired != total_micro_usdc")
    if fee is not None and total >= 0 and \
            total - fee != accepts.get("settlement_charge_micro_usdc"):
        problems.append("total - fee != settlement_charge_micro_usdc")
    if problems:
        raise SystemExit("CHALLENGE MISMATCH — do not sign:\n  "
                         + "\n  ".join(problems))
    v2 = None
    hdr = next((v for k, v in headers.items()
                if k.lower() == "payment-required"), None)
    if hdr:
        v2 = json.loads(base64.b64decode(hdr))
        v2_amount = (v2.get("accepts") or [{}])[0].get("amount")
        if v2_amount != str(total):
            raise SystemExit("CHALLENGE MISMATCH — v2 amount "
                             f"{v2_amount} != v1 total {total}")
    return v1, v2


def present_4lph4(txid, tier="receipt", payload=None, request=None,
                  instance="4LPH4"):
    """Present a landed TRC-20 transfer for its disposition."""
    base = INSTANCES[instance]["base_url"]
    body = {"txid": txid, "tier": tier}
    if payload is not None:
        body["payload"] = payload
    if request is not None:
        body["request"] = request
    status, _h, raw = _request(base + "/crossing", method="POST",
                               body=body)
    if status != 200:
        raise SystemExit(f"presentation answered HTTP {status}: "
                         + raw.decode()[:400])
    return _json(raw)


# ---------------- verification (receipt-chain-rules/1) ----------------

def canonical(obj, ensure_ascii=True):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=ensure_ascii).encode()


def entry_hash(prev, content):
    return hashlib.sha256(prev.encode() + canonical(content)).hexdigest()


def recompute_chain(entries):
    """Verify a list of chain entries from GENESIS.

    Returns (ok, detail). Each entry: {content, hash, i, prev}."""
    prev = "GENESIS"
    for n, e in enumerate(entries, start=1):
        if e.get("prev") != prev:
            return False, f"entry {n}: prev does not continue the chain"
        if entry_hash(prev, e["content"]) != e.get("hash"):
            return False, f"entry {n}: hash does not recompute"
        prev = e["hash"]
    return True, f"{len(entries)} entries recompute from GENESIS; " \
                 f"terminal anchor {prev}"


def find_pair(entries, pair_id):
    idx = [e for e in entries
           if e["content"].get("pair_id") == pair_id]
    if len(idx) != 2:
        return None, f"pair {pair_id}: found {len(idx)} entries, need 2"
    a, b = idx
    if a["content"].get("index_in_pair") != 0 or \
            b["content"].get("index_in_pair") != 1:
        return None, f"pair {pair_id}: index_in_pair is not 0/1"
    if b["content"].get("pair_anchor") != a["hash"]:
        return None, f"pair {pair_id}: pair_anchor != first entry hash"
    return (a, b), f"pair {pair_id} stands; anchor (second entry " \
                   f"hash) {b['hash']}"


def recompute_chain4(entries):
    """Verify a chain4-rules/1 segment (the 4LPH4 rail form).

    Entry: {body, hash, kind, pair_id?, prev, seq}. The entry hash is
    the SHA-256 of the canonical JSON of the full entry excluding
    the hash field; prev links each entry to its predecessor; the
    genesis entry's prev is 64 zero hex digits."""
    prev = "0" * 64
    for n, e in enumerate(entries):
        if e.get("seq") != n:
            return False, f"entry seq {e.get('seq')}: expected {n}"
        if e.get("prev") != prev:
            return False, f"entry seq {n}: prev link broken"
        body = {k: v for k, v in e.items() if k != "hash"}
        # chain4-rules/1 canonical form is ensure_ascii=False (raw
        # UTF-8); the 8374 rail's receipt-chain-rules/1 form escapes
        # non-ASCII. The difference is load-bearing — the genesis
        # body on this rail contains an em-dash.
        digest = hashlib.sha256(canonical(body, ensure_ascii=False))
        if digest.hexdigest() != e.get("hash"):
            return False, f"entry seq {n}: hash does not recompute"
        prev = e["hash"]
    return True, f"{len(entries)} entries recompute from the zero " \
                 f"genesis; terminal anchor {prev}"


def verify_pair_remote(instance, pair_id):
    spec = INSTANCES[instance]
    base = spec["base_url"]
    status, _h, raw = _request(base + spec["export_path"], timeout=60)
    if status != 200:
        raise SystemExit(f"chain export fetch failed: HTTP {status}")
    if spec["export_format"] == "chain4-doc":
        doc = _json(raw)
        entries = doc["segment"]
        ok, detail = recompute_chain4(entries)
        if not ok:
            return False, "CHAIN DOES NOT RECOMPUTE: " + detail
        if doc.get("terminal_anchor") != entries[-1]["hash"]:
            return False, "export terminal_anchor != recomputed anchor"
        idx = [e for e in entries if e.get("pair_id") == pair_id]
        kinds = sorted(e.get("kind") for e in idx)
        if kinds != ["PAIR_A", "PAIR_B"]:
            return False, f"pair {pair_id}: found kinds {kinds}, " \
                          "need PAIR_A + PAIR_B"
        return True, detail + f"; pair {pair_id} stands " \
                              "(PAIR_A + PAIR_B present)"
    entries = [json.loads(line) for line in
               raw.decode().splitlines() if line.strip()]
    ok, detail = recompute_chain(entries)
    if not ok:
        return False, "CHAIN DOES NOT RECOMPUTE: " + detail
    pair, pdetail = find_pair(entries, pair_id)
    if pair is None:
        return False, pdetail
    return True, detail + "; " + pdetail


def verify_bundle(path):
    with open(path) as f:
        bundle = json.load(f)
    if bundle.get("bundle") != "RETENTION_BUNDLE/1":
        return False, "not a RETENTION_BUNDLE/1 file"
    span = bundle["span"]["entries"]
    ok, detail = recompute_chain(span)
    if not ok:
        return False, "BUNDLE SPAN DOES NOT RECOMPUTE: " + detail
    if span[-1]["hash"] != bundle["span"]["anchor_after_span"]:
        return False, "span terminal hash != anchor_after_span"
    pair, pdetail = find_pair(span, bundle["pair_id"])
    if pair is None:
        return False, pdetail
    return True, detail + "; " + pdetail


# ---------------- CLI ----------------

def main(argv=None):
    p = argparse.ArgumentParser(
        description="0R10N15 reference client (schema "
                    "0R10N15-CROSSING-SCHEMA/1)")
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("offer")
    q.add_argument("instance", choices=list(INSTANCES))

    q = sub.add_parser("challenge")
    q.add_argument("--tier", default="receipt-only",
                   choices=["receipt-only", "full-evaluation"])
    q.add_argument("--counterparty", default="reference-client")
    q.add_argument("--scope-ref", default="specimen")
    q.add_argument("--resource", default="governed-evaluation")

    q = sub.add_parser("present")
    q.add_argument("txid")
    q.add_argument("--tier", default="receipt",
                   choices=["receipt", "full-eval"])
    q.add_argument("--payload", default=None)

    q = sub.add_parser("verify-pair")
    q.add_argument("instance", choices=list(INSTANCES))
    q.add_argument("pair_id")

    q = sub.add_parser("verify-bundle")
    q.add_argument("path")

    a = p.parse_args(argv)
    if a.cmd == "offer":
        print(json.dumps(fetch_offer(a.instance), indent=1))
    elif a.cmd == "challenge":
        v1, v2 = fetch_challenge(tier=a.tier,
                                 counterparty=a.counterparty,
                                 scope_ref=a.scope_ref,
                                 resource=a.resource)
        acc = v1["accepts"][0]
        print(f"challenge OK: tier {acc['tier']}, total "
              f"{acc['total_micro_usdc']} micro-USDC (fee "
              f"{acc['governance_fee_micro_usdc']} + settlement "
              f"charge {acc['settlement_charge_micro_usdc']}), "
              f"payTo {acc['payTo']}, network {acc['network']}")
        print("v2 challenge present:", v2 is not None)
        print("Sign the total with any conformant x402 signer "
              "(EIP-3009, USDC domain on Base) and re-POST "
              "/crossing with the X-PAYMENT (v1) or "
              "PAYMENT-SIGNATURE (v2) header.")
    elif a.cmd == "present":
        print(json.dumps(present_4lph4(a.txid, tier=a.tier,
                                       payload=a.payload), indent=1))
    elif a.cmd == "verify-pair":
        ok, detail = verify_pair_remote(a.instance, a.pair_id)
        print(("MATCH: " if ok else "NO MATCH: ") + detail)
        return 0 if ok else 1
    elif a.cmd == "verify-bundle":
        ok, detail = verify_bundle(a.path)
        print(("MATCH: " if ok else "NO MATCH: ") + detail)
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
