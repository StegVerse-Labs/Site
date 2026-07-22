#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'data'/'stegmusic-library.json'
RUNTIME=ROOT/'assets'/'ecosystem-music.js'
EXPECTED={
 'stegdj-night-drive':(0,96),
 'stegdj-low-orbit':(1,78),
 'stegdj-signal-rise':(2,112),
 'stegdj-black-glass':(3,104),
 'stegdj-slow-telemetry':(4,72),
 'stegdj-redline-signal':(5,124),
}
def fail(message:str)->int:
 print(f'STEGMUSIC_RENDERED_LIBRARY_FAIL: {message}')
 return 1
def main()->int:
 if not MANIFEST.exists() or not RUNTIME.exists(): return fail('required files missing')
 try: payload=json.loads(MANIFEST.read_text(encoding='utf-8'))
 except Exception as error: return fail(f'manifest invalid: {error}')
 tracks={track.get('id'):track for track in payload.get('tracks',[])}
 runtime=RUNTIME.read_text(encoding='utf-8')
 if payload.get('authority')!='none': return fail('library authority must remain none')
 for track_id,(index,bpm) in EXPECTED.items():
  track=tracks.get(track_id)
  if not track: return fail(f'missing {track_id}')
  if track.get('playable') is not True: return fail(f'{track_id} not playable')
  if track.get('runtime_index')!=index: return fail(f'{track_id} runtime index mismatch')
  if track.get('bpm')!=bpm: return fail(f'{track_id} bpm mismatch')
  if track.get('library_state')!='active': return fail(f'{track_id} not active')
  if track.get('identifier_status')!='fingerprint_candidate': return fail(f'{track_id} identifier posture mismatch')
  for marker in (track_id, f"bpm:{bpm}"):
   if marker not in runtime: return fail(f'runtime missing marker {marker}')
 playable=[track for track in tracks.values() if track.get('playable')]
 profiles=[track for track in tracks.values() if not track.get('playable')]
 if len(playable)<6: return fail('fewer than six playable tracks')
 if len(profiles)<6: return fail('fewer than six honest generation profiles remain')
 for track in profiles:
  if track.get('runtime_index') is not None: return fail(f"profile {track.get('id')} has runtime index")
  if track.get('identifier_status')!='not_rendered': return fail(f"profile {track.get('id')} identifier status inflated")
 for marker in ('getTrackCount:()=>tracks.length','getTracks:()=>tracks.map'):
  if marker not in runtime: return fail(f'runtime missing introspection marker {marker}')
 print('STEGMUSIC_RENDERED_LIBRARY_PASS')
 print(f'playable_count={len(playable)}')
 print(f'generation_profile_count={len(profiles)}')
 print('authority_effect=NONE')
 return 0
if __name__=='__main__': raise SystemExit(main())
