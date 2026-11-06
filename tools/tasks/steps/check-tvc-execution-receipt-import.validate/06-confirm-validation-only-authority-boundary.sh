python3 - <<'PY'
from pathlib import Path
workflow = Path('tools/tasks/folded/check-tvc-execution-receipt-import.yml').read_text(encoding='utf-8')
forbidden = [
    'actions/' + 'checkout@',
    'actions/' + 'setup-python@',
    'actions/' + 'upload-artifact@',
    'persist-' + 'credentials',
    'git ' + 'push',
    'contents:' + ' write',
    'issues:' + ' write',
    'pull-requests:' + ' write',
    'TVC_EPHEMERAL_GITHUB_TOKEN' + ':',
    'STEGVERSE_PROVIDER_TOKEN' + ':',
]
assert 'permissions: {}' in workflow
assert 'Refuse credential-bearing environment' in workflow
assert 'Fetch exact Site source anonymously' in workflow
assert all(marker not in workflow for marker in forbidden), forbidden
print('TVC_RECEIPT_IMPORT_VALIDATION_ONLY=PASS')
print('TVC_RECEIPT_IMPORT_REPOSITORY_WRITEBACK=NONE')
print('TVC_RECEIPT_IMPORT_ARTIFACT_CUSTODY=NONE')
print('TVC_RECEIPT_IMPORT_RUNTIME_AUTHORITY=NONE')
print('TVC_RECEIPT_IMPORT_EXECUTION_GRANT_AUTHORITY=NONE')
PY
