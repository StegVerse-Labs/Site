#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'data' / 'stegmusic' / 'string-component-standard.v1.json'
RUNTIME = ROOT / 'assets' / 'stegmusic-string-physics.js'
DOC = ROOT / 'docs' / 'STEGMUSIC_STRING_COMPONENT_STANDARD.md'

failures: list[str] = []

for path in (SCHEMA, RUNTIME, DOC):
    if not path.exists():
        failures.append(f'missing file: {path.relative_to(ROOT)}')

if not failures:
    data = json.loads(SCHEMA.read_text(encoding='utf-8'))
    if data.get('schema_version') != '1.0.0': failures.append('schema version mismatch')
    if data.get('scope') != 'all_tensioned_musical_strings_and_string_like_linear_elements': failures.append('canonical scope mismatch')
    groups = data.get('canonical_attributes', {})
    required_groups = {'identity','construction','geometry','mechanical_state','tuning_state','attachment','environment','usage','condition','acoustics','failure','repair'}
    missing = sorted(required_groups - set(groups))
    if missing: failures.append('missing canonical groups: ' + ', '.join(missing))
    required_fields = {
        'material_family','speaking_length_mm','current_tension_n','breaking_load_n','target_frequency_hz',
        'temperature_c','age_hours','peak_excitation_force_n','bow_pressure_n','wear_ratio','fatigue_ratio',
        'notch_severity','fray_ratio','inharmonicity','hazard_score','break_transient_profile','repairability','reentry_stability'
    }
    flattened = {item for values in groups.values() for item in values}
    missing_fields = sorted(required_fields - flattened)
    if missing_fields: failures.append('missing canonical fields: ' + ', '.join(missing_fields))
    adapters = data.get('instrument_adapters', {})
    for name in ('plucked','bowed','struck','resonant_or_sympathetic','performance_tools'):
        if not adapters.get(name): failures.append(f'missing adapter class: {name}')
    boundaries = '\n'.join(data.get('required_boundaries', []))
    for marker in ('must not redefine canonical fields','remains stochastic','repair state must affect subsequent tuning and sound'):
        if marker not in boundaries: failures.append(f'missing boundary marker: {marker}')

if RUNTIME.exists():
    runtime = RUNTIME.read_text(encoding='utf-8')
    for marker in (
        'stegmusic-string-component-v1','createStringComponent','calculateFailureHazard','advanceStringState',
        'sampleFailure','registerInstrumentAdapter','exact_bar_locked: false','authority: \'none\''
    ):
        if marker not in runtime: failures.append(f'runtime missing marker: {marker}')

if DOC.exists():
    doc = DOC.read_text(encoding='utf-8')
    for marker in ('one string standard','Instrument adapters','Failure model','Repair continuity','shared schema != identical sound'):
        if marker not in doc: failures.append(f'document missing marker: {marker}')

if failures:
    print('STEGMUSIC_STRING_COMPONENT_STANDARD_FAIL')
    for failure in failures: print(f'- {failure}')
    sys.exit(1)

print('STEGMUSIC_STRING_COMPONENT_STANDARD_PASS')
print('scope=all_tensioned_musical_strings_and_string_like_linear_elements')
print('instrument_adapters=plucked,bowed,struck,sympathetic,performance_tools')
print('failure_timing=state_derived_stochastic')
print('authority=none')
