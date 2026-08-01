#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("papers/development-without-domination")
STATUS = ROOT / "site-publication-status.json"
PDF = ROOT / "Development_Without_Domination_Rigel_Randolph_Final.pdf"
RECEIPT = ROOT / "site-mirror-receipt.json"
EXPECTED = "c2fcb0ce76f5eaba1a6dd4ccdd358fcae29b32b3110767b5f2b5b2ffa347c29d"
ROUTE = "/papers/development-without-domination/"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    current = json.loads(STATUS.read_text())
    actual = digest(PDF) if PDF.exists() else None
    verified = actual == EXPECTED
    deployed = bool(current.get("deployed_route_verified"))
    remaining = []
    if not verified:
        remaining.append({"repository":"StegVerse-Labs/Site","path":str(PDF),"issue":"StegVerse-Labs/Site#128","action":"Commit exact PDF bytes matching the declared SHA-256."})
    if not deployed:
        remaining.append({"repository":"StegVerse-Labs/Site","path":str(RECEIPT),"issue":"StegVerse-Labs/Site#128","action":"Verify the deployed route and record content identity."})
    state = "ACTIVATED" if verified and deployed else "ROUTE_READY" if verified else "SOURCE_OBSERVED"
    status = {**current,"state":state,"observed_at":datetime.now(timezone.utc).isoformat(),"observed_pdf_sha256":actual,"pdf_verified":verified,"public_route":ROUTE,"remaining_tasks":remaining}
    status["authority"]={"publication":state=="ACTIVATED","admissibility":False,"execution":False,"release":False}
    STATUS.write_text(json.dumps(status,indent=2)+"\n")
    if state == "ACTIVATED":
        RECEIPT.write_text(json.dumps({"schema_version":"1.0.0","paper_id":status["paper_id"],"state":"ACTIVATED","site_repository":"StegVerse-Labs/Site","pdf_path":str(PDF),"pdf_sha256":actual,"public_route":ROUTE,"route_verified":True,"generated_at":status["observed_at"],"publication_is_admissibility":False},indent=2)+"\n")
    print(json.dumps({"state":state,"remaining_tasks":remaining},indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
