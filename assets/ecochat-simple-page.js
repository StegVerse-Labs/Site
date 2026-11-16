"use strict";
/*
 * ecochat-simple-page.js — the StegVerse.org front page chat.
 * Claim: SITE-ECOCHAT-SIMPLE-PAGE-20261115.
 * Gateway mechanism: SITE-ECOCHAT-GATEWAY-POSTURE-20261115 — the page
 * reads data/ecochat/gateway-binding.json at load and uses the gateway
 * route only when that binding enables it and names an endpoint; the
 * binding ships disabled, and any gateway failure falls back to the
 * filed device-local behavior below.
 *
 * One self-contained script. Record-bound questions are answered
 * deterministically from the filed texts below (the same texts the shared
 * Ecosystem Chat runtime carries). Device-local questions (the time on
 * this device, arithmetic) are computed on this device. Everything else
 * receives the filed gateway state — never an invented answer and never
 * "try again". Nothing in this file may throw into the ask path: every
 * optional browser capability is guarded.
 */
(function () {
  var STARTERS = {
  "how do i use this chat?": {
    "capability": "homepage_chat_help",
    "text": "Use the starter questions or type what you need in your own words. StegVerse routes the request through the capabilities available to this browser and keeps execution, evidence, and authority separate. Some questions can be answered directly from admitted local or public-source capabilities; others may use the bounded local model. You can continue the conversation naturally, and the system should say when a required capability or live data source is unavailable rather than inventing an answer."
  },
  "what is stegverse?": {
    "capability": "homepage_stegverse_overview",
    "text": "StegVerse is a governed, continuity-focused ecosystem for connecting people, software, AI, data, and services without treating model output as authority. Actions are intended to pass through explicit governance and evidence boundaries so decisions can be inspected, replayed, and reconstructed. The public site is one interface into that ecosystem; individual capabilities may have different readiness states."
  },
  "what is my kv?": {
    "capability": "homepage_kv_overview",
    "text": "My KV is your KnowledgeVault: a user-controlled place for information that StegVerse may use only through governed access when a capability needs it. Personal information is intended to remain under your control rather than becoming a StegVerse-hosted profile database. Your Node continuity records can track that KV steps occurred without storing the personal values themselves."
  }
};
  var PRODUCTS = {
  "sdk": {
    "text": "The StegVerse SDK is a public governance experiment and validation environment for StegGate-style admissibility, AdmittedCode receipt verification, LLM/agent outputs, governed submissions, replay, reconstruction, and inspectable request/receipt boundaries. It also provides the manifest builder and submission interfaces used to construct and submit governed operations. A validated request, manifest, model output, receipt, or locator does not become execution authority merely because it validates."
  },
  "steggate": {
    "text": "StegGate is StegCore's portable product surface for evaluating one proposed consequential transition before execution. It applies the canonical StegCore admissibility chain and returns a bounded disposition with reasons, predicate state, and hashes; it does not itself mint continuity receipts, establish identity truth, or grant provider authority."
  },
  "stegcore": {
    "text": "StegCore is the canonical StegVerse commit-time governance runtime. It owns the admissibility chain used to evaluate proposed consequential transitions; interfaces may adapt input or presentation but must not create a separate policy or admissibility engine."
  },
  "knowledgevault": {
    "text": "KnowledgeVault is the StegVerse continuity and knowledge layer: a portable, inspectable vault for preserving notes, records, research, projects, media references, policy, and enough context to reconstruct ongoing work across devices and sessions. Baseline use is file-based and requires no account, hosted service, SDK, or AI provider."
  }
};
  var PRODUCT_ALIASES = {
    "sdk": "sdk",
    "steggate": "steggate",
    "stegcore": "stegcore",
    "knowledgevault": "knowledgevault",
    "knowledge vault": "knowledgevault",
    "my kv": "knowledgevault"
  };
  var GATEWAY_STATE_TEXT = "That question needs a governed route. This page's governed routes run through a connected StegVerse node, and the SDK gateway is bound today to a proving instance that is not publicly reachable — so I cannot take it further from this page yet, and I will not improvise an answer. What I can answer right here, from the filed record: the three starter questions, what the SDK, StegGate, StegCore, and KnowledgeVault are, the time on this device, and arithmetic.";

  function normalize(value) {
    return String(value || "").trim().toLowerCase().replace(/\s+/g, " ");
  }

  function productKey(message) {
    var m = normalize(message).replace(/[?!.]+$/, "");
    m = m.replace(/^what(?:'s| is)( the)? /, "").replace(/^define /, "").trim();
    return Object.prototype.hasOwnProperty.call(PRODUCT_ALIASES, m) ? PRODUCT_ALIASES[m] : null;
  }

  function isClockQuestion(message) {
    var m = normalize(message).replace(/[?!.]+$/, "");
    return m === "what time is it" || m === "what is the time" || m === "what's the time" ||
      m === "current time" || m === "tell me the time" || m.indexOf("what time") === 0;
  }

  function clockText() {
    var now = new Date();
    var formatted;
    try {
      formatted = new Intl.DateTimeFormat(undefined, {
        weekday: "long", hour: "numeric", minute: "2-digit", second: "2-digit", timeZoneName: "short"
      }).format(now);
    } catch (e) {
      formatted = now.toLocaleString();
    }
    return "On this device it is " + formatted + ". That time comes from this device's own clock, computed locally — no route was crossed to answer it.";
  }

  function arithmeticCandidate(message) {
    var raw = String(message || "").trim();
    var stripped = raw
      .replace(/^(?:please\s+)?(?:calculate|compute|evaluate|solve)\s+/i, "")
      .replace(/^(?:what(?:'s| is)\s+)/i, "")
      .replace(/[?!.]+$/, "")
      .trim();
    if (!stripped || stripped.length > 256) return null;
    if (!/^[0-9eE+\-*/%().\s]+$/.test(stripped)) return null;
    if (!/[+\-*/%]/.test(stripped)) return null;
    return stripped;
  }

  function evaluateArithmetic(expr) {
    // Strict lexical consumption: the tokens must reproduce the whole
    // expression (whitespace aside). A partial tokenization — ".5" read as
    // "5", or the dangling "e" in "1e" silently dropped — is a rejection,
    // never a number.
    // Scan left to right: whitespace separates tokens; a number's exponent
    // is consumed only when its digits follow immediately, so the dangling
    // "e" in "1e + 1" is an unconsumable character and rejects the input.
    var tokens = [];
    var numberPattern = /^(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?/;
    var i = 0;
    while (i < expr.length) {
      var ch = expr[i];
      if (ch === " " || ch === "\t") { i++; continue; }
      if ("+-*/%()".indexOf(ch) !== -1) { tokens.push(ch); i++; continue; }
      var match = numberPattern.exec(expr.slice(i));
      if (!match) return null;
      tokens.push(match[0]);
      i += match[0].length;
    }
    if (!tokens.length) return null;
    var pos = 0;
    function peek() { return tokens[pos]; }
    function parseExpr() {
      var v = parseTerm();
      while (peek() === "+" || peek() === "-") { var op = tokens[pos++]; var r = parseTerm(); v = op === "+" ? v + r : v - r; }
      return v;
    }
    function parseTerm() {
      var v = parseFactor();
      while (peek() === "*" || peek() === "/" || peek() === "%") {
        var op = tokens[pos++]; var r = parseFactor();
        if ((op === "/" || op === "%") && r === 0) throw new Error("division_by_zero");
        v = op === "*" ? v * r : op === "/" ? v / r : v % r;
      }
      return v;
    }
    function parseFactor() {
      var t = tokens[pos++];
      if (t === "(") { var v = parseExpr(); if (tokens[pos++] !== ")") throw new Error("paren"); return v; }
      if (t === "-") return -parseFactor();
      if (t === "+") return parseFactor();
      var n = Number(t);
      if (Number.isNaN(n)) throw new Error("token");
      return n;
    }
    var result = parseExpr();
    if (pos !== tokens.length || typeof result !== "number" || !Number.isFinite(result)) return null;
    return result;
  }

  function answer(message) {
    var key = normalize(message);
    if (Object.prototype.hasOwnProperty.call(STARTERS, key)) return STARTERS[key].text;
    var pk = productKey(message);
    if (pk && PRODUCTS[pk]) return PRODUCTS[pk].text;
    if (isClockQuestion(message)) return clockText();
    var expr = arithmeticCandidate(message);
    if (expr) {
      try {
        var value = evaluateArithmetic(expr);
        if (value !== null) return expr + " = " + (Math.round(value * 1e10) / 1e10).toString() + ". Computed on this device — no route was crossed to answer it.";
      } catch (e) { /* fall through to the honest state answer */ }
      return "That arithmetic could not be evaluated on this device (it may divide by zero or be malformed). Nothing was routed elsewhere to answer it.";
    }
    return GATEWAY_STATE_TEXT;
  }

  async function receiptLine(text) {
    try {
      if (!window.crypto || !crypto.subtle || typeof crypto.subtle.digest !== "function") return "";
      var bytes = new TextEncoder().encode(text);
      var digest = await crypto.subtle.digest("SHA-256", bytes);
      var hex = Array.from(new Uint8Array(digest), function (b) { return b.toString(16).padStart(2, "0"); }).join("");
      return "\n\nDeterministic response · sha256 " + hex;
    } catch (e) {
      return "";
    }
  }

  // Binding-driven gateway state (SITE-ECOCHAT-GATEWAY-POSTURE-20261115).
  // Disabled unless the binding file enables it and names an endpoint.
  var GATEWAY = { enabled: false, endpoint: null, segment: null };

  function loadBinding() {
    try {
      if (typeof fetch !== "function") return;
      fetch("data/ecochat/gateway-binding.json").then(function (res) {
        return res.ok ? res.json() : null;
      }).then(function (binding) {
        try {
          var client = binding && binding.client;
          if (client && client.client_gateway_enabled === true &&
              typeof client.endpoint === "string" && client.endpoint) {
            GATEWAY.enabled = true;
            GATEWAY.endpoint = client.endpoint.replace(/\/+$/, "");
          }
        } catch (e) { /* binding stays disabled */ }
      }).catch(function () { /* binding stays disabled */ });
    } catch (e) { /* binding stays disabled */ }
  }

  function newSegmentId() {
    try {
      var buf = new Uint8Array(6);
      crypto.getRandomValues(buf);
      return "site-" + Array.from(buf, function (b) { return b.toString(16).padStart(2, "0"); }).join("");
    } catch (e) {
      return "site-" + Date.now().toString(36);
    }
  }

  async function gatewayTurn(message) {
    // Returns the gateway's answer text, or null on any failure — the
    // caller then falls back to the filed device-local state answer.
    try {
      if (!GATEWAY.segment) {
        GATEWAY.segment = newSegmentId();
        var opened = await fetch(GATEWAY.endpoint + "/api/eos/open", {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ segment: GATEWAY.segment })
        });
        if (!opened.ok) return null;
      }
      var res = await fetch(GATEWAY.endpoint + "/api/eos/turn", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ segment: GATEWAY.segment, message: message })
      });
      if (!res.ok) return null;
      var data = await res.json();
      var text = data && data.answer && typeof data.answer.text === "string" ? data.answer.text : null;
      if (!text) return null;
      var cls = data.disposition && data.disposition.class ? data.disposition.class : "RESPONSE";
      return text + "\n\nGoverned route · " + cls + " · segment " + GATEWAY.segment + " · seq " + data.seq;
    } catch (e) {
      return null;
    }
  }

  function init() {
    var form = document.getElementById("chatForm");
    var input = document.getElementById("messageInput");
    var log = document.getElementById("chatLog");
    if (!form || !input || !log) return;

    function addBubble(text, cls) {
      var wrap = document.createElement("div");
      wrap.className = "chat-message " + cls;
      var body = document.createElement("div");
      body.className = "body";
      body.textContent = text;
      wrap.appendChild(body);
      log.appendChild(wrap);
      log.scrollTop = log.scrollHeight;
      return body;
    }

    async function ask(raw) {
      var message = String(raw || "").trim();
      if (!message) return;
      addBubble(message, "user");
      var text = answer(message);
      if (text === GATEWAY_STATE_TEXT && GATEWAY.enabled) {
        var routed = await gatewayTurn(message);
        if (routed) text = routed;
      }
      var receipt = await receiptLine(text);
      addBubble(text + receipt, "system");
    }

    loadBinding();

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var value = input.value;
      input.value = "";
      ask(value);
    });
    input.addEventListener("keydown", function (event) {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event("submit", { cancelable: true }));
      }
    });

    var starters = document.querySelectorAll("[data-chat-prompt]");
    Array.prototype.forEach.call(starters, function (button) {
      button.addEventListener("click", function () { ask(button.getAttribute("data-chat-prompt")); });
    });

    // The My KV launcher is bound by the governed entry chain
    // (assets/kv-entrypoint-intr-launcher.js), which validates the
    // installation-status bridge and projection before navigating and
    // fails closed otherwise. This script deliberately does not bind it.
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
