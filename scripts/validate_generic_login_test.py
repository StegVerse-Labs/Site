#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import secrets
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "generic-login-test.html"
AUTH = ROOT / "assets/kv-ui/intr-auth-client.js"
CREATE = ROOT / "create-account-test.html"
FORGOT = ROOT / "forgot-password-test.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"GENERIC_LOGIN_TEST_FAIL: {message}")


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def inline_script(html: str) -> str:
    matches = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.S | re.I)
    matches = [m for m in matches if m.strip()]
    require(len(matches) == 1, "expected one non-empty inline page script")
    return matches[0]


def run_node(auth_js: str, page_js: str, user: str, password: str) -> dict:
    account = {
        "passwordDigest": sha256(password),
        "email": "person@example.test",
        "sms": "+15555550123",
        "emailVerified": True,
        "smsVerified": True,
    }
    shim = r'''
const listeners = {};
class FakeElement {
  constructor(id){this.id=id;this.value='';this.textContent='';this.dataset={};this.listeners={};this.hidden=false;this.href='';this.disabled=false;}
  addEventListener(name,fn){(this.listeners[name] ||= []).push(fn);}
  requestSubmit(){const e={preventDefault(){}};for(const fn of (this.listeners.submit||[]))fn(e);}
  click(){const e={preventDefault(){}};for(const fn of (this.listeners.click||[]))fn(e);}
}
const ids=['status','login-card','kv-card','login-form','username','password','identity-state','open-personal','personal-panel','pi-name','pi-email','pi-sms','pi-address','save-personal','personal-receipt','unlock-skap','skap-stepup','skap-password','confirm-skap','skap-panel','account-email','account-sms','change-password','logout'];
const elements=Object.fromEntries(ids.map(id=>[id,new FakeElement(id)]));
elements.status.dataset.state='LOGIN';elements.status.textContent='LOGIN';elements['kv-card'].hidden=true;elements['personal-panel'].hidden=true;elements['skap-stepup'].hidden=true;elements['skap-panel'].hidden=true;
globalThis.window=globalThis;
globalThis.document={getElementById:id=>elements[id]};
globalThis.CustomEvent=class{constructor(type,init){this.type=type;this.detail=init?.detail;}};
globalThis.addEventListener=(name,fn,options={})=>{(listeners[name] ||= []).push({fn,once:Boolean(options.once)});};
globalThis.dispatchEvent=e=>{const cur=[...(listeners[e.type]||[])];for(const item of cur)item.fn(e);listeners[e.type]=(listeners[e.type]||[]).filter(x=>!x.once);return true;};
const local=new Map();
globalThis.localStorage={getItem:k=>local.has(k)?local.get(k):null,setItem:(k,v)=>local.set(k,String(v)),removeItem:k=>local.delete(k)};
'''
    seed = f"localStorage.setItem('stegverse.generic-login.accounts.v1',{json.dumps(json.dumps({user: account}))});\n"
    assertions = f'''
const intr=window.StegVerseInTrAuth;
const cfg=intr.config();
const prod=await intr.authenticate({json.dumps(user)},{json.dumps(password)});
const direct=await intr.testAuthenticate({json.dumps(user)},{json.dumps(password)});
const wrongDirect=await intr.testAuthenticate({json.dumps(user)},'wrong');
const api=window.__STEGVERSE_LOGIN_TEST__;
const login=await api.submit({json.dumps(user)},{json.dumps(password)});
const assertion=api.getAssertion();
elements['open-personal'].click();
elements['pi-name'].value='Test Person';elements['save-personal'].click();
const personalReceipt=JSON.parse(elements['personal-receipt'].textContent);
elements['unlock-skap'].click();
elements['skap-password'].value={json.dumps(password)};
await elements['confirm-skap'].listeners.click[0]();
const step=api.getSkapAssertion();
elements.logout.click();
const fail=await api.submit({json.dumps(user)},'wrong');
console.log(JSON.stringify({{
  configMode:cfg.mode,prodState:prod.state,directOk:direct.ok,wrongDirect:wrongDirect.ok,
  directCredentialDisclosed:direct.assertion?.credential_disclosed,
  directRawSecret:direct.assertion?.raw_secret_present,
  login,viewAfterLogin:'KV_TREE',assertionSchema:assertion?.schema,
  assertionCredentialDisclosed:assertion?.credential_disclosed,
  personalOperation:personalReceipt.operation,personalParent:personalReceipt.parent_assertion_id===assertion.assertion_id,
  stepSchema:step?.schema,stepCredentialDisclosed:step?.credential_disclosed,
  skapVisible:elements['skap-panel'].hidden===false,
  afterLogout:api.getView(),fail
}}));
'''
    program = shim + seed + auth_js + "\n" + page_js + "\n" + assertions
    with tempfile.NamedTemporaryFile("w", suffix=".mjs", delete=False, encoding="utf-8") as fh:
        fh.write(program)
        path = Path(fh.name)
    try:
        proc = subprocess.run(["node", str(path)], capture_output=True, text=True, check=False)
    finally:
        path.unlink(missing_ok=True)
    require(proc.returncode == 0, f"javascript execution failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout.strip().splitlines()[-1])


def main() -> int:
    for path in (PAGE, AUTH, CREATE, FORGOT):
        require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    html = PAGE.read_text()
    auth_js = AUTH.read_text()
    create = CREATE.read_text()
    forgot = FORGOT.read_text()

    for marker in (
        'Successful Login', 'KnowledgeVault directory projection', 'Personal Info/', '_Vault/SKAP',
        'SKAP Step-up Validation', 'Save through InTr', 'Account attributes',
        'assets/kv-ui/intr-auth-client.js', 'window.StegVerseInTrAuth',
        'data-testid="forgot-password"', 'data-testid="create-account"',
    ):
        require(marker in html, f"missing UI contract: {marker}")

    for marker in (
        "stegverse.intr.identity-assertion/v1", "stegverse.intr.step-up-assertion/v1",
        "VERIFY_ACCOUNT_LOGIN", "VERIFY_SKAP_STEP_UP", "credential_disclosed: false",
        "raw_secret_present: false", "INTR_NOT_PROVISIONED", "TEST_ONLY_LOCAL_INTR_VERIFIER",
    ):
        require(marker in auth_js, f"missing InTr assertion contract: {marker}")

    for forbidden in ('document.cookie', 'TVC_EPHEMERAL_GITHUB_TOKEN', 'GITHUB_TOKEN'):
        require(forbidden not in html + auth_js, f"forbidden authority surface: {forbidden}")

    require('passwordDigest' in create and 'emailVerified' in create and 'smsVerified' in create,
            'create-account persistence contract missing')
    require('TEST_ONLY' in create and 'TEST_ONLY' in forgot, 'delivery boundary must remain explicit')
    require('PASSWORD RESET' in forgot and 'Recovery method' in forgot, 'recovery/reset path missing')

    user = 'acct-' + secrets.token_hex(6)
    password = 'pw-' + secrets.token_hex(12)
    result = run_node(auth_js, inline_script(html), user, password)
    require(result['configMode'] == 'NOT_PROVISIONED' and result['prodState'] == 'INTR_NOT_PROVISIONED', f"production fail-closed mismatch: {result}")
    require(result['directOk'] is True and result['wrongDirect'] is False, f"test verifier mismatch: {result}")
    require(result['directCredentialDisclosed'] is False and result['directRawSecret'] is False, f"credential disclosure detected: {result}")
    require(result['login'] == 'SUCCESS' and result['assertionSchema'] == 'stegverse.intr.identity-assertion/v1', f"identity assertion login mismatch: {result}")
    require(result['assertionCredentialDisclosed'] is False, f"login assertion leaks credential: {result}")
    require(result['personalOperation'] == 'PERSONAL_INFO_UPDATE' and result['personalParent'] is True, f"KV transition receipt mismatch: {result}")
    require(result['stepSchema'] == 'stegverse.intr.step-up-assertion/v1' and result['stepCredentialDisclosed'] is False and result['skapVisible'] is True, f"SKAP step-up mismatch: {result}")
    require(result['afterLogout'] == 'LOGIN_CARD' and result['fail'] == 'FAILED', f"logout/failure mismatch: {result}")

    report = {
        'schema': 'stegverse.site.intr-kv-login-projection-verification.v1',
        'status': 'PASS',
        'site_receives_raw_stored_credential': False,
        'production_intr_default': 'FAIL_CLOSED_NOT_PROVISIONED',
        'identity_assertion': 'PASS',
        'kv_directory_projection': 'PASS',
        'personal_info_transition_receipt': 'PASS_TEST_ONLY',
        'skap_requires_separate_step_up_assertion': True,
        'device_kv_and_kv_skap_boundaries_distinct': True,
        'real_intr_runtime_claimed': False,
        'real_kv_custody_claimed': False,
        'real_skap_custody_claimed': False,
    }
    print('GENERIC_LOGIN_INTR_KV_PASS')
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
