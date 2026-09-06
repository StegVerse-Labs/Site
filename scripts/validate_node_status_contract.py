#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

contract_path = ROOT / "data/node-status-contract.json"
resolver_path = ROOT / "assets/stegverse-node-status.js"
explainer_path = ROOT / "node-status.html"
product_path = ROOT / "nodes.html"
hf_path = ROOT / "hugging-face-analysis.html"
handoff_path = ROOT / "docs/NODE_STATUS_CONTRACT_MIRROR_HANDOFF.md"

for path in [contract_path, resolver_path, explainer_path, product_path, hf_path, handoff_path]:
    require(path.exists(), f"missing required file: {path.relative_to(ROOT)}")

if contract_path.exists():
    data = json.loads(contract_path.read_text())
    require(data.get("schema") == "stegverse.node_status_contract.v1", "wrong Node status contract schema")
    expected = ["UNSELECTED", "PRIVATE_SOVEREIGN", "MAIN_ECOSYSTEM", "PRIVATE_SOVEREIGN_STEGOS", "ECOSYSTEM_SOVEREIGN_STEGOS"]
    ids = [item.get("id") for item in data.get("node_classes", [])]
    require(ids == expected, f"Node class order/ids differ: {ids}")
    require(data.get("new_context", {}).get("display") == "Unselected Node not established.", "new-context display is not canonical")
    require(data.get("new_context", {}).get("page_load_mutation_allowed") is False, "page-load mutation must be false")
    require(data.get("new_context", {}).get("explicit_connect_required") is True, "explicit connect must be required")
    require(data.get("invariants", {}).get("node_established_implies_capability_established") is False, "Node/capability separation missing")
    require(data.get("authority_effect") == "NONE", "contract must grant no authority")

if resolver_path.exists():
    js = resolver_path.read_text()
    for marker in ['DB_NAME = "stegos-node-v1"', 'indexedDB.databases', 'never open/create IndexedDB merely to discover whether a Node exists', 'explicitConnect', 'registerDevice()', 'explicitSelectNodeClass', 'NODE_CLASS_REQUESTED', 'NODE_CLASS_ESTABLISHED', 'ECOSYSTEM_ELIGIBILITY_REQUIRED']:
        require(marker in js, f"resolver missing marker: {marker}")
    passive_start = js.find("function resolveExisting")
    explicit_start = js.find("function explicitConnect")
    passive = js[passive_start:explicit_start]
    require("registerDevice(" not in passive, "resolveExisting must never register a Node")
    require("appendCapabilityReceipt(" not in passive, "resolveExisting must never append a capability receipt")

if explainer_path.exists():
    text = explainer_path.read_text()
    for marker in ["Unselected Node not established.", "Connect a StegVerse Node", "Observation does not authorize transition.", "Node established does not mean capability established.", 'href="nodes.html"']:
        require(marker in text, f"Node explainer missing marker: {marker}")

if product_path.exists():
    text = product_path.read_text()
    for label in ["Unselected Node", "Private Sovereign Node", "Main Ecosystem Node", "Private Sovereign StegOS Node", "Ecosystem Sovereign StegOS Node", "Node status describes capability and sovereignty—not rank.", "Choose where your StegVerse capability lives."]:
        require(label in text, f"Node product page missing: {label}")
    require('data-select-node-class="ECOSYSTEM_SOVEREIGN_STEGOS"' not in text, "restricted ecosystem StegOS class must not have consumer-select button")

if hf_path.exists():
    text = hf_path.read_text()
    require('src="assets/stegverse-node-status.js"' in text, "Hugging Face hub does not use shared Node status resolver")
    require('href="node-status.html"' in text, "Hugging Face What-is-this link must use canonical explainer")
    require("statusApi.resolveExisting()" in text, "Hugging Face refresh must verify existing shared Node state")
    require("registerDevice()" not in text, "Hugging Face page must not directly register a Node")
    require("View / test Hugging Face observation capability" in text, "Hugging Face function-specific technical link missing")

if errors:
    print("NODE_STATUS_CONTRACT_VALIDATION_FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)
print("NODE_STATUS_CONTRACT_VALIDATION_PASS")
