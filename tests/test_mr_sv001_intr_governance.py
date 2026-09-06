from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts/check_mr_sv001_intr_governance.py"


def test_mr_sv001_intr_governance_source_contract():
    spec = importlib.util.spec_from_file_location("mr_sv001_intr_governance", CHECK)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    assert module.main() == 0
