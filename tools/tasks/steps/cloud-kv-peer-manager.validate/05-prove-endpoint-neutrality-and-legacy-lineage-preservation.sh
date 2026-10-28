python3 - <<'PY'
from pathlib import Path
legacy=Path('assets/cloud-kv-peer-manager.js').read_text(encoding='utf-8')
endpoint=Path('assets/kv-storage-endpoint-manager.js').read_text(encoding='utf-8')
page=Path('cloud-kv-peers.html').read_text(encoding='utf-8')
required=['device-local','icloud-drive','google-drive','onedrive','dropbox','nas','removable-storage','CREATE_KV_STORAGE_ENDPOINT','ADOPT_EXISTING_KV_STORAGE_ENDPOINT','normalizeLegacyV1','PENDING_INTERLOCK_INTR','NOT_CONNECTED']
missing=[x for x in required if x not in endpoint]
if missing: raise SystemExit('missing endpoint-v2 marker: '+', '.join(missing))
for marker in ['stegverse.site.cloud-kv-peer-create-request/v1','stegverse.site.cloud-kv-peer-adoption-request/v1','ADOPT_EXISTING_CLOUD_KV_PEER']:
  if marker not in legacy: raise SystemExit('legacy v1 contract changed or missing: '+marker)
if 'SITE-CLOUD-KV-4347408852127319cbda574f02e03edb' not in page:
  raise SystemExit('existing Google Drive KV #2 request lineage not retained in UI')
for marker in ['provider_operation_authorized:true','instance_materialized:true','relationship_mutation_authorized:true','data_moved:true','replication_started:true','ai_corpus_exposed:true']:
  if marker in endpoint or marker in page: raise SystemExit('prohibited runtime effect marker: '+marker)
print('KV_STORAGE_ENDPOINT_V2=PASS')
print('LEGACY_CLOUD_V1_COMPATIBILITY=PASS')
print('GOOGLE_DRIVE_KV2_LINEAGE_PRESERVED=PASS')
print('RUNTIME_AUTHORITY=NONE')
PY
