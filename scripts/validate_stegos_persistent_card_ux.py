#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "stegos-bootstrap" / "index.html"
HELPER = ROOT / "stegos-bootstrap" / "persistent-card-ux.js"
RECOVERY = ROOT / "stegos-bootstrap" / "master-records-sv001-recovery.js"
AUTO_RECOVERY = ROOT / "stegos-bootstrap" / "master-records-auto-recovery.js"
PACKAGE = ROOT / "stegos-bootstrap" / "master-records-sv001-custody-package.json"
HANDOFF = ROOT / "docs" / "STEGOS_PERSISTENT_CARD_UX_MIRROR_HANDOFF.md"
HELP = ROOT / "stegos-bootstrap" / "help"
SERVICE_WORKER = ROOT / "stegos-bootstrap" / "service-worker.js"
README = ROOT / "README.md"

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

index = INDEX.read_text(encoding="utf-8")
helper = HELPER.read_text(encoding="utf-8")
recovery = RECOVERY.read_text(encoding="utf-8")
auto_recovery = AUTO_RECOVERY.read_text(encoding="utf-8")
package = PACKAGE.read_text(encoding="utf-8")
handoff = HANDOFF.read_text(encoding="utf-8")
service_worker = SERVICE_WORKER.read_text(encoding="utf-8")
readme = README.read_text(encoding="utf-8")

required_shell_assets = {
    "./persistent-card-ux.js",
    "./master-records-sv001-recovery.js",
    "./master-records-auto-recovery.js",
} | {"./help/" + name for name in required_help}

target = "81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35"

checks = {
    "helper loaded": 'src="./persistent-card-ux.js"' in index,
    "canonical recovery loaded": 'src="./master-records-sv001-recovery.js"' in index,
    "automatic recovery carrier loaded": 'src="./master-records-auto-recovery.js"' in index,
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
    "canonical G23 recovery target": target in package and target in auto_recovery,
    "canonical G23 claim fence": "SHWP-SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001-G23" in package and '"target_fencing_token": 23' in package,
    "unique hash verified recovery": "RECOVERED_HASH_VERIFIED" in recovery and "unique_match_count: 1" in recovery,
    "auto recovery remains non-authorizing": 'custody_executed: false' in auto_recovery and 'authority_effect: "NONE_RECOVERY_ONLY"' in auto_recovery,
    "auto recovery waits for machine governance": "CONTEMPORANEOUS_INTERLOCK_INTR_GOVERNANCE_FOR_SV001_MASTER_RECORDS_CUSTODY_AND_RECONSTRUCTION" in auto_recovery,
    "manual fallback remains fail closed": "Manual exact-proof import remains a fail-closed fallback. SV001 must not be rerun." in auto_recovery,
    "root InTr custody gate preserved": "contemporaneous InTr admission required before Master Records custody" in service_worker,
    "historical retroactive authorization prohibited": "retroactive authorization forbidden" in service_worker,
    "README documents v13 auto recovery": "stegos-web-bootstrap-v13" in readme and "canonical G23" in readme and "automatic" in readme.lower(),
    "README preserves non-authority boundary": "recovery does not grant custody authority" in readme.lower() and "source/ci/merge" in readme.lower(),
}

failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + " - " + name)

for asset in sorted(required_shell_assets):
    if ('"' + asset + '"') not in service_worker:
        failed.append("explicit shell asset missing: " + asset)

if failed:
    raise SystemExit("FAIL: " + ", ".join(sorted(set(failed))))

print("PASS - StegOS persistent same-device card UX, canonical G23 auto-recovery, and offline-shell contract")
