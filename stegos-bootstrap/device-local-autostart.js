(function (root) {
  "use strict";

  var MAX_ATTEMPTS = 120;
  var RETRY_MS = 500;
  var DEVICE_ENDPOINT = "https://stegverse.org/stegos-bootstrap/local-model";
  var preparedWorker = null;

  function text(id, value) {
    var node = document.getElementById(id);
    if (node) { node.textContent = value; }
  }

  function delay() {
    return new Promise(function (resolve) { root.setTimeout(resolve, RETRY_MS); });
  }

  function markReady(result, reused) {
    var evidence = result && result.evidence ? result.evidence : result;
    text("evidence-admission-state", reused ? "ADMITTED_DEVICE_LOCAL_REUSED" : "ADMITTED_DEVICE_LOCAL");
    text("admitted-inference-state", "READY");
    text("inference-state", "ADMITTED_STEGVERSE_DEVICE_LOCAL_ROUTE_READY");
    var button = document.getElementById("run-inference");
    if (button) { button.disabled = false; }
    var output = document.getElementById("evidence-admission-output");
    if (output && evidence) { output.textContent = JSON.stringify(evidence, null, 2); }
    return result;
  }

  function prepareWorker() {
    if (preparedWorker) { return preparedWorker; }
    preparedWorker = root.StegOSWebBootstrap.registerOfflineShell().then(function () {
      if (!(navigator.serviceWorker && navigator.serviceWorker.getRegistration)) { return null; }
      return navigator.serviceWorker.getRegistration().then(function (registration) {
        if (!registration || typeof registration.update !== "function") { return registration; }
        return registration.update().then(function () { return registration; }).catch(function () { return registration; });
      });
    });
    return preparedWorker;
  }

  function admittedDeviceLocalEvidence() {
    return root.StegOSAdmittedInference.readAdmittedInferenceEvidence().then(function (evidence) {
      if (
        evidence && evidence.state === "ADMITTED" &&
        evidence.endpoint === DEVICE_ENDPOINT &&
        evidence.endpoint_transport === "SERVICE_WORKER_LOCAL_INTERCEPT"
      ) {
        return evidence;
      }
      return null;
    });
  }

  function attempt(number) {
    if (number >= MAX_ATTEMPTS) {
      text("evidence-admission-state", "FAIL_CLOSED_DEVICE_LOCAL_BOOTSTRAP_TIMEOUT");
      text("admitted-inference-state", "WAITING_FOR_DEVICE_LOCAL_RUNTIME");
      return Promise.resolve(null);
    }

    return root.StegOSWebBootstrap.readExistingNode().then(function (node) {
      if (!node || !node.node_id) { throw new Error("DEVICE_LOCAL_NODE_NOT_ESTABLISHED_YET"); }
      return admittedDeviceLocalEvidence();
    }).then(function (existing) {
      if (existing) { return markReady(existing, true); }
      text("evidence-admission-state", "CHECKING_DEVICE_LOCAL");
      text("admitted-inference-state", "WAITING_FOR_DEVICE_LOCAL_RUNTIME");
      return prepareWorker().then(function () {
        return root.StegOSAdmittedInference.bootstrapDeviceLocalInferenceEvidence();
      }).then(function (result) { return markReady(result, false); });
    }).catch(function () {
      return delay().then(function () { return attempt(number + 1); });
    });
  }

  function start() {
    if (!root.StegOSWebBootstrap || !root.StegOSAdmittedInference) {
      text("evidence-admission-state", "FAIL_CLOSED_DEVICE_LOCAL_BOOTSTRAP_API_MISSING");
      return;
    }
    admittedDeviceLocalEvidence().then(function (existing) {
      if (existing) { return markReady(existing, true); }
      return attempt(0);
    }).catch(function () { return attempt(0); });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
}(window));
