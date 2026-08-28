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

(async function testOpenRequiresBridge() {
  await assert.rejects(
    () => api.openEntry("finance", { name: "Finance_Overview.md", kind: "file" }, null),
    /FAIL_CLOSED/
  );
})();

console.log("My KV directory tests: PASS");
