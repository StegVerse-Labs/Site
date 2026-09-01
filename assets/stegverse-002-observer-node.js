(() => {
  "use strict";

  const CONFIG_URL = "data/stegverse-002-experiment.json";
  const VIEWER_NODE_STORAGE_KEY = "stegverse.viewer_node.v1";
  const PAIR_STORAGE_PREFIX = "stegverse.viewer_experiment_pair.v1:";
  const RECEIPT_STORAGE_PREFIX = "stegverse.viewer_node_receipt.v1:";

  function byId(id) {
    return document.getElementById(id);
  }

  function setText(id, value) {
    const el = byId(id);
    if (el) el.textContent = value;
  }

  function toHex(buffer) {
    return Array.from(new Uint8Array(buffer), b => b.toString(16).padStart(2, "0")).join("");
  }

  function canonicalize(value) {
    if (Array.isArray(value)) return "[" + value.map(canonicalize).join(",") + "]";
    if (value && typeof value === "object") {
      return "{" + Object.keys(value).sort().map(key =>
        JSON.stringify(key) + ":" + canonicalize(value[key])
      ).join(",") + "}";
    }
    return JSON.stringify(value);
  }

  async function sha256Hex(value) {
    const bytes = new TextEncoder().encode(typeof value === "string" ? value : canonicalize(value));
    return toHex(await crypto.subtle.digest("SHA-256", bytes));
  }

  function secureContextReady() {
    return location.protocol === "https:" && window.isSecureContext && !!window.crypto && !!crypto.subtle;
  }

  function randomViewerNodeId() {
    if (typeof crypto.randomUUID === "function") {
      return "node:observer:" + crypto.randomUUID();
    }
    const bytes = new Uint8Array(16);
    crypto.getRandomValues(bytes);
    bytes[6] = (bytes[6] & 0x0f) | 0x40;
    bytes[8] = (bytes[8] & 0x3f) | 0x80;
    const h = Array.from(bytes, b => b.toString(16).padStart(2, "0")).join("");
    return "node:observer:" + [
      h.slice(0,8), h.slice(8,12), h.slice(12,16), h.slice(16,20), h.slice(20)
    ].join("-");
  }

  function loadOrCreateViewerNode() {
    const stored = localStorage.getItem(VIEWER_NODE_STORAGE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        if (parsed && typeof parsed.viewer_node_id === "string" && parsed.viewer_node_id.startsWith("node:observer:")) {
          return parsed;
        }
      } catch (_) {}
    }
    const node = {
      schema: "stegverse.browser-observer-node.v1",
      viewer_node_id: randomViewerNodeId(),
      established_at: new Date().toISOString(),
      establishment_transport: "HTTPS",
      identity_source: "SECURE_RANDOM_BROWSER_LOCAL",
      pii_collected: false,
      device_fingerprint_used: false,
      network_identity_used: false,
      authority_effect: "NONE",
      activation_effect: false
    };
    localStorage.setItem(VIEWER_NODE_STORAGE_KEY, JSON.stringify(node));
    return node;
  }

  async function bindExperiment(config, node) {
    const pairPayload = {
      schema: config.viewer_experiment_pair_schema,
      experiment_id: config.experiment_id,
      viewer_node_id: node.viewer_node_id
    };
    const pairId = "VE-" + (await sha256Hex(pairPayload)).toUpperCase();
    const storageKey = PAIR_STORAGE_PREFIX + config.experiment_id;
    const existing = localStorage.getItem(storageKey);
    let pairing = null;
    if (existing) {
      try { pairing = JSON.parse(existing); } catch (_) {}
    }
    if (!pairing || pairing.viewer_experiment_pair_id !== pairId) {
      pairing = {
        ...pairPayload,
        viewer_experiment_pair_id: pairId,
        paired_at: new Date().toISOString(),
        secure_context: true,
        canonical_manifest_receipt_id: config.manifest_receipt_id,
        authority_effect: "NONE",
        activation_effect: false
      };
      localStorage.setItem(storageKey, JSON.stringify(pairing));
    } else if (config.manifest_receipt_id && pairing.canonical_manifest_receipt_id !== config.manifest_receipt_id) {
      pairing.canonical_manifest_receipt_id = config.manifest_receipt_id;
      pairing.manifest_bound_at = new Date().toISOString();
      localStorage.setItem(storageKey, JSON.stringify(pairing));
    }
    return pairing;
  }

  async function registerObserverNode(config, node, pairing) {
    if (!config.observer_registration_endpoint) {
      return {
        state: "PRE_RUN_LOCAL_ONLY",
        canonical_registration_receipt_id: null,
        authority_effect: "NONE"
      };
    }

    const request = {
      schema: "stegverse.public-observer-node-registration-request.v1",
      experiment_id: config.experiment_id,
      viewer_node_id: node.viewer_node_id,
      viewer_experiment_pair_id: pairing.viewer_experiment_pair_id,
      node_established_at: node.established_at,
      secure_context: true,
      requested_role: "OBSERVER_ONLY",
      authority_effect: "NONE",
      activation_effect: false
    };
    request.request_sha256 = await sha256Hex(request);

    const response = await fetch(config.observer_registration_endpoint, {
      method: "POST",
      credentials: "omit",
      cache: "no-store",
      headers: {"content-type": "application/json"},
      body: JSON.stringify(request)
    });
    if (!response.ok) {
      throw new Error("canonical observer registration failed");
    }
    const receipt = await response.json();
    if (
      !receipt ||
      receipt.schema !== "stegverse.public-observer-node-registration-receipt.v1" ||
      receipt.experiment_id !== config.experiment_id ||
      receipt.viewer_node_id !== node.viewer_node_id ||
      receipt.viewer_experiment_pair_id !== pairing.viewer_experiment_pair_id ||
      receipt.authority_effect !== "NONE"
    ) {
      throw new Error("invalid canonical observer registration receipt");
    }
    return {
      state: "CANONICALLY_REGISTERED",
      canonical_registration_receipt_id: receipt.registration_receipt_id || null,
      receipt
    };
  }

  async function deriveViewerOperationId(config, viewerNodeId, operation) {
    if (!config.manifest_receipt_id) return null;
    const payload = {
      schema: config.viewer_operation_schema,
      lane_schema: config.sdk_lane_schema,
      manifest_receipt_id: String(config.manifest_receipt_id).trim().toUpperCase(),
      viewer_node_id: viewerNodeId,
      operation
    };
    const digest = (await sha256Hex(payload)).toUpperCase();
    return (operation === "REPLAY" ? "VR-" : "VC-") + digest;
  }

  async function establish() {
    const panel = byId("observer-node-panel");
    if (!secureContextReady()) {
      if (panel) panel.dataset.state = "FAIL_CLOSED";
      setText("observer-node-state", "FAIL_CLOSED — HTTPS secure context required");
      setText("observer-node-id", "not established");
      setText("observer-pair-id", "not established");
      return;
    }

    let config;
    try {
      const response = await fetch(CONFIG_URL, {cache: "no-store", credentials: "omit"});
      if (!response.ok) throw new Error("observer configuration unavailable");
      config = await response.json();
    } catch (error) {
      if (panel) panel.dataset.state = "FAIL_CLOSED";
      setText("observer-node-state", "FAIL_CLOSED — experiment identity unavailable");
      return;
    }

    if (!config.secure_context_required || !config.experiment_id) {
      if (panel) panel.dataset.state = "FAIL_CLOSED";
      setText("observer-node-state", "FAIL_CLOSED — invalid experiment observer contract");
      return;
    }

    const node = loadOrCreateViewerNode();
    const pairing = await bindExperiment(config, node);
    const registration = await registerObserverNode(config, node, pairing);
    const replayId = await deriveViewerOperationId(config, node.viewer_node_id, "REPLAY");
    const reconstructId = await deriveViewerOperationId(config, node.viewer_node_id, "RECONSTRUCT");

    const receipt = {
      schema: "stegverse.browser-observer-node-establishment-receipt.v1",
      experiment_id: config.experiment_id,
      viewer_node_id: node.viewer_node_id,
      viewer_experiment_pair_id: pairing.viewer_experiment_pair_id,
      established_at: node.established_at,
      observed_at: new Date().toISOString(),
      secure_context: true,
      origin: location.origin,
      manifest_receipt_id: config.manifest_receipt_id,
      observer_registration_state: registration.state,
      observer_registration_receipt_id: registration.canonical_registration_receipt_id,
      replay_id: replayId,
      reconstruction_id: reconstructId,
      authority_effect: "NONE",
      activation_effect: false
    };
    receipt.receipt_sha256 = await sha256Hex(receipt);
    localStorage.setItem(RECEIPT_STORAGE_PREFIX + config.experiment_id, JSON.stringify(receipt));

    const stateText = config.manifest_receipt_id
      ? "ESTABLISHED · MANIFEST BOUND"
      : registration.state === "CANONICALLY_REGISTERED"
        ? "ESTABLISHED · CANONICALLY REGISTERED"
        : "ESTABLISHED · PRE-RUN PAIRED";
    if (panel) panel.dataset.state = config.manifest_receipt_id ? "MANIFEST_BOUND" : registration.state;
    setText("observer-node-state", stateText);
    setText("observer-node-id", node.viewer_node_id);
    setText("observer-experiment-id", config.experiment_id);
    setText("observer-pair-id", pairing.viewer_experiment_pair_id);
    setText("observer-node-receipt", receipt.receipt_sha256);
    setText("observer-registration-id", registration.canonical_registration_receipt_id || "not yet enabled — local pairing retained");
    setText("observer-manifest-id", config.manifest_receipt_id || "pending authentic run receipt");
    setText("observer-replay-id", replayId || "will derive when manifest receipt is available");
    setText("observer-reconstruct-id", reconstructId || "will derive when manifest receipt is available");
  }

  if (location.protocol === "http:" && location.hostname !== "localhost" && location.hostname !== "127.0.0.1") {
    location.replace("https://" + location.host + location.pathname + location.search + location.hash);
    return;
  }

  establish().catch(() => {
    setText("observer-node-state", "FAIL_CLOSED — observer node establishment error");
  });
})();
