"""
StegVerse Site Data Pipeline v1.0
Reads engine receipts, Triad results, and ecosystem state.
Writes JSON data files that the Site's transition pages fetch and render.
Run as a declared task via StegOps after each validation run.
Outputs go to Site repo (or a data/ directory fetched by GitHub Pages).
"""

import json
import hashlib
import glob
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


# ── Data collectors ───────────────────────────────────────────────────────────

def collect_triad_results(triad_receipts_path: str) -> dict:
    """Parse triad_receipts.jsonl and produce summary."""
    path = Path(triad_receipts_path)
    if not path.exists():
        return {"status": "no_data", "receipts": []}

    receipts, allow_count, deny_count, fail_count = [], 0, 0, 0
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
                receipts.append(r)
                d = r.get("decision", "")
                if d == "ALLOW":        allow_count += 1
                elif d == "DENY":       deny_count  += 1
                elif d == "FAIL_CLOSED": fail_count += 1
            except json.JSONDecodeError:
                pass

    return {
        "status": "loaded",
        "total": len(receipts),
        "allow": allow_count,
        "deny": deny_count,
        "fail_closed": fail_count,
        "latest_receipt": receipts[-1] if receipts else None,
        "receipts_sample": receipts[-10:],
    }


def collect_cge_status(cge_path: str) -> dict:
    """Read CGE fingerprint."""
    path = Path(cge_path)
    if not path.exists():
        return {"status": "missing", "cge_status": "unknown"}
    try:
        with open(path) as f:
            cge = json.load(f)
        return {
            "status": "loaded",
            "cge_status": cge.get("status", "unknown"),
            "drift_flags": cge.get("drift_flags", []),
            "generated_at": cge.get("generated_at"),
            "fingerprint_hash": cge.get("fingerprint_hash"),
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def collect_validation_results(results_glob: str) -> list:
    """Collect all validation_results_*.json files."""
    results = []
    for path in sorted(glob.glob(results_glob)):
        try:
            with open(path) as f:
                data = json.load(f)
            results.append({
                "file": Path(path).name,
                "data": data,
            })
        except Exception:
            pass
    return results


def collect_brain_reports(brain_dir: str) -> dict:
    """Read StegBrain next_action and run reports."""
    brain_path = Path(brain_dir)
    result = {}

    na_path = brain_path / "next_action.json"
    if na_path.exists():
        try:
            with open(na_path) as f:
                result["next_action"] = json.load(f)
        except Exception:
            pass

    run_path = brain_path / "stegclaw_run_report.json"
    if run_path.exists():
        try:
            with open(run_path) as f:
                result["run_report"] = json.load(f)
        except Exception:
            pass

    return result


def collect_finco_chain(finco_path: str) -> dict:
    """Read latest FinCo chain receipts."""
    path = Path(finco_path)
    if not path.exists():
        return {"status": "no_data"}

    receipts = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    receipts.append(json.loads(line))
                except Exception:
                    pass

    gov_receipts = [r for r in receipts if r.get("type") == "governance"]
    return {
        "status": "loaded",
        "total_receipts": len(receipts),
        "governance_decisions": [
            {"decision": r.get("admissibility_result"), "reason": r.get("reason"), "at": r.get("generated_at")}
            for r in gov_receipts
        ],
    }


# ── Site page data builders ───────────────────────────────────────────────────

def build_transition_release_index(
    triad_data: dict,
    cge_data: dict,
    validation_data: list,
    brain_data: dict,
    finco_data: dict,
) -> dict:
    """
    Builds the data for transition-release-index.html
    """
    allow_rate = 0
    if triad_data.get("total", 0) > 0:
        allow_rate = round(triad_data["allow"] / triad_data["total"] * 100, 1)

    stages = [
        {
            "stage": "Stage 1",
            "name": "GCAT/BCAT Engine",
            "status": "verified" if triad_data.get("allow", 0) > 0 else "pending",
            "description": "Governance capacity and boundary admissibility.",
            "allow_rate": allow_rate,
        },
        {
            "stage": "Stage 2",
            "name": "ECAT/ICAT Engine",
            "status": "verified" if triad_data.get("allow", 0) > 0 else "pending",
            "description": "External and internal coherence checks.",
        },
        {
            "stage": "Stage 3",
            "name": "% Existence Engine",
            "status": "verified" if triad_data.get("allow", 0) > 0 else "pending",
            "description": "Probability of realizable existence.",
        },
        {
            "stage": "Stage 4",
            "name": "Triad Integration",
            "status": "verified" if triad_data.get("allow", 0) > 0 else "pending",
            "description": "Unified admissibility decision across all axes.",
            "receipts": triad_data.get("total", 0),
        },
        {
            "stage": "Stage 5",
            "name": "Core-Lite + CGE",
            "status": cge_data.get("cge_status", "pending"),
            "description": "Ecosystem health and fingerprint.",
            "drift_flags": cge_data.get("drift_flags", []),
        },
        {
            "stage": "Stage 6",
            "name": "FinCo Receipt Chain",
            "status": "active" if finco_data.get("status") == "loaded" else "pending",
            "description": "Private-state value governance receipts.",
            "governance_decisions": finco_data.get("governance_decisions", []),
        },
        {
            "stage": "Stage 7",
            "name": "Personal Entity (Genesis)",
            "status": "in_progress",
            "description": "Knowledge Vault + StegID + StegClaw personal entity activation.",
            "next_action": brain_data.get("next_action", {}).get("next_action", {}).get("action", "pending"),
        },
    ]

    return {
        "schema": "stegverse_site_release_index.v1",
        "generated_at": now(),
        "title": "StegVerse Transition Release Index",
        "summary": {
            "total_triad_receipts":  triad_data.get("total", 0),
            "triad_allow_rate_pct":  allow_rate,
            "cge_status":            cge_data.get("cge_status", "unknown"),
            "ecosystem_health":      "healthy" if cge_data.get("cge_status") == "healthy" else "drift_detected",
            "finco_chains":          finco_data.get("total_receipts", 0),
            "next_build":            "P0-001",
        },
        "stages": stages,
        "validation_runs": [v["file"] for v in validation_data],
        "data_hash": sha256(json.dumps(stages, sort_keys=True)),
    }


def build_transition_dev_status(
    triad_data: dict,
    brain_data: dict,
    cge_data: dict,
) -> dict:
    """
    Builds data for transition-development-status.html
    """
    next_action_data = brain_data.get("next_action", {})
    next_action      = next_action_data.get("next_action", {})
    blockers         = next_action_data.get("blockers", [])

    return {
        "schema": "stegverse_site_dev_status.v1",
        "generated_at": now(),
        "status_label": "Active Development",
        "next_integration_target": next_action.get("action", "P0-001: Master Dependency Map"),
        "next_integration_description": next_action.get("description", "Create canonical dependency map."),
        "blockers": blockers,
        "metrics": {
            "triad_receipts":     triad_data.get("total", 0),
            "triad_allow":        triad_data.get("allow", 0),
            "triad_fail":         triad_data.get("fail_closed", 0),
            "cge_status":         cge_data.get("cge_status", "unknown"),
            "drift_flags":        len(cge_data.get("drift_flags", [])),
        },
        "last_triad_receipt": triad_data.get("latest_receipt"),
        "data_hash": sha256(json.dumps({"next": next_action.get("action"), "blockers": blockers}, sort_keys=True)),
    }


def build_transition_proof_surface(triad_data: dict, validation_data: list) -> dict:
    """
    Builds data for transition-proof-surface.html
    """
    receipts_sample = triad_data.get("receipts_sample", [])
    return {
        "schema": "stegverse_site_proof_surface.v1",
        "generated_at": now(),
        "proof_status": "active" if triad_data.get("allow", 0) > 0 else "pending",
        "verified_task_chain": [
            {
                "task": r.get("input_ref", "unknown"),
                "decision": r.get("decision"),
                "generated_at": r.get("generated_at"),
                "receipt_hash": sha256(json.dumps(r, sort_keys=True)),
            }
            for r in receipts_sample
        ],
        "source_artifacts": [
            "GCAT-BCAT-Engine/workflows/triad/",
            "GCAT-BCAT-Engine/workflows/triad_validator.py",
            "GCAT-BCAT-Engine/workflows/receipt_replay.py",
        ],
        "validation_runs": validation_data,
        "data_hash": sha256(str(triad_data.get("total", 0))),
    }


# ── Main pipeline ─────────────────────────────────────────────────────────────

def run_pipeline(config: dict, output_dir: str = "./site_data"):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    print("Collecting data...")
    triad_data      = collect_triad_results(config.get("triad_receipts", "./triad/brain_reports/triad_receipts.jsonl"))
    cge_data        = collect_cge_status(config.get("cge_path", "./.stegverse/cge_fingerprint.json"))
    validation_data = collect_validation_results(config.get("validation_glob", "./validation_results_*.json"))
    brain_data      = collect_brain_reports(config.get("brain_dir", "./brain_reports"))
    finco_data      = collect_finco_chain(config.get("finco_chain", "./finco_chain.jsonl"))

    print(f"  Triad receipts: {triad_data.get('total', 0)}")
    print(f"  CGE status: {cge_data.get('cge_status', 'unknown')}")
    print(f"  Validation runs: {len(validation_data)}")

    # Build site pages
    pages = {
        "transition_release_index.json": build_transition_release_index(
            triad_data, cge_data, validation_data, brain_data, finco_data
        ),
        "transition_dev_status.json": build_transition_dev_status(
            triad_data, brain_data, cge_data
        ),
        "transition_proof_surface.json": build_transition_proof_surface(
            triad_data, validation_data
        ),
    }

    for filename, data in pages.items():
        path = out / filename
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Written: {path}")

    # Master run report
    report = {
        "schema": "stegverse_site_pipeline_report.v1",
        "generated_at": now(),
        "pages_written": list(pages.keys()),
        "triad_total": triad_data.get("total", 0),
        "cge_status": cge_data.get("cge_status", "unknown"),
        "data_hash": sha256(json.dumps(list(pages.keys()), sort_keys=True)),
    }
    report_path = out / "pipeline_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nPipeline complete. {len(pages)} pages written to {out}/")
    return report


if __name__ == "__main__":
    import sys
    config_path = sys.argv[1] if len(sys.argv) > 1 else None
    config = {}
    if config_path and Path(config_path).exists():
        with open(config_path) as f:
            config = json.load(f)
    run_pipeline(config, output_dir=sys.argv[2] if len(sys.argv) > 2 else "./site_data")
