#!/usr/bin/env python3
from pathlib import Path

impl = Path(__file__).with_name("check_mr_sv001_intr_governance_impl.py")
source = impl.read_text(encoding="utf-8")
source = source.replace('ROOT / "stegos-bootstrap/stegos-bootstrap.js"', 'ROOT / "stegos-bootstrap/stegos-bootstrap-impl.js"')
namespace = {"__name__": "__main__", "__file__": str(impl)}
exec(compile(source, str(impl), "exec"), namespace)
