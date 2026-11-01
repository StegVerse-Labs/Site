from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts/check_mr_sv001_intr_governance.py"


def test_mr_sv001_intr_governance_source_contract():
    # The check is a wrapper that runs its implementation as __main__, which exits; run it as a process.
    result = subprocess.run([sys.executable, str(CHECK)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "MR_SV001_INTR_GOVERNANCE_PASS" in result.stdout
