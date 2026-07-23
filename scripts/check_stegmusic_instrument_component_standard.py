#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "STEGMUSIC_INSTRUMENT_COMPONENT_STANDARD.md"
DATA = ROOT / "data" / "stegmusic" / "instrument-component-standard.v1.json"
RUNTIME = ROOT / "assets" / "stegmusic-instrument-physics.js"

required_doc = [
    "all musical instrument and performance-tool classes",
    "Aerophones and air-path components",
    "Reed components",
    "Lip-reed interfaces",
    "Membranophones",
    "Idiophones",
    "Electroacoustic and electronic components",
    "Excitation and maintenance tools",
    "bounded stochastic degradation or failure hazard",
    "component realism != performance tradition",
    "Site fixture != production synthesis activation",
]
required_classes = {
    "tensioned_linear",
    "air_path",
    "reed",
    "lip_reed_interface",
    "membrane",
    "idiophone",
    "resonator",
    "electroacoustic",
    "excitation_tool",
    "maintenance_and_test_tool",
}
required_runtime = [
    "StegMusicInstrumentPhysics",
    "createComponent",
    "failureHazard",
    "sampleFailure",
    "repair",
    "recalibrate",
    "componentClasses",
    "authority: 'none'",
]

failures = []
for path in (DOC, DATA, RUNTIME):
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")

if not failures:
    doc = DOC.read_text(encoding="utf-8")
    failures.extend(f"missing doc marker: {marker}" for marker in required_doc if marker not in doc)

    payload = json.loads(DATA.read_text(encoding="utf-8"))
    classes = set(payload.get("component_classes", {}))
    missing_classes = sorted(required_classes - classes)
    if missing_classes:
        failures.append(f"missing component classes: {', '.join(missing_classes)}")
    if payload.get("authority") != "none":
        failures.append("machine record authority must be none")
    if payload.get("component_classes", {}).get("tensioned_linear", {}).get("canonical_dependency") != "data/stegmusic/string-component-standard.v1.json":
        failures.append("string standard dependency is not canonical")

    runtime = RUNTIME.read_text(encoding="utf-8")
    failures.extend(f"missing runtime marker: {marker}" for marker in required_runtime if marker not in runtime)

if failures:
    print("STEGMUSIC_INSTRUMENT_COMPONENT_STANDARD_FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("STEGMUSIC_INSTRUMENT_COMPONENT_STANDARD_PASS")
print("scope=all_instrument_and_tool_classes")
print("classes=tensioned_linear_air_path_reed_lip_reed_membrane_idiophone_resonator_electroacoustic_tools")
print("failure=bounded_stochastic_state_derived")
print("continuity=repair_recalibration_residual_instability")
print("authority=none")
