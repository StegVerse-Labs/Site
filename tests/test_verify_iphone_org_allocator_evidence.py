from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/verify_iphone_org_allocator_evidence.py"

def load():
    spec=importlib.util.spec_from_file_location("verify_iphone_org_allocator_evidence",SCRIPT)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def test_verifier_targets_exact_task_and_surface():
    mod=load()
    assert mod.TARGET_TASK=="TASK-2026-0008"
    assert mod.TARGET_SURFACE=="site:stegos-de006-bound-inference-publication"

def test_verifier_requires_reconstructable_same_device_evidence():
    text=SCRIPT.read_text(encoding="utf-8")
    for marker in [
      "continued node receipts missing",
      "node/device binding receipt missing",
      "journal tail mismatch",
      "allocator receipt self-hash mismatch",
      "claim snapshot hash mismatch",
      "TASK-0008 dependency surface missing",
      "same_device_verified",
      "canonical_allocator_authority_verified",
    ]:
        assert marker in text
