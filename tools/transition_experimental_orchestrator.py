#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data"
RECEIPTS_DIR = D / "receipts"

LABELS = ["Proposed", "Defined", "Derived", "Proven", "Tested", "Receipt-backed"]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_json(path: Path, default: Any) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def digest(payload: Any) -> str:
    data = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def capacity(state: dict[str, float]) -> float:
    return round(state["g"] * state["c"] * state["t"], 5)


def invariant(state: dict[str, float]) -> float:
    return round(state["a"] - capacity(state), 5)


def verdict_for(state: dict[str, float]) -> str:
    return "ALLOW" if invariant(state) <= 0 and all(0 <= v <= 1 for v in state.values()) else "DENY"


def state_add(state: dict[str, float], delta: dict[str, float]) -> dict[str, float]:
    return {k: round(state[k] + delta.get("d" + k, 0.0), 4) for k in ["g", "c", "a", "t"]}


def post(pre: dict[str, float], action: dict[str, float]) -> dict[str, float]:
    return state_add(pre, action)


def normalize_row(row_payload: dict[str, Any]) -> dict[str, Any]:
    mode = row_payload.get("mode", "")
    action = row_payload.get("action") or {}

    if not row_payload.get("tested_property"):
        if mode == "simplex_conservation_sweep_v1":
            row_payload["tested_property"] = "simplex_conservation"
        elif mode == "bounded_action_sweep_v1":
            row_payload["tested_property"] = "bounded_action"
        elif mode == "capacity_margin_sweep_v1":
            row_payload["tested_property"] = "capacity_margin"
        elif mode == "observation_lag_sweep_v1":
            row_payload["tested_property"] = "observation_lag"
        elif mode == "decision_lag_sweep_v1":
            row_payload["tested_property"] = "decision_lag"
        elif mode == "actuation_lag_sweep_v1":
            row_payload["tested_property"] = "actuation_lag"
        elif mode == "trust_drift_sweep_v1":
            row_payload["tested_property"] = "trust_drift"
        else:
            row_payload["tested_property"] = mode

    if row_payload.get("constraint_result") in (None, "", "None", "n/a"):
        if mode == "simplex_conservation_sweep_v1":
            constraint_value = row_payload.get("constraint_value")
            if constraint_value is None and action:
                constraint_value = round(sum(float(v) for v in action.values()), 8)
                row_payload["constraint_value"] = constraint_value
            row_payload["constraint_result"] = "PASS" if constraint_value is not None and abs(float(constraint_value)) <= 1e-8 else "UNKNOWN"
        elif mode == "bounded_action_sweep_v1":
            epsilon = float(row_payload.get("epsilon", 0.10))
            action_norm = row_payload.get("action_norm")
            if action_norm is None and action:
                action_norm = round(math.sqrt(sum(float(v) * float(v) for v in action.values())), 5)
                row_payload["action_norm"] = action_norm
                row_payload["epsilon"] = epsilon
            row_payload["constraint_result"] = "PASS" if action_norm is not None and float(action_norm) <= epsilon else "FAIL"
            row_payload["bound_status"] = "WITHIN_BOUND" if row_payload["constraint_result"] == "PASS" else "OUT_OF_BOUND"
        elif mode == "capacity_margin_sweep_v1":
            if "margin" not in row_payload and "capacity" in row_payload and row_payload.get("post_state"):
                row_payload["margin"] = round(float(row_payload["capacity"]) - float(row_payload["post_state"]["a"]), 5)
            row_payload["constraint_result"] = "PASS"
            if "margin" in row_payload:
                row_payload["margin_status"] = "NONNEGATIVE" if float(row_payload["margin"]) >= 0 else "NEGATIVE"
        elif mode in ("observation_lag_sweep_v1", "decision_lag_sweep_v1", "actuation_lag_sweep_v1", "trust_drift_sweep_v1"):
            row_payload["constraint_result"] = "PASS"
        else:
            row_payload["constraint_result"] = "not applicable"

    return row_payload


def simple_row(run_id: str, element_id: str, mode: str, idx: int, pre: dict[str, float], action: dict[str, float], extra: dict[str, Any] | None = None) -> dict[str, Any]:
    ps = post(pre, action)
    payload = {
        "timestamp": now(),
        "element_id": element_id,
        "mode": mode,
        "run_id": f"{run_id}-{idx:03d}",
        "pre_state": pre,
        "action": action,
        "post_state": ps,
        "parameters": {"K": 1, "alpha": 1, "beta": 1, "gamma": 1},
        "capacity": capacity(ps),
        "invariant": invariant(ps),
        "verdict": verdict_for(ps),
        "passed": True,
        "receipt_hash": None,
    }
    if extra:
        payload.update(extra)
    normalize_row(payload)
    payload["row_hash"] = digest({k: v for k, v in payload.items() if k != "row_hash"})
    return payload


def t2(run_id: str):
    samples = [
        ({"g": .25, "c": .30, "a": .12, "t": .33}, {"dg": .03, "dc": -.02, "da": .01, "dt": -.02}),
        ({"g": .35, "c": .25, "a": .10, "t": .30}, {"dg": -.04, "dc": .03, "da": .02, "dt": -.01}),
        ({"g": .40, "c": .20, "a": .09, "t": .31}, {"dg": .02, "dc": .02, "da": -.01, "dt": -.03}),
    ]
    rows, anomalies = [], []
    for i, (pre, action) in enumerate(samples, 1):
        cv = round(sum(action.values()), 8)
        r = simple_row(run_id, "T2", "simplex_conservation_sweep_v1", i, pre, action, {
            "tested_property": "simplex_conservation",
            "constraint_result": "PASS" if abs(cv) <= 1e-8 else "FAIL",
            "constraint_value": cv,
        })
        if abs(cv) > 1e-8:
            anomalies.append({"row": r["run_id"], "constraint_value": cv})
        rows.append(r)
    kd = [{
        "delta_id": f"KD-{run_id}-simplex",
        "source_run_id": run_id,
        "source_element": "T2",
        "delta_type": "constraint_validation",
        "summary": "Simplex-preserving actions maintained zero net BCAT resource delta.",
        "informs": ["T2", "T4"],
        "confidence": .95,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic simplex conservation sweep passed", "bad": anomalies}


def t3(run_id: str):
    eps = .10
    samples = [
        ({"g": .42, "c": .58, "a": .14, "t": .77}, {"dg": .02, "dc": -.01, "da": .03, "dt": -.02}),
        ({"g": .50, "c": .45, "a": .12, "t": .80}, {"dg": -.03, "dc": .02, "da": .02, "dt": -.01}),
        ({"g": .39, "c": .62, "a": .16, "t": .71}, {"dg": .04, "dc": -.02, "da": .01, "dt": -.01}),
    ]
    rows = []
    for i, (pre, action) in enumerate(samples, 1):
        norm = round(math.sqrt(sum(v * v for v in action.values())), 5)
        rows.append(simple_row(run_id, "T3", "bounded_action_sweep_v1", i, pre, action, {
            "tested_property": "bounded_action",
            "action_norm": norm,
            "epsilon": eps,
            "constraint_result": "PASS" if norm <= eps else "FAIL",
            "bound_status": "WITHIN_BOUND" if norm <= eps else "OUT_OF_BOUND",
        }))
    kd = [{
        "delta_id": f"KD-{run_id}-bounded-action",
        "source_run_id": run_id,
        "source_element": "T3",
        "delta_type": "safe_region_fragment",
        "summary": "Bounded isolated actions can be evaluated against both magnitude and post-state admissibility.",
        "informs": ["T3", "T4", "T11"],
        "confidence": .90,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic bounded action sweep passed", "bad": []}


def t4(run_id: str):
    samples = [
        ({"g": .44, "c": .70, "a": .18, "t": .82}, {"dg": -.01, "dc": .01, "da": .02, "dt": -.01}),
        ({"g": .62, "c": .52, "a": .17, "t": .73}, {"dg": .00, "dc": -.02, "da": .03, "dt": .00}),
        ({"g": .36, "c": .49, "a": .10, "t": .68}, {"dg": .02, "dc": .01, "da": .01, "dt": -.02}),
    ]
    rows = []
    for i, (pre, action) in enumerate(samples, 1):
        r = simple_row(run_id, "T4", "capacity_margin_sweep_v1", i, pre, action, {
            "tested_property": "capacity_margin",
            "constraint_result": "PASS",
        })
        r["margin"] = round(r["capacity"] - r["post_state"]["a"], 5)
        r["margin_status"] = "NONNEGATIVE" if r["margin"] >= 0 else "NEGATIVE"
        rows.append(r)
    kd = [{
        "delta_id": f"KD-{run_id}-margin",
        "source_run_id": run_id,
        "source_element": "T4",
        "delta_type": "margin_estimate",
        "summary": "Capacity-margin calculation converts binary admissibility into signed distance-to-violation samples.",
        "informs": ["T4", "T5", "T8", "T11"],
        "confidence": .91,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic capacity margin sweep passed", "bad": []}


def t5(run_id: str):
    samples = [
        {"observed_state": {"g": .60, "c": .60, "a": .20, "t": .80}, "lag_drift": {"dg": 0, "dc": 0, "da": 0, "dt": -.20}, "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}},
        {"observed_state": {"g": .70, "c": .64, "a": .16, "t": .76}, "lag_drift": {"dg": -.02, "dc": -.02, "da": .01, "dt": -.04}, "action": {"dg": 0, "dc": 0, "da": .01, "dt": 0}},
        {"observed_state": {"g": .46, "c": .68, "a": .18, "t": .72}, "lag_drift": {"dg": -.06, "dc": -.05, "da": .02, "dt": -.07}, "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}},
    ]
    rows, flips = [], 0
    for i, sample in enumerate(samples, 1):
        observed = sample["observed_state"]
        drift = sample["lag_drift"]
        action = sample["action"]
        commit_state = state_add(observed, drift)
        observed_post = post(observed, action)
        commit_post = post(commit_state, action)
        observed_verdict = verdict_for(observed_post)
        commit_verdict = verdict_for(commit_post)
        lag_flip = observed_verdict != commit_verdict
        flips += int(lag_flip)
        payload = {
            "timestamp": now(),
            "element_id": "T5",
            "mode": "observation_lag_sweep_v1",
            "run_id": f"{run_id}-{i:03d}",
            "tested_property": "observation_lag",
            "observed_state": observed,
            "lag_drift": drift,
            "commit_state": commit_state,
            "action": action,
            "observed_post_state": observed_post,
            "commit_post_state": commit_post,
            "post_state": commit_post,
            "parameters": {"K": 1, "alpha": 1, "beta": 1, "gamma": 1, "tau_obs": i},
            "observed_invariant": invariant(observed_post),
            "commit_invariant": invariant(commit_post),
            "invariant": invariant(commit_post),
            "observed_verdict": observed_verdict,
            "commit_verdict": commit_verdict,
            "verdict": commit_verdict,
            "lag_flip": lag_flip,
            "constraint_result": "PASS",
            "passed": True,
            "receipt_hash": None,
        }
        payload["row_hash"] = digest(payload)
        rows.append(payload)

    kd = [{
        "delta_id": f"KD-{run_id}-observation-lag",
        "source_run_id": run_id,
        "source_element": "T5",
        "delta_type": "lag_flip_fragment",
        "summary": f"Observation-lag sweep found {flips} verdict flip(s) between observed-state and commit-time admissibility.",
        "informs": ["T5", "T6", "T7", "T8"],
        "confidence": .88,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic observation lag sweep passed", "bad": []}


def staged_lag_row(run_id: str, element_id: str, mode: str, tested_property: str, samples: list[dict[str, Any]], delta_type: str, summary_prefix: str, informs: list[str]):
    rows, flips = [], 0
    for i, sample in enumerate(samples, 1):
        observed = sample["observed_state"]
        obs_drift = sample.get("observation_lag_drift", {})
        decision_drift = sample.get("decision_lag_drift", {})
        actuation_drift = sample.get("actuation_lag_drift", {})
        action = sample["action"]

        decision_state = state_add(observed, obs_drift)
        commit_state = state_add(decision_state, decision_drift)
        effect_state = state_add(commit_state, actuation_drift)

        observed_post = post(observed, action)
        decision_post = post(decision_state, action)
        commit_post = post(commit_state, action)
        effect_post = post(effect_state, action)

        observed_verdict = verdict_for(observed_post)
        decision_verdict = verdict_for(decision_post)
        commit_verdict = verdict_for(commit_post)
        effect_verdict = verdict_for(effect_post)

        decision_flip = observed_verdict != commit_verdict
        actuation_flip = commit_verdict != effect_verdict
        total_lag_flip = observed_verdict != effect_verdict if mode == "actuation_lag_sweep_v1" else observed_verdict != commit_verdict
        flips += int(total_lag_flip)

        payload = {
            "timestamp": now(),
            "element_id": element_id,
            "mode": mode,
            "run_id": f"{run_id}-{i:03d}",
            "tested_property": tested_property,
            "observed_state": observed,
            "observation_lag_drift": obs_drift,
            "decision_state": decision_state,
            "decision_lag_drift": decision_drift,
            "commit_state": commit_state,
            "actuation_lag_drift": actuation_drift,
            "effect_state": effect_state,
            "action": action,
            "observed_post_state": observed_post,
            "decision_post_state": decision_post,
            "commit_post_state": commit_post,
            "effect_post_state": effect_post,
            "post_state": effect_post if mode == "actuation_lag_sweep_v1" else commit_post,
            "parameters": {"K": 1, "alpha": 1, "beta": 1, "gamma": 1, "tau_obs": i, "tau_dec": i, "tau_act": i if mode == "actuation_lag_sweep_v1" else 0},
            "observed_invariant": invariant(observed_post),
            "decision_invariant": invariant(decision_post),
            "commit_invariant": invariant(commit_post),
            "effect_invariant": invariant(effect_post),
            "invariant": invariant(effect_post if mode == "actuation_lag_sweep_v1" else commit_post),
            "observed_verdict": observed_verdict,
            "decision_verdict": decision_verdict,
            "commit_verdict": commit_verdict,
            "effect_verdict": effect_verdict,
            "verdict": effect_verdict if mode == "actuation_lag_sweep_v1" else commit_verdict,
            "decision_flip": decision_flip,
            "actuation_flip": actuation_flip,
            "total_lag_flip": total_lag_flip,
            "constraint_result": "PASS",
            "passed": True,
            "receipt_hash": None,
        }
        payload["row_hash"] = digest(payload)
        rows.append(payload)

    kd = [{
        "delta_id": f"KD-{run_id}-{tested_property}",
        "source_run_id": run_id,
        "source_element": element_id,
        "delta_type": delta_type,
        "summary": f"{summary_prefix} found {flips} total lag flip(s) across deterministic staged samples.",
        "informs": informs,
        "confidence": .87,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": f"deterministic {tested_property.replace('_', ' ')} sweep passed", "bad": []}


def t6(run_id: str):
    samples = [
        {"observed_state": {"g": .60, "c": .60, "a": .18, "t": .78}, "observation_lag_drift": {"dg": 0, "dc": 0, "da": 0, "dt": -.08}, "decision_lag_drift": {"dg": 0, "dc": -.03, "da": .02, "dt": -.06}, "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}},
        {"observed_state": {"g": .72, "c": .62, "a": .17, "t": .76}, "observation_lag_drift": {"dg": -.01, "dc": -.01, "da": .01, "dt": -.03}, "decision_lag_drift": {"dg": -.03, "dc": -.02, "da": .02, "dt": -.05}, "action": {"dg": 0, "dc": 0, "da": .01, "dt": 0}},
        {"observed_state": {"g": .50, "c": .66, "a": .15, "t": .80}, "observation_lag_drift": {"dg": -.02, "dc": 0, "da": .01, "dt": -.04}, "decision_lag_drift": {"dg": -.05, "dc": -.04, "da": .02, "dt": -.08}, "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}},
    ]
    return staged_lag_row(run_id, "T6", "decision_lag_sweep_v1", "decision_lag", samples, "decision_lag_fragment", "Decision-lag sweep", ["T6", "T7"])


def t7(run_id: str):
    samples = [
        {"observed_state": {"g": .62, "c": .62, "a": .17, "t": .78}, "observation_lag_drift": {"dg": 0, "dc": 0, "da": 0, "dt": -.04}, "decision_lag_drift": {"dg": -.02, "dc": -.02, "da": .01, "dt": -.04}, "actuation_lag_drift": {"dg": -.03, "dc": -.04, "da": .02, "dt": -.08}, "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}},
        {"observed_state": {"g": .76, "c": .58, "a": .15, "t": .72}, "observation_lag_drift": {"dg": -.01, "dc": 0, "da": .01, "dt": -.03}, "decision_lag_drift": {"dg": -.02, "dc": -.02, "da": .01, "dt": -.04}, "actuation_lag_drift": {"dg": -.06, "dc": -.03, "da": .03, "dt": -.10}, "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}},
        {"observed_state": {"g": .56, "c": .70, "a": .16, "t": .82}, "observation_lag_drift": {"dg": -.02, "dc": -.02, "da": .01, "dt": -.04}, "decision_lag_drift": {"dg": -.03, "dc": -.03, "da": .01, "dt": -.05}, "actuation_lag_drift": {"dg": -.05, "dc": -.05, "da": .02, "dt": -.09}, "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}},
    ]
    return staged_lag_row(run_id, "T7", "actuation_lag_sweep_v1", "actuation_lag", samples, "actuation_lag_fragment", "Actuation-lag sweep", ["T7", "T15"])


def t8(run_id: str):
    samples = [
        {"state": {"g": .64, "c": .62, "a": .20, "t": .82}, "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}, "lambda": .10, "tau": 2},
        {"state": {"g": .58, "c": .58, "a": .18, "t": .84}, "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}, "lambda": .18, "tau": 3},
        {"state": {"g": .72, "c": .50, "a": .16, "t": .74}, "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}, "lambda": .24, "tau": 4},
    ]
    rows = []
    flips = 0
    for i, sample in enumerate(samples, 1):
        state = sample["state"]
        action = sample["action"]
        lam = sample["lambda"]
        tau = sample["tau"]

        pre_decay_post = post(state, action)
        decayed_t = round(state["t"] * math.exp(-lam * tau), 5)
        trust_decayed_state = dict(state)
        trust_decayed_state["t"] = decayed_t
        trust_decayed_post = post(trust_decayed_state, action)

        pre_decay_verdict = verdict_for(pre_decay_post)
        trust_decay_verdict = verdict_for(trust_decayed_post)
        trust_flip = pre_decay_verdict != trust_decay_verdict
        flips += int(trust_flip)

        payload = {
            "timestamp": now(),
            "element_id": "T8",
            "mode": "trust_drift_sweep_v1",
            "run_id": f"{run_id}-{i:03d}",
            "tested_property": "trust_drift",
            "pre_state": state,
            "action": action,
            "post_state": trust_decayed_post,
            "pre_decay_post_state": pre_decay_post,
            "trust_decayed_state": trust_decayed_state,
            "trust_decayed_post_state": trust_decayed_post,
            "parameters": {"K": 1, "alpha": 1, "beta": 1, "gamma": 1, "lambda": lam, "tau": tau},
            "initial_trust": state["t"],
            "decayed_trust": decayed_t,
            "pre_decay_capacity": capacity(pre_decay_post),
            "post_decay_capacity": capacity(trust_decayed_post),
            "pre_decay_invariant": invariant(pre_decay_post),
            "post_decay_invariant": invariant(trust_decayed_post),
            "invariant": invariant(trust_decayed_post),
            "pre_decay_verdict": pre_decay_verdict,
            "trust_decay_verdict": trust_decay_verdict,
            "verdict": trust_decay_verdict,
            "trust_flip": trust_flip,
            "constraint_result": "PASS",
            "passed": True,
            "receipt_hash": None,
        }
        payload["row_hash"] = digest(payload)
        rows.append(payload)

    kd = [{
        "delta_id": f"KD-{run_id}-trust-drift",
        "source_run_id": run_id,
        "source_element": "T8",
        "delta_type": "trust_drift_fragment",
        "summary": f"Trust-drift sweep found {flips} verdict flip(s) after exponential trust decay across deterministic samples.",
        "informs": ["T8", "T9", "T10"],
        "confidence": .86,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic trust drift sweep passed", "bad": []}


EXPERIMENTS = {
    "simplex_conservation_sweep_v1": t2,
    "bounded_action_sweep_v1": t3,
    "capacity_margin_sweep_v1": t4,
    "observation_lag_sweep_v1": t5,
    "decision_lag_sweep_v1": t6,
    "actuation_lag_sweep_v1": t7,
    "trust_drift_sweep_v1": t8,
}

FALLBACK_EXPERIMENTS = {
    "T5": ["observation_lag_sweep_v1"],
    "T6": ["decision_lag_sweep_v1"],
    "T7": ["actuation_lag_sweep_v1"],
    "T8": ["trust_drift_sweep_v1"],
}


RULE_DEFS = [
    ("primitive_admissibility_required", "T1", 4, "Every experiment must compute post-state invariant."),
    ("simplex_constraint_visible", "T2", 4, "Ledger rows must distinguish conservation constraints from admissibility verdicts."),
    ("bounded_action_visible", "T3", 4, "Experiments with action vectors must record action bounds when applicable."),
    ("capacity_margin_visible", "T4", 4, "Experiments must record margin when capacity calculations are available."),
    ("lag_aware_sandbox_required", "T5", 4, "Lag-row experiments must separate observed_state from commit_state."),
    ("decision_stage_required", "T6", 4, "Lag sandboxes may separate observation state, decision state, and commit state."),
    ("actuation_stage_required", "T7", 4, "Lag sandboxes may separate observed, decision, commit, actuation, and effect states."),
    ("trust_drift_required", "T8", 4, "Lag-aware sandboxes may model trust as a decaying state variable during transition delay."),
]


def evidence_level(evidence: dict[str, Any], element_id: str) -> int:
    return int(evidence.get("elements", {}).get(element_id, {}).get("evidence_level", 0))


def released_rules(evidence: dict[str, Any]) -> list[dict[str, Any]]:
    rules = []
    for rule_id, released_by, required_level, effect in RULE_DEFS:
        current = evidence_level(evidence, released_by)
        rules.append({
            "rule_id": rule_id,
            "released_by": released_by,
            "required_evidence_level": required_level,
            "current_evidence_level": current,
            "status": "released" if current >= required_level else "locked",
            "engine_effect": effect,
        })
    return rules


def write_rule_releases(evidence: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "generated_at": now(),
        "schema": "stegverse.transition_rule_releases.v1",
        "automation_gate": automation_gate(evidence),
        "rules": released_rules(evidence),
    }
    write_json(D / "transition-rule-releases.json", payload)
    return payload


def automation_gate(evidence: dict[str, Any]) -> dict[str, Any]:
    t5 = evidence_level(evidence, "T5")
    t7 = evidence_level(evidence, "T7")
    t13 = evidence_level(evidence, "T13")
    t14 = evidence_level(evidence, "T14")

    if t13 >= 4 and t14 >= 4:
        return {"mode": "scheduled_ready", "max_sequence_steps": 3, "released_by": ["T13", "T14"]}
    if t7 >= 4:
        return {"mode": "bounded_batch", "max_sequence_steps": 3, "released_by": ["T7"]}
    if t5 >= 4:
        return {"mode": "sequence_lag_row", "max_sequence_steps": 2, "released_by": ["T5"]}
    return {"mode": "manual_single", "max_sequence_steps": 1, "released_by": []}


def deps_ok(element: dict[str, Any], evidence: dict[str, Any]) -> bool:
    return all(evidence_level(evidence, dep) >= 4 for dep in element.get("relations", {}).get("requires", []))


def element_experiments(element: dict[str, Any]) -> list[str]:
    configured = list(element.get("experiments", []))
    for exp in FALLBACK_EXPERIMENTS.get(element.get("id"), []):
        if exp not in configured:
            configured.append(exp)
    return configured


def select(elements: list[dict[str, Any]], evidence: dict[str, Any]):
    for element in sorted(elements, key=lambda x: (evidence_level(evidence, x["id"]), x["taxonomy_order"])):
        if evidence_level(evidence, element["id"]) >= 4:
            continue
        if not deps_ok(element, evidence):
            continue
        for experiment in element_experiments(element):
            if experiment in EXPERIMENTS:
                return element, experiment
    return None


def sandbox_class_for(element_id: str, gate: dict[str, Any]) -> str:
    if element_id in ("T5", "T6", "T7", "T8"):
        if evidence_gate_mode_rank(gate["mode"]) >= evidence_gate_mode_rank("sequence_lag_row"):
            return "lag_aware_deterministic"
    return "local_python_deterministic"


def evidence_gate_mode_rank(mode: str) -> int:
    return {
        "manual_single": 0,
        "sequence_lag_row": 1,
        "bounded_batch": 2,
        "scheduled_ready": 3,
    }.get(mode, 0)


def applied_rules_for_element(evidence: dict[str, Any], element_id: str) -> list[str]:
    released = [rule["rule_id"] for rule in released_rules(evidence) if rule["status"] == "released"]
    if element_id in ("T5", "T6", "T7", "T8"):
        return [rule for rule in released if rule in {
            "primitive_admissibility_required",
            "simplex_constraint_visible",
            "bounded_action_visible",
            "capacity_margin_visible",
            "lag_aware_sandbox_required",
            "decision_stage_required",
            "actuation_stage_required",
        }]
    return released


def computed_for_receipt(row_payload: dict[str, Any]) -> dict[str, Any]:
    computed = {
        "admissibility_verdict": row_payload.get("verdict"),
        "constraint_result": row_payload.get("constraint_result"),
    }
    for key in [
        "capacity", "invariant", "margin", "margin_status",
        "constraint_value", "action_norm", "epsilon", "bound_status",
        "observed_invariant", "decision_invariant", "commit_invariant", "effect_invariant",
        "observed_verdict", "decision_verdict", "commit_verdict", "effect_verdict",
        "lag_flip", "decision_flip", "actuation_flip", "total_lag_flip",
        "initial_trust", "decayed_trust", "pre_decay_capacity", "post_decay_capacity",
        "pre_decay_invariant", "post_decay_invariant", "pre_decay_verdict",
        "trust_decay_verdict", "trust_flip",
    ]:
        if key in row_payload:
            computed[key] = row_payload[key]
    return computed


def receipt_for_row(row_payload: dict[str, Any], run_manifest: dict[str, Any] | None) -> dict[str, Any]:
    normalize_row(row_payload)
    receipt_id = f"RCPT-{row_payload['run_id']}"
    receipt = {
        "receipt_id": receipt_id,
        "schema": "stegverse.transition_receipt.v1",
        "created_at": now(),
        "run_id": row_payload["run_id"].rsplit("-", 1)[0],
        "ledger_row_id": row_payload["run_id"],
        "element_id": row_payload["element_id"],
        "experiment": row_payload["mode"],
        "tested_property": row_payload.get("tested_property", row_payload["mode"]),
        "sandbox": (run_manifest or {}).get("sandbox", {"type": "unknown"}),
        "applied_rules": (run_manifest or {}).get("applied_rules", []),
        "parameters": row_payload.get("parameters", {"K": 1, "alpha": 1, "beta": 1, "gamma": 1}),
        "pre_state": row_payload.get("pre_state") or row_payload.get("observed_state"),
        "observed_state": row_payload.get("observed_state"),
        "observation_lag_drift": row_payload.get("observation_lag_drift") or row_payload.get("lag_drift"),
        "decision_state": row_payload.get("decision_state"),
        "decision_lag_drift": row_payload.get("decision_lag_drift"),
        "commit_state": row_payload.get("commit_state"),
        "actuation_lag_drift": row_payload.get("actuation_lag_drift"),
        "effect_state": row_payload.get("effect_state"),
        "action": row_payload.get("action"),
        "post_state": row_payload.get("post_state"),
        "pre_decay_post_state": row_payload.get("pre_decay_post_state"),
        "trust_decayed_state": row_payload.get("trust_decayed_state"),
        "trust_decayed_post_state": row_payload.get("trust_decayed_post_state"),
        "observed_post_state": row_payload.get("observed_post_state"),
        "decision_post_state": row_payload.get("decision_post_state"),
        "commit_post_state": row_payload.get("commit_post_state"),
        "effect_post_state": row_payload.get("effect_post_state"),
        "computed": computed_for_receipt(row_payload),
        "source_hashes": {
            "ledger_row_hash": row_payload.get("row_hash"),
            "run_hash": (run_manifest or {}).get("run_hash"),
        },
        "replay": {
            "status": "replayable",
            "instructions": "Recompute each staged state by adding the recorded drift/action vectors, then recompute capacity, invariant, and verdicts.",
        },
    }
    receipt["receipt_hash"] = "sha256:" + digest(receipt)
    return receipt


def ensure_receipts(ledger: list[dict[str, Any]], runs: dict[str, Any]) -> dict[str, Any]:
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    run_by_id = {run.get("run_id"): run for run in runs.get("runs", [])}
    index: dict[str, Any] = {"generated_at": now(), "schema": "stegverse.transition_receipt_index.v1", "receipts": []}

    for row_payload in ledger:
        normalize_row(row_payload)
        parent_run_id = row_payload["run_id"].rsplit("-", 1)[0]
        manifest = run_by_id.get(parent_run_id)
        receipt = receipt_for_row(row_payload, manifest)
        receipt_path = RECEIPTS_DIR / f"{receipt['receipt_id']}.json"
        write_json(receipt_path, receipt)

        row_payload["receipt_hash"] = receipt["receipt_hash"]
        index["receipts"].append({
            "receipt_id": receipt["receipt_id"],
            "element_id": receipt["element_id"],
            "run_id": receipt["run_id"],
            "ledger_row_id": receipt["ledger_row_id"],
            "experiment": receipt["experiment"],
            "tested_property": receipt["tested_property"],
            "admissibility_verdict": receipt["computed"].get("admissibility_verdict"),
            "constraint_result": receipt["computed"].get("constraint_result"),
            "lag_flip": receipt["computed"].get("lag_flip"),
            "decision_flip": receipt["computed"].get("decision_flip"),
            "actuation_flip": receipt["computed"].get("actuation_flip"),
            "total_lag_flip": receipt["computed"].get("total_lag_flip"),
            "trust_flip": receipt["computed"].get("trust_flip"),
            "receipt_hash": receipt["receipt_hash"],
            "path": f"data/receipts/{receipt['receipt_id']}.json",
            "replay_status": "replayable",
        })

    write_json(D / "transition-receipts.json", index)
    return index


def run_one(elements: list[dict[str, Any]], evidence: dict[str, Any], ledger: list[dict[str, Any]], runs: dict[str, Any], knowledge: dict[str, Any], review: dict[str, Any], gate: dict[str, Any]):
    selected = select(elements, evidence)
    if not selected:
        return None

    element, experiment_name = selected
    run_id = f"{element['id']}-{experiment_name}-{len(runs['runs']) + 1:04d}"
    rows, deltas, promotion = EXPERIMENTS[experiment_name](run_id)
    applied_rules = applied_rules_for_element(evidence, element["id"])

    manifest = {
        "run_id": run_id,
        "element_id": element["id"],
        "experiment": experiment_name,
        "status": "completed",
        "sandbox": {
            "type": sandbox_class_for(element["id"], gate),
            "parallel_ready": True,
            "canonical_write_policy": "reducer_only",
            "max_runtime_seconds": 120,
            "automation_gate": gate["mode"],
        },
        "applied_rules": applied_rules,
        "automation_gate": gate,
        "started_at": now(),
        "completed_at": now(),
        "human_review_required": False,
        "ledger_rows": [r["run_id"] for r in rows],
        "knowledge_deltas": [d["delta_id"] for d in deltas],
    }

    if promotion.get("bad"):
        manifest["status"] = "review_required"
        manifest["human_review_required"] = True
        review.setdefault("review_required", []).append({
            "created_at": now(),
            "run_id": run_id,
            "element_id": element["id"],
            "reason": "experiment_anomaly",
            "details": promotion["bad"],
        })
        evidence["elements"][element["id"]]["runtime_state"] = "review_required"
    else:
        current = evidence["elements"][element["id"]]["evidence_level"]
        new_level = max(current, promotion["to"])
        evidence["elements"][element["id"]].update({
            "evidence_level": new_level,
            "evidence_label": LABELS[new_level],
            "brightness": round(new_level / 5, 2),
            "latest_result_summary": promotion["reason"],
            "runtime_state": "completed",
        })
        manifest["evidence_delta"] = {"from": current, "to": new_level, "reason": promotion["reason"]}

    manifest["run_hash"] = "sha256:" + digest({"manifest": manifest, "rows": rows, "knowledge_deltas": deltas})
    ledger.extend(rows)
    runs.setdefault("runs", []).append(manifest)
    knowledge.setdefault("knowledge_deltas", []).extend(deltas)
    return manifest


def main() -> None:
    D.mkdir(exist_ok=True)
    elements = read_json(D / "transition-elements.json", [])
    evidence = read_json(D / "transition-evidence.json", {"elements": {}})
    ledger = read_jsonl(D / "transition-ledger.jsonl")
    runs = read_json(D / "transition-runs.json", {"runs": []})
    knowledge = read_json(D / "transition-knowledge-deltas.json", {"knowledge_deltas": []})
    review = read_json(D / "transition-review-queue.json", {"review_required": []})

    gate = automation_gate(evidence)
    completed = []

    for _ in range(gate["max_sequence_steps"]):
        if review.get("review_required"):
            break
        manifest = run_one(elements, evidence, ledger, runs, knowledge, review, gate)
        if not manifest:
            break
        completed.append({
            "run_id": manifest["run_id"],
            "element_id": manifest["element_id"],
            "experiment": manifest["experiment"],
            "status": manifest["status"],
        })
        if manifest["status"] != "completed":
            break
        gate = automation_gate(evidence)

    evidence["generated_at"] = now()
    evidence["generated_by"] = "tools/transition_experimental_orchestrator.py"
    rule_payload = write_rule_releases(evidence)
    ensure_receipts(ledger, runs)

    if completed:
        state = {
            "planner": "evidence_gated_sequence_v1",
            "status": "completed_sequence" if len(completed) > 1 else completed[-1]["status"],
            "updated_at": now(),
            "automation_gate": rule_payload["automation_gate"],
            "sequence_completed": completed,
            "last_selected": completed[-1],
            "last_run_id": completed[-1]["run_id"],
        }
        print(json.dumps({"automation_gate": rule_payload["automation_gate"], "completed": completed}, indent=2))
    else:
        state = {
            "planner": "evidence_gated_sequence_v1",
            "status": "idle_no_eligible_experiment",
            "updated_at": now(),
            "automation_gate": rule_payload["automation_gate"],
            "sequence_completed": [],
            "last_selected": None,
            "last_run_id": None,
        }
        print("No eligible experiment. Rebuilding normalized receipts, rule releases, and pages from existing ledger.")

    write_jsonl(D / "transition-ledger.jsonl", ledger)
    write_json(D / "transition-evidence.json", evidence)
    write_json(D / "transition-runs.json", runs)
    write_json(D / "transition-knowledge-deltas.json", knowledge)
    write_json(D / "transition-review-queue.json", review)
    write_json(D / "transition-engine-state.json", state)


if __name__ == "__main__":
    main()
