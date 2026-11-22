#!/usr/bin/env python3
"""Standalone verifier for the 8374 receipt-chain export
(receipt-chain-rules/1).

Recomputes the receipt chain LOCALLY from an exported NDJSON record
stream -- linkage, per-entry hashes, pair structure, payment-nonce
single-use -- and compares the recomputed terminal anchor against the
anchor stated in the export manifest. The server is not trusted: the
export is the evidence, this script is the recompute.

Chain rules (receipt-chain-rules/1), as implemented by the endpoint:
  entry  = {"i": n, "prev": <hex digest | "GENESIS">,
            "content": {...}, "hash": <hex digest>}
  hash   = SHA-256( prev encoded as UTF-8
                    || canonical(content) )
  canonical(obj) = JSON, sorted keys, separators (",", ":")
  entries are sequential from i = 1; each entry's prev is the
  previous entry's hash ("GENESIS" for the first).
  a receipt pair is two entries sharing content.pair_id, with
  content.index_in_pair 0 and 1; the second member's
  content.pair_anchor equals the first member's entry hash.
  a verified payment authorization's nonce (content.payment.nonce)
  stands under exactly ONE pair on the chain.
  the terminal anchor is the last entry's hash.

Usage:
    python3 verify_chain.py [SOURCE] [--manifest SRC] [--anchor HEX]

SOURCE may be:
  - the chain service root URL
        https://8374.stegverse.org/chain
    (the manifest and the export are fetched from it)
  - the export URL itself (..../chain/export.ndjson)
  - the manifest URL (..../chain/manifest.json)
  - a local NDJSON export file (give the expected anchor with
    --anchor, or a manifest with --manifest)
  - a local manifest JSON file (its export is fetched from the
    manifest's export_url, or read beside it when the URL is a
    plain file name)
Default SOURCE is the public chain service root.

Transport note: some public legs truncate large single responses
for some client classes (observed on the origin's Cloudflare leg,
2026-11-19). The fetch therefore checks every response for
completeness against its Content-Length and, when a single fetch
of the export comes back incomplete, reassembles the export from
entry windows (?offset=&limit=, stated in the manifest). Paging
is transport only: the recompute below runs over the assembled
stream, and a manipulated window breaks the chain exactly like a
manipulated file.

Exit code 0 on MATCH, 1 on MISMATCH or an unreadable source.
Stdlib only.
"""
import hashlib, http.client, json, os, sys
import urllib.request

DEFAULT_SOURCE = "https://8374.stegverse.org/chain"
UA = "8374-chain-verifier/1 (+https://8374.stegverse.org/chain)"
TIMEOUT = 30
PAGE_ENTRIES = 32


def canonical(obj):
    return json.dumps(obj, sort_keys=True,
                      separators=(",", ":")).encode()


def entry_digest(prev, content):
    return hashlib.sha256(prev.encode() + canonical(content)).hexdigest()


def fetch_bytes(src, base_dir=None):
    """Read bytes from an http(s) URL or a local path (a relative
    path resolves against base_dir when given)."""
    if src.startswith("http://") or src.startswith("https://"):
        req = urllib.request.Request(src, method="GET")
        req.add_header("User-Agent", UA)
        req.add_header("Accept", "*/*")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.read()
    path = src
    if base_dir and not os.path.isabs(path):
        path = os.path.join(base_dir, path)
    with open(path, "rb") as f:
        return f.read()


def fetch_url_full(url, max_attempts=16):
    """Fetch a URL's complete body despite a leg that drops
    responses mid-body: every attempt's partial bytes are kept,
    and the next attempt resumes from the exact byte count held
    (Range: bytes=N-). Completion is judged against the
    Content-Length the server stated for the whole resource.
    A server that ignores Range and resends the whole body is
    handled (the resent body replaces the held prefix). Raises
    ValueError when the body cannot be completed."""
    got = bytearray()
    total = None
    last_err = None
    for _attempt in range(max_attempts):
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", UA)
        req.add_header("Accept", "*/*")
        if got and total is not None:
            req.add_header("Range", f"bytes={len(got)}-")
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                status = r.status
                stated = r.headers.get("Content-Length")
                crange = r.headers.get("Content-Range") or ""
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
        except Exception as e:  # dropped before/without a body
            last_err = e
            continue
        if status == 206:
            got += data
        elif complete and stated is not None \
                and len(data) == int(stated):
            return bytes(data)
        elif not complete:
            # a 200 response that broke mid-body: its bytes are a
            # PREFIX of the whole body -- keep them as the held
            # prefix (replacing any shorter held prefix).
            if len(data) > len(got):
                got = bytearray(data)
        else:
            return bytes(data)
        if total is not None and len(got) == total:
            return bytes(got)
        if total is not None and len(got) > total:
            raise ValueError("server sent more bytes than the "
                             "stated Content-Length")
    raise ValueError(
        f"could not fetch a complete body from {url} in "
        f"{max_attempts} attempts (held {len(got)}"
        + (f" of {total}" if total is not None else "")
        + f" bytes; last error: {last_err})")


def fetch_manifest(url):
    """Manifest fetch (a small document) via the same
    completeness discipline."""
    return is_manifest(fetch_url_full(url))


def fetch_export(export_url, total_entries):
    """Fetch the complete export from a URL: Range-resume first;
    if a leg defeats even that, entry windows of PAGE_ENTRIES
    (stated in the manifest), each fetched complete. Raises
    ValueError when the export cannot be obtained complete."""
    if not (export_url.startswith("http://")
            or export_url.startswith("https://")):
        return fetch_bytes(export_url)
    try:
        return fetch_url_full(export_url)
    except ValueError:
        if not total_entries:
            raise
    parts = []
    offset = 0
    while offset < total_entries:
        sep = "&" if "?" in export_url else "?"
        page_url = (f"{export_url}{sep}offset={offset}"
                    f"&limit={PAGE_ENTRIES}")
        parts.append(fetch_url_full(page_url))
        offset += PAGE_ENTRIES
    return b"".join(parts)


def is_manifest(data):
    try:
        doc = json.loads(data)
    except Exception:
        return None
    if isinstance(doc, dict) and ("terminal_anchor" in doc
                                  or "export_url" in doc):
        return doc
    return None


def resolve(source, manifest_src, anchor_arg):
    """Resolve (export_bytes, expected_anchor, manifest_doc).
    Raises ValueError with a located reason on any failure."""
    manifest = None
    export = None
    base_dir = None
    if manifest_src:
        if manifest_src.startswith("http://") \
                or manifest_src.startswith("https://"):
            manifest = fetch_manifest(manifest_src)
        else:
            manifest = is_manifest(fetch_bytes(manifest_src))
        if manifest is None:
            raise ValueError(f"--manifest source {manifest_src} is "
                             "not a chain-export manifest")
    if source.endswith("/chain") or source.endswith("/chain/"):
        root = source.rstrip("/")
        manifest = fetch_manifest(root + "/manifest.json") or manifest
        if manifest is None:
            raise ValueError(f"no chain-export manifest at {root}")
        export = fetch_export(manifest.get("export_url")
                              or (root + "/export.ndjson"),
                              manifest.get("entries"))
    else:
        doc = None
        if source.startswith("http://") \
                or source.startswith("https://"):
            try:
                data = fetch_url_full(source)
                doc = is_manifest(data)
                if doc is None:
                    export = data
            except ValueError:
                export = None  # windowed fallback below
        else:
            data = fetch_bytes(source)
            doc = is_manifest(data)
            if doc is None:
                export = data
        if doc is not None:
            manifest = doc
            if not (source.startswith("http://")
                    or source.startswith("https://")):
                base_dir = os.path.dirname(os.path.abspath(source))
                export = fetch_bytes(manifest["export_url"], base_dir)
            else:
                export = fetch_export(manifest["export_url"],
                                      manifest.get("entries"))
        elif export is None:
            # a bare export URL whose single fetch arrived
            # incomplete: learn the entry count from the sibling
            # manifest and reassemble from entry windows.
            root = source.rsplit("/", 1)[0]
            doc = fetch_manifest(root + "/manifest.json")
            if doc is None:
                raise ValueError(
                    "export fetch arrived incomplete and no "
                    "sibling manifest could be read to plan a "
                    "windowed fetch")
            manifest = manifest or doc
            export = fetch_export(source, doc.get("entries"))
    if export is None:
        raise ValueError("no export bytes resolved")
    anchor = anchor_arg or (manifest or {}).get("terminal_anchor")
    if not anchor:
        raise ValueError("no expected anchor: pass --anchor HEX or "
                         "verify against a manifest that states one")
    return export, anchor, manifest


def recompute(export_bytes):
    """Recompute the chain from NDJSON bytes. Returns
    (entries, pairs, terminal_anchor, problems) where problems are
    located strings (\"entry N: ...\" / \"PAIR-...: ...\")."""
    problems = []
    entries = []
    for ln, raw in enumerate(
            export_bytes.decode("utf-8", "replace").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            entries.append(json.loads(raw))
        except ValueError:
            problems.append(f"line {ln}: undecodable JSON record")
    prev = "GENESIS"
    pairs = {}
    pair_first_hash = {}
    nonce_owner = {}
    for pos, r in enumerate(entries, 1):
        if not isinstance(r, dict) or not all(
                k in r for k in ("i", "prev", "content", "hash")):
            problems.append(f"entry {pos}: record is missing one of "
                            "i/prev/content/hash")
            continue
        if r["i"] != pos:
            problems.append(f"entry {pos}: index gap "
                            f"(stored i={r['i']})")
        if r["prev"] != prev:
            problems.append(f"entry {pos}: prev linkage broken "
                            f"(stored prev does not equal the "
                            f"recomputed predecessor)")
        if entry_digest(r["prev"], r["content"]) != r["hash"]:
            problems.append(f"entry {pos}: hash does not recompute "
                            "from (prev, content)")
        prev = r["hash"]
        c = r["content"]
        pid = c.get("pair_id")
        pairs.setdefault(pid, []).append((pos, r))
        if c.get("index_in_pair") == 0:
            pair_first_hash[pid] = r["hash"]
        pay = c.get("payment")
        if pay and pay.get("nonce"):
            nonce = str(pay["nonce"]).lower()
            owner = nonce_owner.setdefault(nonce, pid)
            if owner != pid:
                problems.append(
                    f"entry {pos}: payment nonce recorded under two "
                    f"pairs ({owner} and {pid}): authorization "
                    "replayed")
    for pid, members in pairs.items():
        if len(members) != 2:
            problems.append(f"{pid}: {len(members)} member(s), pair "
                            "unmatched")
            continue
        ordered = sorted(members,
                         key=lambda m: m[1]["content"].get(
                             "index_in_pair"))
        idxs = [m[1]["content"].get("index_in_pair") for m in ordered]
        if idxs != [0, 1]:
            problems.append(f"{pid}: member index_in_pair values "
                            f"are {idxs}, not [0, 1]")
        second = ordered[1][1]["content"]
        anchor = second.get("pair_anchor")
        if anchor is None:
            problems.append(f"{pid}: second member carries no "
                            "pair anchor")
        elif pid in pair_first_hash and anchor != pair_first_hash[pid]:
            problems.append(f"{pid}: second member's pair_anchor "
                            "does not equal the first member's "
                            "entry hash")
    return entries, pairs, prev, problems


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    opts = {}
    i = 1
    while i < len(argv):
        if argv[i].startswith("--") and i + 1 < len(argv):
            opts[argv[i][2:]] = argv[i + 1]
            i += 2
        else:
            i += 1
    source = args[0] if args else DEFAULT_SOURCE
    try:
        export, expected, manifest = resolve(
            source, opts.get("manifest"), opts.get("anchor"))
    except Exception as e:
        print(f"verdict: MISMATCH")
        print(f"problem: source unreadable: {type(e).__name__}: {e}")
        return 1
    entries, pairs, terminal, problems = recompute(export)
    if manifest:
        if manifest.get("entries") is not None \
                and manifest["entries"] != len(entries):
            problems.append(
                f"manifest states {manifest['entries']} entries; "
                f"the export carries {len(entries)}")
        if manifest.get("pairs") is not None \
                and manifest["pairs"] != len(pairs):
            problems.append(
                f"manifest states {manifest['pairs']} pairs; "
                f"the export carries {len(pairs)}")
    if terminal != expected:
        problems.append(
            f"terminal anchor mismatch: recomputed {terminal}, "
            f"expected {expected}")
    verdict = "MATCH" if not problems else "MISMATCH"
    print(f"source: {source}")
    print(f"entries: {len(entries)}")
    print(f"pairs: {len(pairs)}")
    print(f"terminal_anchor_recomputed: {terminal}")
    print(f"terminal_anchor_expected: {expected}")
    for p in problems:
        print(f"problem: {p}")
    print(f"verdict: {verdict}")
    return 0 if verdict == "MATCH" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
