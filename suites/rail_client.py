#!/usr/bin/env python3
"""Public read-only connection client. Never signs, transfers or registers.
Read the current rail's offer. A successful read is not an ALLOW crossing.
"""
import argparse
import json
import urllib.request

RAILS = {"8374": "https://8374.stegverse.org", "4LPH4": "https://4lph4.stegverse.org"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rail", choices=RAILS)
    parser.add_argument("--resource", choices=["offer", "health"], default="offer")
    args = parser.parse_args()
    url = RAILS[args.rail] + "/" + args.resource
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read(1024 * 1024 + 1)
            if len(data) > 1024 * 1024:
                raise ValueError("response exceeds bound")
            print(json.dumps({"source": url, "authority_effect": "NONE", "observation": json.loads(data)}, indent=2))
    except Exception:
        print(json.dumps({"failure_code": "RAIL_READ_UNAVAILABLE", "failed_predicate": "current public rail response",
            "required_evidence_or_repair": "Restore public rail reads; do not guess prices or admission.",
            "retry_entrypoint": url, "owning_goal": "Q-67", "next_attempt": "When the public read is available."}, indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
