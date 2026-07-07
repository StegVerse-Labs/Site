import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "cross-wiki-metadata-graph-status.json"
REQUIRED_WIKIS = {
    "stegguardian-wiki": "StegVerse-002/stegguardian-wiki",
    "admissibility-wiki": "StegVerse-Labs/admissibility-wiki",
    "stegverse-site": "StegVerse-Labs/Site",
    "stegtalk-wiki": "StegVerse-Labs/stegtalk-wiki",
}
REQUIRED_NON_CLAIMS = {
    "cross_wiki_authority_granted": False,
    "public_url_confirmed_by_connector": False,
    "standing_conferred": False,
    "execution_authority": False,
}


def main() -> int:
    errors = []
    if not STATUS.exists():
        errors.append("missing_cross_wiki_metadata_graph_status")
        payload = {}
    else:
        payload = json.loads(STATUS.read_text(encoding="utf-8"))

    if payload.get("status_type") != "cross_wiki_metadata_graph_status":
        errors.append("status_type_mismatch")
    if payload.get("repo") != "StegVerse-Labs/Site":
        errors.append("repo_mismatch")
    if payload.get("role") != "public_ecosystem_surface":
        errors.append("role_mismatch")

    linked = {item.get("id"): item for item in payload.get("linked_wikis", [])}
    for wiki_id, repo in REQUIRED_WIKIS.items():
        item = linked.get(wiki_id)
        if item is None:
            errors.append("missing_linked_wiki:" + wiki_id)
            continue
        if item.get("repo") != repo:
            errors.append("linked_wiki_repo_mismatch:" + wiki_id)
        if not item.get("public_url", "").startswith("https://"):
            errors.append("linked_wiki_public_url_missing:" + wiki_id)

    verification = payload.get("verification_state", {})
    if verification.get("local_status_artifact") != "installed":
        errors.append("local_status_artifact_mismatch")
    if verification.get("site_aggregate_checker_wiring") != "pending":
        errors.append("site_aggregate_checker_wiring_must_remain_pending")
    if verification.get("cross_wiki_public_url_confirmation") != "pending":
        errors.append("public_url_confirmation_must_remain_pending")
    if verification.get("cross_wiki_machine_record_confirmation") != "pending":
        errors.append("machine_record_confirmation_must_remain_pending")

    non_claims = payload.get("non_claims", {})
    for key, value in REQUIRED_NON_CLAIMS.items():
        if non_claims.get(key) is not value:
            errors.append("non_claim_mismatch:" + key)

    if errors:
        print("SITE CROSS WIKI METADATA GRAPH STATUS: FAIL - " + ", ".join(errors))
        return 1
    print("SITE CROSS WIKI METADATA GRAPH STATUS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
