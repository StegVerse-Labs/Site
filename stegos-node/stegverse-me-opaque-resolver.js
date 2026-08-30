(function (root, factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.StegVerseOpaqueNodeResolver = api;
}(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  var DOMAIN_SEPARATOR = "stegverse.me/opaque-node/v1";
  var NODE_PATTERN = /^sv1_[A-Za-z0-9_-]{43}$/;
  var ROUTE_PATTERN = /^\/n\/([^/]+)\/(?:services\.html)?$/;

  function canonicalize(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return "[" + value.map(canonicalize).join(",") + "]";
    return "{" + Object.keys(value).sort().map(function (key) {
      return JSON.stringify(key) + ":" + canonicalize(value[key]);
    }).join(",") + "}";
  }

  function bytesToHex(bytes) {
    return Array.prototype.map.call(new Uint8Array(bytes), function (value) {
      return value.toString(16).padStart(2, "0");
    }).join("");
  }

  function bytesToBase64Url(bytes) {
    var binary = "";
    new Uint8Array(bytes).forEach(function (value) { binary += String.fromCharCode(value); });
    if (typeof btoa === "function") return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
    return Buffer.from(binary, "binary").toString("base64url");
  }

  function digestBytes(value) {
    if (!globalThis.crypto || !globalThis.crypto.subtle) {
      return Promise.reject(new Error("WebCrypto SHA-256 unavailable"));
    }
    return globalThis.crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  }

  function hashCanonical(value) {
    return digestBytes(canonicalize(value)).then(bytesToHex);
  }

  function deriveOpaqueNode(nodeId, deviceContinuityId) {
    if (typeof nodeId !== "string" || !nodeId || typeof deviceContinuityId !== "string" || !deviceContinuityId) {
      return Promise.reject(new Error("Established node and device continuity IDs are required"));
    }
    return digestBytes(DOMAIN_SEPARATOR + "\u0000" + nodeId + "\u0000" + deviceContinuityId)
      .then(function (digest) { return "sv1_" + bytesToBase64Url(digest); });
  }

  function routeOpaqueNode(pathname) {
    var match = String(pathname || "").match(ROUTE_PATTERN);
    return match ? match[1] : null;
  }

  function replayJournal(rows) {
    if (!Array.isArray(rows) || rows.length === 0) return Promise.reject(new Error("Continuity journal missing"));
    var previous = Promise.resolve(null);
    rows.forEach(function (row, index) {
      previous = previous.then(function (priorHash) {
        if (!row || row.schema !== "stegos.web_bootstrap_journal_entry.v1" ||
            row.sequence !== index + 1 || row.previous_entry_sha256 !== priorHash) {
          throw new Error("Continuity journal sequence mismatch");
        }
        return hashCanonical(row.receipt).then(function (receiptHash) {
          if (receiptHash !== row.receipt_sha256) throw new Error("Continuity receipt hash mismatch");
          return hashCanonical({
            schema: row.schema,
            sequence: row.sequence,
            previous_entry_sha256: row.previous_entry_sha256,
            receipt: row.receipt,
            receipt_sha256: row.receipt_sha256
          });
        }).then(function (entryHash) {
          if (entryHash !== row.entry_sha256) throw new Error("Continuity entry hash mismatch");
          return entryHash;
        });
      });
    });
    return previous;
  }

  function verifyRecords(evidence) {
    var node = evidence && evidence.node;
    var device = evidence && evidence.device;
    var receipts = evidence && evidence.receipts;
    if (!node || node.schema !== "stegos.web_node.v1" || node.credential_authority !== "TV/TVC") {
      throw new Error("Established StegVerse node missing or invalid");
    }
    if (!device || device.schema !== "stegos.web_device_continuity_root.v1") {
      throw new Error("Device continuity root missing or invalid");
    }
    if (!Array.isArray(receipts)) throw new Error("Continuity journal missing");
    var bound = receipts.some(function (entry) {
      var receipt = entry && entry.receipt;
      return receipt && receipt.schema === "stegos.web_device_node_binding_receipt.v1" &&
        receipt.node_id === node.node_id &&
        receipt.device_continuity_id === device.device_continuity_id &&
        receipt.authority_effect === "NONE";
    });
    if (!bound) throw new Error("Node/device binding receipt missing");
    return { node: node, device: device, receipts: receipts };
  }

  function result(state, reason, expected, observed) {
    return {
      schema: "stegverse.site.opaque-node-resolution/v1",
      state: state,
      reason: reason,
      route_expected: expected || null,
      route_observed: observed || null,
      local_continuity_verified: state === "LOCAL_CONTINUITY_VERIFIED",
      private_kv_readback_performed: false,
      authenticated_interlock_admission_performed: false,
      route_possession_grants_access: false,
      credential_material_observed: false,
      authority_effect: "NONE",
      activation_effect: false
    };
  }

  function resolve(evidence, pathname) {
    var path = String(pathname || "");
    var observed = routeOpaqueNode(path);
    if (!observed) {
      if (path.indexOf("/n/") === 0) return Promise.resolve(result("FAIL_CLOSED", "OPAQUE_NODE_ROUTE_NOT_ALLOWED", null, null));
      return Promise.resolve(result("REVIEW", "OPAQUE_NODE_ROUTE_REQUIRED", null, null));
    }
    if (!NODE_PATTERN.test(observed)) return Promise.resolve(result("FAIL_CLOSED", "OPAQUE_NODE_FORMAT_INVALID", null, observed));
    var records;
    try { records = verifyRecords(evidence); }
    catch (error) { return Promise.resolve(result("FAIL_CLOSED", error.message, null, observed)); }
    return replayJournal(records.receipts).then(function () {
      return deriveOpaqueNode(records.node.node_id, records.device.device_continuity_id);
    }).then(function (expected) {
      if (expected !== observed) return result("FAIL_CLOSED", "OPAQUE_NODE_ROUTE_MISMATCH", expected, observed);
      return result("LOCAL_CONTINUITY_VERIFIED", "LOCAL_NODE_DEVICE_BINDING_AND_ROUTE_VERIFIED", expected, observed);
    }).catch(function (error) {
      return result("FAIL_CLOSED", error.message, null, observed);
    });
  }

  return {
    DOMAIN_SEPARATOR: DOMAIN_SEPARATOR,
    NODE_PATTERN: NODE_PATTERN,
    ROUTE_PATTERN: ROUTE_PATTERN,
    canonicalize: canonicalize,
    hashCanonical: hashCanonical,
    deriveOpaqueNode: deriveOpaqueNode,
    routeOpaqueNode: routeOpaqueNode,
    replayJournal: replayJournal,
    resolve: resolve
  };
}));
