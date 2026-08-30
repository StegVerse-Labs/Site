#!/usr/bin/env node
"use strict";
const assert = require("node:assert/strict");
if (!globalThis.crypto) globalThis.crypto = require("node:crypto").webcrypto;
const resolver = require("../stegos-node/stegverse-me-opaque-resolver.js");

async function entry(sequence, previous, receipt) {
  const receiptHash = await resolver.hashCanonical(receipt);
  const base = {schema:"stegos.web_bootstrap_journal_entry.v1",sequence,previous_entry_sha256:previous,receipt,receipt_sha256:receiptHash};
  return Object.assign(base,{entry_sha256:await resolver.hashCanonical(base)});
}

(async function () {
  const node={schema:"stegos.web_node.v1",node_id:"node-private-raw-id",credential_authority:"TV/TVC"};
  const device={schema:"stegos.web_device_continuity_root.v1",device_continuity_id:"device-private-raw-id"};
  const binding={schema:"stegos.web_device_node_binding_receipt.v1",node_id:node.node_id,device_continuity_id:device.device_continuity_id,authority_effect:"NONE"};
  const first=await entry(1,null,binding);
  const opaque=await resolver.deriveOpaqueNode(node.node_id,device.device_continuity_id);
  assert.match(opaque,resolver.NODE_PATTERN);
  assert.equal(opaque.includes(node.node_id),false);
  assert.equal(opaque.includes(device.device_continuity_id),false);

  const validRoot=await resolver.resolve({node,device,receipts:[first]},"/n/"+opaque+"/");
  assert.equal(validRoot.state,"LOCAL_CONTINUITY_VERIFIED");

  const validServices=await resolver.resolve({node,device,receipts:[first]},"/n/"+opaque+"/services.html");
  assert.equal(validServices.state,"LOCAL_CONTINUITY_VERIFIED");
  assert.equal(validServices.local_continuity_verified,true);
  assert.equal(validServices.private_kv_readback_performed,false);
  assert.equal(validServices.authenticated_interlock_admission_performed,false);
  assert.equal(validServices.route_possession_grants_access,false);
  assert.equal(validServices.authority_effect,"NONE");
  assert.equal(validServices.activation_effect,false);

  const arbitraryDescendant=await resolver.resolve({node,device,receipts:[first]},"/n/"+opaque+"/anything-else");
  assert.equal(arbitraryDescendant.state,"FAIL_CLOSED");
  assert.equal(arbitraryDescendant.reason,"OPAQUE_NODE_ROUTE_NOT_ALLOWED");

  const possessionOnly=await resolver.resolve(null,"/n/"+opaque+"/");
  assert.equal(possessionOnly.state,"FAIL_CLOSED");
  assert.equal(possessionOnly.local_continuity_verified,false);

  const mismatch=await resolver.resolve({node,device,receipts:[first]},"/n/sv1_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/");
  assert.equal(mismatch.state,"FAIL_CLOSED");
  assert.equal(mismatch.reason,"OPAQUE_NODE_ROUTE_MISMATCH");

  const missingRoute=await resolver.resolve({node,device,receipts:[first]},"/");
  assert.equal(missingRoute.state,"REVIEW");

  const tampered=JSON.parse(JSON.stringify(first)); tampered.receipt.node_id="different";
  const badJournal=await resolver.resolve({node,device,receipts:[tampered]},"/n/"+opaque+"/");
  assert.equal(badJournal.state,"FAIL_CLOSED");

  console.log("STEGVERSE_ME_OPAQUE_RESOLVER_TEST_PASS");
  console.log("ROUTE_POSSESSION_AUTHORITY=false");
  console.log("PRIVATE_KV_READBACK=false");
  console.log("AUTHORITY_EFFECT=NONE");
  console.log("ACTIVATION_EFFECT=false");
}()).catch(function(error){console.error(error);process.exit(1)});
