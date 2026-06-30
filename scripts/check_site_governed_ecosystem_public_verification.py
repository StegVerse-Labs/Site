from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "docs" / "SITE_GOVERNED_ECOSYSTEM_PUBLIC_VERIFICATION.json"
PAGE = ROOT / "governed-ecosystem.html"
LOCAL_CHECKER = ROOT / "scripts" / "check_site_governed_ecosystem_mirror.py"
LIVE_URL_CHECKER = ROOT / "scripts" / "check_site_governed_ecosystem_live_url.py"
GUARD = ROOT / ".github" / "workflows" / "site-public-mirror-status-guard.yml"
LIVE_URL_WORKFLOW = ROOT / ".github" / "workflows" / "site-governed-ecosystem-live-url.yml"


def main():
    errors = []
    if not STATE.exists():
        errors.append("missing_state")
        data = {}
    else:
        data = json.loads(STATE.read_text(encoding="utf-8"))
    for path, label in [
        (PAGE, "missing_page"),
        (LOCAL_CHECKER, "missing_local_checker"),
        (LIVE_URL_CHECKER, "missing_live_url_checker"),
        (GUARD, "missing_guard"),
        (LIVE_URL_WORKFLOW, "missing_live_url_workflow"),
    ]:
        if not path.exists():
            errors.append(label)
    if data.get("schema") != "site.governed_ecosystem_public_verification.v1":
        errors.append("schema")
    if data.get("status") != "PUBLIC_VERIFICATION_PENDING":
        errors.append("status")
    if data.get("site_role") != "display_mirror":
        errors.append("site_role")
    checks = data.get("checks", {})
    for key in [
        "local_page_present",
        "local_checker_present",
        "public_guard_wired",
        "live_url_checker_present",
        "live_url_workflow_present",
    ]:
        if checks.get(key) is not True:
            errors.append(key)
    if checks.get("public_url_verified") is not False:
        errors.append("public_url_verified")
    boundary = data.get("boundary", {})
    for key in [
        "public_verification_record_is_authority",
        "display_mirror_grants_production_authority",
        "display_mirror_grants_operational_standing",
    ]:
        if boundary.get(key) is not False:
            errors.append(key)
    if errors:
        print("SITE GOVERNED ECOSYSTEM PUBLIC VERIFICATION: FAIL - " + ", ".join(errors))
        return 1
    print("SITE GOVERNED ECOSYSTEM PUBLIC VERIFICATION: PASS - pending public URL verification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
