#!/usr/bin/env python3
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "stegos-bootstrap" / "index.html"
HELPER = ROOT / "stegos-bootstrap" / "persistent-card-ux.js"
HANDOFF = ROOT / "docs" / "STEGOS_PERSISTENT_CARD_UX_MIRROR_HANDOFF.md"
HELP = ROOT / "stegos-bootstrap" / "help"
SERVICE_WORKER = ROOT / "stegos-bootstrap" / "service-worker.js"
RECOVERY = ROOT / "stegos-bootstrap" / "master-records-sv001-recovery.js"
AUTO_RECOVERY = ROOT / "stegos-bootstrap" / "master-records-auto-recovery.js"
PACKAGE = ROOT / "stegos-bootstrap" / "master-records-sv001-custody-package.json"
README = ROOT / "README.md"

CANONICAL_RECOVERY_BLOB = "5ca977c4214c3eec13bd2ac1109405e7f1571723"
CANONICAL_PACKAGE_BLOB = "70e02082d63d046101fa0a21d82e12261c891e79"
CANONICAL_G23 = "sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35"

required_help = {
    "authority-boundary.html",
    "interaction-coordinator.html",
    "runtime-capability.html",
    "node.html",
    "ecosystem-chat.html",
    "canonical-inference-evidence.html",
    "admitted-inference.html",
    "sv001-bounded-autonomy.html",
    "master-records-sv001.html",
    "continuity.html",
    "offline-shell.html",
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


index = INDEX.read_text(encoding="utf-8")
helper = HELPER.read_text(encoding="utf-8")
handoff = HANDOFF.read_text(encoding="utf-8")
service_worker = SERVICE_WORKER.read_text(encoding="utf-8")
recovery = RECOVERY.read_text(encoding="utf-8")
auto_recovery = AUTO_RECOVERY.read_text(encoding="utf-8")
package = PACKAGE.read_text(encoding="utf-8")
readme = README.read_text(encoding="utf-8")

required_shell_assets = {
    "./persistent-card-ux.js",
    "./master-records-sv001-recovery.js",
    "./master-records-auto-recovery.js",
} | {"./help/" + name for name in required_help}

checks = {
    "helper loaded": 'src="./persistent-card-ux.js"' in index,
    "canonical recovery module loaded": 'src="./master-records-sv001-recovery.js"' in index,
    "automatic recovery continuation loaded": 'src="./master-records-auto-recovery.js"' in index,
    "recovery loads after persistent helper": index.index('src="./persistent-card-ux.js"') < index.index('src="./master-records-sv001-recovery.js"') < index.index('src="./master-records-auto-recovery.js"'),
    "SV001 history-first state": "CHECKING_DEVICE_HISTORY" in index,
    "Master Records same-device proof state": "CHECKING_SAME_DEVICE_PROOF" in index,
    "SV001 rerun guard": "SV001 is already terminal on this device. Rerun is prohibited." in index,
    "same-device snapshot schema": "stegos.same-device-card-snapshot/v1" in helper,
    "green completed border": "#2fbf71" in helper and "card-complete" in helper,
    "red incomplete border": "#d94b4b" in helper and "card-incomplete" in helper,
    "copy text control": 'button.textContent = "Copy Text"' in helper,
    "card help links": "Purpose / remediation / troubleshooting" in helper,
    "terminal SV001 discovery": "scanTerminalSv001" in helper,
    "same-device proof discovery": "findStoredSv001Proof" in helper,
    "authority effect none": 'authority_effect: "NONE"' in helper,
    "handoff present": "SITE-STEGOS-PERSISTENT-CARD-UX-1000" in handoff,
    "help pages complete": required_help.issubset({p.name for p in HELP.glob("*.html")}),
    "offline shell cache generation v13": 'var CACHE_NAME = "stegos-web-bootstrap-v13";' in service_worker,
    "stale v12 cache generation removed": 'var CACHE_NAME = "stegos-web-bootstrap-v12";' not in service_worker,
    "persistent helper explicitly cached": '"./persistent-card-ux.js"' in service_worker,
    "canonical recovery explicitly cached": '"./master-records-sv001-recovery.js"' in service_worker,
    "automatic recovery explicitly cached": '"./master-records-auto-recovery.js"' in service_worker,
    "all help routes explicitly cached": all(('"./help/' + name + '"') in service_worker for name in required_help),
    "canonical recovery exact blob": git_blob_sha(RECOVERY) == CANONICAL_RECOVERY_BLOB,
    "canonical package exact blob": git_blob_sha(PACKAGE) == CANONICAL_PACKAGE_BLOB,
    "canonical G23 recovery target": CANONICAL_G23 in recovery and CANONICAL_G23 in package,
    "unique journal recovery fail closed": "canonical cycle receipt is not uniquely recoverable from retained journal" in recovery,
    "automatic custody uses existing API": "executeMasterRecordsSv001Custody(resolved.receipt)" in auto_recovery,
    "automatic custody requires current governance": "REQUESTING_CONTEMPORANEOUS_INTR_GOVERNANCE" in auto_recovery and "prior_receipt_authorizes_transition: false" in auto_recovery,
    "automatic path no human approval": "humanApprovalRequired: false" in auto_recovery,
    "automatic path forbids rerun": "sv001RerunAllowed: false" in auto_recovery,
    "manual fallback remains": "Manual Custody Fallback" in index and "manual exact-proof import" in index.lower(),
    "README documents v13 recovery shell": "StegOS same-device operational cards" in readme and "stegos-web-bootstrap-v13" in readme,
    "README documents canonical journal recovery": "canonical G23" in readme and "retained-journal" in readme,
    "README preserves non-authority boundary": "Source, merge, validation, cache generation, or publication must not be substituted for authentic current-device evidence" in readme,
}

failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + " - " + name)

missing_shell = {
    asset for asset in required_shell_assets
    if ('"' + asset + '"') not in service_worker
}
if missing_shell:
    failed.append("explicit shell asset set: " + ", ".join(sorted(missing_shell)))

if failed:
    raise SystemExit("FAIL: " + ", ".join(sorted(set(failed))))

print("PASS - StegOS persistent same-device card UX, canonical G23 recovery, and v13 offline-shell contract")
