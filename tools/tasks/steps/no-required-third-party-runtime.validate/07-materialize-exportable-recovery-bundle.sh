set -euo pipefail
python3 scripts/materialize_site_recovery_bundle.py --output build/site-recovery-bundle
python3 - <<'PY'
from pathlib import Path
import hashlib, json, os, zipfile
root = Path('build/site-recovery-bundle')
source_commit = os.environ['STEGVERSE_SITE_SOURCE_COMMIT']
out = Path('build') / f'StegVerse-Site-recovery-{source_commit}.zip'
with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(root.rglob('*')):
        if path.is_file():
            archive.write(path, path.relative_to(root).as_posix())
digest = hashlib.sha256(out.read_bytes()).hexdigest()
manifest_digest = hashlib.sha256((root / 'manifest.json').read_bytes()).hexdigest()
metadata = {
    'schema': 'stegverse.site.recovery_bundle_export.v1',
    'source_commit': source_commit,
    'archive': out.name,
    'archive_sha256': digest,
    'archive_bytes': out.stat().st_size,
    'manifest_sha256': manifest_digest,
    'transport_role': 'SHORT_LIVED_VALIDATION_EXPORT_ONLY',
    'external_retention_proven': False,
    'off_github_restore_proven': False,
}
Path('build/site-recovery-bundle-export.json').write_text(json.dumps(metadata, indent=2, sort_keys=True) + '\n', encoding='utf-8')
print('SITE_RECOVERY_EXPORT=' + str(out))
print('SITE_RECOVERY_EXPORT_SHA256=' + digest)
print('SITE_RECOVERY_MANIFEST_SHA256=' + manifest_digest)
PY
