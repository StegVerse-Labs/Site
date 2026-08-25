#!/usr/bin/env python3
from __future__ import annotations

import json
import re
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


def run_js(script: str, search: str, assertions: str) -> dict:
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
const elements = {'status':status,'login-form':form,'username':username,'password':password};
globalThis.window = globalThis;
globalThis.document = {
  documentElement: { dataset: {} },
  getElementById: (id) => elements[id],
  querySelectorAll: () => []
};
globalThis.location = { search: __SEARCH__ };
Object.defineProperty(globalThis, 'navigator', {
  configurable: true,
  value: { clipboard: { writeText: async () => {} } }
});
globalThis.CustomEvent = class { constructor(type, init){ this.type=type; this.detail=init?.detail; } };
globalThis.addEventListener = (name, fn) => { (listeners[name] ||= []).push(fn); };
globalThis.dispatchEvent = (event) => { for (const fn of (listeners[event.type] || [])) fn(event); return true; };
'''.replace('__SEARCH__', json.dumps(search))
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
        'data-testid="submit"',
        '>LOGIN</div>',
        '<code id="fixture-username">test</code>',
        '<code id="fixture-password">stegverse</code>',
        "form.addEventListener('submit'",
        "form.requestSubmit()",
        "?auto=success",
        "?auto=failure",
        "window.__STEGVERSE_LOGIN_TEST__",
    ):
        require(marker in html, f"missing contract marker: {marker}")

    for forbidden in (
        "localStorage",
        "sessionStorage",
        "document.cookie",
        "fetch(",
        "XMLHttpRequest",
        "TVC_EPHEMERAL_GITHUB_TOKEN",
    ):
        require(forbidden not in html, f"forbidden persistence/network/credential behavior: {forbidden}")

    script = extract_inline_script(html)

    manual = run_js(
        script,
        "",
        r'''
const api = window.__STEGVERSE_LOGIN_TEST__;
if (!api || api.getState() !== 'LOGIN') throw new Error('initial state');
const success = api.submit('test','stegverse');
const afterSuccessPasswordCleared = password.value === '';
const failure = api.submit('test','wrong');
const afterFailurePasswordCleared = password.value === '';
console.log(JSON.stringify({initial:'LOGIN', success, failure, afterSuccessPasswordCleared, afterFailurePasswordCleared}));
''',
    )
    require(manual == {
        "initial": "LOGIN",
        "success": "SUCCESS",
        "failure": "FAILED",
        "afterSuccessPasswordCleared": True,
        "afterFailurePasswordCleared": True,
    }, f"manual path mismatch: {manual}")

    auto_success = run_js(
        script,
        "?auto=success",
        r'''
await new Promise(resolve => queueMicrotask(resolve));
console.log(JSON.stringify({state: status.dataset.state, passwordCleared: password.value === ''}));
''',
    )
    require(auto_success == {"state": "SUCCESS", "passwordCleared": True}, f"auto success mismatch: {auto_success}")

    auto_failure = run_js(
        script,
        "?auto=failure",
        r'''
await new Promise(resolve => queueMicrotask(resolve));
console.log(JSON.stringify({state: status.dataset.state, passwordCleared: password.value === ''}));
''',
    )
    require(auto_failure == {"state": "FAILED", "passwordCleared": True}, f"auto failure mismatch: {auto_failure}")

    report = {
        "schema": "stegverse.site.generic-login-verification.v1",
        "status": "PASS",
        "page": "generic-login-test.html",
        "manual_initial": "LOGIN",
        "manual_valid": "SUCCESS",
        "manual_invalid": "FAILED",
        "auto_success": "SUCCESS",
        "auto_failure": "FAILED",
        "same_submit_handler": True,
        "password_cleared_after_submit": True,
        "credential_persistence": False,
        "authentication_authority": "NONE_TEST_FIXTURE_ONLY",
    }
    print("GENERIC_LOGIN_TEST_PASS")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
