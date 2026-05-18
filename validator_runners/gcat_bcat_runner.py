#!/usr/bin/env python3
"""
GCAT-BCAT Legitimacy Invariant Validator
==========================================
Implements T1: I(x) = a - K * g^alpha * c^beta * t^gamma <= 0

Loads candidate vectors from GCAT-BCAT/proposed/
Runs invariant check
Emits chained receipts to GCAT-BCAT/validated/ or GCAT-BCAT/invalidated/
Writes cost record to tracker/

Usage:
    python3 gcat_bcat_runner.py \
        --candidates ../../GCAT-BCAT/proposed/gcat_bcat_candidates_001.json \
        --validated  ../../GCAT-BCAT/validated/ \
        --invalidated ../../GCAT-BCAT/invalidated/ \
        --tracker    ../../tracker/runs/ \
        --run-id     GCAT-BCAT-VAL-001
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# GCAT-BCAT Invariant
# ---------------------------------------------------------------------------

TRUST_COLLAPSE_THRESHOLD = 0.10
POLICY_ALLOW_THRESHOLD = 0.50  # capability may exceed raw capacity under policy


def compute_legitimacy_capacity(g: float, c: float, t: float,
                                 K: float = 1.0,
                                 alpha: float = 1.0,
                                 beta: float = 1.0,
                                 gamma: float = 1.0) -> float:
    return K * (g ** alpha) * (c ** beta) * (t ** gamma)


def check_simplex(g: float, c: float, a: float, t: float) -> tuple[bool, str]:
    total = g + c + a + t
    if abs(total - 1.0) > 0.01:
        return False, f"Simplex violation: g+c+a+t = {total:.4f} != 1.0"
    if any(v < 0 for v in [g, c, a, t]):
        return False, "Simplex violation: negative component"
    return True, "Simplex constraint satisfied"


def gcat_bcat_invariant(state: dict) -> tuple[str, str]:
    """
    Returns (decision, basis).
    decision: ALLOW | DENY | FAIL_CLOSED
    """
    g = state.get("g")
    c = state.get("c")
    a = state.get("a")
    t = state.get("t")
    K = state.get("K", 1.0)
    alpha = state.get("alpha", 1.0)
    beta = state.get("beta", 1.0)
    gamma = state.get("gamma", 1.0)

    # Unobservable state → FAIL_CLOSED
    if any(v is None for v in [g, c, a, t]):
        missing = [k for k, v in {"g": g, "c": c, "a": a, "t": t}.items() if v is None]
        return "FAIL_CLOSED", f"State unobservable: {missing}; cannot verify invariant"

    # Simplex check
    simplex_ok, simplex_msg = check_simplex(g, c, a, t)
    if not simplex_ok:
        return "FAIL_CLOSED", simplex_msg

    # Trust collapse check
    if t <= TRUST_COLLAPSE_THRESHOLD:
        cap = compute_legitimacy_capacity(g, c, t, K, alpha, beta, gamma)
        return "FAIL_CLOSED", (
            f"Trust collapse: t={t} <= threshold {TRUST_COLLAPSE_THRESHOLD}; "
            f"legitimacy capacity={cap:.6f} near zero; cannot verify admissibility"
        )

    # Compute invariant
    cap = compute_legitimacy_capacity(g, c, t, K, alpha, beta, gamma)
    invariant_value = a - cap

    if invariant_value > 0:
        return "DENY", (
            f"INVARIANT VIOLATION: a={a} > Λ={cap:.6f}; "
            f"I(x) = {invariant_value:.6f} > 0; "
            f"autonomous capability exceeds legitimacy capacity"
        )

    return "ALLOW", (
        f"Invariant satisfied: a={a} <= Λ={cap:.6f}; "
        f"I(x) = {invariant_value:.6f} <= 0"
    )


# ---------------------------------------------------------------------------
# Receipt generation
# ---------------------------------------------------------------------------

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def make_receipt(candidate: dict, decision: str, basis: str,
                 expected: str, prev_hash: str | None,
                 run_id: str, elapsed: float) -> dict:
    cid = candidate["candidate_id"]
    basis_hash = sha256(json.dumps(candidate, sort_keys=True))
    receipt_str = f"{cid}{decision}{basis}{basis_hash}{prev_hash or ''}"
    receipt_hash = sha256(receipt_str)

    return {
        "receipt_id": f"{run_id}-{cid}",
        "parent_receipt_id": None,
        "run_id": run_id,
        "source_repo": "Admissible-Existence/GCAT-BCAT",
        "component": "GCAT-BCAT",
        "theorem": "T1-GCAT-BCAT-LEGITIMACY",
        "invariant": "I(x) = a - K*g^alpha*c^beta*t^gamma <= 0",
        "candidate_id": cid,
        "candidate_hash": basis_hash,
        "invariant_tested": candidate.get("invariant_tested", "T1-GCAT-BCAT-LEGITIMACY"),
        "decision": decision,
        "basis": basis,
        "expected_decision": expected,
        "match": decision == expected,
        "task_identity_preserved": True,
        "model_used": "local",
        "tokens_in": 0,
        "tokens_out": 0,
        "cost_usd": 0.0,
        "batch_discount_applied": False,
        "sandbox_used": "local_python",
        "sandbox_ephemeral": True,
        "latency_seconds": round(elapsed, 4),
        "prev_receipt_hash": prev_hash,
        "receipt_hash": receipt_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "known_gaps": [],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(args: argparse.Namespace) -> int:
    candidates_path = Path(args.candidates)
    validated_dir = Path(args.validated)
    invalidated_dir = Path(args.invalidated)
    tracker_dir = Path(args.tracker)
    run_id = args.run_id

    for d in [validated_dir, invalidated_dir, tracker_dir]:
        d.mkdir(parents=True, exist_ok=True)

    candidates: list[dict[str, Any]] = json.loads(
        candidates_path.read_text(encoding="utf-8")
    )

    receipts = []
    prev_hash = None
    allow_count = deny_count = fail_count = mismatch_count = 0
    total_elapsed = 0.0

    print(f"=== GCAT-BCAT Validator: {run_id} ===")
    print(f"Theorem: T1 — Legitimacy Invariant I(x) = a - Λ(x) <= 0")
    print(f"Candidates: {len(candidates)}")
    print()

    for cand in candidates:
        cid = cand["candidate_id"]
        expected = cand["expected_decision"]

        t0 = time.perf_counter()
        decision, basis = gcat_bcat_invariant(cand["state"])
        elapsed = time.perf_counter() - t0
        total_elapsed += elapsed

        receipt = make_receipt(cand, decision, basis, expected,
                               prev_hash, run_id, elapsed)
        prev_hash = receipt["receipt_hash"]
        receipts.append(receipt)

        match_str = "✓" if receipt["match"] else "✗ MISMATCH"
        print(f"  {cid}: {decision} [{match_str}]")
        print(f"    {basis[:90]}")

        if decision == "ALLOW":
            allow_count += 1
        elif decision == "DENY":
            deny_count += 1
        else:
            fail_count += 1

        if not receipt["match"]:
            mismatch_count += 1

        target_dir = validated_dir if decision == "ALLOW" else invalidated_dir
        receipt_path = target_dir / f"{cid}_receipt.json"
        receipt_path.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    run_record = {
        "run_id": run_id,
        "source_repo": "Admissible-Existence/GCAT-BCAT",
        "component": "GCAT-BCAT",
        "theorem": "T1-GCAT-BCAT-LEGITIMACY",
        "total_candidates": len(candidates),
        "allow": allow_count,
        "deny": deny_count,
        "fail_closed": fail_count,
        "mismatches": mismatch_count,
        "total_actual_cost_usd": 0.0,
        "sandbox_type": "local_python",
        "sandbox_ephemeral": True,
        "model_used": "local",
        "total_latency_seconds": round(total_elapsed, 4),
        "overall_outcome": "ALLOW" if mismatch_count == 0 else "FAIL_CLOSED",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    tracker_path = tracker_dir / f"{run_id}_run_record.json"
    tracker_path.write_text(
        json.dumps(run_record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print()
    print(f"=== Results: {allow_count} ALLOW, {deny_count} DENY, {fail_count} FAIL_CLOSED ===")
    print(f"Mismatches: {mismatch_count}")
    print(f"Overall: {run_record['overall_outcome']}")

    return 0 if mismatch_count == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="GCAT-BCAT Legitimacy Invariant Validator")
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--validated", required=True)
    parser.add_argument("--invalidated", required=True)
    parser.add_argument("--tracker", required=True)
    parser.add_argument("--run-id", default="GCAT-BCAT-VAL-001")
    return run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
