#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'data' / 'stegmusic-library.json'
RUNTIME = ROOT / 'assets' / 'ecosystem-music-library.js'
LOADER = ROOT / 'assets' / 'ecosystem-music-transition.js'

failures: list[str] = []

if not MANIFEST.exists():
    failures.append('missing data/stegmusic-library.json')
else:
    try:
        data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    except json.JSONDecodeError as error:
        failures.append(f'library manifest invalid JSON: {error}')
        data = {}

    if data.get('schema_version') != '1.0.0':
        failures.append('schema_version must be 1.0.0')
    if data.get('authority') != 'none':
        failures.append('library authority must remain none')
    if 'does not establish ownership' not in str(data.get('rights_boundary', '')).lower():
        failures.append('rights boundary must separate indexing from ownership')

    collections = data.get('collections', [])
    tracks = data.get('tracks', [])
    collection_ids = [entry.get('id') for entry in collections if isinstance(entry, dict)]
    track_ids = [entry.get('id') for entry in tracks if isinstance(entry, dict)]

    if len(collection_ids) < 4 or len(set(collection_ids)) != len(collection_ids):
        failures.append('collections must contain at least four unique IDs')
    if len(track_ids) < 12 or len(set(track_ids)) != len(track_ids):
        failures.append('tracks must contain at least twelve unique IDs')

    playable = 0
    profiles = 0
    for track in tracks:
        if not isinstance(track, dict):
            failures.append('every track must be an object')
            continue
        missing = [field for field in ('id','title','artist','collection_ids','genres','moods','tags','bpm','playable','source_class','rights_status','identifier_status','library_state') if field not in track]
        if missing:
            failures.append(f"{track.get('id','unknown')} missing fields: {', '.join(missing)}")
        unknown_collections = set(track.get('collection_ids', [])) - set(collection_ids)
        if unknown_collections:
            failures.append(f"{track.get('id','unknown')} references unknown collections: {sorted(unknown_collections)}")
        if track.get('playable'):
            playable += 1
            if not isinstance(track.get('runtime_index'), int):
                failures.append(f"{track.get('id','unknown')} playable entry requires integer runtime_index")
            if track.get('library_state') != 'active':
                failures.append(f"{track.get('id','unknown')} playable entry must be active")
        else:
            profiles += 1
            if track.get('runtime_index') is not None:
                failures.append(f"{track.get('id','unknown')} non-playable entry must have null runtime_index")
            if track.get('identifier_status') != 'not_rendered':
                failures.append(f"{track.get('id','unknown')} non-playable entry must be not_rendered")

    if playable < 3:
        failures.append('library requires at least three playable entries')
    if profiles < 6:
        failures.append('library requires at least six honest generation profiles')

required_markers = {
    RUNTIME: [
        'music_library_loaded', 'music_library_track_selected', 'music_library_favorite_changed',
        'data/stegmusic-library.json', 'GENERATION PROFILE', 'NOT YET RENDERED',
        "authority:'none'", 'stegmusic.library.favorites.v1'
    ],
    LOADER: ['assets/ecosystem-music-library.js', 'data-stegmusic-library', 'loadLibrary']
}
for path, markers in required_markers.items():
    if not path.exists():
        failures.append(f'missing {path.relative_to(ROOT)}')
        continue
    text = path.read_text(encoding='utf-8')
    for marker in markers:
        if marker not in text:
            failures.append(f'{path.relative_to(ROOT)} missing marker: {marker}')

if failures:
    print('STEGMUSIC_LIBRARY_FAIL')
    for failure in failures:
        print(f'- {failure}')
    sys.exit(1)

print('STEGMUSIC_LIBRARY_PASS')
print('library_entries>=12')
print('collections>=4')
print('playable_entries>=3')
print('generation_profiles>=6')
print('authority_effect=NONE')
