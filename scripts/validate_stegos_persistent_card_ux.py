#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "stegos-bootstrap" / "index.html"
HELPER = ROOT / "stegos-bootstrap" / "persistent-card-ux.js"
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
handoff = HANDOFF.read_text(encoding="utf-8")
service_worker = SERVICE_WORKER.read_text(encoding="utf-8")
readme = README.read_text(encoding="utf-8")

required_shell_assets = {"./persistent-card-ux.js"} | {"./help/" + name for name in required_help}

checks = {
    "helper loaded": 'src="./persistent-card-ux.js"' in index,
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
    "offline shell cache generation v12": 'var CACHE_NAME = "stegos-web-bootstrap-v12";' in service_worker,
    "stale v11 cache generation removed": 'var CACHE_NAME = "stegos-web-bootstrap-v11";' not in service_worker,
    "persistent helper explicitly cached": '"./persistent-card-ux.js"' in service_worker,
    "all help routes explicitly cached": all(('"./help/' + name + '"') in service_worker for name in required_help),
    "README documents offline card shell": "StegOS same-device operational cards" in readme and "stegos-web-bootstrap-v12" in readme,
    "README preserves non-authority boundary": "Offline caching and same-device UI persistence do not establish Master Records custody" in readme,
}

failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + " - " + name)

if required_shell_assets - {
    asset.strip('"')
    for asset in required_shell_assets
    if ('"' + asset + '"') in service_worker
}:
    failed.append("explicit shell asset set")

if failed:
    raise SystemExit("FAIL: " + ", ".join(sorted(set(failed))))

print("PASS - StegOS persistent same-device card UX source and offline-shell contract")
