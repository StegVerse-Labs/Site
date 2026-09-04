"use strict";

(function (root) {
  var MANIFEST_URL = "./current-ios-interaction-manifest.json";
  var MANIFEST_SCHEMA = "stegverse.site-current-ios-interaction-manifest/v1";
  var GUARDED_WORKER_URL = "./service-worker.js?current_ios_guard=991";
  var MUTATION_IDS = [
    "establish",
    "activate-chat",
    "admit-evidence",
    "run-inference",
    "run-de006-inference",
    "run-sv001",
    "commit-mr-sv001"
  ];
  var READ_ONLY_IDS = ["replay", "evidence", "copy-evidence"];
  var INPUT_BINDINGS = {
    "canonical-evidence": ["admit-evidence"],
    "inference-prompt": ["run-inference", "run-de006-inference"],
    "mr-sv001-receipt": ["commit-mr-sv001"]
  };
  var manifest = null;
  var localFailClosedReason = null;
  var consumedActionId = null;

  function byId(id) { return document.getElementById(id); }
  function isMutationControl(node) {
    return !!(node && node.id && MUTATION_IDS.indexOf(node.id) !== -1);
  }
  function validateManifest(value) {
    if (!value || value.schema !== MANIFEST_SCHEMA) { throw new Error("interaction manifest schema mismatch"); }
    if (value.authority_effect !== "NONE_UI_SERIALIZATION_ONLY") { throw new Error("interaction manifest authority widening"); }
    if (value.credential_authority !== "TV/TVC" || value.github_token_runtime_authority !== "NONE") {
      throw new Error("interaction manifest credential boundary drift");
    }
    if (value.state === "ADMITTED_SINGLE_ACTION") {
      if (!value.active_action_id || !value.enabled_mutation_control_id) { throw new Error("admitted interaction missing exact action/control"); }
      if (MUTATION_IDS.indexOf(value.enabled_mutation_control_id) === -1) { throw new Error("admitted interaction control is not recognized"); }
    } else if (value.enabled_mutation_control_id || value.active_action_id) {
      throw new Error("non-admitted interaction manifest exposes mutation");
    }
    return value;
  }
  function permittedMutationId() {
    if (localFailClosedReason || !manifest || manifest.state !== "ADMITTED_SINGLE_ACTION") { return null; }
    if (consumedActionId && consumedActionId === manifest.active_action_id) { return null; }
    return manifest.enabled_mutation_control_id || null;
  }
  function inputAllowed(bindings, allowed) {
    return !!allowed && bindings.indexOf(allowed) !== -1;
  }
  function applyGuard() {
    var allowed = permittedMutationId();
    MUTATION_IDS.forEach(function (id) {
      var el = byId(id);
      if (!el) { return; }
      el.disabled = id !== allowed;
      el.setAttribute("aria-disabled", id === allowed ? "false" : "true");
      el.dataset.interactionGuard = id === allowed ? "ADMITTED" : "BLOCKED";
    });
    Object.keys(INPUT_BINDINGS).forEach(function (id) {
      var el = byId(id);
      if (!el) { return; }
      var writable = inputAllowed(INPUT_BINDINGS[id], allowed);
      el.readOnly = !writable;
      el.setAttribute("aria-readonly", writable ? "false" : "true");
      el.dataset.interactionGuard = writable ? "ADMITTED_INPUT" : "READ_ONLY_BLOCKED";
    });
    READ_ONLY_IDS.forEach(function (id) {
      var el = byId(id);
      if (el) { el.dataset.interactionGuard = "READ_ONLY"; }
    });
    var state = byId("interaction-guard-state");
    var action = byId("interaction-guard-action");
    if (state) {
      state.textContent = localFailClosedReason ? "LOCAL_FAIL_CLOSED" : (manifest ? manifest.state : "HOLD_MANIFEST_UNAVAILABLE");
    }
    if (action) {
      action.textContent = localFailClosedReason ? ("NONE — " + localFailClosedReason) : (allowed || "NONE — READ ONLY");
    }
  }
  function blockUnadmitted(event) {
    var node = event.target;
    if (!isMutationControl(node)) { return; }
    var allowed = permittedMutationId();
    if (node.id !== allowed) {
      event.preventDefault();
      event.stopImmediatePropagation();
      applyGuard();
      return;
    }
    if (event.type === "click") {
      consumedActionId = manifest.active_action_id;
      root.setTimeout(applyGuard, 0);
    }
  }
  function failClosed(reason) {
    localFailClosedReason = String(reason || "LOCAL_GUARD_FAILURE");
    applyGuard();
  }
  function refreshGuardedWorker() {
    if (!(navigator.serviceWorker && navigator.serviceWorker.register)) { return Promise.resolve(null); }
    return navigator.serviceWorker.register(GUARDED_WORKER_URL, { scope: "./" }).then(function (registration) {
      if (registration && typeof registration.update === "function") {
        return registration.update().then(function () { return registration; }).catch(function () { return registration; });
      }
      return registration;
    }).catch(function (error) {
      failClosed("SERVICE_WORKER_GUARD_REFRESH_FAILED");
      return null;
    });
  }
  function loadManifest() {
    var requestUrl = MANIFEST_URL + "?interaction_guard_ts=" + Date.now();
    return fetch(requestUrl, { cache: "no-store", credentials: "same-origin" }).then(function (response) {
      if (!response.ok) { throw new Error("interaction manifest unavailable"); }
      return response.json();
    }).then(function (value) {
      value = validateManifest(value);
      if (!manifest || value.active_action_id !== manifest.active_action_id) {
        consumedActionId = null;
      }
      manifest = value;
      localFailClosedReason = null;
      applyGuard();
      return refreshGuardedWorker().then(function () { return value; });
    }).catch(function (error) {
      manifest = null;
      localFailClosedReason = String(error && error.message ? error.message : error);
      applyGuard();
      return null;
    });
  }

  document.addEventListener("click", blockUnadmitted, true);
  document.addEventListener("touchend", blockUnadmitted, true);
  new MutationObserver(function () { applyGuard(); }).observe(document.documentElement, {
    attributes: true,
    subtree: true,
    attributeFilter: ["disabled", "readonly"]
  });
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { applyGuard(); loadManifest(); });
  } else {
    applyGuard();
    loadManifest();
  }

  root.StegOSCurrentIOSInteractionGuard = {
    reload: loadManifest,
    apply: applyGuard,
    failClosed: failClosed,
    refreshGuardedWorker: refreshGuardedWorker,
    mutationControlIds: MUTATION_IDS.slice(),
    readOnlyControlIds: READ_ONLY_IDS.slice(),
    inputBindings: JSON.parse(JSON.stringify(INPUT_BINDINGS))
  };
}(typeof self !== "undefined" ? self : globalThis));
