"use strict";

(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.StegVerseServiceState = api;
}(typeof globalThis !== "undefined" ? globalThis : this, function () {
  var COLORS = {
    ACTIVE: "GREEN",
    REVIEW: "YELLOW",
    UNAVAILABLE: "RED",
    INACTIVE: "GRAY"
  };

  function result(state, reason, requiredAction) {
    return {
      service_state: state,
      color: COLORS[state],
      reason: reason,
      required_action: requiredAction || null,
      authority_effect: "NONE",
      activation_performed: false
    };
  }

  function classify(entry, context) {
    var registrationVerified = !!(context && context.registration_verified);
    var runtimeActivated = !!(context && context.production_interlock_runtime_activated);
    if (!registrationVerified) {
      return result("REVIEW", "Receipt #1 device continuity is required", "REGISTER DEVICE");
    }
    if (!entry || entry.entry_type !== "SERVICE" || typeof entry.entry_id !== "string") {
      return result("UNAVAILABLE", "Canonical service readiness is unavailable");
    }
    if (entry.authority_effect !== "NONE" || entry.activation_performed !== false) {
      return result("UNAVAILABLE", "Readiness source violated the non-authority boundary");
    }
    if (!Array.isArray(entry.governed_blockers)) {
      return result("UNAVAILABLE", "Governed blocker evidence is invalid");
    }
    if (entry.governed_action_readiness === "READY_FOR_GOVERNED_ACTION") {
      if (!runtimeActivated || entry.governed_blockers.length) {
        return result("UNAVAILABLE", "Governed-ready evidence is inconsistent");
      }
      return result("ACTIVE", "Activated in KV and governed action prerequisites are satisfied");
    }
    if (entry.governed_action_readiness !== "BLOCKED") {
      return result("UNAVAILABLE", "Governed readiness state is unknown");
    }
    if (entry.governed_blockers.indexOf("current_identity_continuity_receipt_observed") >= 0 ||
        entry.local_materialization === "BLOCKED_CURRENT_IDENTITY") {
      return result("REVIEW", "Device or identity continuity must be re-established", "RE-REGISTER DEVICE");
    }
    if (typeof entry.local_materialization !== "string" ||
        entry.local_materialization.indexOf("BLOCKED_") === 0) {
      return result("UNAVAILABLE", "Service is not presently available on this node");
    }
    return result("INACTIVE", "Service is available but not activated in this KnowledgeVault", "OPEN GOVERNED SETUP");
  }

  return {
    COLORS: Object.freeze(COLORS),
    classify: classify
  };
}));
