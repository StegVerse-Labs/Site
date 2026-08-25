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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"GENERIC_LOGIN_TEST_FAIL: {message}")


def extract_inline_script(html: str) -> str:
    matches = re.findall(r"<script>(.*?)</script>", html, flags=re.S | re.I)
    require(len(matches) == 1, "expected exactly one inline script")
    return matches[0]


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def run_js(script: str, assertions: str) -> dict:
    shim = r'''
const listeners = {};
class FakeElement {
  constructor(id) { this.id=id; this.value=''; this.textContent=''; this.dataset={}; this.listeners={}; }
  addEventListener(name, fn) { (this.listeners[name] ||= []).push(fn); }
  requestSubmit() {
    const event = { preventDefault(){} };
    for (const fn of (this.listeners.submit || [])) fn(event);
  }
}
const status = new FakeElement('status'); status.dataset.state='LOGIN'; status.textContent='LOGIN';
const form = new FakeElement('login-form');
const username = new FakeElement('username');
const password = new FakeElement('password');
const forgot = new FakeElement('forgot-password');
const create = new FakeElement('create-account');
const elements = {'status':status,'login-form':form,'username':username,'password':password,'forgot-password':forgot,'create-account':create};
globalThis.window = globalThis;
globalThis.document = {
  documentElement: { dataset: {} },
  getElementById: (id) => elements[id]
};
globalThis.CustomEvent = class { constructor(type, init){ this.type=type; this.detail=init?.detail; } };
globalThis.addEventListener = (name, fn, options={}) => { (listeners[name] ||= []).push({fn, once:Boolean(options.once)}); };
globalThis.dispatchEvent = (event) => {
  const current = [...(listeners[event.type] || [])];
  for (const item of current) item.fn(event);
  listeners[event.type] = (listeners[event.type] || []).filter(item => !item.once);
  return true;
};
'''
    program = shim + "\n" + script + "\n" + assertions
    with tempfile.NamedTemporaryFile("w", suffix=".mjs", delete=False, encoding="utf-8") as handle:
        handle.write(program)
        path = Path(handle.name)
    try:
        proc = subprocess.run(["node", str(path)], text=True, capture_output=True, check=False)
    finally:
        path.unlink(missing_ok=True)
    require(proc.returncode == 0, f"javascript execution failed: {proc.stderr.strip()}")
    line = proc.stdout.strip().splitlines()[-1]
    return json.loads(line)


def main() -> int:
    require(PAGE.is_file(), "page missing")
    html = PAGE.read_text(encoding="utf-8")

    for marker in (
        'data-testid="login-status"',
        'data-testid="username"',
        'data-testid="password"',
        'data-testid="forgot-password"',
        'data-testid="create-account"',
        'data-testid="submit"',
        '>LOGIN</div>',
        'Forgot password?',
        'Create account',
        "form.addEventListener('submit'",
        "form.requestSubmit()",
        "window.__STEGVERSE_LOGIN_TEST__",
        "EXPECTED_USERNAME_SHA256",
        "EXPECTED_PASSWORD_SHA256",
    ):
        require(marker in html, f"missing contract marker: {marker}")

    for forbidden in (
        'aria-label="Test credentials"',
        'fixture-username',
        'fixture-password',
        'data-copy=',
        '?auto=success',
        '?auto=failure',
        "localStorage",
        "sessionStorage",
        "document.cookie",
        "fetch(",
        "XMLHttpRequest",
        "TVC_EPHEMERAL_GITHUB_TOKEN",
    ):
        require(forbidden not in html, f"forbidden credential propagation/persistence/network behavior: {forbidden}")

    script = extract_inline_script(html)

    # CI proves the exact handler with an ephemeral runtime-only fixture. The
    # repository never needs to publish the manual operator's plaintext values.
    ephemeral_user = "ci-" + secrets.token_hex(8)
    ephemeral_pass = "ci-" + secrets.token_hex(16)
    synthetic_script = re.sub(
        r"const EXPECTED_USERNAME_SHA256 = '[0-9a-f]{64}';",
        f"const EXPECTED_USERNAME_SHA256 = '{sha256(ephemeral_user)}';",
        script,
        count=1,
    )
    synthetic_script = re.sub(
        r"const EXPECTED_PASSWORD_SHA256 = '[0-9a-f]{64}';",
        f"const EXPECTED_PASSWORD_SHA256 = '{sha256(ephemeral_pass)}';",
        synthetic_script,
        count=1,
    )
    require(synthetic_script != script, "ephemeral credential digest substitution failed")

    assertions = f'''
const api = window.__STEGVERSE_LOGIN_TEST__;
if (!api || api.getState() !== 'LOGIN') throw new Error('initial state');
const success = await api.submit({json.dumps(ephemeral_user)}, {json.dumps(ephemeral_pass)});
const afterSuccessPasswordCleared = password.value === '';
const failure = await api.submit({json.dumps(ephemeral_user)}, 'wrong');
const afterFailurePasswordCleared = password.value === '';
let forgotOption = null;
let createOption = null;
window.addEventListener('stegverse-login-option', (event) => {{
  if (event.detail.option === 'forgot-password') forgotOption = event.detail.option;
  if (event.detail.option === 'create-account') createOption = event.detail.option;
}});
for (const fn of forgot.listeners.click || []) fn({{preventDefault(){{}}}});
for (const fn of create.listeners.click || []) fn({{preventDefault(){{}}}});
console.log(JSON.stringify({{
  initial:'LOGIN', success, failure,
  afterSuccessPasswordCleared, afterFailurePasswordCleared,
  forgotOption, createOption,
  finalState: api.getState()
}}));
'''
    result = run_js(synthetic_script, assertions)
    require(result == {
        "initial": "LOGIN",
        "success": "SUCCESS",
        "failure": "FAILED",
        "afterSuccessPasswordCleared": True,
        "afterFailurePasswordCleared": True,
        "forgotOption": "forgot-password",
        "createOption": "create-account",
        "finalState": "FAILED",
    }, f"login/options path mismatch: {result}")

    report = {
        "schema": "stegverse.site.generic-login-verification.v2",
        "status": "PASS",
        "page": "generic-login-test.html",
        "manual_initial": "LOGIN",
        "automated_valid": "SUCCESS",
        "automated_invalid": "FAILED",
        "same_submit_handler": True,
        "forgot_password_link_present": True,
        "create_account_link_present": True,
        "account_option_authority": "NONE_TEST_FIXTURE_ONLY",
        "published_plaintext_fixture": False,
        "password_cleared_after_submit": True,
        "credential_persistence": False,
        "authentication_authority": "NONE_TEST_FIXTURE_ONLY",
    }
    print("GENERIC_LOGIN_TEST_PASS")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
