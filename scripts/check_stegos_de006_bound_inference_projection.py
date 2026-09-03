#!/usr/bin/env python3
from __future__ import annotations
import hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXPECTED={
"stegos-bootstrap/index.html":"b2c6f72c6947d09be0d7128e4a7df5d237a3b2d5",
"stegos-bootstrap/stegos-bootstrap.js":"d1ae2940d16f757b4bb5964f36dab75fc48bf9c5",
"stegos-bootstrap/admitted-inference.js":"5619540b9a953b58f2a859b5776241809aad1932",
"stegos-bootstrap/service-worker.js":"7c5d62d5fba1fcde13b3a47c3b9b561d03b77087",
"stegos-bootstrap/command-ingress.js":"c1aec1e12efd0f646a5f5ddd75a74f660b0cb43c",
"stegos-bootstrap/command.html":"f05ab222d5a142e88178d8f7c8cb3cb0b520f833",
"stegos-bootstrap/kv-readiness-persistence.js":"a61556dca95a9d7632e873baacbd6b6903f9e689",
"stegos-bootstrap/kv-session-persistence.js":"b2b80022b139378a2280188edde5bd7e0d74be52",
"stegos-bootstrap/workercoordinator-portable-checkout.js":"85a2146c9f6e6868f107c1d55dde74e1844e6217",
"stegos-bootstrap/workercoordinator-portable-adapter.js":"e6833f8b25c52554d69a7f67b69677713f685f68",
"stegos-bootstrap/workercoordinator-portable-sv001.json":"c4503d0620cdc54c27c69ce1655f8ee3cc9dce39",
"stegos-bootstrap/workercoordinator-portable-authority-contract.json":"ea288f43d75f13fd4fbe0801bf4959eebe72b156",
"stegos-bootstrap/tvc-sv001-portable-lease.js":"60ff3afd56f6afaabb84b010a43cdeea5061d2ab",
"stegos-bootstrap/tvc-sv001-portable-lease-package.json":"f902a733b3302026fb730f0e077d501fd33ca29c",
"stegos-bootstrap/tvc-sv001-portable-tv-request.json":"94f37d7ac794e0028411681747db2a4f1e2c4806",
"stegos-bootstrap/tvc-sv001-portable-lease-policy.json":"f2e902679ce7e53ce06efe703a16743656f41790",
"stegos-bootstrap/tvc-sv001-portable-lease-state.schema.json":"daa0e1771aae44e331af6880816d94e3e86d4714",
}

def blob_sha(path:Path)->str:
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def main()->int:
    for rel,expected in EXPECTED.items():
        p=ROOT/rel
        if not p.is_file():
            raise SystemExit(f"MISSING {rel}")
        observed=blob_sha(p)
        if observed!=expected:
            raise SystemExit(f"BLOB_MISMATCH {rel} {observed} != {expected}")
    print("STEGOS_DE006_BOUND_INFERENCE_PROJECTION_VALID")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
