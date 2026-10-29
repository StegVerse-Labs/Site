python3 - <<'PY'
from pathlib import Path
src=Path('assets/device-local-kv-installer.js').read_text(encoding='utf-8')
page=Path('device-kv-install.html').read_text(encoding='utf-8')
required=[
  'stegverse-device-local-kv-v1',
  'device-local-browser-indexeddb',
  '_System/Instances/instance.json',
  '_System/installation.receipt.json',
  '_System/my-kv-set-projection.json',
  'NOT_CONNECTED',
  'provider_operation_authorized:false',
  'relationship_mutation_authorized:false',
  'authority_effect:"NONE"',
  'activation_effect:false',
  'exact_readback_verified:true',
]
missing=[x for x in required if x not in src]
if missing: raise SystemExit('missing installer markers: '+', '.join(missing))
if 'stegverse-device-local-intr-v1' in src:
  raise SystemExit('device-local KV must not reuse DEVICE_KV transport database')
page_required=['Create browser-local KV','not a durable/native installation','assets/device-local-kv-installer.js']
missing=[x for x in page_required if x not in page]
if missing: raise SystemExit('missing page markers: '+', '.join(missing))
print('DEVICE_LOCAL_KV_BROWSER_INITIALIZATION=PASS')
print('DEVICE_LOCAL_KV_AND_DEVICE_KV_TRANSPORT=SEPARATE')
print('CLOUD_PROVIDER_AUTHORITY=NONE')
PY
