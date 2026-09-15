(function(){
  "use strict";

  const installed = window.matchMedia && window.matchMedia("(display-mode: standalone)").matches;
  const iosStandalone = window.navigator && window.navigator.standalone === true;
  document.documentElement.dataset.mykvInstalled = (installed || iosStandalone) ? "true" : "false";

  window.addEventListener("DOMContentLoaded", function(){
    const summary = document.getElementById("kv-summary");
    if (!summary) return;
    const marker = installed || iosStandalone ? "Installed MyKV" : "Browser MyKV";
    summary.dataset.mykvSurface = marker;
  });
})();
