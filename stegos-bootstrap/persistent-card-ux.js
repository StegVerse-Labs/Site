(function (root) {
  "use strict";

  var DB_NAME = "stegos-web-bootstrap-v1";
  var DB_VERSION = 1;
  var META_STORE = "meta";
  var RECEIPT_STORE = "receipts";
  var CARD_KEY_PREFIX = "ui-card-state:";
  var SV001_TASK_ID = "SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001";

  var HELP = {
    "Authority boundary": "./help/authority-boundary.html",
    "Current iPhone interaction coordinator": "./help/interaction-coordinator.html",
    "Runtime capability": "./help/runtime-capability.html",
    "Node": "./help/node.html",
    "Ecosystem Chat": "./help/ecosystem-chat.html",
    "Canonical inference evidence": "./help/canonical-inference-evidence.html",
    "Admitted inference": "./help/admitted-inference.html",
    "StegVerse-001 bounded autonomy": "./help/sv001-bounded-autonomy.html",
    "Master Records — completed SV001 custody": "./help/master-records-sv001.html",
    "Continuity": "./help/continuity.html",
    "Offline shell": "./help/offline-shell.html"
  };

  function openDb() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = function () {
        var db = request.result;
        if (!db.objectStoreNames.contains(META_STORE)) { db.createObjectStore(META_STORE, { keyPath: "key" }); }
        if (!db.objectStoreNames.contains(RECEIPT_STORE)) { db.createObjectStore(RECEIPT_STORE, { keyPath: "sequence" }); }
      };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error || new Error("persistent card state IndexedDB open failed")); };
      request.onblocked = function () { reject(new Error("persistent card state IndexedDB open blocked")); };
    });
  }

  function getMeta(db, key) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(META_STORE, "readonly");
      var req = tx.objectStore(META_STORE).get(key);
      req.onsuccess = function () { resolve(req.result ? req.result.value : null); };
      req.onerror = function () { reject(req.error || new Error("persistent card state read failed")); };
    });
  }

  function putMeta(db, key, value) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(META_STORE, "readwrite");
      tx.objectStore(META_STORE).put({ key: key, value: value });
      tx.oncomplete = function () { resolve(value); };
      tx.onerror = function () { reject(tx.error || new Error("persistent card state write failed")); };
      tx.onabort = function () { reject(tx.error || new Error("persistent card state write aborted")); };
    });
  }

  function getAllMeta(db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(META_STORE, "readonly");
      var req = tx.objectStore(META_STORE).getAll();
      req.onsuccess = function () { resolve(req.result || []); };
      req.onerror = function () { reject(req.error || new Error("persistent card metadata scan failed")); };
    });
  }

  function getReceipts(db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction(RECEIPT_STORE, "readonly");
      var req = tx.objectStore(RECEIPT_STORE).getAll();
      req.onsuccess = function () { resolve(req.result || []); };
      req.onerror = function () { reject(req.error || new Error("persistent card journal scan failed")); };
    });
  }

  function cardId(section, index) {
    if (section.dataset.cardId) { return section.dataset.cardId; }
    var titleNode = section.querySelector("strong");
    var title = titleNode ? titleNode.textContent.trim() : "card-" + index;
    var id = title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "card-" + index;
    section.dataset.cardId = id;
    return id;
  }

  function titleOf(section) {
    var title = section.querySelector("strong");
    return title ? title.textContent.trim() : "";
  }

  function readField(node) {
    if (node.tagName === "TEXTAREA" || node.tagName === "INPUT") { return node.value; }
    return node.textContent;
  }

  function writeField(node, value) {
    if (node.tagName === "TEXTAREA" || node.tagName === "INPUT") { node.value = value; }
    else { node.textContent = value; }
  }

  function collect(section) {
    var fields = {};
    section.querySelectorAll("[id]").forEach(function (node) {
      if (node.tagName === "BUTTON") { return; }
      fields[node.id] = readField(node);
    });
    return fields;
  }

  function restore(section, snapshot) {
    if (!snapshot || !snapshot.fields) { return; }
    Object.keys(snapshot.fields).forEach(function (id) {
      var node = document.getElementById(id);
      if (node && section.contains(node) && snapshot.fields[id] !== undefined && snapshot.fields[id] !== null) {
        writeField(node, snapshot.fields[id]);
      }
    });
    if (snapshot.completed === true) { section.dataset.persistedCompleted = "true"; }
  }

  function textById(id) {
    var node = document.getElementById(id);
    return node ? String(node.textContent || "").trim() : "";
  }

  function isCompleted(section) {
    var title = titleOf(section);
    if (title === "Authority boundary") { return true; }
    if (title === "Current iPhone interaction coordinator") {
      return !/^HOLD_|^FAIL_|^BLOCKED|^ERROR/.test(textById("interaction-guard-state")) && textById("interaction-guard-state") !== "";
    }
    if (title === "Runtime capability") { return textById("operational-readiness") === "READY"; }
    if (title === "Node") { return textById("node-state") === "ESTABLISHED"; }
    if (title === "Ecosystem Chat") { return /ACTIVATED|ACTIVE/.test(textById("chat-state")); }
    if (title === "Canonical inference evidence") { return /^ADMITTED/.test(textById("evidence-admission-state")); }
    if (title === "Admitted inference") { return /^PASS/.test(textById("admitted-inference-state")); }
    if (title === "StegVerse-001 bounded autonomy") { return /^COMPLETED/.test(textById("sv001-state")); }
    if (title === "Master Records — completed SV001 custody") { return /^PASS/.test(textById("mr-sv001-state")); }
    if (title === "Continuity") { return /^PASS/.test(textById("replay-state")); }
    if (title === "Offline shell") { return /^REGISTERED/.test(textById("offline-state")); }
    return section.dataset.persistedCompleted === "true";
  }

  function paint(section) {
    var complete = isCompleted(section);
    section.classList.toggle("card-complete", complete);
    section.classList.toggle("card-incomplete", !complete);
    section.dataset.cardState = complete ? "complete" : "incomplete";
  }

  function persist(section, index) {
    var id = cardId(section, index);
    var snapshot = {
      schema: "stegos.same-device-card-snapshot/v1",
      card_id: id,
      title: titleOf(section),
      completed: isCompleted(section),
      fields: collect(section),
      persisted_at: new Date().toISOString(),
      authority_effect: "NONE"
    };
    return openDb().then(function (db) {
      return putMeta(db, CARD_KEY_PREFIX + id, snapshot).then(function () { db.close(); return snapshot; });
    });
  }

  function copyText(text, button) {
    function done() {
      var prior = button.textContent;
      button.textContent = "Copied";
      root.setTimeout(function () { button.textContent = prior; }, 1200);
    }
    function fallback() {
      var field = document.createElement("textarea");
      field.value = text;
      field.setAttribute("readonly", "");
      field.style.position = "fixed";
      field.style.opacity = "0";
      document.body.appendChild(field);
      field.focus(); field.select(); field.setSelectionRange(0, field.value.length);
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (error) { ok = false; }
      document.body.removeChild(field);
      if (ok) { done(); }
    }
    if (!text) { return; }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(fallback);
    } else { fallback(); }
  }

  function addCopyButton(node) {
    if (!node.id || node.dataset.copyControlInstalled === "true") { return; }
    node.dataset.copyControlInstalled = "true";
    var button = document.createElement("button");
    button.type = "button";
    button.className = "copy-text-button";
    button.textContent = "Copy Text";
    button.setAttribute("aria-label", "Copy " + node.id + " text");
    button.addEventListener("click", function () { copyText(readField(node), button); });
    node.insertAdjacentElement("afterend", button);
  }

  function addHelp(section) {
    var title = titleOf(section);
    var href = HELP[title];
    if (!href || section.querySelector(".card-help-link")) { return; }
    var link = document.createElement("a");
    link.className = "card-help-link";
    link.href = href;
    link.textContent = "Purpose / remediation / troubleshooting";
    link.setAttribute("aria-label", title + " help");
    section.appendChild(link);
  }

  function installStyles() {
    if (document.getElementById("persistent-card-ux-style")) { return; }
    var style = document.createElement("style");
    style.id = "persistent-card-ux-style";
    style.textContent = [
      "section{border-width:2px!important;transition:border-color .18s ease,box-shadow .18s ease}",
      "section.card-complete{border-color:#2fbf71!important;box-shadow:0 0 0 1px rgba(47,191,113,.18)}",
      "section.card-incomplete{border-color:#d94b4b!important;box-shadow:0 0 0 1px rgba(217,75,75,.12)}",
      ".card-help-link{display:inline-block;margin-top:10px;font-size:.88rem}",
      ".copy-text-button{font-size:.88rem;padding:8px 10px;margin-top:6px}",
      "section[data-persisted-completed='true']::before{content:'Completed data retained on this device';display:block;font-size:.75rem;font-weight:700;margin-bottom:8px;opacity:.78}"
    ].join("");
    document.head.appendChild(style);
  }

  function scanTerminalSv001() {
    return openDb().then(function (db) {
      return Promise.all([getAllMeta(db), getReceipts(db)]).then(function (parts) {
        db.close();
        var meta = parts[0];
        var receipts = parts[1];
        var terminal = false;
        meta.forEach(function (row) {
          var value = row && row.value;
          if (value && value.task_id === SV001_TASK_ID && value.state === "COMPLETED") { terminal = true; }
        });
        receipts.forEach(function (entry) {
          var receipt = entry && entry.receipt;
          if (receipt && receipt.task_id === SV001_TASK_ID && receipt.transition_id === "SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED" && receipt.state === "COMPLETED") { terminal = true; }
        });
        return terminal;
      });
    });
  }

  function findStoredSv001Proof() {
    return openDb().then(function (db) {
      return getMeta(db, CARD_KEY_PREFIX + "stegverse-001-bounded-autonomy").then(function (snapshot) {
        db.close();
        if (!snapshot || !snapshot.fields || !snapshot.fields["sv001-output"]) { return null; }
        try {
          var proof = JSON.parse(snapshot.fields["sv001-output"]);
          if (proof && proof.schema === "stegos.workercoordinator_tvc_portable_sv001_execution_proof/v1" && proof.state === "COMPLETED" && proof.subordinate_execution_proof && proof.subordinate_execution_proof.cycle_receipt) { return proof; }
        } catch (error) {}
        return null;
      });
    });
  }

  function applySv001Continuity() {
    var state = document.getElementById("sv001-state");
    var button = document.getElementById("run-sv001");
    var output = document.getElementById("sv001-output");
    return scanTerminalSv001().then(function (terminal) {
      if (!terminal) { return null; }
      if (state) { state.textContent = "COMPLETED — TERMINAL"; }
      if (button) { button.disabled = true; button.textContent = "SV001 Cycle Completed"; }
      return findStoredSv001Proof().then(function (proof) {
        if (proof) {
          if (output && !output.textContent.trim()) { output.textContent = JSON.stringify(proof, null, 2); }
          var mrInput = document.getElementById("mr-sv001-receipt");
          var mrState = document.getElementById("mr-sv001-state");
          if (mrInput && !mrInput.value.trim()) { mrInput.value = JSON.stringify(proof, null, 2); }
          if (mrState && !/^PASS/.test(mrState.textContent)) { mrState.textContent = "READY_FROM_SAME_DEVICE_SV001_PROOF"; }
        } else if (output && !output.textContent.trim()) {
          output.textContent = "Terminal SV001 execution is recorded on this device. The exact full proof predates persistent-card retention, so rerun is prohibited. Use the Master Records manual import fallback once if the exact immutable proof is not otherwise present on this device.";
        }
        return proof;
      });
    });
  }

  function install() {
    if (!root.indexedDB || document.documentElement.dataset.persistentCardUxInstalled === "true") { return; }
    document.documentElement.dataset.persistentCardUxInstalled = "true";
    installStyles();
    var sections = Array.prototype.slice.call(document.querySelectorAll("section"));

    Promise.all(sections.map(function (section, index) {
      addHelp(section);
      section.querySelectorAll("textarea,pre").forEach(addCopyButton);
      return openDb().then(function (db) {
        return getMeta(db, CARD_KEY_PREFIX + cardId(section, index)).then(function (snapshot) {
          db.close();
          restore(section, snapshot);
          paint(section);
        });
      }).catch(function () { paint(section); });
    })).then(function () { return applySv001Continuity(); }).then(function () {
      sections.forEach(paint);
    });

    sections.forEach(function (section, index) {
      var timer = null;
      var observer = new MutationObserver(function () {
        paint(section);
        root.clearTimeout(timer);
        timer = root.setTimeout(function () { persist(section, index).catch(function () {}); }, 120);
      });
      observer.observe(section, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ["value"] });
      section.addEventListener("input", function () {
        paint(section);
        root.clearTimeout(timer);
        timer = root.setTimeout(function () { persist(section, index).catch(function () {}); }, 120);
      });
      section.addEventListener("click", function () {
        root.setTimeout(function () { paint(section); persist(section, index).catch(function () {}); }, 250);
      });
    });
  }

  root.StegOSPersistentCardUX = {
    install: install,
    persistCard: function (cardIdValue, snapshot) {
      return openDb().then(function (db) { return putMeta(db, CARD_KEY_PREFIX + cardIdValue, snapshot).then(function () { db.close(); return snapshot; }); });
    },
    readCard: function (cardIdValue) {
      return openDb().then(function (db) { return getMeta(db, CARD_KEY_PREFIX + cardIdValue).then(function (value) { db.close(); return value; }); });
    },
    findStoredSv001Proof: findStoredSv001Proof
  };

  if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", install); }
  else { install(); }
}(window));
