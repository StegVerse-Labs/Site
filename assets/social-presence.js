"use strict";

(function () {
  const root = document.querySelector("[data-social-presence]");
  if (!root) return;

  function render(networks) {
    const cards = root.querySelectorAll("[data-social-network]");
    cards.forEach(function (card) {
      const key = card.getAttribute("data-social-network");
      const record = networks.find(function (item) { return item.network === key; });
      const status = card.querySelector("[data-social-status]");
      const link = card.querySelector("[data-social-outbound]");
      if (!record) {
        if (status) status.textContent = "Not configured";
        if (link) link.hidden = true;
        return;
      }

      if (status) {
        status.textContent = record.state === "VERIFIED"
          ? "Official page verified"
          : "Official page pending creation / verification";
      }

      if (!link) return;
      if (record.state === "VERIFIED" && record.canonical_url) {
        link.href = record.canonical_url;
        link.hidden = false;
        link.rel = "me noopener noreferrer";
      } else {
        link.hidden = true;
        link.removeAttribute("href");
      }
    });
  }

  fetch("data/social-presence.json", { cache: "no-store" })
    .then(function (response) {
      if (!response.ok) throw new Error("social presence manifest unavailable");
      return response.json();
    })
    .then(function (manifest) {
      render(Array.isArray(manifest.networks) ? manifest.networks : []);
    })
    .catch(function () {
      root.querySelectorAll("[data-social-status]").forEach(function (status) {
        status.textContent = "Official destination status unavailable";
      });
      root.querySelectorAll("[data-social-outbound]").forEach(function (link) {
        link.hidden = true;
      });
    });
}());
