python3 - <<'PY'
import json
from pathlib import Path
cfg=json.loads(Path('assets/stegfin-phone/coinbase-skap-ingress-config.json').read_text())
route=json.loads(Path('assets/stegfin-phone/coinbase-skap-intr-route.json').read_text())
assert cfg['activation_effect'] == 'NONE'
assert cfg['credential_authority'] == 'TV/TVC'
assert cfg['physical_execution_surface'] == 'CURRENT_USER_IPHONE'
assert cfg['second_machine_required'] is False
assert cfg['github_environment_secret_access'] is False
assert route['status'] == 'NOT_PROVISIONED'
assert route['credential_authority'] == 'TV/TVC'
assert route['credential_custody_target'] == 'SKAP'
assert route['public_route_authority'] is False
assert route['provider_operation_authorized'] is False
assert route['credential_plaintext_carried'] is False
assert route['github_token_runtime_authority'] is False
assert route['public_origin'] is None
print('SITE_COINBASE_SKAP_INGRESS_VALIDATION_ONLY=true')
print('SITE_COINBASE_SKAP_INTR_ROUTE=NOT_PROVISIONED')
print('production_execution_authority=NONE')
PY
