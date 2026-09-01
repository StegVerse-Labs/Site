const assert = require("assert");
const api = require("../assets/my-kv-directory.js");

(function testRegistry() {
  const domains = api.listDomains();
  assert(domains.length >= 11);
  assert.strictEqual(api.getDomain("finance").path, "03_Records/Finance");
  assert.strictEqual(api.getDomain("assets").path, "03_Records/Assets");
  assert.strictEqual(api.getDomain("liabilities").path, "03_Records/Liabilities");
  assert.strictEqual(api.getDomain("email").path, "03_Records/Email");
  assert.strictEqual(api.getDomain("music").path, "04_Media/Music");
  assert.strictEqual(api.getDomain("pictures").path, "04_Media/Pictures");
})();

(async function testFailClosedListing() {
  const result = await api.loadDirectory("finance", null);
  assert.strictEqual(result.state, "BRIDGE_UNAVAILABLE");
  assert.deepStrictEqual(result.entries, []);
})();

(async function testCanonicalListing() {
  const bridge = {
    listDirectory(request) {
      assert.strictEqual(request.access, "READ_ONLY");
      assert.strictEqual(request.authority_effect, "NONE");
      return {
        canonical_path: request.canonical_path,
        entries: [
          { name: "Finance_Overview.md", kind: "file", size_bytes: 1234 },
          { name: "Accounts", kind: "directory" }
        ]
      };
    }
  };
  const result = await api.loadDirectory("finance", bridge);
  assert.strictEqual(result.state, "KV_LISTED");
  assert.strictEqual(result.entries.length, 2);
})();

(async function testWrongPathFailsClosed() {
  const bridge = {
    listDirectory() {
      return { canonical_path: "wrong/path", entries: [] };
    }
  };
  await assert.rejects(() => api.loadDirectory("finance", bridge), /FAIL_CLOSED/);
})();

(function testSecretMetadataRejected() {
  assert.throws(() => api.assertSafeListing({ access_token: "secret" }), /Secret-bearing/);
})();

(async function testSourceConnectRequiresBridge() {
  await assert.rejects(
    () => api.connectSource("finance", null),
    /FAIL_CLOSED/
  );
})();

(async function testSourceConnectUsesSkapBoundary() {
  const bridge = {
    connectDirectSource(request) {
      assert.strictEqual(request.access, "READ_ONLY");
      assert.strictEqual(request.direct_source_required, true);
      assert.strictEqual(request.minimum_necessary, true);
      assert.strictEqual(request.credential_destination, "SKAP_VAULT");
      return {
        direct_source_required: true,
        credential_boundary: "SKAP_VAULT",
        message: "synthetic direct source connected"
      };
    }
  };
  const result = await api.connectSource("finance", bridge);
  assert.strictEqual(result.credential_boundary, "SKAP_VAULT");
})();

(async function testOwnerControlledPortableSourceAccepted() {
  const bridge = {
    connectDirectSource(request) {
      assert.strictEqual(request.access, "READ_ONLY");
      assert.strictEqual(request.minimum_necessary, true);
      return {
        direct_source_required: true,
        state: "QUEUED_FOR_KV_ADMISSION",
        source_class: "OWNER_CONTROLLED_FILE",
        credential_requirement: "NONE",
        credential_boundary: "NOT_REQUIRED_OWNER_CONTROLLED_SOURCE",
        canonical_kv_persistence_observed: false,
        provider_session_observed: false,
        credential_material_present: false,
        provider_operation_authorized: false,
        authority_effect: "NONE",
        materialization_id: "INTR-MAT-0123456789abcdef01234567"
      };
    }
  };
  const result = await api.connectSource("pictures", bridge);
  assert.strictEqual(result.state, "QUEUED_FOR_KV_ADMISSION");
  assert.strictEqual(result.credential_requirement, "NONE");
})();

(async function testMalformedCredentialFreeSourceRejected() {
  const bridge = {
    connectDirectSource() {
      return {
        direct_source_required: true,
        state: "QUEUED_FOR_KV_ADMISSION",
        source_class: "OWNER_CONTROLLED_FILE",
        credential_requirement: "NONE",
        credential_boundary: "NOT_REQUIRED_OWNER_CONTROLLED_SOURCE",
        canonical_kv_persistence_observed: true,
        provider_session_observed: false,
        credential_material_present: false,
        provider_operation_authorized: false
      };
    }
  };
  await assert.rejects(() => api.connectSource("pictures", bridge), /FAIL_CLOSED/);
})();

(function testPortableResidentPacketSourceContract() {
  const fs = require("fs");
  const source = fs.readFileSync(require("path").join(__dirname, "../assets/my-kv-portable-direct-source-bridge.js"), "utf8");
  const generated = fs.readFileSync(require("path").join(__dirname, "../assets/generated/site-browser-intr-connectors.js"), "utf8");
  assert(source.includes('MAX_INLINE_BYTES=4*1024*1024'));
  assert(source.includes('stegverse.kv.portable-direct-source-inline-payload/v1'));
  assert(generated.includes('"destination":{"boundary":"KV","subsystem":"KnowledgeVault:Interlock"}'));
  assert(generated.includes('"downstream_owner_ref":"StegVerse-Labs/continuity-vault-kit#79"'));
  assert(source.includes('"inline://materialization_request.portable_payload"'));
  assert(source.includes('portable_payload:inlinePayload'));
  assert(source.includes('content_base64'));
  assert(source.includes('portable direct-source packet exceeds 4 MiB bounded inline transport limit'));
  assert(!source.includes('KnowledgeVault:DirectSourceIngress'));
  assert(!source.includes('continuity-vault-kit#108'));
})();

(function testIOSPortablePickerSettlementAndStatusContract() {
  const fs = require("fs");
  const path = require("path");
  const source = fs.readFileSync(path.join(__dirname, "../assets/my-kv-portable-direct-source-bridge.js"), "utf8");
  const page = fs.readFileSync(path.join(__dirname, "../my-kv-directory.html"), "utf8");
  for (const marker of [
    'input.addEventListener("cancel",onCancel)',
    'window.addEventListener("focus",onFocus)',
    'document.addEventListener("visibilitychange",onVisibility)',
    'owner-controlled file selection cancelled; no files were changed'
  ]) assert(source.includes(marker), marker);
  assert(page.includes("Choose owner-controlled files from this device. No SKAP credential is required."));
  assert(page.includes("Requesting owner-authorized direct source through SKAP Vault…"));
  assert(page.includes("connectButton.disabled=true"));
  assert(page.includes("connectButton.disabled=false"));
})();

(function testQueryBridgeBootstrapAndRecoveryContract() {
  const fs = require("fs");
  const path = require("path");
  const source = fs.readFileSync(path.join(__dirname, "../assets/my-kv-device-kv-query-bridge.js"), "utf8");
  const directoryPage = fs.readFileSync(path.join(__dirname, "../my-kv-directory.html"), "utf8");
  const landingPage = fs.readFileSync(path.join(__dirname, "../my-kv.html"), "utf8");
  for (const required of [
    "existingDirectoryBridge",
    "existingHealthBridge",
    "existingInstallationBridge",
    "StegVerseKVQueryBridgeModuleState",
    "directory_bridge_ready",
    "connection_health_bridge_ready",
    "installation_status_bridge_ready"
  ]) assert(source.includes(required), required);
  for (const required of [
    "QUERY_BRIDGE_SRC",
    "ensureQueryBridge()",
    'retry.src=QUERY_BRIDGE_SRC+"&retry="+Date.now()',
    "canonical DEVICE_KV query bridge asset unavailable",
    "canonical DEVICE_KV query bridge loaded but did not initialize"
  ]) assert(directoryPage.includes(required), required);
  assert(directoryPage.includes("assets/my-kv-device-kv-query-bridge.js?v="));
  assert(!directoryPage.includes('api.loadDirectory(domain.id,bridge).then(function(result){'));
  assert(landingPage.includes("ensureHealthBridge()"));
  assert(landingPage.includes("healthBridgePromise=ensureHealthBridge()"));
  assert(landingPage.includes("assets/my-kv-device-kv-query-bridge.js?v="));
})();


(function testMyKvLiveInstallationStatusPrimaryContract() {
  const fs = require("fs");
  const path = require("path");
  const source = fs.readFileSync(path.join(__dirname, "../assets/my-kv-device-kv-query-bridge.js"), "utf8");
  const page = fs.readFileSync(path.join(__dirname, "../my-kv.html"), "utf8");
  for (const marker of [
    "StegVerseKVInstallationStatusBridge",
    "MY_KV_INSTALLATION_STATUS",
    "KV_INSTALLATION_VERIFIED",
    "KV_INSTALLATION_NOT_VERIFIED",
    "current_cloud_provider_observation",
    "getInstallationStatus:function()"
  ]) assert(source.includes(marker), marker);
  for (const marker of [
    "ensureInstallationStatusBridge()",
    "readLiveInstallationStatus()",
    "liveInstallationVerified(",
    "Checking the current resident KnowledgeVault over DEVICE_KV",
    "No receipt selection was required.",
    "No file picker was opened.",
    "Use installation receipt from Files"
  ]) assert(page.includes(marker), marker);
  const clickStart = page.indexOf('document.getElementById("kv-install").addEventListener');
  const liveCheck = page.indexOf("readLiveInstallationStatus()", clickStart);
  const primaryEnd = page.indexOf("installReceiptFallback.addEventListener", clickStart);
  const fallback = page.indexOf("installBridge.installAndVerify()", primaryEnd);
  assert(clickStart >= 0 && liveCheck > clickStart && primaryEnd > liveCheck && fallback > primaryEnd);
  assert(!page.slice(clickStart, primaryEnd).includes("installBridge.installAndVerify()"));
  assert(page.includes('id="kv-cloud-receipt-fallback"'));
  assert(page.includes("Browse → your KnowledgeVault folder"));
  assert(page.includes("No installation receipt selected. Nothing changed."));
})();

(function testCanonicalDeviceKvQueryBridgeSourceContract() {
  const fs = require("fs");
  const path = require("path");
  const source = fs.readFileSync(path.join(__dirname, "../assets/my-kv-device-kv-query-bridge.js"), "utf8");
  const directoryPage = fs.readFileSync(path.join(__dirname, "../my-kv-directory.html"), "utf8");
  const landingPage = fs.readFileSync(path.join(__dirname, "../my-kv.html"), "utf8");
  for (const required of [
    "MY_KV_DIRECTORY_PROJECTION",
    "MY_KV_CONNECTION_HEALTH",
    "MY_KV_INSTALLATION_STATUS",
    "stegverse.kv.installation-status-projection/v1",
    "inline://materialization_request.kv_request",
    "{kv_request:query}",
    "stegos-node://",
    "StegVerseHBInTrCarrier",
    "recoverSignal",
    "StegVerseDeviceKVInTrSync",
    "RESULT_AVAILABLE",
    "NONE_RESULT_LOOKUP_ONLY",
    "NONE_RESULT_DELIVERY_ONLY",
    "response_transported_on_hb_derived_carrier",
    "exact_response_packet_recovered"
  ]) assert(source.includes(required), required);
  assert(source.includes("root.StegVerseKVDirectoryBridge"));
  assert(source.includes("root.StegVerseKVConnectionHealthBridge"));
  assert(source.includes("root.StegVerseKVInstallationStatusBridge"));
  assert(source.includes("getInstallationStatus:function()"));
  assert(source.includes('requester:{module:"Site",component:"MyKVOnboarding"}'));
  assert(source.includes('selector:{receipt_path:"_System/installation.receipt.json"}'));
  assert(source.includes('requested_scope:["installation_status"]'));
  assert(!source.includes("openEntry:function"));
  assert(directoryPage.includes("assets/generated/site-browser-intr-connectors.js"));
  assert(directoryPage.includes("assets/my-kv-device-kv-query-bridge.js"));
  assert(landingPage.includes("assets/generated/site-browser-intr-connectors.js"));
  assert(landingPage.includes("assets/my-kv-device-kv-query-bridge.js"));
})();

(async function testOpenRequiresBridge() {
  await assert.rejects(
    () => api.openEntry("finance", { name: "Finance_Overview.md", kind: "file" }, null),
    /FAIL_CLOSED/
  );
})();

console.log("My KV directory tests: PASS");


(async function testConnectionHealthBridgeUnavailable() {
  const result = await api.loadConnectionHealth("finance", null);
  assert.strictEqual(result.state, "BRIDGE_UNAVAILABLE");
  assert.strictEqual(result.health, null);
})();

(async function testConnectionHealthVerifiedBoundary() {
  const bridge = {
    getDomainHealth(request) {
      assert.strictEqual(request.access, "READ_ONLY");
      assert.strictEqual(request.authority_effect, "NONE");
      return {
        canonical_path: request.canonical_path,
        compatibility_state: "VERIFIED",
        revalidation_required: false,
        credential_material_present: false,
        provider_operation_authorized: false,
        observed_at: "2026-08-28T16:00:00Z"
      };
    }
  };
  const result = await api.loadConnectionHealth("finance", bridge);
  assert.strictEqual(result.state, "HEALTH_LISTED");
  assert.strictEqual(result.health.compatibility_state, "VERIFIED");
})();

(async function testConnectionHealthWrongPathFailsClosed() {
  const bridge = {
    getDomainHealth() {
      return {
        canonical_path: "wrong/path",
        compatibility_state: "VERIFIED",
        revalidation_required: false,
        credential_material_present: false,
        provider_operation_authorized: false
      };
    }
  };
  await assert.rejects(() => api.loadConnectionHealth("finance", bridge), /FAIL_CLOSED/);
})();

(async function testConnectionHealthAuthorityBoundaryFailsClosed() {
  const bridge = {
    getDomainHealth(request) {
      return {
        canonical_path: request.canonical_path,
        compatibility_state: "VERIFIED",
        revalidation_required: false,
        credential_material_present: false,
        provider_operation_authorized: true
      };
    }
  };
  await assert.rejects(() => api.loadConnectionHealth("finance", bridge), /FAIL_CLOSED/);
})();
