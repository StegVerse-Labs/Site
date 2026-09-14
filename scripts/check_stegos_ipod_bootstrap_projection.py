#!/usr/bin/env python3
from pathlib import Path

impl = Path(__file__).with_name("check_stegos_ipod_bootstrap_projection_impl.py")
source = impl.read_text(encoding="utf-8")
source = source.replace('stegos-bootstrap/stegos-bootstrap.js', 'stegos-bootstrap/stegos-bootstrap-impl.js')
source = source.replace('stegos-bootstrap/sv001-native-resident-activation.js', 'stegos-bootstrap/sv001-native-resident-activation-impl.js')
source = source.replace(
    '"a27fb3d98f32924452da9b19921b9824d3d2a7c3"},',
    '"a27fb3d98f32924452da9b19921b9824d3d2a7c3", "7f869e3cda4fa2476da6891f720186a37ca41a44"},',
    1,
)
namespace = {"__name__": "__main__", "__file__": str(impl)}
exec(compile(source, str(impl), "exec"), namespace)
