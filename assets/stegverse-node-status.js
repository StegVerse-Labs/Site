(function (root) {
  "use strict";

  var DB_NAME = "stegos-node-v1";
  var CLASSES = {
    UNSELECTED: { label: "Unselected Node", resident: false, selectable: false },
    PRIVATE_SOVEREIGN: { label: "Private Sovereign Node", resident: false, selectable: true },
    MAIN_ECOSYSTEM: { label: "Main Ecosystem Node", resident: false, selectable: true },
    PRIVATE_SOVEREIGN_STEGOS: { label: "Private Sovereign StegOS Node", resident: true, selectable: true },
    ECOSYSTEM_SOVEREIGN_STEGOS: { label: "Ecosystem Sovereign StegOS Node", resident: true, selectable: false }
  };

  function emptyState(reason) {
    return {
      node_id: null,
      continuity_established: false,
      requested_node_class: "UNSELECTED",
      class_established: false,
      display_node_class: "UNSELECTED",
      display_label: CLASSES.UNSELECTED.label,
      reason: reason
    };
  }

  function classLabel(id) {
    return CLASSES[id] ? CLASSES[id].label : CLASSES.UNSELECTED.label;
  }

  function nodeClassReceipts(receipts) {
    return (receipts || []).filter(function (receipt) {
      return receipt && receipt.schema === "stegos.node_capability_receipt.v1" && receipt.capability === "node-class";
    });
  }

  function passiveDatabaseExists() {
    if (!root.indexedDB) return Promise.resolve(false);
    if (typeof root.indexedDB.databases !== "function") {
      /* Fail passive: never open/create IndexedDB merely to discover whether a Node exists. */
      return Promise.resolve(false);
    }
    return root.indexedDB.databases().then(function (databases) {
      return (databases || []).some(function (db) { return db && db.name === DB_NAME; });
    }).catch(function () { return false; });
  }

  function resolveExisting() {
    if (!root.StegVerseNodeContinuity || typeof root.StegVerseNodeContinuity.status !== "function") {
      return Promise.resolve(emptyState("NODE_CONTINUITY_UNAVAILABLE"));
    }
    return passiveDatabaseExists().then(function (exists) {
      if (!exists) return emptyState("NO_PASSIVELY_DISCOVERABLE_EXISTING_NODE");
      return root.StegVerseNodeContinuity.status().then(function (current) {
        if (!current.registered) return emptyState("EXISTING_NODE_DB_WITHOUT_REGISTRATION");
        var classReceipts = nodeClassReceipts(current.receipts);
        var latest = classReceipts.length ? classReceipts[classReceipts.length - 1] : null;
        var requested = latest && CLASSES[latest.resulting_state] ? latest.resulting_state : "UNSELECTED";
        var established = requested === "UNSELECTED" || !!(latest && latest.transition === "NODE_CLASS_ESTABLISHED");
        return {
          node_id: current.registration.node_id,
          continuity_established: true,
          requested_node_class: requested,
          class_established: established,
          display_node_class: requested,
          display_label: classLabel(requested),
          registration: current.registration,
          receipts: current.receipts,
          reason: established ? "EXISTING_NODE_AND_CLASS_RESOLVED" : "CLASS_REQUESTED_PREDICATES_PENDING"
        };
      });
    }).catch(function (error) {
      return emptyState("FAIL_CLOSED:" + String(error && error.message || error));
    });
  }

  function explicitConnect() {
    if (!root.StegVerseNodeContinuity || typeof root.StegVerseNodeContinuity.registerDevice !== "function") {
      return Promise.reject(new Error("Node continuity registration is unavailable"));
    }
    /* This is the mutating path and must only be invoked from an explicit user action. */
    return root.StegVerseNodeContinuity.registerDevice().then(function () {
      return root.StegVerseNodeContinuity.status();
    }).then(function (current) {
      return {
        node_id: current.registration.node_id,
        continuity_established: true,
        requested_node_class: "UNSELECTED",
        class_established: true,
        display_node_class: "UNSELECTED",
        display_label: CLASSES.UNSELECTED.label,
        registration: current.registration,
        receipts: current.receipts,
        reason: "EXPLICIT_NODE_ESTABLISHMENT_COMPLETED"
      };
    });
  }

  function explicitSelectNodeClass(classId) {
    classId = String(classId || "").toUpperCase();
    if (!CLASSES[classId] || classId === "UNSELECTED") return Promise.reject(new Error("Invalid selectable Node class"));
    if (classId === "ECOSYSTEM_SOVEREIGN_STEGOS") return Promise.reject(new Error("ECOSYSTEM_ELIGIBILITY_REQUIRED"));
    if (!root.StegVerseNodeContinuity || typeof root.StegVerseNodeContinuity.appendCapabilityReceipt !== "function") {
      return Promise.reject(new Error("Node continuity capability receipts are unavailable"));
    }
    return resolveExisting().then(function (current) {
      if (!current.continuity_established) throw new Error("CONNECT_NODE_REQUIRED");
      var transition = CLASSES[classId].resident ? "NODE_CLASS_REQUESTED" : "NODE_CLASS_ESTABLISHED";
      return root.StegVerseNodeContinuity.appendCapabilityReceipt({
        transition: transition,
        capability: "node-class",
        step: "class-selection",
        resulting_state: classId,
        evidence_ref: "stegverse.node_status_contract.v1"
      });
    }).then(function () { return resolveExisting(); });
  }

  function renderStatus(target, state, options) {
    options = options || {};
    if (!target) return;
    var established = state.continuity_established && state.class_established;
    var text = state.display_label + (established ? " established." : " not established.");
    target.classList.remove("established", "not-established", "checking");
    target.classList.add(established ? "established" : "not-established");
    var textNode = target.querySelector("[data-node-status-text]");
    if (textNode) textNode.textContent = text;
    var detail = target.querySelector("[data-node-status-detail]");
    if (detail) {
      detail.textContent = state.continuity_established
        ? (state.class_established ? "Existing Node continuity and class state verified." : "Node continuity exists; selected class still requires its establishment predicates.")
        : "No Node has been established in this browser context.";
    }
    var connect = target.querySelector("[data-node-connect]");
    if (connect) connect.hidden = state.continuity_established;
    target.dataset.nodeClass = state.display_node_class;
    target.dataset.nodeEstablished = established ? "true" : "false";
  }

  function bindHeader(target, options) {
    options = options || {};
    function refresh() {
      return resolveExisting().then(function (state) {
        renderStatus(target, state, options);
        if (typeof options.onResolved === "function") options.onResolved(state);
        return state;
      });
    }
    var connect = target && target.querySelector("[data-node-connect]");
    if (connect) {
      connect.addEventListener("click", function () {
        connect.disabled = true;
        explicitConnect().then(function (state) {
          renderStatus(target, state, options);
          if (typeof options.onResolved === "function") options.onResolved(state);
        }).catch(function (error) {
          var detail = target.querySelector("[data-node-status-detail]");
          if (detail) detail.textContent = "Node connection failed: " + String(error && error.message || error);
        }).finally(function () { connect.disabled = false; });
      });
    }
    return refresh();
  }

  root.StegVerseNodeStatus = {
    contract_version: "1.0.0",
    classes: CLASSES,
    resolveExisting: resolveExisting,
    explicitConnect: explicitConnect,
    explicitSelectNodeClass: explicitSelectNodeClass,
    renderStatus: renderStatus,
    bindHeader: bindHeader
  };
})(window);
