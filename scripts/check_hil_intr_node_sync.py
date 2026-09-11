#!/usr/bin/env python3
from pathlib import Path

_impl = Path(__file__).with_name("check_hil_intr_node_sync_impl.py")
_source = _impl.read_text(encoding="utf-8")
_source = _source.replace('root / "stegos-node/stegos-node.js"', 'root / "stegos-node/stegos-node-impl.js"')
exec(compile(_source, str(_impl), "exec"), globals())
