(function (root) {
  "use strict";

  var MAX_ATTEMPTS = 120;
  var RETRY_MS = 500;
  var DEVICE_ENDPOINT = "https://stegverse.org/stegos-bootstrap/local-model";
  var DB_NAME = "stegos-web-bootstrap-v1";
  var DB_VERSION = 1;
  var META_STORE = "meta";
  var RECEIPT_STORE = "receipts";
  var DEVICE_ROOT_KEY = "device-continuity-root";
  var BINDING_KEY_PREFIX = "device-continuity-binding:";
  var preparedWorker = null;
  var deviceRootPromise = null;

  function text(id, value) {
    var node = document.getElementById(id);
    if (node) { node.textContent = value; }
  }

  function bytesToHex(bytes) {
    var out = "";
    for (var i = 0; i < bytes.length; i += 1) { out += bytes[i].toString(16).padStart(2, "0"); }
    return out;
  }

  function randomHex(length) {
    var bytes = new Uint8Array(length);
    crypto.getRandomValues(bytes);
    return bytesToHex(bytes);
  }

  function canonicalize(value) {
    if (value === null || typeof value !== "object") { return JSON.stringify(value); }
    if (Array.isArray(value)) { return "[" + value.map(canonicalize).join(",") + "]"; }
    return "{" + Object.keys(value).sort().map(function (key) {
      return JSON.stringify(key) + ":" + canonicalize(value[key]);
    }).join(",") + "}";
  }

  function sha256Hex(value) {
    var textValue = typeof value === "string" ? value : canonicalize(value);
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(textValue)).then(function (digest) {
      return bytesToHex(new Uint8Array(digest));
    });
  }

  function openDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = function () {
        var db = request.result;
        if (!db.objectStoreNames.contains(META_STORE)) { db.createObjectStore(META_STORE, { keyPath: "key" }); }
        if (!db.objectStoreNames.contains(RECEIPT_STORE)) { db.createObjectStore(RECEIPT_STORE, { keyPath: "sequence" }); }
      };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("device continuity IndexedDB open failed")); };
      request.onblocked = function () { reject(new Error("device continuity IndexedDB open blocked")); };
    });
  }

  function transactionPromise(tx) {
    return new Promise(function (resolve, reject) {
      tx.oncomplete = function () { resolve(); };
      tx.onerror = function () { reject(tx.error || new Error("device continuity transaction failed")); };
      tx.onabort = function () { reject(tx.error || new Error("device continuity transaction aborted")); };
    });
  }

  function getMeta(db, key) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(META_STORE, "readonly");
      var req = tx.objectStore(META_STORE).get(key);
      req.onsuccess = function () { resolve(req.result ? req.result.value : null); };
      req.onerror = function () { reject(req.error || new Error("device continuity metadata read failed")); };
    });
  }

  function putMeta(db, key, value) {
    var tx = db.transaction(META_STORE, "readwrite");
    tx.objectStore(META_STORE).put({ key: key, value: value });
    return transactionPromise(tx);
  }

  function getReceipts(db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(RECEIPT_STORE, "readonly");
      var req = tx.objectStore(RECEIPT_STORE).getAll();
      req.onsuccess = function () {
        var rows = req.result || [];
        rows.sort(function (a, b) { return a.sequence - b.sequence; });
        resolve(rows);
      };
      req.onerror = function () { reject(req.error || new Error("device continuity journal read failed")); };
    });
  }

  function appendReceipt(db, body) {
    return getReceipts(db).then(function (existing) {
      var envelope = {
        schema: "stegos.web_bootstrap_journal_entry.v1",
        sequence: existing.length + 1,
        previous_entry_sha256: existing.length ? existing[existing.length - 1].entry_sha256 : null,
        receipt: body
      };
      return sha256Hex(body).then(function (receiptHash) {
        envelope.receipt_sha256 = receiptHash;
        return sha256Hex(envelope);
      }).then(function (entryHash) {
        envelope.entry_sha256 = entryHash;
        var tx = db.transaction(RECEIPT_STORE, "readwrite");
        tx.objectStore(RECEIPT_STORE).add(envelope);
        return transactionPromise(tx).then(function () { return envelope; });
      });
    });
  }

  function readDeviceContinuityRoot() {
    return openDb().then(function (db) {
      return getMeta(db, DEVICE_ROOT_KEY).then(function (value) { db.close(); return value; });
    });
  }

  function ensureDeviceContinuityRootOnce() {
    if (!(root.crypto && root.crypto.subtle && root.crypto.getRandomValues)) {
      return Promise.reject(new Error("FAIL_CLOSED: WebCrypto required for device continuity root"));
    }
    return openDb().then(function (db) {
      return getMeta(db, DEVICE_ROOT_KEY).then(function (existing) {
        if (existing) { db.close(); return existing; }
        return getReceipts(db).then(function (prior) {
          var createdAt = new Date().toISOString();
          return sha256Hex("stegverse-device-continuity-v1|" + location.origin + "|" + randomHex(32)).then(function (digest) {
            var continuity = {
              schema: "stegos.web_device_continuity_root.v1",
              device_continuity_id: "stegdevice-" + digest.slice(0, 40),
              created_at: createdAt,
              origin: location.origin,
              root_method: "LOCAL_WEBCRYPTO_RANDOM",
              hardware_attestation: "UNAVAILABLE_TO_BROWSER",
              sync_state: "UNSYNCED",
              parent_continuity_id: null,
              implicit_cross_root_continuation_allowed: false,
              governed_transfer_required_for_cross_root: true,
              preexisting_journal_entries: prior.length,
              authority_effect: "NONE"
            };
            return putMeta(db, DEVICE_ROOT_KEY, continuity).then(function () {
              return appendReceipt(db, {
                schema: "stegos.web_device_continuity_root_receipt.v1",
                device_continuity: continuity,
                prior_history_relation: prior.length ? "ROOT_ESTABLISHED_AFTER_EXISTING_LOCAL_HISTORY" : "ROOT_IS_JOURNAL_ORIGIN",
                cross_root_sync_performed: false,
                authority_effect: "NONE"
              });
            }).then(function () {
              return getMeta(db, DEVICE_ROOT_KEY);
            }).then(function (persisted) {
              db.close();
              if (!persisted || persisted.device_continuity_id !== continuity.device_continuity_id) {
                throw new Error("FAIL_CLOSED: device continuity root changed during establishment");
              }
              return persisted;
            });
          });
        });
      }).catch(function (error) { db.close(); throw error; });
    });
  }

  function ensureDeviceContinuityRoot() {
    if (deviceRootPromise) { return deviceRootPromise; }
    deviceRootPromise = ensureDeviceContinuityRootOnce().catch(function (error) {
      deviceRootPromise = null;
      throw error;
    });
    return deviceRootPromise;
  }

  function bindNodeToDeviceContinuity(node) {
    if (!node || !node.node_id) { return Promise.resolve(node); }
    return ensureDeviceContinuityRoot().then(function (continuity) {
      return openDb().then(function (db) {
        var bindingKey = BINDING_KEY_PREFIX + node.node_id;
        return getMeta(db, bindingKey).then(function (existing) {
          if (existing) {
            if (existing.device_continuity_id !== continuity.device_continuity_id) {
              throw new Error("FAIL_CLOSED: node is already bound to a different device continuity root");
            }
            db.close();
            return Object.assign({}, node, { device_continuity_id: continuity.device_continuity_id });
          }
          var binding = {
            schema: "stegos.web_device_node_binding.v1",
            device_continuity_id: continuity.device_continuity_id,
            node_id: node.node_id,
            bound_at: new Date().toISOString(),
            relation: "NODE_INSTANCE_BOUND_TO_DEVICE_CONTINUITY_ROOT",
            same_continuity_root: true,
            implicit_cross_root_continuation: false,
            authority_effect: "NONE"
          };
          return putMeta(db, bindingKey, binding).then(function () {
            return appendReceipt(db, {
              schema: "stegos.web_device_node_binding_receipt.v1",
              device_continuity_id: continuity.device_continuity_id,
              node_id: node.node_id,
              relation: binding.relation,
              sync_state: continuity.sync_state,
              cross_root_sync_performed: false,
              authority_effect: "NONE"
            });
          }).then(function () {
            db.close();
            return Object.assign({}, node, { device_continuity_id: continuity.device_continuity_id });
          });
        }).catch(function (error) { db.close(); throw error; });
      });
    });
  }

  function installContinuityLayer() {
    var api = root.StegOSWebBootstrap;
    if (!api || api.__deviceContinuityInstalled) { return; }
    var originalEstablish = api.establishNode;
    var originalRead = api.readExistingNode;
    var originalActivate = api.activateEcosystemChat;
    var originalExport = api.exportEvidence;

    api.establishNode = function () {
      return ensureDeviceContinuityRoot().then(function () { return originalEstablish(); }).then(function (state) {
        return bindNodeToDeviceContinuity(state.node).then(function (node) {
          state.node = node;
          return state;
        });
      });
    };

    api.readExistingNode = function () {
      return ensureDeviceContinuityRoot().then(function () { return originalRead(); }).then(function (node) {
        return bindNodeToDeviceContinuity(node);
      });
    };

    api.activateEcosystemChat = function () {
      return ensureDeviceContinuityRoot().then(function () { return originalActivate(); }).then(function (result) {
        return bindNodeToDeviceContinuity(result.node).then(function (node) {
          result.node = node;
          return result;
        });
      });
    };

    api.exportEvidence = function () {
      return ensureDeviceContinuityRoot().then(function (continuity) {
        return originalEstablish().then(function (state) {
          return bindNodeToDeviceContinuity(state.node).then(function () {
            return originalExport();
          }).then(function (bundle) {
            bundle.device_continuity = continuity;
            bundle.node_instance_id = bundle.node && bundle.node.node_id;
            bundle.device_continuity_id = continuity.device_continuity_id;
            bundle.continuity_semantics = {
              node_identity_is_device_identity: false,
              different_unsynced_device_continuity_roots_are_separate_chains: true,
              governed_transfer_required_for_cross_root_continuation: true,
              implicit_cross_root_continuation_allowed: false
            };
            return bundle;
          });
        });
      });
    };

    api.__deviceContinuityInstalled = true;
    root.StegOSDeviceContinuity = {
      ensureRoot: ensureDeviceContinuityRoot,
      readRoot: readDeviceContinuityRoot,
      bindNode: bindNodeToDeviceContinuity,
      semantics: {
        browser_node_identity_is_physical_device_identity: false,
        different_unsynced_roots_are_separate_chains: true,
        governed_transfer_required_for_cross_root_continuation: true,
        hardware_attestation_available_to_browser: false
      }
    };
  }

  function delay() {
    return new Promise(function (resolve) { root.setTimeout(resolve, RETRY_MS); });
  }

  function markReady(result, reused) {
    var evidence = result && result.evidence ? result.evidence : result;
    text("evidence-admission-state", reused ? "ADMITTED_DEVICE_LOCAL_REUSED" : "ADMITTED_DEVICE_LOCAL");
    text("admitted-inference-state", "READY");
    text("inference-state", "ADMITTED_STEGVERSE_DEVICE_LOCAL_ROUTE_READY");
    var button = document.getElementById("run-inference");
    if (button) { button.disabled = false; }
    var output = document.getElementById("evidence-admission-output");
    if (output && evidence) { output.textContent = JSON.stringify(evidence, null, 2); }
    return result;
  }

  function prepareWorker() {
    if (preparedWorker) { return preparedWorker; }
    preparedWorker = root.StegOSWebBootstrap.registerOfflineShell().then(function () {
      if (!(navigator.serviceWorker && navigator.serviceWorker.getRegistration)) { return null; }
      return navigator.serviceWorker.getRegistration().then(function (registration) {
        if (!registration || typeof registration.update !== "function") { return registration; }
        return registration.update().then(function () { return registration; }).catch(function () { return registration; });
      });
    });
    return preparedWorker;
  }

  function admittedDeviceLocalEvidence() {
    return root.StegOSAdmittedInference.readAdmittedInferenceEvidence().then(function (evidence) {
      if (
        evidence && evidence.state === "ADMITTED" &&
        evidence.endpoint === DEVICE_ENDPOINT &&
        evidence.endpoint_transport === "SERVICE_WORKER_LOCAL_INTERCEPT"
      ) {
        return evidence;
      }
      return null;
    });
  }

  function attempt(number) {
    if (number >= MAX_ATTEMPTS) {
      text("evidence-admission-state", "FAIL_CLOSED_DEVICE_LOCAL_BOOTSTRAP_TIMEOUT");
      text("admitted-inference-state", "WAITING_FOR_DEVICE_LOCAL_RUNTIME");
      return Promise.resolve(null);
    }

    return root.StegOSWebBootstrap.readExistingNode().then(function (node) {
      if (!node || !node.node_id) { throw new Error("DEVICE_LOCAL_NODE_NOT_ESTABLISHED_YET"); }
      return admittedDeviceLocalEvidence();
    }).then(function (existing) {
      if (existing) { return markReady(existing, true); }
      text("evidence-admission-state", "CHECKING_DEVICE_LOCAL");
      text("admitted-inference-state", "WAITING_FOR_DEVICE_LOCAL_RUNTIME");
      return prepareWorker().then(function () {
        return root.StegOSAdmittedInference.bootstrapDeviceLocalInferenceEvidence();
      }).then(function (result) { return markReady(result, false); });
    }).catch(function () {
      return delay().then(function () { return attempt(number + 1); });
    });
  }

  function start() {
    if (!root.StegOSWebBootstrap || !root.StegOSAdmittedInference) {
      text("evidence-admission-state", "FAIL_CLOSED_DEVICE_LOCAL_BOOTSTRAP_API_MISSING");
      return;
    }
    installContinuityLayer();
    ensureDeviceContinuityRoot().then(function () {
      return admittedDeviceLocalEvidence();
    }).then(function (existing) {
      if (existing) { return markReady(existing, true); }
      return attempt(0);
    }).catch(function () { return attempt(0); });
  }

  installContinuityLayer();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
}(window));
