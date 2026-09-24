#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "Household-Economic-Conditions.html"
FIXTURE = ROOT / "data/household-economic-conditions.fixture.json"
GOAL = "ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001"

page = PAGE.read_text(encoding="utf-8")
fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

assert fixture["schema"] == "stegverse.erl.household-economic-conditions-output/v1"
assert fixture["goal_task_id"] == GOAL
assert fixture["evidence_state"] == "FIXTURE_ONLY"
assert fixture["public_activation_authorized"] is False
assert fixture["interpretation"]["what_changed"] == []
assert fixture["interpretation"]["what_it_may_mean"] == []
assert all(series["source_agency"] == "FIXTURE_ONLY" for series in fixture["series"])
assert all(series["comparison_mode"] == "NORMALIZED_INDEX_ONLY" for series in fixture["series"])

required_components = {
    "gross_labor_income", "net_disposable_resources", "required_cost_burden",
    "debt_service", "necessary_consumption", "discretionary_residual",
    "saving_dissaving", "new_borrowing", "delinquency_arrears",
    "unmet_foregone_consumption",
}
assert set(fixture["household_state"]) == required_components

for marker in [
    "FIXTURE ONLY · PUBLIC ACTIVATION DISABLED",
    "Fail closed until governed ERL output is present",
    "1Y", "5Y", "10Y", "2000→Now", "Max",
    "Normalized index (selected start = 100)",
    "Absolute values — only compatible units",
    "Absolute-value overlay refused",
    "Current credit-bureau methodology is comparable from 2005 forward",
    "Main public household-debt continuity begins in 2003",
    "The 2020 experimental 1-year release is noncomparable",
    "Gross real weekly earnings do not establish net take-home resources",
    "aggregate debt-service ratio below a prior crisis peak",
    "payload.public_activation_authorized!==false",
    "payload.evidence_state!=='FIXTURE_ONLY'",
]:
    assert marker in page, marker

assert '<meta name="household-economic-conditions-endpoint" content="">' in page
assert "const fixtureUrl='data/household-economic-conditions.fixture.json'" in page
assert "dual-axis" not in page.lower()

print("HOUSEHOLD_ECONOMIC_CONDITIONS_SITE_CONTRACT=PASS")
print("HOUSEHOLD_ECONOMIC_CONDITIONS_SITE_FIXTURE_FAIL_CLOSED=PASS")
print("HOUSEHOLD_ECONOMIC_CONDITIONS_SITE_PUBLIC_ACTIVATION=false")

publication = json.loads((ROOT / "data/household-economic-conditions.publication.json").read_text(encoding="utf-8"))
assert publication["schema"] == "stegverse.site.household-economic-conditions-publication/v1"
assert publication["goal_task_id"] == GOAL
assert publication["public_activation_authorized"] is False
assert publication["master_records"]["state"] == "UNKNOWN"
assert publication["served_body"]["status"] == "NOT_OBSERVED"
for guard in ["getGovernedPublication()", "validGovernedOutput(", "sha256hex(", "manifest.public_activation_authorized!==true", "mr.reconstruction_status!=='PASS'", "mr.required_evidence_validation_status!=='PASS'", "mr.receipt_sha256!==mr.reconstructed_receipt_sha256", "sha256hex(bodyBytes)!==served.sha256", "sha256hex(outBytes)!==manifest.output_sha256", "sameOriginPath(manifest.output_path)", "payload.public_activation_authorized!==false"]:
    assert guard in page, guard
print("HOUSEHOLD_ECONOMIC_CONDITIONS_SITE_GOVERNED_CONSUMER_FAIL_CLOSED=PASS")
