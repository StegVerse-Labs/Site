"use strict";

// The current wrapper preserves the released v13 runtime, HIL_BROWSER_EVIDENCE_V16
// protocol, existing portable HIL checkout/ESRL state, and adds only the bounded
// same-device custody continuation. The custody continuation consumes an already-
// staged exact packet plus accepted ESRL lineage, uses canonical generated InTr
// profiles, and does not mint a new claim/fence or claim TVC lifecycle admission.
importScripts("./service-worker-v13-runtime.js");
importScripts("./hil-portable-state-bridge.js");
importScripts("./hil-portable-native-bridge.js");

CACHE_NAME = "stegos-web-bootstrap-v16";
var ESRL_PAGE_PATH = "/stegos-bootstrap/hil-esrl-activate.html";

[
  "./sv001-native-resident-activation.js",
  "./native-resident-activate.html",
  "./hil-esrl-activate.html",
  "./hil-custody-activate.html"
].forEach(function (asset) {
  if (Array.isArray(SHELL) && SHELL.indexOf(asset) < 0) { SHELL.push(asset); }
});

// Installed Safari clients may retain ESRL HTML from before automatic same-context
// continuation even after source has advanced. Re-installing this wrapper refreshes
// the exact ESRL page inside the existing v16 cache via the predecessor install
// handler. The separate custody page is cached as an additive continuation only;
// cache propagation itself is never custody evidence.
self.addEventListener("install", function (event) {
  event.waitUntil(self.skipWaiting());
});
self.addEventListener("activate", function (event) {
  event.waitUntil(
    self.clients.claim().then(function () {
      return self.clients.matchAll({ type: "window", includeUncontrolled: true });
    }).then(function (clients) {
      return Promise.all(clients.map(function (client) {
        var url;
        try { url = new URL(client.url); } catch (_) { return null; }
        if (url.origin !== self.location.origin || url.pathname !== ESRL_PAGE_PATH || typeof client.navigate !== "function") { return null; }
        return client.navigate(client.url);
      }));
    })
  );
});
