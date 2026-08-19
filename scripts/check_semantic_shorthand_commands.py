#!/usr/bin/env python3
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
router = (ROOT / 'assets' / 'semantic-command-router.js').read_text(encoding='utf-8')
vacc = (ROOT / 'assets' / 'va-claims-chat-runtime.js').read_text(encoding='utf-8')
ecosystem = (ROOT / 'assets' / 'ecosystem-chat-semantic-commands.js').read_text(encoding='utf-8')
ecosystem_html = (ROOT / 'ecosystem-chat.html').read_text(encoding='utf-8')
node_test = ROOT / 'tests' / 'semantic-command-router.test.cjs'

required_router = [
    "disability:{",
    "VA disability topics",
    "Disability compensation",
    "Service connection",
    "Secondary conditions",
    "Individual unemployability (TDIU)",
    "Permanent & Total (P&T)",
    "Combined disability ratings",
    "Effective dates",
    "C&P examinations",
    "Evidence and medical records",
    "Special Monthly Compensation (SMC)",
    "Common VA forms",
    "Common regulations and references",
    "I do not know which topic applies",
    "commit_intent:false",
    "authority_effect:false",
    "activation_effect:false",
    "Topic discovery only. No diagnosis, rating prediction, representation, filing, or private-record activation.",
]
required_vacc = [
    "interceptSemanticCommand",
    "loadSemanticCommands",
    "assets/semantic-command-router.js",
    "resolve(q,'VA_CLAIMS_CHAT')",
    "No intent was inferred and no action was taken.",
]
required_ecosystem = [
    "resolve(value,'ECOSYSTEM_CHAT')",
    "form.addEventListener('submit',submitCommand,true)",
    "input.addEventListener('input',previewInput,true)",
    "commit_intent=false",
    "authority_effect=false",
    "activation_effect=false",
    "execution=not_attempted",
    "provider_call=false",
]

missing = [f"router:{item}" for item in required_router if item not in router]
missing += [f"vacc:{item}" for item in required_vacc if item not in vacc]
missing += [f"ecosystem:{item}" for item in required_ecosystem if item not in ecosystem]
if not node_test.is_file():
    missing.append('tests:semantic-command-router.test.cjs')

# VACC shorthand must be intercepted before a blocked/verified provider runtime decision.
semantic_pos = vacc.find("if(await interceptSemanticCommand(event))return;")
runtime_pos = vacc.find("if(!generalMode||!ready)return;")
if semantic_pos < 0 or runtime_pos < 0 or semantic_pos > runtime_pos:
    missing.append('vacc:semantic_command_not_intercepted_before_runtime_gate')

# Ecosystem Chat must load semantic routing before generic chat routing registers.
router_script = '<script src="assets/semantic-command-router.js"></script>'
bridge_script = '<script src="assets/ecosystem-chat-semantic-commands.js"></script>'
chat_script = '<script src="assets/ecosystem-chat.js"></script>'
router_pos = ecosystem_html.find(router_script)
bridge_pos = ecosystem_html.find(bridge_script)
chat_pos = ecosystem_html.find(chat_script)
if min(router_pos, bridge_pos, chat_pos) < 0 or not (router_pos < bridge_pos < chat_pos):
    missing.append('ecosystem_html:semantic_router_and_bridge_must_load_before_generic_chat')

# The shared router and discovery bridge must not perform network, storage, or authority-bearing execution.
for name, source in (("router", router), ("ecosystem", ecosystem)):
    for forbidden in ("fetch(", "XMLHttpRequest", "WebSocket(", "EventSource(", "localStorage", "sessionStorage", "document.cookie", "eval("):
        if forbidden in source:
            missing.append(f"{name}:forbidden_execution_surface:{forbidden}")

# Semantic discovery messages must still enter the existing DOM event stream so the canonical projection observer ingests them.
for marker in ("chat-message", "receipt-block", "log.appendChild(wrapper)"):
    if marker not in ecosystem:
        missing.append(f"ecosystem:canonical_projection_ingest_surface_missing:{marker}")

if missing:
    print('SEMANTIC SHORTHAND COMMAND VALIDATION: FAIL')
    for item in missing:
        print('-', item)
    raise SystemExit(1)

node = subprocess.run(
    ['node', str(node_test)],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)
if node.returncode != 0:
    print('SEMANTIC SHORTHAND COMMAND VALIDATION: FAIL')
    print(node.stdout.rstrip())
    raise SystemExit(node.returncode)

print(node.stdout.rstrip())
print('SEMANTIC SHORTHAND COMMAND VALIDATION: PASS')
print('shared_router=assets/semantic-command-router.js')
print('vacc_context=VA_CLAIMS_CHAT')
print('ecosystem_context=ECOSYSTEM_CHAT')
print('recognized_unknown_argument_regression=PASS')
print('disability_command=topic_discovery_only')
print('commit_intent=false')
print('authority_effect=false')
print('activation_effect=false')
print('provider_call=false')
