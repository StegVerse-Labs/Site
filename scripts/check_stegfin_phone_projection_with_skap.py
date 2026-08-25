#!/usr/bin/env python3
from __future__ import annotations

import re, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'stegfin-trade.html'
LEGACY=ROOT/'scripts/check_stegfin_phone_projection.py'
SKAP='./assets/stegfin-phone/coinbase-skap-ingress.js'
SKAP_UI='./assets/stegfin-phone/coinbase-skap-ingress-ui.js'


def require(ok: bool, msg: str):
    if not ok: raise SystemExit('STEGFIN_PHONE_SKAP_EXTENSION_FAIL:'+msg)


def main() -> int:
    original=PAGE.read_text(encoding='utf-8')
    scripts=re.findall(r'<script\s+src="([^"]+)"',original)
    expected=[
      './assets/stegfin-phone/rpc-resilience.js',
      './assets/stegfin-phone/phone-direct-route.js',
      './assets/stegfin-phone/stegid-device-wallet-bootstrap.js',
      './assets/stegfin-phone/device-wallet-identity.js',
      SKAP, SKAP_UI,
      './assets/stegfin-phone/app.js',
      './assets/stegfin-phone/evidence-export.js',
    ]
    require(scripts==expected,f'unexpected extended script order: {scripts}')
    ingress=(ROOT/'assets/stegfin-phone/coinbase-skap-ingress.js').read_text(encoding='utf-8')
    for marker in (
      "config?.private_key_liveness_required !== true",
      "config.lease_expires_at",
      "lease <= Date.now()",
      "recipient_public_jwk_sha256 !== await sha256(config.recipient_public_jwk)",
      "credential_custody_target !== 'SKAP'",
      "transport_protocol !== 'InTr'",
      "private_key_present !== false",
      "recipient_runtime_instance_id: config.runtime_instance_id",
      "recipient_lease_expires_at: config.lease_expires_at",
    ):
        require(marker in ingress,'missing SKAP ingress invariant: '+marker)
    require("'d' in config.recipient_public_jwk" in ingress,'public-only recipient JWK check missing')

    # Preserve the legacy checker exactly: remove only the two explicitly validated
    # SKAP extension script tags from a temporary working copy, then run every
    # historical exact projection check unchanged.
    normalized=original
    for src in (SKAP,SKAP_UI):
        normalized=re.sub(rf'\s*<script\s+src="{re.escape(src)}"[^>]*></script>', '', normalized, count=1)
    PAGE.write_text(normalized,encoding='utf-8')
    try:
        completed=subprocess.run(['python3',str(LEGACY)],cwd=ROOT,check=False)
        require(completed.returncode==0,'legacy phone projection checker failed')
    finally:
        PAGE.write_text(original,encoding='utf-8')
    print('STEGFIN_PHONE_SKAP_EXTENSION_PASS')
    return 0

if __name__=='__main__': raise SystemExit(main())
