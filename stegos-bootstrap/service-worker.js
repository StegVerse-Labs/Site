"use strict";

importScripts("./stegverse-reference-model.js", "./tvc-sovereign-local-model-route.js");

var CACHE_NAME = "stegos-web-bootstrap-v3";
var SHELL = [
  "./",
  "./index.html",
  "./stegos-bootstrap.js",
  "./admitted-inference.js",
  "./stegverse-reference-model.js",
  "./tvc-sovereign-local-model-route.js",
  "./manifest.webmanifest"
];
var LOCAL_PATH = "/stegos-bootstrap/local-model";
var LOCAL_ENDPOINT = "https://stegverse.org" + LOCAL_PATH;

function jsonResponse(status, payload) {
  return new Response(JSON.stringify(payload), {
    status: status,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
      "X-StegVerse-Execution": "SERVICE_WORKER_LOCAL_INTERCEPT"
    }
  });
}

function canonicalEvidence() {
  return self.StegVerseReferenceBrowserModel.runtimeProof(LOCAL_ENDPOINT).then(function (proof) {
    return self.StegVerseTVCPortableRoute.evaluate(proof, LOCAL_ENDPOINT).then(function (route) {
      if (route.state !== "ROUTE_ADMITTED") { throw new Error("TVC device-local route denied: " + route.reason); }
      return {
        schema: "stegos.web_canonical_inference_evidence.v1",
        model: {
          canonical_owner: "StegVerse-002/micro-node-runtime",
          model_id: "stegverse-reference-lm-v1",
          credential_authority: "TV/TVC",
          github_token_required: false,
          third_party_inference_required: false,
          model_output_authority: "NONE",
          proof_valid: proof.state === "VERIFIED_REFERENCE_MODEL_RUNTIME",
          endpoint_scope: "stegverse-local",
          endpoint: LOCAL_ENDPOINT,
          proof_sha256: route.runtime_proof_hash,
          proof: proof
        },
        route: {
          canonical_owner: "StegVerse-Labs/TVC",
          task_id: "TVC-SOVEREIGN-LOCAL-MODEL-ROUTE-002",
          credential_authority: "TV/TVC",
          model_output_authority: "NONE",
          endpoint_scope: "stegverse-local",
          receipt: route
        },
        source_provenance: {
          model_runtime_commit: "ce142a56bf4ac14c2fb075c78bcc413a02bc0f5e",
          tvc_route_commit: "cf673ced2b0f13d0c2ef4fa581e477a660771a75"
        },
        external_non_stegverse_machine_required: false,
        network_egress_required: false,
        authority_effect: "NONE"
      };
    });
  });
}

function handleLocalModel(request, url) {
  var suffix = url.pathname.slice(LOCAL_PATH.length) || "/";
  if (request.method === "GET" && (suffix === "/" || suffix === "/health")) {
    return self.StegVerseReferenceBrowserModel.modelHash().then(function (hash) {
      return jsonResponse(200, {
        state: "READY",
        model: "stegverse-reference-lm-v1",
        model_hash: hash,
        runtime: "browser-service-worker",
        device_local_intercepted_endpoint: true,
        network_egress_required: false,
        third_party_inference_required: false,
        authority_effect: "NONE"
      });
    });
  }
  if (request.method === "GET" && suffix === "/v1/models") {
    return jsonResponse(200, { object: "list", data: [{ id: "stegverse-reference-lm-v1", object: "model", owned_by: "StegVerse" }] });
  }
  if (request.method === "GET" && suffix === "/canonical-evidence") {
    return canonicalEvidence().then(function (bundle) { return jsonResponse(200, bundle); }).catch(function (error) {
      return jsonResponse(503, { state: "FAIL_CLOSED", reason: String(error && error.message ? error.message : error), authority_effect: "NONE" });
    });
  }
  if (request.method === "POST" && suffix === "/v1/chat/completions") {
    return request.json().then(function (body) {
      return self.StegVerseReferenceBrowserModel.chatCompletion(body);
    }).then(function (result) {
      result.model_id = result.model;
      return jsonResponse(200, result);
    }).catch(function (error) {
      return jsonResponse(400, { error: String(error && error.message ? error.message : error), authority_effect: "NONE" });
    });
  }
  return Promise.resolve(jsonResponse(404, { error: "not_found", authority_effect: "NONE" }));
}

self.addEventListener("install", function (event) {
  event.waitUntil(caches.open(CACHE_NAME).then(function (cache) { return cache.addAll(SHELL); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener("activate", function (event) {
  event.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (key) { return key !== CACHE_NAME; }).map(function (key) { return caches.delete(key); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener("fetch", function (event) {
  var url = new URL(event.request.url);
  if (url.origin === self.location.origin && (url.pathname === LOCAL_PATH || url.pathname.indexOf(LOCAL_PATH + "/") === 0)) {
    event.respondWith(handleLocalModel(event.request, url));
    return;
  }
  if (event.request.method !== "GET") { return; }
  event.respondWith(caches.match(event.request).then(function (cached) {
    if (cached) { return cached; }
    return fetch(event.request).then(function (response) {
      if (!response || response.status !== 200 || response.type === "opaque") { return response; }
      var copy = response.clone();
      caches.open(CACHE_NAME).then(function (cache) { cache.put(event.request, copy); });
      return response;
    });
  }));
});
