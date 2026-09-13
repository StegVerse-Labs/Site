"use strict";

(function (root) {
  var PROFILE_ID = "ERL_ACTIVE_RESEARCH_INTR_SAME_DEVICE_V1";
  var PACKAGE_URL = new URL("./workercoordinator-portable-device-kv.json", root.location.href).toString();

  function fail(reason) { throw new Error("FAIL_CLOSED: " + reason); }

  function readPortableState() {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(META_STORE, "readonly");
        var req = tx.objectStore(META_STORE).get(PORTABLE_WC_STATE_KEY);
        req.onsuccess = function () {
          var value = req.result ? req.result.value : null;
          db.close();
          resolve(value);
        };
        req.onerror = function () {
          var error = req.error || new Error("portable WorkerCoordinator state read failed");
          db.close();
          reject(error);
        };
      });
    });
  }

  function portableStateStoreForPackage(pkg) {
    return {
      read: readPortableState,
      atomicCompareAndSwap: function (expected, nextState) {
        return openDb().then(function (db) {
          return new Promise(function (resolve, reject) {
            var tx = db.transaction(META_STORE, "readwrite");
            var store = tx.objectStore(META_STORE);
            var req = store.get(PORTABLE_WC_STATE_KEY);
            var matched = false;
            req.onerror = function () { reject(req.error || new Error("portable WorkerCoordinator state CAS read failed")); };
            req.onsuccess = function () {
              var current = req.result ? req.result.value : null;
              if (current === null) {
                if (!root.StegVersePortableWorkerCoordinator || typeof root.StegVersePortableWorkerCoordinator.initialState !== "function") { return; }
                matched = canonicalize(expected) === canonicalize(root.StegVersePortableWorkerCoordinator.initialState(pkg));
              } else {
                matched = canonicalize(current) === canonicalize(expected);
              }
              if (matched) { store.put({ key: PORTABLE_WC_STATE_KEY, value: nextState }); }
            };
            tx.oncomplete = function () { db.close(); resolve(matched); };
            tx.onerror = function () {
              var error = tx.error || new Error("portable WorkerCoordinator state CAS failed");
              db.close();
              reject(error);
            };
            tx.onabort = function () {
              var error = tx.error || new Error("portable WorkerCoordinator state CAS aborted");
              db.close();
              reject(error);
            };
          });
        });
      }
    };
  }

  root.StegOSEcosystemChatServiceWorkerBridge = root.StegOSEcosystemChatServiceWorkerBridge || {};
  root.StegOSEcosystemChatServiceWorkerBridge.portableStateStoreForPackage = portableStateStoreForPackage;

  root.StegOSERLDeviceKVPackageReady = caches.open(CACHE_NAME).then(function (cache) {
    return cache.add(PACKAGE_URL).then(function () { return true; });
  }).catch(function () { return false; });
}(self));

importScripts("./site-browser-intr-connectors.js");
importScripts("./erl-active-research-resident-task-extension.js");

(function (root) {
  var PROFILE_ID = "ERL_ACTIVE_RESEARCH_INTR_SAME_DEVICE_V1";
  if (!root.StegOSExternalResidentTask || typeof root.StegOSExternalResidentTask.execute !== "function") {
    throw new Error("FAIL_CLOSED: existing resident-task dispatcher unavailable");
  }
  var priorExecute = root.StegOSExternalResidentTask.execute;
  root.StegOSExternalResidentTask.execute = function (envelope, api) {
    if (!envelope || envelope.profile_id !== PROFILE_ID) { return priorExecute(envelope, api); }
    return Promise.resolve(root.StegOSERLDeviceKVPackageReady).then(function (ready) {
      if (ready !== true) { throw new Error("FAIL_CLOSED: DEVICE_KV portable package cache failed"); }
      return priorExecute(envelope, api);
    });
  };
}(self));
