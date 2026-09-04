"use strict";

(function (root) {
  var MANIFEST_URL = "./current-ios-interaction-manifest.json";
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
  var manifest = null;

  function byId(id) { return document.getElementById(id); }
  function isMutationControl(node) {
    return !!(node && node.id && MUTATION_IDS.indexOf(node.id) !== -1);
  }
  function permittedMutationId() {
    if (!manifest || manifest.state !== "ADMITTED_SINGLE_ACTION") { return null; }
    return manifest.enabled_mutation_control_id || null;
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
    READ_ONLY_IDS.forEach(function (id) {
      var el = byId(id);
      if (el) { el.dataset.interactionGuard = "READ_ONLY"; }
    });
    var state = byId("interaction-guard-state");
    var action = byId("interaction-guard-action");
    if (state) { state.textContent = manifest ? manifest.state : "HOLD_MANIFEST_UNAVAILABLE"; }
    if (action) { action.textContent = allowed || "NONE — READ ONLY"; }
  }
  function blockUnadmitted(event) {
    var node = event.target;
    if (!isMutationControl(node)) { return; }
    if (node.id === permittedMutationId()) { return; }
    event.preventDefault();
    event.stopImmediatePropagation();
    applyGuard();
  }
  function loadManifest() {
    return fetch(MANIFEST_URL, { cache: "no-store" }).then(function (response) {
      if (!response.ok) { throw new Error("interaction manifest unavailable"); }
      return response.json();
    }).then(function (value) {
      manifest = value;
      applyGuard();
      return value;
    }).catch(function () {
      manifest = null;
      applyGuard();
      return null;
    });
  }

  document.addEventListener("click", blockUnadmitted, true);
  document.addEventListener("touchend", blockUnadmitted, true);
  new MutationObserver(function () { applyGuard(); }).observe(document.documentElement, { attributes: true, subtree: true, attributeFilter: ["disabled"] });
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { applyGuard(); loadManifest(); });
  } else {
    applyGuard();
    loadManifest();
  }

  root.StegOSCurrentIOSInteractionGuard = {
    reload: loadManifest,
    apply: applyGuard,
    mutationControlIds: MUTATION_IDS.slice(),
    readOnlyControlIds: READ_ONLY_IDS.slice()
  };
}(typeof self !== "undefined" ? self : globalThis));
