#!/usr/bin/env python3
from pathlib import Path

impl = Path(__file__).with_name("check_stegos_node_projection_impl.py")
source = impl.read_text(encoding="utf-8")
source = source.replace('ROOT / "stegos-node" / "stegos-node.js"', 'ROOT / "stegos-node" / "stegos-node-impl.js"')
namespace = {"__name__": "__main__", "__file__": str(impl)}
exec(compile(source, str(impl), "exec"), namespace)
