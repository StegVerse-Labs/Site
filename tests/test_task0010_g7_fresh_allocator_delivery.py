from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "stegos-node" / "org-allocator-bootstrap-task0010-g7-v1.html"
SW = ROOT / "stegos-node" / "service-worker.js"


def test_fresh_entrypoint_rejects_pre_repair_allocator_source_and_recovers_first():
    text = ENTRY.read_text(encoding="utf-8")
    assert 'const RELEASE="task0010-g7-v1-20260910"' in text
    assert 'org-allocator-bootstrap-task0010-g6-v2.html?delivery=' in text
    assert 'fetch(SOURCE,{cache:"no-store"' in text
    assert "auto-execution requires exactly one queued canonical successor" in text
    assert "stale pre-repair allocator source detected; execution refused" in text
    assert 'function alreadyExecuted()' in text
    assert 'TASK-2026-0010 already retained; no allocator mutation performed' in text
    assert 'result.receipt.queued.indexOf(EXPECTED_TASK)===-1' in text
    assert 'result.receipt.selected!==EXPECTED_TASK' in text
    assert 'allocator_mutation_performed:false' in text
    assert "document.write(text)" in text


def test_fresh_entrypoint_is_network_only_and_cache_lineage_advances():
    text = SW.read_text(encoding="utf-8")
    assert 'stegos-node-shell-v12-task0010-g7-fresh-delivery-v1' in text
    assert '"/stegos-node/org-allocator-bootstrap-task0010-g7-v1.html": true' in text
    assert '"/stegos-node/org-allocator-bootstrap-task0010-g6-v2.html": true' in text
    assert 'fetch(event.request, {cache: "no-store"})' in text
