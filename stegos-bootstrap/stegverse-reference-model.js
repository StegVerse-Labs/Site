(function (root) {
  "use strict";

  var MODEL_ID = "stegverse-reference-lm-v1";
  var MODEL_CLASS = "REFERENCE_LANGUAGE_MODEL";
  var EXPECTED_MODEL_HASH = "5c1a425a40cd63cf5f4bb4cc28c3eebaad9713a42cfdcfb85e025d3371013a4d";
  var CORPUS = "StegVerse is a sovereign governance and continuity system. Model output does not grant execution authority. A proposed transition must be evaluated against identity, policy, delegation, consent, continuity, evidence, and applicable governance before execution. Missing required evidence fails closed. Approval is not continuity. Execution is not admissibility. A boundary remains admissible only while it preserves recoverability and convergence toward the intended governed state. Third party platform availability is not a production blocker; an unavailable provider means the current solution path must change. Receipts preserve evidence of what was evaluated and observed, but custody is not authority and publication is not activation. Local sovereign operation should preserve bounded authority, deterministic evidence, replayability, reconstructability, and safe degradation. A StegVerse node may use local inference to propose text or structured candidates, but model output must pass the same governance boundary as any other proposal. The system should prefer private local execution, explicit resource bounds, inspectable state transitions, and machine-observable recovery conditions. When a dependency fails, select another compliant solution instead of waiting indefinitely. The heartbeat coordinates work but does not create authority. Master Records reconstructs custody and continuity without becoming the decision authority. StegGate evaluates commit-time admissibility and must distinguish allow, deny, review, and fail-closed outcomes. The reference language model exists to ensure that sovereign model development and inference-path testing can execute without an external inference service. It is intentionally small and must not be described as a large production language model. Stronger local models may replace it when locally available and admitted, but absence of optional software or weights cannot eliminate the sovereign reference path.\n";
  var BOS = "<BOS>";
  var EOS = "<EOS>";
  var SEP = "\u241f";
  var endpointBase = "https://stegverse.org/stegos-bootstrap/local-model";

  function tokenPattern() {
    try { return new RegExp("[\\p{L}\\p{N}_]+|[^\\p{L}\\p{N}_\\s]", "gu"); }
    catch (_error) { return /[A-Za-z0-9_]+|[^A-Za-z0-9_\\s]/g; }
  }

  function tokenize(text) { return String(text || "").match(tokenPattern()) || []; }

  function detokenize(tokens) {
    var out = "";
    tokens.forEach(function (token) {
      if (!out) { out = token; }
      else if (/^[,.;:!?) ]$/.test(token) && token !== " ") { out += token; }
      else if (token === "'") { out += token; }
      else { out += " " + token; }
    });
    return out;
  }

  function cmp(a, b) { return a < b ? -1 : a > b ? 1 : 0; }

  function pythonJsonQuote(value) {
    var raw = JSON.stringify(String(value));
    return raw.replace(/[\u007f-\uffff]/g, function (ch) {
      var code = ch.charCodeAt(0).toString(16).padStart(4, "0");
      return "\\u" + code;
    });
  }

  function pythonCanonical(value) {
    if (value === null) { return "null"; }
    if (value === true) { return "true"; }
    if (value === false) { return "false"; }
    if (typeof value === "number") { return String(value); }
    if (typeof value === "string") { return pythonJsonQuote(value); }
    if (Array.isArray(value)) { return "[" + value.map(pythonCanonical).join(",") + "]"; }
    var keys = Object.keys(value).sort(cmp);
    return "{" + keys.map(function (key) { return pythonJsonQuote(key) + ":" + pythonCanonical(value[key]); }).join(",") + "}";
  }

  function stableJson(value) {
    if (value === null || typeof value !== "object") { return JSON.stringify(value); }
    if (Array.isArray(value)) { return "[" + value.map(stableJson).join(",") + "]"; }
    return "{" + Object.keys(value).sort(cmp).map(function (key) { return JSON.stringify(key) + ":" + stableJson(value[key]); }).join(",") + "}";
  }

  function hex(bytes) { return Array.prototype.map.call(bytes, function (b) { return b.toString(16).padStart(2, "0"); }).join(""); }

  function sha256Hex(value) {
    var text = typeof value === "string" ? value : stableJson(value);
    return root.crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)).then(function (digest) { return hex(new Uint8Array(digest)); });
  }

  function increment(counter, token) { counter[token] = (counter[token] || 0) + 1; }

  function train() {
    var transitions = Object.create(null);
    var fallback = Object.create(null);
    var tokens = tokenize(CORPUS);
    var context = [BOS, BOS];
    tokens.forEach(function (token) {
      var key = context[0] + SEP + context[1];
      transitions[key] = transitions[key] || Object.create(null);
      increment(transitions[key], token);
      increment(fallback, token);
      context = [context[1], token];
    });
    var finalKey = context[0] + SEP + context[1];
    transitions[finalKey] = transitions[finalKey] || Object.create(null);
    increment(transitions[finalKey], EOS);
    return { transitions: transitions, fallback: fallback, trainingTokenCount: tokens.length };
  }

  var trained = train();
  var modelHashPromise = null;

  function modelHash() {
    if (!modelHashPromise) {
      var transitionObject = {};
      Object.keys(trained.transitions).sort(cmp).forEach(function (key) {
        transitionObject[key] = Object.keys(trained.transitions[key]).sort(cmp).map(function (token) {
          return [token, trained.transitions[key][token]];
        });
      });
      var fallback = Object.keys(trained.fallback).sort(cmp).map(function (token) { return [token, trained.fallback[token]]; });
      var canonical = pythonCanonical({ order: 2, transitions: transitionObject, fallback: fallback });
      modelHashPromise = sha256Hex(canonical).then(function (value) {
        if (value !== EXPECTED_MODEL_HASH) { throw new Error("FAIL_CLOSED: browser model hash mismatch: " + value); }
        return value;
      });
    }
    return modelHashPromise;
  }

  function choicesFor(context) {
    var key = context[0] + SEP + context[1];
    if (trained.transitions[key]) { return trained.transitions[key]; }
    var suffix = Object.create(null);
    Object.keys(trained.transitions).forEach(function (candidate) {
      var parts = candidate.split(SEP);
      if (parts[1] === context[1]) {
        Object.keys(trained.transitions[candidate]).forEach(function (token) {
          suffix[token] = (suffix[token] || 0) + trained.transitions[candidate][token];
        });
      }
    });
    return Object.keys(suffix).length ? suffix : trained.fallback;
  }

  function seedContext(promptTokens) {
    if (promptTokens.length >= 2) {
      var candidate = [promptTokens[promptTokens.length - 2], promptTokens[promptTokens.length - 1]];
      if (trained.transitions[candidate[0] + SEP + candidate[1]]) { return candidate; }
    }
    if (promptTokens.length) {
      var suffix = promptTokens[promptTokens.length - 1];
      var keys = Object.keys(trained.transitions).filter(function (key) { return key.split(SEP)[1] === suffix; }).sort(cmp);
      if (keys.length) { return keys[0].split(SEP); }
    }
    return [BOS, BOS];
  }

  function choose(context, prompt, step, seed, hash) {
    var choices = choicesFor(context);
    var population = [];
    Object.keys(choices).sort(cmp).forEach(function (token) {
      for (var i = 0; i < choices[token]; i += 1) { population.push(token); }
    });
    if (!population.length) { return Promise.resolve(EOS); }
    return root.crypto.subtle.digest("SHA-256", new TextEncoder().encode(hash + "|" + prompt + "|" + seed + "|" + step + "|" + context.join(SEP))).then(function (digest) {
      var bytes = new Uint8Array(digest).slice(0, 8);
      var remainder = 0;
      bytes.forEach(function (byte) { remainder = (remainder * 256 + byte) % population.length; });
      return population[remainder];
    });
  }

  function generate(prompt, options) {
    options = options || {};
    var maxTokens = Math.min(Number(options.max_tokens || options.maxTokens || 96), 256);
    var seed = Number(options.seed || 0);
    var promptTokens = tokenize(prompt);
    var context = seedContext(promptTokens);
    var generated = [];
    var started = root.performance && root.performance.now ? root.performance.now() : Date.now();
    return modelHash().then(function (hash) {
      var chain = Promise.resolve();
      for (var step = 0; step < maxTokens; step += 1) {
        (function (currentStep) {
          chain = chain.then(function () {
            return choose(context, prompt, currentStep, seed, hash).then(function (token) {
              if (token === EOS) {
                if (generated.length) { throw { __stegverse_stop: true }; }
                context = [BOS, BOS];
                return;
              }
              generated.push(token);
              context = [context[1], token];
            });
          });
        }(step));
      }
      return chain.catch(function (error) {
        if (!error || !error.__stegverse_stop) { throw error; }
      }).then(function () {
        var finished = root.performance && root.performance.now ? root.performance.now() : Date.now();
        var latency = Math.max(finished - started, 0.001);
        return {
          model: MODEL_ID,
          model_hash: hash,
          text: detokenize(generated),
          usage: {
            prompt_tokens: promptTokens.length,
            completion_tokens: generated.length,
            total_tokens: promptTokens.length + generated.length,
            latency_ms: Math.round(latency * 1000) / 1000
          },
          training: { training_tokens: trained.trainingTokenCount, order: 2, external_training_service_required: false },
          authority_effect: "NONE"
        };
      });
    });
  }

  function chatCompletion(request) {
    request = request || {};
    var messages = Array.isArray(request.messages) ? request.messages : [];
    var prompt = messages.filter(function (m) { return m && typeof m === "object"; }).map(function (m) { return String(m.content || ""); }).join("\n");
    if (!prompt.trim()) { return Promise.reject(new Error("messages must contain content")); }
    return generate(prompt, { max_tokens: Math.min(Number(request.max_tokens || 64), 256), seed: Number(request.seed || 0) }).then(function (result) {
      return {
        id: "chatcmpl-stegverse-browser-" + Date.now().toString(16),
        object: "chat.completion",
        created: Math.floor(Date.now() / 1000),
        model: MODEL_ID,
        choices: [{ index: 0, message: { role: "assistant", content: result.text }, finish_reason: "stop" }],
        usage: result.usage,
        usage_proof: {
          measured: true,
          model_used: true,
          prompt_tokens: result.usage.prompt_tokens,
          completion_tokens: result.usage.completion_tokens,
          total_tokens: result.usage.total_tokens,
          latency_ms: result.usage.latency_ms
        },
        stegverse: {
          model_hash: result.model_hash,
          training: result.training,
          runtime: "browser-service-worker",
          third_party_inference_required: false,
          network_egress_required: false,
          authority_effect: "NONE"
        }
      };
    });
  }

  function runtimeProof(endpoint) {
    endpoint = String(endpoint || endpointBase).replace(/\/$/, "");
    var started = Date.now();
    return chatCompletion({ model: MODEL_ID, messages: [{ role: "user", content: "Explain why model output does not grant execution authority." }], max_tokens: 48, seed: 7 }).then(function (response) {
      var text = response.choices[0].message.content;
      return Promise.all([modelHash(), sha256Hex(text)]).then(function (parts) {
        var selection = {
          schema: "stegverse.local-model-runtime-selection/v1",
          selected: { engine: "stegverse-reference-browser", ready: true, command: [], model_ref: "models/stegverse_reference_language_model.v1.json", private_only: true, reason: "device_local_service_worker_zero_external_dependency_fallback" },
          candidates: [],
          third_party_inference_required: false,
          hosted_provider_fallback_allowed: false,
          private_endpoint_only: false,
          device_local_intercepted_endpoint: true,
          authority_effect: "NONE"
        };
        var proof = {
          schema: "stegverse.sovereign-local-model-proof/v1",
          goal_id: "SOVEREIGN-LOCAL-MODEL-001",
          model_id: MODEL_ID,
          model_class: MODEL_CLASS,
          production_llm_equivalent: false,
          process_runtime_seconds: Math.max((Date.now() - started) / 1000, 0.001),
          endpoint: endpoint,
          endpoint_transport: "SERVICE_WORKER_LOCAL_INTERCEPT",
          service_worker_scope: "https://stegverse.org/stegos-bootstrap/",
          process_owned_by_verifier: false,
          predicates: {
            real_model_process_observed: false,
            browser_service_worker_runtime_observed: true,
            device_local_intercepted_endpoint: true,
            network_egress_required: false,
            private_endpoint_only: false,
            real_inference_response_observed: Boolean(text.trim()),
            measured_usage_persistable: true,
            local_training_observed: true,
            third_party_inference_required: false,
            model_output_grants_authority: false,
            model_identity_matches_manifest: response.model === MODEL_ID,
            live_endpoint_remains_available: true
          },
          usage: response.usage,
          result_text_sha256: parts[1],
          model_hash: parts[0],
          selection: selection,
          state: "VERIFIED_REFERENCE_MODEL_RUNTIME",
          authority_effect: "NONE",
          qualifies_as_large_production_llm: false,
          github_token_required: false,
          third_party_execution_platform_required: false
        };
        var canonical = stableJson({ endpoint: endpoint, model_hash: parts[0], response_text_sha256: parts[1], selection: selection, transport: proof.endpoint_transport });
        return sha256Hex(canonical).then(function (proofHash) { proof.proof_hash = proofHash; return proof; });
      });
    });
  }

  var api = {
    MODEL_ID: MODEL_ID,
    MODEL_CLASS: MODEL_CLASS,
    EXPECTED_MODEL_HASH: EXPECTED_MODEL_HASH,
    DEFAULT_ENDPOINT: endpointBase,
    tokenize: tokenize,
    stableJson: stableJson,
    sha256Hex: sha256Hex,
    modelHash: modelHash,
    generate: generate,
    chatCompletion: chatCompletion,
    runtimeProof: runtimeProof
  };
  root.StegVerseReferenceBrowserModel = api;
  if (typeof module !== "undefined" && module.exports) { module.exports = api; }
}(typeof self !== "undefined" ? self : globalThis));
