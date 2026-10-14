#!/usr/bin/env python3
"""Deterministic tests for the one-attempt HIL public page proof (no network)."""
from __future__ import annotations

import inspect

import hil_public_page_proof as proof

SOURCES = {path: f"<html>{path}</html>".encode() for path in proof.SURFACES}


def read(commit: str, path: str) -> bytes | None:
    return SOURCES.get(path)


def serving(overrides: dict | None = None, calls: list | None = None):
    def get(url: str):
        if calls is not None:
            calls.append(url)
        path = url[len(proof.BASE_URL):].split("?", 1)[0]
        return (overrides or {}).get(path, (200, SOURCES[path]))
    return get


def main() -> None:
    calls: list[str] = []
    passed = proof.prove("abc", {}, get=serving(calls=calls), read=read)
    assert passed["result"] == "PASS", passed
    assert passed["attempts"] == 1 and len(calls) == len(proof.SURFACES), calls
    assert all(entry["served_bytes_match_source"] for entry in passed["surfaces"])
    assert "failure_code" not in passed and passed["authority_effect"] is False

    calls.clear()
    unchanged = proof.prove("def", passed, get=serving(calls=calls), read=read)
    assert unchanged["result"] == "NO_TRANSITION" and calls == [], (unchanged, calls)

    resume = proof.SURFACES[1]
    stale = proof.prove("ghi", {}, get=serving({resume: (200, b"old bytes")}), read=read)
    assert stale["result"] == "FAIL_CLOSED" and stale["failure_code"] == "HIL_PUBLIC_SURFACE_BYTES_DIFFER", stale
    for field in ("failure_code", "failed_predicate", "required_evidence_or_repair", "retry_entrypoint", "owning_existing_goal", "next_attempt"):
        assert stale.get(field), field
    assert stale["retry_entrypoint"] == proof.WORKFLOW and stale["owning_existing_goal"] == proof.OWNING_GOAL

    unserved = proof.prove("jkl", {}, get=serving({proof.SURFACES[0]: (0, b"")}), read=read)
    assert unserved["failure_code"] == "HIL_PUBLIC_SURFACE_NOT_SERVED", unserved
    assert proof.prove("mno", stale, get=serving(), read=read)["result"] == "PASS", "a FAIL_CLOSED record never short-circuits"

    # Repeating the same failure does not rewrite the record, so a proof commit cannot re-trigger itself.
    again = proof.prove("ghi", stale, get=serving({resume: (200, b"old bytes")}), read=read)
    assert proof.same_outcome(stale, again)

    source = inspect.getsource(proof)
    for forbidden in ("time.sleep", "while True", "for attempt"):
        assert forbidden not in source, forbidden
    print("HIL_PUBLIC_PAGE_PROOF_TESTS=PASS")


if __name__ == "__main__":
    main()
