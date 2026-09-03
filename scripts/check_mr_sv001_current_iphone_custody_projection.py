#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

EXPECTED_JS_BLOB="ea390cee958c67ff5d144abb43963e07f891a1ef"
EXPECTED_PACKAGE_BLOB="568644fc302d75bacf10cc577f27f101cd8d4ac4"
SOURCE_MERGE="9b617459ec0b9dfceb894ac19495ee72106d1e94"

def git_blob(path:Path)->str:
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def require(condition:bool,message:str)->None:
    if not condition:
        raise SystemExit("FAIL: "+message)

def main()->int:
    js=ROOT/"stegos-bootstrap/master-records-sv001-custody.js"
    pkgp=ROOT/"stegos-bootstrap/master-records-sv001-custody-package.json"
    sw=(ROOT/"stegos-bootstrap/service-worker.js").read_text()
    client=(ROOT/"stegos-bootstrap/stegos-bootstrap.js").read_text()
    ui=(ROOT/"stegos-bootstrap/index.html").read_text()
    handoff=(ROOT/"docs/MR_SV001_CURRENT_IPHONE_CUSTODY_MIRROR_HANDOFF.md").read_text()
    pkg=json.loads(pkgp.read_text())

    require(git_blob(js)==EXPECTED_JS_BLOB,"Master Records JS projection is not exact canonical blob")
    require(git_blob(pkgp)==EXPECTED_PACKAGE_BLOB,"Master Records package projection is not exact canonical blob")
    require(SOURCE_MERGE in handoff and EXPECTED_JS_BLOB in handoff and EXPECTED_PACKAGE_BLOB in handoff,"handoff source pins missing")

    require(pkg.get("canonical_owner")=="master-records/orchestration","canonical owner drift")
    require(pkg.get("execution_surface")=="CURRENT_USER_IPHONE","execution surface drift")
    require(pkg.get("custody_authority") is True,"Master Records custody authority missing")
    require(pkg.get("execution_authority") is False,"portable package execution authority widened")
    require(pkg.get("lease_issuance_authority") is False,"portable package lease authority widened")
    require(pkg.get("external_non_stegverse_machine_required") is False,"second-machine dependency introduced")

    for marker in [
        '"./master-records-sv001-custody.js"',
        'MASTER_RECORDS_SV001_PATH = "/stegos-bootstrap/master-records/sv001"',
        'handleMasterRecordsSv001Custody',
        'site_custody_authority: false',
        'site_execution_authority: false',
        'github_token_runtime_authority: "NONE"',
        'external_non_stegverse_machine_required: false',
        'findMasterRecordsSv001Custody',
        'partial Master Records custody state requires explicit recovery',
    ]:
        require(marker in sw,"service-worker marker missing: "+marker)

    require('executeMasterRecordsSv001Custody' in client,"client custody API missing")
    require('./master-records/sv001' in client,"client custody endpoint missing")
    require('do not rerun SV001' in client.lower(),"client explicit no-rerun guard missing")
    require('Commit Master Records Custody' in ui,"custody UI missing")
    require('does not run StegVerse-001 again' in ui,"UI no-rerun boundary missing")
    require('cycle_receipt' in ui,"exact cycle receipt input missing")
    require('api.executeMasterRecordsSv001Custody' in ui,"UI not wired to custody API")

    print("MR_SV001_CURRENT_IPHONE_CUSTODY_PROJECTION_VALID")
    print("master_records_module_blob="+EXPECTED_JS_BLOB)
    print("master_records_package_blob="+EXPECTED_PACKAGE_BLOB)
    print("source_merge="+SOURCE_MERGE)
    print("site_custody_authority=false")
    print("second_machine_required=false")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
