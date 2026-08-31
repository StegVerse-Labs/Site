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
  assert(source.includes('MAX_INLINE_BYTES=4*1024*1024'));
  assert(source.includes('stegverse.kv.portable-direct-source-inline-payload/v1'));
  assert(source.includes('destination:{boundary:"KV",subsystem:"KnowledgeVault:Interlock"}'));
  assert(source.includes('downstream_owner_ref:"StegVerse-Labs/continuity-vault-kit#79"'));
  assert(source.includes('payload_ref:"inline://materialization_request.portable_payload"'));
  assert(source.includes('portable_payload:inlinePayload'));
  assert(source.includes('content_base64'));
  assert(source.includes('portable direct-source packet exceeds 4 MiB bounded inline transport limit'));
  assert(!source.includes('KnowledgeVault:DirectSourceIngress'));
  assert(!source.includes('continuity-vault-kit#108'));
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
