#!/usr/bin/env python3
from __future__ import annotations
import hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

EXPECTED={
    "stegos-bootstrap/service-worker.js":"0bf8c8df1ae678bc73170978f6c6fdae7b9341f1",
    "stegos-bootstrap/external-resident-task.js":"87dbfdf156224df80ab5f24ae263ed13cb7577c9",
}

def git_blob_sha(path:Path)->str:
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def main()->int:
    for rel,expected in EXPECTED.items():
        path=ROOT/rel
        if not path.is_file():
            raise SystemExit(f"FAIL: missing {rel}")
        actual=git_blob_sha(path)
        if actual!=expected:
            raise SystemExit(f"FAIL: {rel} blob {actual} != {expected}")
    sw=(ROOT/"stegos-bootstrap/service-worker.js").read_text(encoding="utf-8")
    task=(ROOT/"stegos-bootstrap/external-resident-task.js").read_text(encoding="utf-8")
    required=[
        'stegos-web-bootstrap-v6',
        'RESIDENT_TASK_PATH = "/stegos-bootstrap/resident-task"',
        'STEGVERSE001_BOUNDED_CONTINUITY_AUDIT_V1',
        'SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED',
        'global_workercoordinator_authority: false',
        'external_claim_promoted_to_browser_authority: false',
        'credential_authority: "TV/TVC"',
        'external_non_stegverse_machine_required: false',
    ]
    body=sw+"\n"+task
    for marker in required:
        if marker not in body:
            raise SystemExit(f"FAIL: missing invariant {marker}")
    if "global_workercoordinator_authority: true" in body:
        raise SystemExit("FAIL: browser authority widening detected")
    print("STEGOS_IPHONE_RESIDENT_TASK_PROJECTION_PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
