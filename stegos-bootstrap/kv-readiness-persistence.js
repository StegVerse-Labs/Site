(function (root) {
  "use strict";

  var DB_NAME = "stegos-web-bootstrap-v1";
  var DB_VERSION = 1;
  var META_STORE = "meta";
  var STATE_KEY = "kv-readiness-device-state";
  var STATE_SCHEMA = "stegos.kv_device_readiness_state.v1";

  function canonicalize(value) {
    if (value === null || typeof value !== "object") { return JSON.stringify(value); }
    if (Array.isArray(value)) { return "[" + value.map(canonicalize).join(",") + "]"; }
    return "{" + Object.keys(value).sort().map(function (key) {
      return JSON.stringify(key) + ":" + canonicalize(value[key]);
    }).join(",") + "}";
  }

  function bytesToHex(bytes) {
    var out = "";
    for (var i = 0; i < bytes.length; i += 1) { out += bytes[i].toString(16).padStart(2, "0"); }
    return out;
  }

  function sha256(value) {
    if (!(root.crypto && root.crypto.subtle)) {
      return Promise.reject(new Error("FAIL_CLOSED: WebCrypto required for KV readiness persistence"));
    }
    return root.crypto.subtle.digest("SHA-256", new TextEncoder().encode(canonicalize(value))).then(function (digest) {
      return "sha256:" + bytesToHex(new Uint8Array(digest));
    });
  }

  function openDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = function () {
        var db = request.result;
        if (!db.objectStoreNames.contains(META_STORE)) {
          db.createObjectStore(META_STORE, { keyPath: "key" });
        }
      };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("KV readiness IndexedDB open failed")); };
      request.onblocked = function () { reject(new Error("KV readiness IndexedDB open blocked")); };
    });
  }

  function verifyState(state) {
    if (!state || state.schema !== STATE_SCHEMA) {
      return Promise.reject(new Error("unexpected KV device readiness state schema"));
    }
    if (state.transport_delivery_performed !== false ||
        state.interlock_delivery_admission_observed !== false ||
        state.kv_mutation_performed !== false ||
        state.activation_performed !== false ||
        state.provider_operation_authorized !== false ||
        state.execution_authority !== "NONE" ||
        state.authority_effect !== "NONE") {
      return Promise.reject(new Error("FAIL_CLOSED: KV readiness state violates non-authorizing boundary"));
    }
    if (!state.current_snapshot_sha256 || !state.current_shell_view ||
        state.current_shell_view.view_sha256 !== state.current_shell_view_sha256) {
      return Promise.reject(new Error("FAIL_CLOSED: KV readiness state shell/head binding invalid"));
    }
    if (!Number.isInteger(state.applied_update_count) || state.applied_update_count < 0) {
      return Promise.reject(new Error("FAIL_CLOSED: applied_update_count invalid"));
    }
    var body = Object.assign({}, state);
    var claimed = body.state_sha256;
    delete body.state_sha256;
    return sha256(body).then(function (actual) {
      if (claimed !== actual) { throw new Error("FAIL_CLOSED: KV readiness state digest mismatch"); }
      return state;
    });
  }

  function readState() {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(META_STORE, "readonly");
        var req = tx.objectStore(META_STORE).get(STATE_KEY);
        req.onsuccess = function () {
          var value = req.result ? req.result.value : null;
          db.close();
          if (!value) { resolve(null); return; }
          verifyState(value).then(resolve, reject);
        };
        req.onerror = function () {
          db.close();
          reject(req.error || new Error("KV readiness state read failed"));
        };
      });
    });
  }

  function initializeState(state) {
    return verifyState(state).then(function (verified) {
      return openDb().then(function (db) {
        return new Promise(function (resolve, reject) {
          var settled = false;
          var tx = db.transaction(META_STORE, "readwrite");
          var req = tx.objectStore(META_STORE).add({ key: STATE_KEY, value: verified });
          req.onerror = function (event) {
            if (req.error && req.error.name === "ConstraintError") {
              event.preventDefault();
              event.stopPropagation();
              var readReq = tx.objectStore(META_STORE).get(STATE_KEY);
              readReq.onsuccess = function () {
                var existing = readReq.result ? readReq.result.value : null;
                if (!existing || existing.current_snapshot_sha256 !== verified.current_snapshot_sha256) {
                  settled = true;
                  tx.abort();
                  reject(new Error("FAIL_CLOSED: readiness state already initialized to a different head"));
                }
              };
              return;
            }
            settled = true;
            reject(req.error || new Error("KV readiness initialization failed"));
          };
          tx.oncomplete = function () {
            db.close();
            if (!settled) { resolve(verified); }
          };
          tx.onerror = function () {
            db.close();
            if (!settled) { reject(tx.error || new Error("KV readiness initialization transaction failed")); }
          };
          tx.onabort = function () {
            db.close();
            if (!settled) { reject(tx.error || new Error("KV readiness initialization transaction aborted")); }
          };
        });
      });
    });
  }

  function replaceIfCurrent(expectedSnapshotSha256, nextState) {
    if (!expectedSnapshotSha256) {
      return Promise.reject(new Error("expected current readiness snapshot digest required"));
    }
    return verifyState(nextState).then(function (verifiedNext) {
      if (verifiedNext.last_prior_snapshot_sha256 !== expectedSnapshotSha256) {
        throw new Error("FAIL_CLOSED: successor state prior binding mismatch");
      }
      return openDb().then(function (db) {
        return new Promise(function (resolve, reject) {
          var tx = db.transaction(META_STORE, "readwrite");
          var store = tx.objectStore(META_STORE);
          var req = store.get(STATE_KEY);
          var accepted = false;
          req.onsuccess = function () {
            var current = req.result ? req.result.value : null;
            if (!current) {
              tx.abort();
              reject(new Error("FAIL_CLOSED: KV readiness state not initialized"));
              return;
            }
            verifyState(current).then(function () {
              if (current.current_snapshot_sha256 !== expectedSnapshotSha256) {
                tx.abort();
                reject(new Error("FAIL_CLOSED: stale/replayed readiness update"));
                return;
              }
              if (verifiedNext.applied_update_count !== current.applied_update_count + 1) {
                tx.abort();
                reject(new Error("FAIL_CLOSED: readiness update count discontinuity"));
                return;
              }
              if (verifiedNext.last_applied_envelope_sha256 &&
                  verifiedNext.last_applied_envelope_sha256 === current.last_applied_envelope_sha256) {
                tx.abort();
                reject(new Error("FAIL_CLOSED: readiness envelope replay"));
                return;
              }
              store.put({ key: STATE_KEY, value: verifiedNext });
              accepted = true;
            }).catch(function (error) {
              tx.abort();
              reject(error);
            });
          };
          req.onerror = function () {
            reject(req.error || new Error("KV readiness current-state read failed"));
          };
          tx.oncomplete = function () {
            db.close();
            if (accepted) { resolve(verifiedNext); }
          };
          tx.onerror = function () { db.close(); };
          tx.onabort = function () { db.close(); };
        });
      });
    });
  }

  root.StegOSKVReadinessPersistence = {
    schema: STATE_SCHEMA,
    stateKey: STATE_KEY,
    readState: readState,
    initializeState: initializeState,
    replaceIfCurrent: replaceIfCurrent,
    verifyState: verifyState
  };
}(window));
