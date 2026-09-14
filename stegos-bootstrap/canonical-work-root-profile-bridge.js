(function (root) {
  "use strict";

  var nativeFetch = root.fetch.bind(root);

  function queryRootIntrProfile() {
    if (!(navigator.serviceWorker && navigator.serviceWorker.getRegistration)) {
      return Promise.reject(new Error("root InTr service worker API unavailable"));
    }
    return navigator.serviceWorker.getRegistration("/").then(function (registration) {
      var worker = registration && (registration.active || registration.waiting || registration.installing);
      if (!worker) throw new Error("root Universal InTr service worker unavailable");
      return new Promise(function (resolve, reject) {
        var channel = new MessageChannel();
        var timer = setTimeout(function () { reject(new Error("root InTr profile direct-message timed out")); }, 3000);
        channel.port1.onmessage = function (event) {
          clearTimeout(timer);
          var data = event.data || {};
          if (!data.ok || !data.profile) {
            reject(new Error("root InTr profile direct-message denied: " + String(data.reason || "unknown")));
            return;
          }
          resolve(new Response(JSON.stringify(data.profile), {
            status: 200,
            headers: { "Content-Type": "application/json", "Cache-Control": "no-store", "X-StegVerse-Runtime": "DEVICE_LOCAL_INTR_DIRECT_PROFILE" }
          }));
        };
        worker.postMessage({ type: "STEGVERSE_INTR_PROFILE_QUERY" }, [channel.port2]);
      });
    });
  }

  root.fetch = function (input, init) {
    var url = typeof input === "string" ? new URL(input, location.href) : new URL(input.url, location.href);
    if (url.origin === location.origin && url.pathname === "/intr/profile") {
      return queryRootIntrProfile();
    }
    return nativeFetch(input, init);
  };
}(window));
