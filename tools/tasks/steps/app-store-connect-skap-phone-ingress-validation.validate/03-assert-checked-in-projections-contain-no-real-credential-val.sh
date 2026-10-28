python - <<'PY'
import json
from pathlib import Path
config=json.loads(Path('assets/stegos-apple/app-store-connect-skap-ingress-config.json').read_text())
route=json.loads(Path('assets/stegos-apple/app-store-connect-skap-intr-route.json').read_text())
assert config['status']=='NOT_PROVISIONED'
assert config['recipient_key_id'] is None
assert config['recipient_public_jwk'] is None
assert route['status']=='NOT_PROVISIONED'
assert route['public_ingress_url'] is None
print('checked_in_apple_credential_values=false')
PY
