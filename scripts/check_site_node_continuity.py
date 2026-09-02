#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NODE=(ROOT/"assets/stegverse-node-continuity.js").read_text()
MYKV=(ROOT/"my-kv.html").read_text()
VA=(ROOT/"va-disability-claim-guide.html").read_text()
CHAT=(ROOT/"ecosystem-chat.html").read_text()
HOME=(ROOT/"index.html").read_text()
SIMPLE=(ROOT/"assets/ecosystem-chat-simple.js").read_text()
VARUNTIME=(ROOT/"assets/ecosystem-chat-va-runtime.js").read_text()

def main():
    failures=[]
    required_node=[
        'DB_NAME = "stegos-node-v1"',
        'stegos.node_handoff_receipt.v1',
        'NODE_REGISTERED',
        'stegos.node_capability_receipt.v1',
        'contains_personal_information: false',
        'contains_credentials: false',
        'MAX_UNREGISTERED_LLM = 10',
        'beforeLlmRequest',
        'recordLlmExecution',
        'capabilityProgress',
        'recordStep',
    ]
    for marker in required_node:
        if marker not in NODE: failures.append("node client missing: "+marker)
    for marker in [
        "StegVerse does not maintain the personal information",
        'data-kv-step="1"','data-kv-step="2"','data-kv-step="3"','data-kv-step="4"','data-kv-step="5"',
        "Register this device","Install your KnowledgeVault","Add Personal Information","Vault &amp; Connections","Verify your KnowledgeVault",
        'node.recordStep("my-kv-onboarding"',
        "Checking the current resident KnowledgeVault over DEVICE_KV",
        "StegVerseKVInstallationStatusBridge",
        "Cloud-provider revalidation remains Step 5",
        "Automatic cloud/storage verification is unavailable on this device",
        "Everything here is optional",
        "How KV improves comprehension",
    ]:
        if marker not in MYKV: failures.append("My KV missing: "+marker)
    for marker in [
        "Save progress with a StegVerse Node",
        "(optional)",
        "Continue without Node",
        "vaClaimsNodeContinuityOptInV1",
        "va-claims-guide",
        "MIGRATED_FROM_EXISTING_LOCAL_GUIDE_PROGRESS",
        "browser-local",
    ]:
        if marker not in VA: failures.append("VA guide missing: "+marker)
    for surface,name in [(CHAT,"ecosystem-chat.html"),(HOME,"index.html")]:
        if 'assets/stegverse-node-continuity.js' not in surface: failures.append(name+" missing Node client")
        if 'id="node-llm-status"' not in surface: failures.append(name+" missing Node/LLM status")
    for source,name in [(SIMPLE,"simple"),(VARUNTIME,"VA runtime")]:
        if "beforeLlmRequest" not in source: failures.append(name+" missing pre-model Node gate")
        if "recordLlmExecution" not in source: failures.append(name+" missing successful-model counter")
        if "UNREGISTERED_LLM_LIMIT_REACHED" not in source: failures.append(name+" missing limit handling")
    for forbidden in ['type="password"','name="password"','name="token"']:
        if forbidden in MYKV: failures.append("My KV secret input prohibited: "+forbidden)
    if failures:
        print("SITE_NODE_CONTINUITY_FAIL")
        for f in failures: print("- "+f)
        return 1
    print("SITE_NODE_CONTINUITY_PASS")
    return 0
if __name__=="__main__":
    raise SystemExit(main())
