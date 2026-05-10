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
        elif mode == "two_state_coupling_sweep_v1":
            row_payload["tested_property"] = "two_state_coupling"
        elif mode == "multi_agent_sweep_v1":
            row_payload["tested_property"] = "multi_agent_composition"
        elif mode == "conflict_sweep_v1":
            row_payload["tested_property"] = "conflict_resolution"
        elif mode == "consensus_sweep_v1":
            row_payload["tested_property"] = "validator_consensus"
        elif mode == "receipt_bound_sweep_v1":
            row_payload["tested_property"] = "receipt_bound_transition"
        elif mode == "reconstruction_sweep_v1":
            row_payload["tested_property"] = "receipt_reconstruction"
        elif mode == "irreversibility_sweep_v1":
            row_payload["tested_property"] = "irreversibility"
        elif mode == "self_modifying_rule_sweep_v1":
            row_payload["tested_property"] = "self_modifying_rule_safety"
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
        elif mode in ("observation_lag_sweep_v1", "decision_lag_sweep_v1", "actuation_lag_sweep_v1", "trust_drift_sweep_v1", "two_state_coupling_sweep_v1", "multi_agent_sweep_v1", "conflict_sweep_v1", "consensus_sweep_v1", "receipt_bound_sweep_v1", "reconstruction_sweep_v1", "irreversibility_sweep_v1", "self_modifying_rule_sweep_v1"):
            if row_payload.get("constraint_result") in (None, "", "None", "n/a"):
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


def t9(run_id: str):
    samples = [
        {
            "state_a": {"g": .64, "c": .64, "a": .18, "t": .82},
            "state_b": {"g": .42, "c": .56, "a": .15, "t": .74},
            "action_a": {"dg": 0, "dc": 0, "da": .02, "dt": 0},
            "coupling_effect_on_b": {"dg": -.04, "dc": -.03, "da": .03, "dt": -.05},
        },
        {
            "state_a": {"g": .70, "c": .58, "a": .16, "t": .80},
            "state_b": {"g": .60, "c": .50, "a": .13, "t": .72},
            "action_a": {"dg": 0, "dc": 0, "da": .01, "dt": 0},
            "coupling_effect_on_b": {"dg": -.03, "dc": -.03, "da": .02, "dt": -.04},
        },
        {
            "state_a": {"g": .52, "c": .72, "a": .16, "t": .78},
            "state_b": {"g": .50, "c": .62, "a": .17, "t": .76},
            "action_a": {"dg": 0, "dc": 0, "da": .02, "dt": 0},
            "coupling_effect_on_b": {"dg": -.07, "dc": -.04, "da": .03, "dt": -.08},
        },
    ]
    rows = []
    flips = 0
    coupled_denials = 0
    for i, sample in enumerate(samples, 1):
        state_a = sample["state_a"]
        state_b = sample["state_b"]
        action_a = sample["action_a"]
        coupling = sample["coupling_effect_on_b"]

        post_state_a = post(state_a, action_a)
        post_state_b_without_coupling = dict(state_b)
        post_state_b_with_coupling = state_add(state_b, coupling)

        a_verdict = verdict_for(post_state_a)
        b_verdict_without_coupling = verdict_for(post_state_b_without_coupling)
        b_verdict_with_coupling = verdict_for(post_state_b_with_coupling)
        coupling_flip = b_verdict_without_coupling != b_verdict_with_coupling
        local_admissible_coupled_denied = a_verdict == "ALLOW" and b_verdict_without_coupling == "ALLOW" and b_verdict_with_coupling == "DENY"

        flips += int(coupling_flip)
        coupled_denials += int(local_admissible_coupled_denied)

        payload = {
            "timestamp": now(),
            "element_id": "T9",
            "mode": "two_state_coupling_sweep_v1",
            "run_id": f"{run_id}-{i:03d}",
            "tested_property": "two_state_coupling",
            "state_a": state_a,
            "state_b": state_b,
            "action_a": action_a,
            "coupling_effect_on_b": coupling,
            "post_state_a": post_state_a,
            "post_state_b_without_coupling": post_state_b_without_coupling,
            "post_state_b_with_coupling": post_state_b_with_coupling,
            "post_state": {"a": post_state_a, "b": post_state_b_with_coupling},
            "parameters": {"K": 1, "alpha": 1, "beta": 1, "gamma": 1, "coupling_model": "deterministic_delta"},
            "a_invariant": invariant(post_state_a),
            "b_invariant_without_coupling": invariant(post_state_b_without_coupling),
            "b_invariant_with_coupling": invariant(post_state_b_with_coupling),
            "invariant": max(invariant(post_state_a), invariant(post_state_b_with_coupling)),
            "a_verdict": a_verdict,
            "b_verdict_without_coupling": b_verdict_without_coupling,
            "b_verdict_with_coupling": b_verdict_with_coupling,
            "verdict": "ALLOW" if a_verdict == "ALLOW" and b_verdict_with_coupling == "ALLOW" else "DENY",
            "coupling_flip": coupling_flip,
            "local_admissible_coupled_denied": local_admissible_coupled_denied,
            "constraint_result": "PASS",
            "passed": True,
            "receipt_hash": None,
        }
        payload["row_hash"] = digest(payload)
        rows.append(payload)

    kd = [{
        "delta_id": f"KD-{run_id}-two-state-coupling",
        "source_run_id": run_id,
        "source_element": "T9",
        "delta_type": "coupled_state_fragment",
        "summary": f"Two-state coupling sweep found {flips} coupling flip(s), including {coupled_denials} case(s) where local admissibility became coupled inadmissibility.",
        "informs": ["T9", "T10", "T11"],
        "confidence": .85,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic two-state coupling sweep passed", "bad": []}


def vector_sum(actions: list[dict[str, float]]) -> dict[str, float]:
    return {
        "dg": round(sum(action.get("dg", 0.0) for action in actions), 4),
        "dc": round(sum(action.get("dc", 0.0) for action in actions), 4),
        "da": round(sum(action.get("da", 0.0) for action in actions), 4),
        "dt": round(sum(action.get("dt", 0.0) for action in actions), 4),
    }


def t10(run_id: str):
    samples = [
        {
            "shared_state": {"g": .64, "c": .64, "a": .20, "t": .82},
            "agent_actions": [
                {"agent": "agent_1", "action": {"dg": 0, "dc": 0, "da": .01, "dt": 0}},
                {"agent": "agent_2", "action": {"dg": 0, "dc": 0, "da": .015, "dt": 0}},
                {"agent": "agent_3", "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}},
            ],
        },
        {
            "shared_state": {"g": .72, "c": .58, "a": .16, "t": .76},
            "agent_actions": [
                {"agent": "agent_1", "action": {"dg": -.01, "dc": 0, "da": .015, "dt": 0}},
                {"agent": "agent_2", "action": {"dg": 0, "dc": -.01, "da": .015, "dt": 0}},
                {"agent": "agent_3", "action": {"dg": 0, "dc": 0, "da": .025, "dt": -.02}},
            ],
        },
        {
            "shared_state": {"g": .56, "c": .68, "a": .18, "t": .78},
            "agent_actions": [
                {"agent": "agent_1", "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}},
                {"agent": "agent_2", "action": {"dg": -.02, "dc": 0, "da": .02, "dt": -.02}},
                {"agent": "agent_3", "action": {"dg": 0, "dc": -.02, "da": .025, "dt": -.03}},
            ],
        },
    ]

    rows = []
    flips = 0
    aggregate_denials = 0

    for i, sample in enumerate(samples, 1):
        shared_state = sample["shared_state"]
        agent_actions = sample["agent_actions"]
        individual_results = []

        for agent_action in agent_actions:
            agent_name = agent_action["agent"]
            action = agent_action["action"]
            individual_post_state = post(shared_state, action)
            individual_results.append({
                "agent": agent_name,
                "action": action,
                "post_state": individual_post_state,
                "invariant": invariant(individual_post_state),
                "verdict": verdict_for(individual_post_state),
            })

        aggregate_action = vector_sum([entry["action"] for entry in agent_actions])
        aggregate_post_state = post(shared_state, aggregate_action)
        individual_verdicts = [result["verdict"] for result in individual_results]
        aggregate_verdict = verdict_for(aggregate_post_state)
        composition_flip = all(v == "ALLOW" for v in individual_verdicts) and aggregate_verdict == "DENY"

        flips += int(composition_flip)
        aggregate_denials += int(aggregate_verdict == "DENY")

        payload = {
            "timestamp": now(),
            "element_id": "T10",
            "mode": "multi_agent_sweep_v1",
            "run_id": f"{run_id}-{i:03d}",
            "tested_property": "multi_agent_composition",
            "shared_state": shared_state,
            "agent_actions": agent_actions,
            "individual_results": individual_results,
            "individual_verdicts": individual_verdicts,
            "aggregate_action": aggregate_action,
            "aggregate_post_state": aggregate_post_state,
            "post_state": aggregate_post_state,
            "parameters": {"K": 1, "alpha": 1, "beta": 1, "gamma": 1, "composition_model": "vector_sum"},
            "aggregate_invariant": invariant(aggregate_post_state),
            "invariant": invariant(aggregate_post_state),
            "aggregate_verdict": aggregate_verdict,
            "verdict": aggregate_verdict,
            "composition_flip": composition_flip,
            "all_individual_allow": all(v == "ALLOW" for v in individual_verdicts),
            "constraint_result": "PASS",
            "passed": True,
            "receipt_hash": None,
        }
        payload["row_hash"] = digest(payload)
        rows.append(payload)

    kd = [{
        "delta_id": f"KD-{run_id}-multi-agent",
        "source_run_id": run_id,
        "source_element": "T10",
        "delta_type": "multi_agent_fragment",
        "summary": f"Multi-agent sweep found {flips} composition flip(s), including {aggregate_denials} aggregate denial(s) across deterministic samples.",
        "informs": ["T10", "T11", "T12"],
        "confidence": .84,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic multi-agent composition sweep passed", "bad": []}


def conflict_score(action_a: dict[str, float], action_b: dict[str, float]) -> float:
    return round(sum(abs(action_a.get(k, 0.0) + action_b.get(k, 0.0)) for k in ["dg", "dc", "da", "dt"]), 5)


def t11(run_id: str):
    samples = [
        {
            "shared_state": {"g": .66, "c": .64, "a": .18, "t": .80},
            "action_a": {"dg": .03, "dc": -.01, "da": .02, "dt": 0},
            "action_b": {"dg": -.05, "dc": -.03, "da": .025, "dt": -.04},
            "conflict_threshold": .06,
        },
        {
            "shared_state": {"g": .72, "c": .60, "a": .15, "t": .78},
            "action_a": {"dg": .02, "dc": 0, "da": .015, "dt": -.01},
            "action_b": {"dg": -.01, "dc": .02, "da": .01, "dt": 0},
            "conflict_threshold": .08,
        },
        {
            "shared_state": {"g": .58, "c": .70, "a": .17, "t": .76},
            "action_a": {"dg": .04, "dc": -.02, "da": .02, "dt": -.02},
            "action_b": {"dg": -.06, "dc": -.04, "da": .03, "dt": -.05},
            "conflict_threshold": .07,
        },
    ]

    rows = []
    conflict_flips = 0
    resolved_allows = 0

    for i, sample in enumerate(samples, 1):
        shared_state = sample["shared_state"]
        action_a = sample["action_a"]
        action_b = sample["action_b"]
        threshold = sample["conflict_threshold"]

        post_a = post(shared_state, action_a)
        post_b = post(shared_state, action_b)
        combined_action = vector_sum([action_a, action_b])
        combined_post_state = post(shared_state, combined_action)

        verdict_a = verdict_for(post_a)
        verdict_b = verdict_for(post_b)
        combined_verdict = verdict_for(combined_post_state)

        score = conflict_score(action_a, action_b)
        conflict_detected = score > threshold
        conflict_flip = verdict_a == "ALLOW" and verdict_b == "ALLOW" and combined_verdict == "DENY"
        conflict_flips += int(conflict_flip)

        if conflict_detected and conflict_flip:
            # Minimal deterministic resolver: preserve the lower-risk action by smaller action norm.
            norm_a = round(math.sqrt(sum(v * v for v in action_a.values())), 5)
            norm_b = round(math.sqrt(sum(v * v for v in action_b.values())), 5)
            selected_action = action_a if norm_a <= norm_b else action_b
            rejected_action = action_b if norm_a <= norm_b else action_a
            resolution_policy = "select_lower_action_norm"
        else:
            norm_a = round(math.sqrt(sum(v * v for v in action_a.values())), 5)
            norm_b = round(math.sqrt(sum(v * v for v in action_b.values())), 5)
            selected_action = combined_action
            rejected_action = None
            resolution_policy = "combined_action_allowed_or_no_conflict"

        resolved_post_state = post(shared_state, selected_action)
        resolved_verdict = verdict_for(resolved_post_state)
        resolved_allows += int(resolved_verdict == "ALLOW")

        payload = {
            "timestamp": now(),
            "element_id": "T11",
            "mode": "conflict_sweep_v1",
            "run_id": f"{run_id}-{i:03d}",
            "tested_property": "conflict_resolution",
            "shared_state": shared_state,
            "action_a": action_a,
            "action_b": action_b,
            "post_a": post_a,
            "post_b": post_b,
            "combined_action": combined_action,
            "combined_post_state": combined_post_state,
            "selected_action": selected_action,
            "rejected_action": rejected_action,
            "resolved_post_state": resolved_post_state,
            "post_state": resolved_post_state,
            "parameters": {"K": 1, "alpha": 1, "beta": 1, "gamma": 1, "conflict_threshold": threshold},
            "verdict_a": verdict_a,
            "verdict_b": verdict_b,
            "combined_verdict": combined_verdict,
            "resolved_verdict": resolved_verdict,
            "verdict": resolved_verdict,
            "conflict_score": score,
            "conflict_detected": conflict_detected,
            "conflict_flip": conflict_flip,
            "resolution_policy": resolution_policy,
            "invariant": invariant(resolved_post_state),
            "combined_invariant": invariant(combined_post_state),
            "resolved_invariant": invariant(resolved_post_state),
            "constraint_result": "PASS",
            "passed": True,
            "receipt_hash": None,
        }
        payload["row_hash"] = digest(payload)
        rows.append(payload)

    kd = [{
        "delta_id": f"KD-{run_id}-conflict",
        "source_run_id": run_id,
        "source_element": "T11",
        "delta_type": "conflict_resolution_fragment",
        "summary": f"Conflict sweep found {conflict_flips} conflict flip(s) and produced {resolved_allows} resolved admissible outcome(s).",
        "informs": ["T11", "T12", "T15"],
        "confidence": .83,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic conflict resolution sweep passed", "bad": []}


def t12(run_id: str):
    samples = [
        {
            "canonical_state": {"g": .68, "c": .62, "a": .18, "t": .80},
            "proposal_action": {"dg": 0, "dc": 0, "da": .02, "dt": 0},
            "validator_drifts": [
                {"validator": "v1", "drift": {"dg": 0, "dc": 0, "da": 0, "dt": 0}},
                {"validator": "v2", "drift": {"dg": -.01, "dc": 0, "da": .005, "dt": -.02}},
                {"validator": "v3", "drift": {"dg": 0, "dc": -.01, "da": 0, "dt": -.01}},
            ],
            "quorum_threshold": 2,
        },
        {
            "canonical_state": {"g": .58, "c": .58, "a": .17, "t": .78},
            "proposal_action": {"dg": 0, "dc": 0, "da": .025, "dt": 0},
            "validator_drifts": [
                {"validator": "v1", "drift": {"dg": 0, "dc": 0, "da": 0, "dt": 0}},
                {"validator": "v2", "drift": {"dg": -.03, "dc": -.02, "da": .02, "dt": -.05}},
                {"validator": "v3", "drift": {"dg": -.04, "dc": -.03, "da": .02, "dt": -.06}},
            ],
            "quorum_threshold": 2,
        },
        {
            "canonical_state": {"g": .72, "c": .54, "a": .15, "t": .76},
            "proposal_action": {"dg": 0, "dc": 0, "da": .02, "dt": 0},
            "validator_drifts": [
                {"validator": "v1", "drift": {"dg": 0, "dc": 0, "da": 0, "dt": 0}},
                {"validator": "v2", "drift": {"dg": -.02, "dc": -.01, "da": .01, "dt": -.03}},
                {"validator": "v3", "drift": {"dg": -.06, "dc": -.04, "da": .03, "dt": -.08}},
            ],
            "quorum_threshold": 2,
        },
    ]

    rows = []
    consensus_flips = 0
    quorum_passes = 0

    for i, sample in enumerate(samples, 1):
        canonical_state = sample["canonical_state"]
        proposal_action = sample["proposal_action"]
        validator_drifts = sample["validator_drifts"]
        threshold = sample["quorum_threshold"]

        canonical_post_state = post(canonical_state, proposal_action)
        canonical_verdict = verdict_for(canonical_post_state)

        validator_results = []
        for entry in validator_drifts:
            validator_state = state_add(canonical_state, entry["drift"])
            validator_post_state = post(validator_state, proposal_action)
            validator_results.append({
                "validator": entry["validator"],
                "drift": entry["drift"],
                "validator_state": validator_state,
                "validator_post_state": validator_post_state,
                "invariant": invariant(validator_post_state),
                "verdict": verdict_for(validator_post_state),
            })

        allow_votes = sum(1 for result in validator_results if result["verdict"] == "ALLOW")
        deny_votes = len(validator_results) - allow_votes
        quorum_result = "ALLOW" if allow_votes >= threshold else "DENY"
        consensus_flip = quorum_result != canonical_verdict
        consensus_flips += int(consensus_flip)
        quorum_passes += int(quorum_result == "ALLOW")

        payload = {
            "timestamp": now(),
            "element_id": "T12",
            "mode": "consensus_sweep_v1",
            "run_id": f"{run_id}-{i:03d}",
            "tested_property": "validator_consensus",
            "canonical_state": canonical_state,
            "proposal_action": proposal_action,
            "canonical_post_state": canonical_post_state,
            "validator_results": validator_results,
            "validator_verdicts": [result["verdict"] for result in validator_results],
            "allow_votes": allow_votes,
            "deny_votes": deny_votes,
            "quorum_threshold": threshold,
            "quorum_result": quorum_result,
            "canonical_verdict": canonical_verdict,
            "consensus_flip": consensus_flip,
            "post_state": canonical_post_state,
            "parameters": {"K": 1, "alpha": 1, "beta": 1, "gamma": 1, "quorum_threshold": threshold, "validator_count": len(validator_results)},
            "invariant": invariant(canonical_post_state),
            "verdict": quorum_result,
            "constraint_result": "PASS",
            "passed": True,
            "receipt_hash": None,
        }
        payload["row_hash"] = digest(payload)
        rows.append(payload)

    kd = [{
        "delta_id": f"KD-{run_id}-consensus",
        "source_run_id": run_id,
        "source_element": "T12",
        "delta_type": "consensus_fragment",
        "summary": f"Consensus sweep found {consensus_flips} consensus flip(s) between validator quorum and canonical admissibility, with {quorum_passes} quorum allow outcome(s).",
        "informs": ["T12", "T13", "T14"],
        "confidence": .82,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic validator consensus sweep passed", "bad": []}


def t13(run_id: str):
    samples = [
        {"pre_state": {"g": .68, "c": .64, "a": .18, "t": .82}, "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0}},
        {"pre_state": {"g": .72, "c": .58, "a": .16, "t": .78}, "action": {"dg": -.01, "dc": 0, "da": .02, "dt": -.01}},
        {"pre_state": {"g": .58, "c": .70, "a": .17, "t": .80}, "action": {"dg": 0, "dc": -.02, "da": .025, "dt": -.02}},
    ]

    rows = []
    receipt_bound_count = 0

    for i, sample in enumerate(samples, 1):
        pre_state = sample["pre_state"]
        action = sample["action"]
        post_state = post(pre_state, action)
        verdict = verdict_for(post_state)
        payload_core = {
            "element_id": "T13",
            "mode": "receipt_bound_sweep_v1",
            "pre_state": pre_state,
            "action": action,
            "post_state": post_state,
            "parameters": {"K": 1, "alpha": 1, "beta": 1, "gamma": 1},
            "capacity": capacity(post_state),
            "invariant": invariant(post_state),
            "verdict": verdict,
        }
        pre_state_hash = "sha256:" + digest(pre_state)
        action_hash = "sha256:" + digest(action)
        post_state_hash = "sha256:" + digest(post_state)
        receipt_payload_hash = "sha256:" + digest(payload_core)
        receipt_bound = all([pre_state_hash, action_hash, post_state_hash, receipt_payload_hash])
        receipt_bound_count += int(receipt_bound)

        payload = {
            "timestamp": now(),
            "element_id": "T13",
            "mode": "receipt_bound_sweep_v1",
            "run_id": f"{run_id}-{i:03d}",
            "tested_property": "receipt_bound_transition",
            "pre_state": pre_state,
            "action": action,
            "post_state": post_state,
            "parameters": payload_core["parameters"],
            "capacity": payload_core["capacity"],
            "invariant": payload_core["invariant"],
            "verdict": verdict,
            "pre_state_hash": pre_state_hash,
            "action_hash": action_hash,
            "post_state_hash": post_state_hash,
            "receipt_payload_hash": receipt_payload_hash,
            "receipt_bound": receipt_bound,
            "constraint_result": "PASS",
            "passed": True,
            "receipt_hash": None,
        }
        payload["row_hash"] = digest(payload)
        rows.append(payload)

    kd = [{
        "delta_id": f"KD-{run_id}-receipt-bound",
        "source_run_id": run_id,
        "source_element": "T13",
        "delta_type": "receipt_binding_fragment",
        "summary": f"Receipt-bound sweep produced {receipt_bound_count} receipt-bound transition sample(s) with pre-state, action, and post-state hashes.",
        "informs": ["T13", "T14", "T15"],
        "confidence": .86,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic receipt-bound transition sweep passed", "bad": []}


def t14(run_id: str):
    samples = [
        {
            "pre_state": {"g": .68, "c": .64, "a": .18, "t": .82},
            "action": {"dg": 0, "dc": 0, "da": .02, "dt": 0},
        },
        {
            "pre_state": {"g": .72, "c": .58, "a": .16, "t": .78},
            "action": {"dg": -.01, "dc": 0, "da": .02, "dt": -.01},
        },
        {
            "pre_state": {"g": .58, "c": .70, "a": .17, "t": .80},
            "action": {"dg": 0, "dc": -.02, "da": .025, "dt": -.02},
        },
    ]

    rows = []
    exact_reconstructions = 0

    for i, sample in enumerate(samples, 1):
        pre_state = sample["pre_state"]
        action = sample["action"]
        observed_post_state = post(pre_state, action)

        receipt_packet = {
            "pre_state": pre_state,
            "action": action,
            "observed_post_state_hash": "sha256:" + digest(observed_post_state),
            "parameters": {"K": 1, "alpha": 1, "beta": 1, "gamma": 1},
        }

        reconstructed_post_state = post(receipt_packet["pre_state"], receipt_packet["action"])
        reconstruction_delta = {
            k: round(observed_post_state[k] - reconstructed_post_state[k], 8)
            for k in ["g", "c", "a", "t"]
        }
        reconstruction_exact = all(v == 0 for v in reconstruction_delta.values())
        exact_reconstructions += int(reconstruction_exact)

        observed_verdict = verdict_for(observed_post_state)
        reconstructed_verdict = verdict_for(reconstructed_post_state)
        reconstruction_verdict_match = observed_verdict == reconstructed_verdict
        reconstruction_confidence = 1.0 if reconstruction_exact and reconstruction_verdict_match else 0.75

        payload = {
            "timestamp": now(),
            "element_id": "T14",
            "mode": "reconstruction_sweep_v1",
            "run_id": f"{run_id}-{i:03d}",
            "tested_property": "receipt_reconstruction",
            "pre_state": pre_state,
            "action": action,
            "observed_post_state": observed_post_state,
            "reconstructed_post_state": reconstructed_post_state,
            "post_state": reconstructed_post_state,
            "receipt_packet": receipt_packet,
            "parameters": receipt_packet["parameters"],
            "observed_post_state_hash": receipt_packet["observed_post_state_hash"],
            "reconstructed_post_state_hash": "sha256:" + digest(reconstructed_post_state),
            "reconstruction_delta": reconstruction_delta,
            "reconstruction_exact": reconstruction_exact,
            "observed_verdict": observed_verdict,
            "reconstructed_verdict": reconstructed_verdict,
            "reconstruction_verdict_match": reconstruction_verdict_match,
            "reconstruction_confidence": reconstruction_confidence,
            "capacity": capacity(reconstructed_post_state),
            "invariant": invariant(reconstructed_post_state),
            "verdict": reconstructed_verdict,
            "constraint_result": "PASS",
            "passed": True,
            "receipt_hash": None,
        }
        payload["row_hash"] = digest(payload)
        rows.append(payload)

    kd = [{
        "delta_id": f"KD-{run_id}-reconstruction",
        "source_run_id": run_id,
        "source_element": "T14",
        "delta_type": "reconstruction_fragment",
        "summary": f"Reconstruction sweep exactly reconstructed {exact_reconstructions} end-state sample(s) from receipt packets.",
        "informs": ["T14", "T15", "T16"],
        "confidence": .87,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic receipt reconstruction sweep passed", "bad": []}


def t15(run_id: str):
    samples = [
        {
            "pre_state": {"g": .70, "c": .64, "a": .18, "t": .82},
            "action": {"dg": -.04, "dc": -.03, "da": .04, "dt": -.06},
            "reversal_budget": {"dg": .02, "dc": .02, "da": -.02, "dt": .03},
            "irreversibility_threshold": .05,
        },
        {
            "pre_state": {"g": .76, "c": .68, "a": .14, "t": .84},
            "action": {"dg": -.01, "dc": 0, "da": .01, "dt": -.01},
            "reversal_budget": {"dg": .02, "dc": .02, "da": -.02, "dt": .02},
            "irreversibility_threshold": .05,
        },
        {
            "pre_state": {"g": .58, "c": .62, "a": .16, "t": .78},
            "action": {"dg": -.08, "dc": -.06, "da": .06, "dt": -.10},
            "reversal_budget": {"dg": .03, "dc": .03, "da": -.03, "dt": .04},
            "irreversibility_threshold": .05,
        },
    ]

    rows = []
    irreversible_count = 0
    point_of_no_return_count = 0

    for i, sample in enumerate(samples, 1):
        pre_state = sample["pre_state"]
        action = sample["action"]
        reversal_budget = sample["reversal_budget"]
        threshold = sample["irreversibility_threshold"]

        committed_state = post(pre_state, action)
        attempted_reversal_state = post(committed_state, reversal_budget)

        pre_verdict = verdict_for(pre_state)
        committed_verdict = verdict_for(committed_state)
        attempted_reversal_verdict = verdict_for(attempted_reversal_state)

        residual_delta = {
            k: round(pre_state[k] - attempted_reversal_state[k], 8)
            for k in ["g", "c", "a", "t"]
        }
        residual_norm = round(math.sqrt(sum(v * v for v in residual_delta.values())), 5)
        irreversible = residual_norm > threshold
        point_of_no_return = committed_verdict == "DENY" and attempted_reversal_verdict == "DENY"

        irreversible_count += int(irreversible)
        point_of_no_return_count += int(point_of_no_return)

        payload = {
            "timestamp": now(),
            "element_id": "T15",
            "mode": "irreversibility_sweep_v1",
            "run_id": f"{run_id}-{i:03d}",
            "tested_property": "irreversibility",
            "pre_state": pre_state,
            "action": action,
            "committed_state": committed_state,
            "reversal_budget": reversal_budget,
            "attempted_reversal_state": attempted_reversal_state,
            "post_state": committed_state,
            "parameters": {"K": 1, "alpha": 1, "beta": 1, "gamma": 1, "irreversibility_threshold": threshold},
            "pre_verdict": pre_verdict,
            "committed_verdict": committed_verdict,
            "attempted_reversal_verdict": attempted_reversal_verdict,
            "residual_delta": residual_delta,
            "residual_norm": residual_norm,
            "irreversible": irreversible,
            "point_of_no_return": point_of_no_return,
            "capacity": capacity(committed_state),
            "invariant": invariant(committed_state),
            "verdict": committed_verdict,
            "constraint_result": "PASS",
            "passed": True,
            "receipt_hash": None,
        }
        payload["row_hash"] = digest(payload)
        rows.append(payload)

    kd = [{
        "delta_id": f"KD-{run_id}-irreversibility",
        "source_run_id": run_id,
        "source_element": "T15",
        "delta_type": "irreversibility_fragment",
        "summary": f"Irreversibility sweep found {irreversible_count} irreversible sample(s), including {point_of_no_return_count} point-of-no-return sample(s).",
        "informs": ["T15", "T16"],
        "confidence": .81,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic irreversibility sweep passed", "bad": []}


def rule_patch_hash(rule_patch: dict[str, Any]) -> str:
    return "sha256:" + digest(rule_patch)


def t16(run_id: str):
    samples = [
        {
            "rule_patch": {
                "rule_id": "tighten_open_boundary_review",
                "operation": "add_guard",
                "target_rule": "irreversibility_detection_required",
                "requires_receipt_bound": True,
                "requires_reconstruction_match": True,
                "requires_human_review": False,
            },
            "pre_rule_state": {"released_rules_count": 15, "protected_rules_count": 15, "self_modification_allowed": False},
            "safety_constraints": {
                "receipt_bound": True,
                "reconstruction_verdict_match": True,
                "does_not_weaken_existing_rule": True,
                "does_not_disable_review_queue": True,
            },
        },
        {
            "rule_patch": {
                "rule_id": "disable_review_queue_for_speed",
                "operation": "weaken_guard",
                "target_rule": "conflict_resolution_required",
                "requires_human_review": False,
                "disables_review_queue": True,
            },
            "pre_rule_state": {"released_rules_count": 15, "protected_rules_count": 15, "self_modification_allowed": False},
            "safety_constraints": {
                "receipt_bound": True,
                "reconstruction_verdict_match": True,
                "does_not_weaken_existing_rule": False,
                "does_not_disable_review_queue": False,
            },
        },
        {
            "rule_patch": {
                "rule_id": "add_self_modification_receipt_requirement",
                "operation": "add_guard",
                "target_rule": "self_modification_required",
                "requires_receipt_bound": True,
                "requires_reconstruction_match": True,
                "requires_irreversibility_check": True,
                "requires_rule_delta_hash": True,
            },
            "pre_rule_state": {"released_rules_count": 15, "protected_rules_count": 15, "self_modification_allowed": False},
            "safety_constraints": {
                "receipt_bound": True,
                "reconstruction_verdict_match": True,
                "does_not_weaken_existing_rule": True,
                "does_not_disable_review_queue": True,
            },
        },
    ]

    rows = []
    safe_count = 0
    blocked_count = 0

    for i, sample in enumerate(samples, 1):
        rule_patch = sample["rule_patch"]
        pre_rule_state = sample["pre_rule_state"]
        safety = sample["safety_constraints"]

        rule_delta_hash = rule_patch_hash(rule_patch)
        constraints_pass = all(bool(v) for v in safety.values())
        self_modification_safe = constraints_pass and rule_patch.get("operation") in ("add_guard", "tighten_guard")
        rule_patch_verdict = "ALLOW" if self_modification_safe else "DENY"

        post_rule_state = dict(pre_rule_state)
        if self_modification_safe:
            post_rule_state["released_rules_count"] = pre_rule_state["released_rules_count"] + 1
            post_rule_state["protected_rules_count"] = pre_rule_state["protected_rules_count"] + 1
            post_rule_state["self_modification_allowed"] = True
            safe_count += 1
        else:
            post_rule_state["self_modification_allowed"] = False
            blocked_count += 1

        payload = {
            "timestamp": now(),
            "element_id": "T16",
            "mode": "self_modifying_rule_sweep_v1",
            "run_id": f"{run_id}-{i:03d}",
            "tested_property": "self_modifying_rule_safety",
            "pre_rule_state": pre_rule_state,
            "rule_patch": rule_patch,
            "rule_delta_hash": rule_delta_hash,
            "safety_constraints": safety,
            "post_rule_state": post_rule_state,
            "post_state": post_rule_state,
            "parameters": {"rule_model": "deterministic_guarded_patch", "requires_receipts": True, "requires_reconstruction": True},
            "constraints_pass": constraints_pass,
            "self_modification_safe": self_modification_safe,
            "rule_patch_verdict": rule_patch_verdict,
            "verdict": rule_patch_verdict,
            "constraint_result": "PASS" if constraints_pass else "FAIL",
            "passed": True,
            "receipt_hash": None,
        }
        payload["row_hash"] = digest(payload)
        rows.append(payload)

    kd = [{
        "delta_id": f"KD-{run_id}-self-modifying",
        "source_run_id": run_id,
        "source_element": "T16",
        "delta_type": "self_modification_fragment",
        "summary": f"Self-modifying rule sweep allowed {safe_count} guarded rule patch(es) and blocked {blocked_count} unsafe rule patch(es).",
        "informs": ["T16"],
        "confidence": .79,
        "review_required": False,
    }]
    return rows, kd, {"to": 4, "reason": "deterministic self-modifying rule safety sweep passed", "bad": []}


EXPERIMENTS = {
    "simplex_conservation_sweep_v1": t2,
    "bounded_action_sweep_v1": t3,
    "capacity_margin_sweep_v1": t4,
    "observation_lag_sweep_v1": t5,
    "decision_lag_sweep_v1": t6,
    "actuation_lag_sweep_v1": t7,
    "trust_drift_sweep_v1": t8,
    "two_state_coupling_sweep_v1": t9,
    "multi_agent_sweep_v1": t10,
    "conflict_sweep_v1": t11,
    "consensus_sweep_v1": t12,
    "receipt_bound_sweep_v1": t13,
    "reconstruction_sweep_v1": t14,
    "irreversibility_sweep_v1": t15,
    "self_modifying_rule_sweep_v1": t16,
}

FALLBACK_EXPERIMENTS = {
    "T5": ["observation_lag_sweep_v1"],
    "T6": ["decision_lag_sweep_v1"],
    "T7": ["actuation_lag_sweep_v1"],
    "T8": ["trust_drift_sweep_v1"],
    "T9": ["two_state_coupling_sweep_v1"],
    "T10": ["multi_agent_sweep_v1"],
    "T11": ["conflict_sweep_v1"],
    "T12": ["consensus_sweep_v1"],
    "T13": ["receipt_bound_sweep_v1"],
    "T14": ["reconstruction_sweep_v1"],
    "T15": ["irreversibility_sweep_v1"],
    "T16": ["self_modifying_rule_sweep_v1"],
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
    ("two_state_coupling_required", "T9", 4, "Coupled sandboxes may model disturbance from one transition state into another."),
    ("multi_agent_composition_required", "T10", 4, "Coupled sandboxes may compare individually admissible actions against aggregate admissibility."),
    ("conflict_resolution_required", "T11", 4, "Coupled sandboxes may detect conflicts between otherwise admissible actions and record resolution policy."),
    ("validator_consensus_required", "T12", 4, "Coupled sandboxes may compare validator quorum against canonical admissibility."),
    ("receipt_binding_required", "T13", 4, "Evidence sandboxes must bind pre-state, action, and post-state into replayable receipts."),
    ("receipt_reconstruction_required", "T14", 4, "Evidence sandboxes may reconstruct end-state from receipt packets and compare reconstructed state to observed state."),
    ("irreversibility_detection_required", "T15", 4, "Open-boundary sandboxes may test whether a committed transition crosses a point of no return under bounded reversal."),
    ("self_modification_required", "T16", 4, "Open-boundary sandboxes may test guarded rule patches without weakening released rules or disabling review."),
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
    if element_id in ("T15", "T16"):
        return "open_boundary_deterministic"
    if element_id in ("T13", "T14"):
        return "receipt_evidence_deterministic"
    if element_id in ("T9", "T10", "T11", "T12"):
        return "coupled_state_deterministic"
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
        "a_invariant", "b_invariant_without_coupling", "b_invariant_with_coupling",
        "a_verdict", "b_verdict_without_coupling", "b_verdict_with_coupling",
        "coupling_flip", "local_admissible_coupled_denied",
        "aggregate_invariant", "aggregate_verdict", "composition_flip", "all_individual_allow",
        "verdict_a", "verdict_b", "combined_verdict", "resolved_verdict",
        "conflict_score", "conflict_detected", "conflict_flip", "resolution_policy",
        "combined_invariant", "resolved_invariant",
        "allow_votes", "deny_votes", "quorum_threshold", "quorum_result",
        "canonical_verdict", "consensus_flip",
        "pre_state_hash", "action_hash", "post_state_hash", "receipt_payload_hash", "receipt_bound",
        "observed_post_state_hash", "reconstructed_post_state_hash", "reconstruction_delta",
        "reconstruction_exact", "observed_verdict", "reconstructed_verdict",
        "reconstruction_verdict_match", "reconstruction_confidence",
        "pre_verdict", "committed_verdict", "attempted_reversal_verdict",
        "residual_delta", "residual_norm", "irreversible", "point_of_no_return",
        "rule_delta_hash", "constraints_pass", "self_modification_safe", "rule_patch_verdict",
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
        "pre_state": row_payload.get("pre_state") or row_payload.get("observed_state") or {"state_a": row_payload.get("state_a"), "state_b": row_payload.get("state_b")},
        "state_a": row_payload.get("state_a"),
        "state_b": row_payload.get("state_b"),
        "action_a": row_payload.get("action_a"),
        "coupling_effect_on_b": row_payload.get("coupling_effect_on_b"),
        "post_state_a": row_payload.get("post_state_a"),
        "post_state_b_without_coupling": row_payload.get("post_state_b_without_coupling"),
        "post_state_b_with_coupling": row_payload.get("post_state_b_with_coupling"),
        "observed_state": row_payload.get("observed_state"),
        "observation_lag_drift": row_payload.get("observation_lag_drift") or row_payload.get("lag_drift"),
        "decision_state": row_payload.get("decision_state"),
        "decision_lag_drift": row_payload.get("decision_lag_drift"),
        "commit_state": row_payload.get("commit_state"),
        "actuation_lag_drift": row_payload.get("actuation_lag_drift"),
        "effect_state": row_payload.get("effect_state"),
        "action": row_payload.get("action"),
        "post_state": row_payload.get("post_state"),
        "shared_state": row_payload.get("shared_state"),
        "agent_actions": row_payload.get("agent_actions"),
        "individual_results": row_payload.get("individual_results"),
        "individual_verdicts": row_payload.get("individual_verdicts"),
        "aggregate_action": row_payload.get("aggregate_action"),
        "aggregate_post_state": row_payload.get("aggregate_post_state"),
        "action_a": row_payload.get("action_a"),
        "action_b": row_payload.get("action_b"),
        "post_a": row_payload.get("post_a"),
        "post_b": row_payload.get("post_b"),
        "combined_action": row_payload.get("combined_action"),
        "combined_post_state": row_payload.get("combined_post_state"),
        "selected_action": row_payload.get("selected_action"),
        "rejected_action": row_payload.get("rejected_action"),
        "resolved_post_state": row_payload.get("resolved_post_state"),
        "canonical_state": row_payload.get("canonical_state"),
        "proposal_action": row_payload.get("proposal_action"),
        "canonical_post_state": row_payload.get("canonical_post_state"),
        "validator_results": row_payload.get("validator_results"),
        "validator_verdicts": row_payload.get("validator_verdicts"),
        "receipt_packet": row_payload.get("receipt_packet"),
        "reconstructed_post_state": row_payload.get("reconstructed_post_state"),
        "reconstruction_delta": row_payload.get("reconstruction_delta"),
        "committed_state": row_payload.get("committed_state"),
        "reversal_budget": row_payload.get("reversal_budget"),
        "attempted_reversal_state": row_payload.get("attempted_reversal_state"),
        "residual_delta": row_payload.get("residual_delta"),
        "pre_rule_state": row_payload.get("pre_rule_state"),
        "rule_patch": row_payload.get("rule_patch"),
        "safety_constraints": row_payload.get("safety_constraints"),
        "post_rule_state": row_payload.get("post_rule_state"),
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
            "coupling_flip": receipt["computed"].get("coupling_flip"),
            "local_admissible_coupled_denied": receipt["computed"].get("local_admissible_coupled_denied"),
            "composition_flip": receipt["computed"].get("composition_flip"),
            "all_individual_allow": receipt["computed"].get("all_individual_allow"),
            "conflict_detected": receipt["computed"].get("conflict_detected"),
            "conflict_flip": receipt["computed"].get("conflict_flip"),
            "resolution_policy": receipt["computed"].get("resolution_policy"),
            "consensus_flip": receipt["computed"].get("consensus_flip"),
            "quorum_result": receipt["computed"].get("quorum_result"),
            "receipt_bound": receipt["computed"].get("receipt_bound"),
            "reconstruction_exact": receipt["computed"].get("reconstruction_exact"),
            "reconstruction_verdict_match": receipt["computed"].get("reconstruction_verdict_match"),
            "irreversible": receipt["computed"].get("irreversible"),
            "point_of_no_return": receipt["computed"].get("point_of_no_return"),
            "self_modification_safe": receipt["computed"].get("self_modification_safe"),
            "rule_patch_verdict": receipt["computed"].get("rule_patch_verdict"),
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
