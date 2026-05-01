#!/usr/bin/env python3
"""
Server-side GCAT/BCAT evaluation for CI pipeline.
Mirrors the client-side JS logic for verification.
"""

import argparse
import json
import hashlib
import math


def vec_add(a, b): return [v + b[i] for i, v in enumerate(a)]
def vec_sub(a, b): return [v - b[i] for i, v in enumerate(a)]
def vec_norm(a): return math.sqrt(sum(v * v for v in a))
def vec_scale(a, s): return [v * s for v in a]
def vec_dist(a, b): return vec_norm(vec_sub(a, b))


def reconstruct_boundary(commit_states, tolerance=1e-9):
    dims = len(commit_states[0])
    n = len(commit_states)
    centroid = [sum(s[i] for s in commit_states) / n for i in range(dims)]
    radius = max(vec_dist(s, centroid) for s in commit_states)
    radius = max(radius, tolerance)
    return {"centroid": centroid, "radius": radius, "tolerance": tolerance, "dims": dims}


def compute_god(proposed, boundary, scale=None):
    d = vec_dist(proposed, boundary["centroid"])
    s = scale or boundary["radius"]
    return d / s


def evaluate(proposed, boundary, epsilon=0.05):
    god = compute_god(proposed, boundary)
    if god <= 1.0:
        verdict = "ALLOW"
        confidence = 1.0 - god
    elif god <= 1.0 + epsilon:
        verdict = "DENY"
        confidence = 1.0 - ((god - 1.0) / epsilon)
    else:
        verdict = "FAIL-CLOSED"
        confidence = 0.0
    return {
        "verdict": verdict,
        "god": god,
        "confidence": max(0, min(1, confidence)),
        "boundary": boundary
    }


def generate_receipt(inputs, result):
    canonical = json.dumps({
        "v": "0.1.0",
        "source": inputs.get("source", "unknown"),
        "demo_id": inputs.get("demo_id"),
        "commit_states": inputs["commit_states"],
        "proposed_state": inputs["proposed_state"],
        "verdict": result["verdict"],
        "god": result["god"],
        "confidence": result["confidence"],
        "boundary_centroid": result["boundary"]["centroid"],
        "boundary_radius": result["boundary"]["radius"],
        "boundary_epsilon": 0.05
    }, separators=(',', ':'))
    return {
        "hash": hashlib.sha256(canonical.encode()).hexdigest(),
        "algo": "SHA-256",
        "canonical": canonical
    }


def run(inputs):
    boundary = reconstruct_boundary(inputs["commit_states"])
    result = evaluate(inputs["proposed_state"], boundary)
    receipt = generate_receipt(inputs, result)
    return {
        **result,
        "receipt": receipt,
        "inputs": {
            "source": inputs.get("source"),
            "commit_count": len(inputs["commit_states"]),
            "dimensions": boundary["dims"]
        }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.input) as f:
        inputs = json.load(f)

    result = run(inputs)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Evaluated: {args.output}")
    print(f"  Verdict: {result['verdict']}")
    print(f"  GOD: {result['god']:.6f}")
    print(f"  Confidence: {result['confidence']:.4f}")
    print(f"  Receipt: {result['receipt']['hash'][:16]}...")


if __name__ == "__main__":
    main()
