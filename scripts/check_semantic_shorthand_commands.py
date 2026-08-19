#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
router = (ROOT / 'assets' / 'semantic-command-router.js').read_text(encoding='utf-8')
vacc = (ROOT / 'assets' / 'va-claims-chat-runtime.js').read_text(encoding='utf-8')

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

missing = [f"router:{item}" for item in required_router if item not in router]
missing += [f"vacc:{item}" for item in required_vacc if item not in vacc]

# Shorthand must be intercepted before a blocked/verified provider runtime decision.
semantic_pos = vacc.find("if(await interceptSemanticCommand(event))return;")
runtime_pos = vacc.find("if(!generalMode||!ready)return;")
if semantic_pos < 0 or runtime_pos < 0 or semantic_pos > runtime_pos:
    missing.append('vacc:semantic_command_not_intercepted_before_runtime_gate')

# The shared router must not perform network, storage, or authority-bearing execution.
for forbidden in ("fetch(", "XMLHttpRequest", "localStorage", "sessionStorage", "document.cookie", "eval("):
    if forbidden in router:
        missing.append(f"router:forbidden_execution_surface:{forbidden}")

if missing:
    print('SEMANTIC SHORTHAND COMMAND VALIDATION: FAIL')
    for item in missing:
        print('-', item)
    raise SystemExit(1)

print('SEMANTIC SHORTHAND COMMAND VALIDATION: PASS')
print('shared_router=assets/semantic-command-router.js')
print('vacc_context=VA_CLAIMS_CHAT')
print('disability_command=topic_discovery_only')
print('commit_intent=false')
print('authority_effect=false')
print('activation_effect=false')
