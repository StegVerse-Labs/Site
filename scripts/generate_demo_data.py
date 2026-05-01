#!/usr/bin/env python3
"""
Generate deterministic demo run data for the StegVerse Tier 0 demo.
Produces JSON matching the client-side evaluator schema.
"""

import argparse
import json
import random
import sys


def generate_commit_states(seed, n=5, dims=3):
    rng = random.Random(seed)
    return [[rng.random() * 2 - 1 for _ in range(dims)] for _ in range(n)]


def generate_proposed(source, commit_states, seed):
    rng = random.Random(seed + 1000)
    centroid = [sum(s[i] for s in commit_states) / len(commit_states) for i in range(3)]
    anchor = commit_states[0]
    scale = max(
        sum((s[i] - centroid[i]) ** 2 for i in range(3)) ** 0.5
        for s in commit_states
    ) or 1e-9

    if source == "sdk":
        # Deep inside → ALLOW (GOD ~0.3)
        proposed = [centroid[i] + (anchor[i] - centroid[i]) * 0.3 for i in range(3)]
    elif source == "llm_adapter":
        # Just outside, in epsilon zone → DENY (GOD ~1.02)
        direction = [anchor[i] - centroid[i] for i in range(3)]
        dnorm = sum(x ** 2 for x in direction) ** 0.5
        unit = [x / dnorm for x in direction] if dnorm > 1e-9 else [1, 0, 0]
        proposed = [centroid[i] + unit[i] * scale * 1.02 for i in range(3)]
    else:
        # Far outside → FAIL-CLOSED (GOD ~2.0)
        direction = [anchor[i] - centroid[i] for i in range(3)]
        dnorm = sum(x ** 2 for x in direction) ** 0.5
        unit = [x / dnorm for x in direction] if dnorm > 1e-9 else [1, 0, 0]
        proposed = [centroid[i] + unit[i] * scale * 2.0 for i in range(3)]

    return proposed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, choices=["sdk", "llm_adapter", "human"])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--demo-id", default="")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    commit_states = generate_commit_states(args.seed)
    proposed = generate_proposed(args.source, commit_states, args.seed)

    data = {
        "source": args.source,
        "demo_id": args.demo_id or f"demo_{args.source}_{args.seed}",
        "commit_states": commit_states,
        "proposed_state": proposed,
        "metadata": {
            "generated_by": "generate_demo_data.py",
            "tier": 0,
            "deterministic": True,
            "seed": args.seed,
            "github_run": True
        }
    }

    with open(args.output, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Generated: {args.output}")
    print(f"  Source: {args.source}")
    print(f"  Commits: {len(commit_states)}")
    print(f"  Dimensions: {len(commit_states[0])}")


if __name__ == "__main__":
    main()
