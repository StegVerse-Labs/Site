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


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


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
  constructor(id){this.id=id;this.value='';this.textContent='';this.dataset={};this.listeners={};this.hidden=false;this.href='';this.disabled=false;this.children=[];this.className='';this.dateTime='';}
  addEventListener(name,fn){(this.listeners[name] ||= []).push(fn);}
  requestSubmit(){const e={preventDefault(){}};for(const fn of (this.listeners.submit||[]))fn(e);}
  click(){const e={preventDefault(){}};for(const fn of (this.listeners.click||[]))fn(e);}
  append(...children){this.children.push(...children);}
}
const ids=['status','login-card','kv-card','login-form','username','password','identity-state','kv-onboarding','kv-onboarding-state','kv-onboarding-note','kv-no-kv-actions','kv-owned-actions','kv-active-actions','kv-onboarding-receipt','create-kv','attach-kv','install-kv','view-kv-ownership','kv-tree','open-personal','personal-panel','pi-name','pi-email','pi-sms','pi-address','save-personal','personal-receipt','unlock-skap','skap-stepup','skap-password','confirm-skap','skap-panel','account-info','account-email','account-sms','change-password','login-history','logout'];
const elements=Object.fromEntries(ids.map(id=>[id,new FakeElement(id)]));
elements.status.dataset.state='LOGIN';elements.status.textContent='LOGIN';elements['kv-card'].hidden=true;elements['kv-tree'].hidden=true;elements['kv-owned-actions'].hidden=true;elements['kv-active-actions'].hidden=true;elements['personal-panel'].hidden=true;elements['skap-stepup'].hidden=true;elements['skap-panel'].hidden=true;
globalThis.window=globalThis;
globalThis.document={getElementById:id=>elements[id],createElement:tag=>new FakeElement(tag)};
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
const initialKv=await api.getKvOnboardingState();
const treeHiddenAfterLogin=elements['kv-tree'].hidden===true;
const skippedInstall=await api.installKv();
const kvAfterSkippedInstall=await api.getKvOnboardingState();
const createKv=await api.createKv();
const kvAfterCreate=await api.getKvOnboardingState();
const treeHiddenAfterCreate=elements['kv-tree'].hidden===true;
const installKv=await api.installKv();
const kvAfterInstall=await api.getKvOnboardingState();
const treeVisibleAfterInstall=elements['kv-tree'].hidden===false;
const kvReceipts=await api.getKvOnboardingReceipts();
const historyAfterSuccess=JSON.parse(localStorage.getItem('stegverse.generic-login.login-history.v1')||'{{}}');
const successEvents=Object.values(historyAfterSuccess)[0]||[];
await elements['open-personal'].listeners.click[0]();
elements['pi-name'].value='Test Person';elements['save-personal'].click();
const personalReceipt=JSON.parse(elements['personal-receipt'].textContent);
await elements['unlock-skap'].listeners.click[0]();
elements['skap-password'].value={json.dumps(password)};
await elements['confirm-skap'].listeners.click[0]();
const step=api.getSkapAssertion();
const skapVisibleBeforeLogout=elements['skap-panel'].hidden===false;
elements.logout.click();
const skapRelockedAfterLogout=elements['skap-panel'].hidden===true;
const fail=await api.submit({json.dumps(user)},'wrong');
const historyAfterFailure=JSON.parse(localStorage.getItem('stegverse.generic-login.login-history.v1')||'{{}}');
const allEvents=Object.values(historyAfterFailure)[0]||[];
console.log(JSON.stringify({{
  configMode:cfg.mode,prodState:prod.state,directOk:direct.ok,wrongDirect:wrongDirect.ok,
  directCredentialDisclosed:direct.assertion?.credential_disclosed,directRawSecret:direct.assertion?.raw_secret_present,
  login,viewAfterLogin:'KV_ACCOUNT',assertionSchema:assertion?.schema,assertionCredentialDisclosed:assertion?.credential_disclosed,
  initialKvState:initialKv.state,treeHiddenAfterLogin,
  skippedInstallState:skippedInstall.state,kvAfterSkippedInstallState:kvAfterSkippedInstall.state,
  createKvState:createKv.state,kvAfterCreateState:kvAfterCreate.state,treeHiddenAfterCreate,
  installKvState:installKv.state,kvAfterInstallState:kvAfterInstall.state,treeVisibleAfterInstall,kvReceipts,
  successEvents,allEvents,
  personalOperation:personalReceipt.operation,personalParent:personalReceipt.parent_assertion_id===assertion.assertion_id,
  stepSchema:step?.schema,stepCredentialDisclosed:step?.credential_disclosed,skapVisibleBeforeLogout,skapRelockedAfterLogout,
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


def validate_audit_chain(events: list[dict], user: str, password: str) -> None:
    require(len(events) == 4, f"expected four audit events, got {len(events)}")
    require([event.get("event_type") for event in events] == ["LOGIN_ATTEMPT", "LOGIN_SUCCESS", "LOGIN_ATTEMPT", "LOGIN_FAILED"], f"audit event ordering invalid: {events}")
    expected_prior = None
    account_refs = set()
    serialized = json.dumps(events, sort_keys=True)
    require(user not in serialized and password not in serialized, "login audit contains raw username/password")
    for index, event in enumerate(events, 1):
        require(event.get("schema") == "stegverse.intr.login-audit-event/v1", f"audit schema invalid at {index}")
        require(event.get("sequence") == index, f"audit sequence invalid at {index}")
        require(event.get("transport_protocol") == "InTr", f"audit transport invalid at {index}")
        require(event.get("secret_plaintext_present") is False and event.get("credential_material_recorded") is False, f"audit secret boundary invalid at {index}")
        require(event.get("authority_effect") == "AUDIT_ONLY", f"audit authority escalation at {index}")
        require(event.get("prior_login_event_hash") == expected_prior, f"audit prior hash mismatch at {index}")
        account_ref = str(event.get("account_ref_sha256") or "")
        require(account_ref.startswith("sha256:") and len(account_ref) == 71, f"account search hash invalid at {index}")
        account_refs.add(account_ref)
        claimed = str(event.get("login_event_hash") or "")
        require(claimed.startswith("sha256:") and len(claimed) == 71, f"login event search hash invalid at {index}")
        body = dict(event)
        body.pop("login_event_hash", None)
        actual = "sha256:" + hashlib.sha256(canonical(body).encode()).hexdigest()
        require(claimed == actual, f"login event hash does not recompute at {index}")
        expected_prior = claimed
    require(len(account_refs) == 1, "audit records do not share one hashed account reference")
    require(events[1].get("assertion_id") and events[1].get("assurance_level"), "success audit lacks assertion correlation")
    require(events[3].get("assertion_id") is None, "failed audit must not invent assertion id")


def validate_kv_onboarding_chain(receipts: list[dict], user: str, password: str) -> None:
    expected = [
        ("KV_CREATED", "NO_KV", "KV_CREATED"),
        ("OWNER_BOUND", "KV_CREATED", "OWNER_BOUND"),
        ("DEVICE_REGISTERED", "OWNER_BOUND", "DEVICE_REGISTERED"),
        ("INSTALLATION_ADMITTED", "DEVICE_REGISTERED", "INSTALLATION_ADMITTED"),
        ("KV_ACTIVE", "INSTALLATION_ADMITTED", "KV_ACTIVE"),
    ]
    require(len(receipts) == len(expected), f"expected five KV onboarding receipts, got {len(receipts)}")
    serialized = json.dumps(receipts, sort_keys=True)
    require(user not in serialized and password not in serialized, "KV onboarding receipts contain raw username/password")
    prior = None
    for index, (receipt, exp) in enumerate(zip(receipts, expected), 1):
        transition, before, after = exp
        require(receipt.get("schema") == "stegverse.intr.kv-onboarding-transition/v1", f"KV receipt schema invalid at {index}")
        require(receipt.get("sequence") == index, f"KV receipt sequence invalid at {index}")
        require(receipt.get("transition") == transition, f"KV transition invalid at {index}: {receipt}")
        require(receipt.get("lifecycle_state_before") == before and receipt.get("lifecycle_state_after") == after, f"KV lifecycle edge invalid at {index}")
        require(receipt.get("prior_transition_receipt_hash") == prior, f"KV prior receipt hash mismatch at {index}")
        require(receipt.get("transport_protocol") == "InTr", f"KV transport marker invalid at {index}")
        require(receipt.get("runtime_class") == "TEST_ONLY_LOCAL_PROJECTION", f"KV runtime class escalated at {index}")
        require(receipt.get("production_intr_receipt_observed") is False, f"KV receipt falsely claims production InTr at {index}")
        require(receipt.get("production_kv_custody") is False, f"KV receipt falsely claims production custody at {index}")
        require(receipt.get("device_authority") is False, f"KV receipt grants device authority at {index}")
        require(receipt.get("secret_plaintext_present") is False, f"KV receipt contains secret plaintext at {index}")
        require(receipt.get("authority_effect") == "NONE", f"KV receipt grants authority at {index}")
        require(receipt.get("skap_unlocked") is False, f"KV onboarding receipt unlocks SKAP at {index}")
        kv_ref = str(receipt.get("kv_ref") or "")
        owner_ref = str(receipt.get("owner_identity_ref_sha256") or "")
        require(kv_ref.startswith("kv://test-created/"), f"KV test reference invalid at {index}")
        require(owner_ref.startswith("sha256:") and len(owner_ref) == 71, f"KV owner reference hash invalid at {index}")
        claimed = str(receipt.get("transition_receipt_hash") or "")
        require(claimed.startswith("sha256:") and len(claimed) == 71, f"KV receipt hash invalid at {index}")
        body = dict(receipt)
        body.pop("transition_receipt_hash", None)
        actual = "sha256:" + hashlib.sha256(canonical(body).encode()).hexdigest()
        require(claimed == actual, f"KV receipt hash does not recompute at {index}")
        prior = claimed


def main() -> int:
    for path in (PAGE, AUTH, CREATE, FORGOT):
        require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    html = PAGE.read_text()
    auth_js = AUTH.read_text()
    create = CREATE.read_text()
    forgot = FORGOT.read_text()

    for marker in (
        'Successful Login', 'KnowledgeVault directory projection', 'KnowledgeVault Status', 'NO_KV',
        'Create My KnowledgeVault', 'Attach Existing KnowledgeVault', 'Install on This Device',
        'KV_OWNED_NOT_INSTALLED', 'KV_ACTIVE', 'stegverse.intr.kv-onboarding-transition/v1',
        'Personal Info/', '_Vault/SKAP', 'SKAP Step-up Validation', 'Save through InTr', 'Account Info', 'Login History',
        'stegverse.intr.login-audit-event/v1', 'prior_login_event_hash', 'login_event_hash', 'account_ref_sha256',
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

    require('passwordDigest' in create and 'emailVerified' in create and 'smsVerified' in create, 'create-account persistence contract missing')
    for marker in ('id="created"', 'id="continue-login"', 'function finishCreated()', 'form.hidden=true', 'created.hidden=false', "window.location.assign('generic-login-test.html')"):
        require(marker in create, f"create-account success transition missing: {marker}")
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
    require(result['initialKvState'] == 'NO_KV' and result['treeHiddenAfterLogin'] is True, f"login incorrectly implied KV ownership: {result}")
    require(result['skippedInstallState'] == 'BLOCKED_INVALID_TRANSITION' and result['kvAfterSkippedInstallState'] == 'NO_KV', f"KV install skipped ownership gate: {result}")
    require(result['createKvState'] == 'KV_OWNED_NOT_INSTALLED' and result['kvAfterCreateState'] == 'KV_OWNED_NOT_INSTALLED' and result['treeHiddenAfterCreate'] is True, f"KV ownership projection state mismatch: {result}")
    require(result['installKvState'] == 'KV_ACTIVE' and result['kvAfterInstallState'] == 'KV_ACTIVE' and result['treeVisibleAfterInstall'] is True, f"KV activation projection state mismatch: {result}")
    validate_kv_onboarding_chain(result['kvReceipts'], user, password)
    require([event.get('event_type') for event in result['successEvents']] == ['LOGIN_ATTEMPT', 'LOGIN_SUCCESS'], f"success audit append mismatch: {result}")
    validate_audit_chain(result['allEvents'], user, password)
    require(result['personalOperation'] == 'PERSONAL_INFO_UPDATE' and result['personalParent'] is True, f"KV transition receipt mismatch: {result}")
    require(result['stepSchema'] == 'stegverse.intr.step-up-assertion/v1' and result['stepCredentialDisclosed'] is False and result['skapVisibleBeforeLogout'] is True, f"SKAP step-up mismatch: {result}")
    require(result['skapRelockedAfterLogout'] is True, f"SKAP did not re-lock on logout: {result}")
    require(result['afterLogout'] == 'LOGIN_CARD' and result['fail'] == 'FAILED', f"logout/failure mismatch: {result}")

    report = {
        'schema': 'stegverse.site.intr-kv-login-projection-verification.v1',
        'status': 'PASS',
        'site_receives_raw_stored_credential': False,
        'production_intr_default': 'FAIL_CLOSED_NOT_PROVISIONED',
        'identity_assertion': 'PASS',
        'kv_directory_projection': 'PASS_AFTER_TEST_ONLY_KV_ACTIVE',
        'kv_onboarding_state_machine': 'PASS_TEST_ONLY',
        'account_login_implies_kv_ownership': False,
        'kv_install_skip_ownership_gate': 'FAIL_CLOSED',
        'kv_onboarding_receipt_chain': 'SHA256_CANONICAL_RECOMPUTED',
        'kv_onboarding_production_custody_claimed': False,
        'personal_info_transition_receipt': 'PASS_TEST_ONLY',
        'account_info_login_history': 'PASS_TEST_ONLY',
        'login_attempt_and_outcome_appended': True,
        'login_event_search_hash': 'SHA256_CANONICAL_RECOMPUTED',
        'login_audit_hash_chain': 'PASS',
        'audit_contains_raw_username_or_password': False,
        'create_account_terminal_transition': 'ACCOUNT_CREATED_TO_LOGIN',
        'skap_requires_separate_step_up_assertion': True,
        'skap_relocks_on_logout': True,
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
