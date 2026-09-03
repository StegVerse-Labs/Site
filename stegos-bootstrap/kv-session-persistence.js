(function (root) {
  "use strict";

  var DB_NAME = "stegos-web-bootstrap-v1";
  var DB_VERSION = 1;
  var META_STORE = "meta";
  var KEY_PREFIX = "kv-persistent-session-state:";
  var STATE_SCHEMA = "stegos.kv_persistent_session_state.v1";
  var PROJECTION_SCHEMA = "stegverse.kv.session-reconstruction-projection/v1";

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
      return Promise.reject(new Error("FAIL_CLOSED: WebCrypto required for KV session persistence"));
    }
    return root.crypto.subtle.digest(
      "SHA-256",
      new TextEncoder().encode(canonicalize(value))
    ).then(function (digest) {
      return "sha256:" + bytesToHex(new Uint8Array(digest));
    });
  }

  function validSha256(value) {
    return typeof value === "string" && /^sha256:[0-9a-f]{64}$/.test(value);
  }

  function validRoot(value) {
    return typeof value === "string" && /^[0-9a-f]{64}$/.test(value);
  }

  function validSessionId(value) {
    return typeof value === "string" && /^[A-Za-z0-9._-]{1,200}$/.test(value);
  }

  function keyFor(sessionId) {
    if (!validSessionId(sessionId)) { throw new Error("invalid persistent session id"); }
    return KEY_PREFIX + sessionId;
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
      request.onerror = function () {
        reject(request.error || new Error("KV session IndexedDB open failed"));
      };
      request.onblocked = function () {
        reject(new Error("KV session IndexedDB open blocked"));
      };
    });
  }

  function verifyState(state) {
    if (!state || state.schema !== STATE_SCHEMA) {
      return Promise.reject(new Error("unexpected persistent session state schema"));
    }
    if (!validSessionId(state.session_id) ||
        !Number.isInteger(state.generation) || state.generation < 0 ||
        !validSha256(state.current_head_sha256) ||
        typeof state.conversation_event_chain_ref !== "string" ||
        !state.conversation_event_chain_ref ||
        !validRoot(state.conversation_event_verification_root)) {
      return Promise.reject(new Error("FAIL_CLOSED: persistent session identity/head invalid"));
    }
    if (!state.current_projection ||
        state.current_projection.schema !== PROJECTION_SCHEMA ||
        state.current_projection.session_id !== state.session_id ||
        state.current_projection.generation !== state.generation ||
        state.current_projection.head_sha256 !== state.current_head_sha256 ||
        state.current_projection.conversation_event_chain_ref !== state.conversation_event_chain_ref ||
        state.current_projection.conversation_event_verification_root !== state.conversation_event_verification_root) {
      return Promise.reject(new Error("FAIL_CLOSED: persistent session projection binding invalid"));
    }
    if (state.current_projection.requires_live_verification !== true ||
        state.current_projection.stored_state_is_authority !== false ||
        state.current_projection.transcript_required !== false ||
        state.current_projection.execution_authority !== "NONE" ||
        state.current_projection.credential_authority !== "TV/TVC" ||
        state.current_projection.authority_effect !== "NONE") {
      return Promise.reject(new Error("FAIL_CLOSED: persistent session projection authority violation"));
    }
    if (state.requires_live_verification !== true ||
        state.live_verification_completed !== false ||
        state.kv_mutation_performed !== false ||
        state.activation_performed !== false ||
        state.provider_operation_authorized !== false ||
        state.execution_authority !== "NONE" ||
        state.credential_authority !== "TV/TVC" ||
        state.authority_effect !== "NONE") {
      return Promise.reject(new Error("FAIL_CLOSED: persistent session local authority violation"));
    }
    if (!Number.isInteger(state.applied_update_count) || state.applied_update_count < 0) {
      return Promise.reject(new Error("FAIL_CLOSED: persistent session update count invalid"));
    }

    var body = Object.assign({}, state);
    var claimed = body.state_sha256;
    delete body.state_sha256;
    return sha256(body).then(function (actual) {
      if (claimed !== actual) {
        throw new Error("FAIL_CLOSED: persistent session state digest mismatch");
      }
      return state;
    });
  }

  function readState(sessionId) {
    var key = keyFor(sessionId);
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(META_STORE, "readonly");
        var req = tx.objectStore(META_STORE).get(key);
        req.onsuccess = function () {
          var value = req.result ? req.result.value : null;
          db.close();
          if (!value) { resolve(null); return; }
          verifyState(value).then(resolve, reject);
        };
        req.onerror = function () {
          db.close();
          reject(req.error || new Error("KV session state read failed"));
        };
      });
    });
  }

  function initializeState(state) {
    return verifyState(state).then(function (verified) {
      var key = keyFor(verified.session_id);
      return openDb().then(function (db) {
        return new Promise(function (resolve, reject) {
          var settled = false;
          var tx = db.transaction(META_STORE, "readwrite");
          var store = tx.objectStore(META_STORE);
          var req = store.add({ key: key, value: verified });
          req.onerror = function (event) {
            if (req.error && req.error.name === "ConstraintError") {
              event.preventDefault();
              event.stopPropagation();
              var readReq = store.get(key);
              readReq.onsuccess = function () {
                var existing = readReq.result ? readReq.result.value : null;
                if (!existing ||
                    existing.generation !== verified.generation ||
                    existing.current_head_sha256 !== verified.current_head_sha256) {
                  settled = true;
                  tx.abort();
                  reject(new Error("FAIL_CLOSED: persistent session already initialized to different head"));
                }
              };
              return;
            }
            settled = true;
            reject(req.error || new Error("persistent session initialization failed"));
          };
          tx.oncomplete = function () {
            db.close();
            if (!settled) { resolve(verified); }
          };
          tx.onerror = function () {
            db.close();
            if (!settled) { reject(tx.error || new Error("persistent session transaction failed")); }
          };
          tx.onabort = function () {
            db.close();
            if (!settled) { reject(tx.error || new Error("persistent session transaction aborted")); }
          };
        });
      });
    });
  }

  function replaceIfNewer(expectedHeadSha256, nextState) {
    if (!validSha256(expectedHeadSha256)) {
      return Promise.reject(new Error("expected persistent session head digest required"));
    }
    return verifyState(nextState).then(function (verifiedNext) {
      var key = keyFor(verifiedNext.session_id);
      return openDb().then(function (db) {
        return new Promise(function (resolve, reject) {
          var tx = db.transaction(META_STORE, "readwrite");
          var store = tx.objectStore(META_STORE);
          var req = store.get(key);
          var accepted = false;
          req.onsuccess = function () {
            var current = req.result ? req.result.value : null;
            if (!current) {
              tx.abort();
              reject(new Error("FAIL_CLOSED: persistent session state not initialized"));
              return;
            }
            verifyState(current).then(function () {
              if (current.current_head_sha256 !== expectedHeadSha256) {
                tx.abort();
                reject(new Error("FAIL_CLOSED: stale persistent session update"));
                return;
              }
              if (verifiedNext.generation < current.generation) {
                tx.abort();
                reject(new Error("FAIL_CLOSED: persistent session generation rollback"));
                return;
              }
              if (verifiedNext.generation === current.generation) {
                if (verifiedNext.current_head_sha256 !== current.current_head_sha256) {
                  tx.abort();
                  reject(new Error("FAIL_CLOSED: same-generation persistent session fork"));
                  return;
                }
                accepted = true;
                return;
              }
              if (verifiedNext.applied_update_count !== current.applied_update_count + 1) {
                tx.abort();
                reject(new Error("FAIL_CLOSED: persistent session update-count discontinuity"));
                return;
              }
              store.put({ key: key, value: verifiedNext });
              accepted = true;
            }).catch(function (error) {
              tx.abort();
              reject(error);
            });
          };
          req.onerror = function () {
            reject(req.error || new Error("persistent session current-state read failed"));
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

  root.StegOSKVPersistentSessionPersistence = {
    schema: STATE_SCHEMA,
    readState: readState,
    initializeState: initializeState,
    replaceIfNewer: replaceIfNewer,
    verifyState: verifyState
  };
}(window));
