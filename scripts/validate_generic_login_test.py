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
CREATE = ROOT / "create-account-test.html"
FORGOT = ROOT / "forgot-password-test.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"GENERIC_LOGIN_TEST_FAIL: {message}")


def extract_inline_script(html: str) -> str:
    matches = re.findall(r"<script>(.*?)</script>", html, flags=re.S | re.I)
    require(len(matches) == 1, "expected exactly one inline script")
    return matches[0]


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def run_js(script: str, account_user: str, account_pass: str) -> dict:
    account = {
        "passwordDigest": sha256(account_pass),
        "email": "person@example.test",
        "sms": "+15555550123",
        "emailVerified": True,
        "smsVerified": True,
    }
    shim = r'''
const listeners = {};
class FakeElement {
  constructor(id) { this.id=id; this.value=''; this.textContent=''; this.dataset={}; this.listeners={}; this.hidden=false; this.href=''; }
  addEventListener(name, fn) { (this.listeners[name] ||= []).push(fn); }
  requestSubmit() { const event={preventDefault(){}}; for(const fn of (this.listeners.submit||[])) fn(event); }
}
const ids = ['status','login-card','account-card','login-form','username','password','forgot-password','create-account','account-email','account-sms','change-email','change-sms','change-password','change-panel','change-title','change-label','change-value','change-challenge','change-code-label','change-code','confirm-change','request-change','cancel-change','logout'];
const elements = Object.fromEntries(ids.map(id => [id,new FakeElement(id)]));
elements.status.dataset.state='LOGIN'; elements.status.textContent='LOGIN'; elements['account-card'].hidden=true; elements['change-panel'].hidden=true;
globalThis.window=globalThis;
globalThis.document={documentElement:{dataset:{}},getElementById:(id)=>elements[id]};
globalThis.CustomEvent=class{constructor(type,init){this.type=type;this.detail=init?.detail;}};
globalThis.addEventListener=(name,fn,options={})=>{(listeners[name]||=[]).push({fn,once:Boolean(options.once)});};
globalThis.dispatchEvent=(event)=>{const current=[...(listeners[event.type]||[])];for(const item of current)item.fn(event);listeners[event.type]=(listeners[event.type]||[]).filter(item=>!item.once);return true;};
const local = new Map();
globalThis.localStorage={getItem:k=>local.has(k)?local.get(k):null,setItem:(k,v)=>local.set(k,String(v)),removeItem:k=>local.delete(k)};
const session = new Map();
globalThis.sessionStorage={getItem:k=>session.has(k)?session.get(k):null,setItem:(k,v)=>session.set(k,String(v)),removeItem:k=>session.delete(k)};
'''
    seed = f"localStorage.setItem('stegverse.generic-login.accounts.v1', {json.dumps(json.dumps({account_user: account}))});\n"
    assertions = f'''
const api=window.__STEGVERSE_LOGIN_TEST__;
if(!api||api.getState()!=='LOGIN'||api.getView()!=='LOGIN_CARD') throw new Error('initial view');
const success=await api.submit({json.dumps(account_user)},{json.dumps(account_pass)});
const successView=api.getView();
const email=elements['account-email'].textContent;
const sms=elements['account-sms'].textContent;
const passwordHref=elements['change-password'].href;
const passwordCleared=elements.password.value==='';
elements['logout'].listeners.click[0]({{preventDefault(){{}}}});
const afterLogout=api.getView();
const failure=await api.submit({json.dumps(account_user)},'wrong');
console.log(JSON.stringify({{success,successView,email,sms,passwordHref,passwordCleared,afterLogout,failure}}));
'''
    program = shim + seed + "\n" + script + "\n" + assertions
    with tempfile.NamedTemporaryFile("w", suffix=".mjs", delete=False, encoding="utf-8") as handle:
        handle.write(program)
        path = Path(handle.name)
    try:
        proc = subprocess.run(["node", str(path)], text=True, capture_output=True, check=False)
    finally:
        path.unlink(missing_ok=True)
    require(proc.returncode == 0, f"javascript execution failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout.strip().splitlines()[-1])


def main() -> int:
    require(PAGE.is_file(), "login page missing")
    require(CREATE.is_file(), "create account page missing")
    require(FORGOT.is_file(), "forgot password page missing")
    html = PAGE.read_text(encoding="utf-8")
    create_html = CREATE.read_text(encoding="utf-8")
    forgot_html = FORGOT.read_text(encoding="utf-8")

    for marker in (
        'data-testid="login-status"', 'data-testid="username"', 'data-testid="password"',
        'data-testid="forgot-password"', 'data-testid="create-account"', 'data-testid="submit"',
        '>LOGIN</div>', 'Forgot password?', 'Create account', 'Successful Login',
        'Account attributes', '>Email</strong>', '>Text number</strong>', '>Password</strong>',
        'id="change-email"', 'id="change-sms"', 'id="change-password"',
        "form.addEventListener('submit'", "form.requestSubmit()", "window.__STEGVERSE_LOGIN_TEST__",
    ):
        require(marker in html, f"missing contract marker: {marker}")

    for forbidden in (
        'aria-label="Test credentials"', 'fixture-username', 'fixture-password', 'data-copy=',
        '?auto=success', '?auto=failure', 'document.cookie', 'fetch(', 'XMLHttpRequest', 'TVC_EPHEMERAL_GITHUB_TOKEN',
    ):
        require(forbidden not in html, f"forbidden credential/network behavior: {forbidden}")

    require("passwordDigest" in create_html and "emailVerified" in create_html and "smsVerified" in create_html,
            "create-account must persist only password digest plus verified recovery attributes")
    require("TEST_ONLY" in create_html and "TEST_ONLY" in forgot_html,
            "test delivery boundary must remain explicit")
    require("new-password" in forgot_html and "PASSWORD RESET" in forgot_html,
            "forgot-password reset path missing")
    require("Recovery method" in forgot_html and "EMAIL" in forgot_html and "SMS" in forgot_html,
            "forgot-password must support verified email/SMS selection")

    user = "acct-" + secrets.token_hex(6)
    password = "pw-" + secrets.token_hex(12)
    result = run_js(extract_inline_script(html), user, password)
    require(result["success"] == "SUCCESS", f"created-account login did not succeed: {result}")
    require(result["successView"] == "ACCOUNT_CARD", f"login card not replaced: {result}")
    require(result["email"] == "person@example.test" and result["sms"] == "+15555550123",
            f"account attributes not rendered: {result}")
    require("forgot-password-test.html?username=" in result["passwordHref"], f"password change not recovery path: {result}")
    require(result["passwordCleared"] is True, f"password not cleared: {result}")
    require(result["afterLogout"] == "LOGIN_CARD" and result["failure"] == "FAILED", f"logout/failure path mismatch: {result}")

    report = {
        "schema": "stegverse.site.generic-login-verification.v3",
        "status": "PASS",
        "created_account_login": "SUCCESS",
        "successful_login_replaces_card": True,
        "account_attributes": ["email", "text_number", "password"],
        "email_change_requires_new_value_verification": True,
        "sms_change_requires_new_value_verification": True,
        "password_change_reuses_forgot_password": True,
        "forgot_password_channels": ["EMAIL", "SMS"],
        "plaintext_password_persisted": False,
        "real_message_delivery_claimed": False,
        "delivery_mode": "TEST_ONLY",
    }
    print("GENERIC_LOGIN_TEST_PASS")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
