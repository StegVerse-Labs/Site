// StegVerse color-preserving site wiring.
// This script intentionally does not set colors, fonts, body styles, or page backgrounds.
(function () {
  const STATE_SOURCE = "data/stegverse-site-state.json";
  const NAV_SOURCE = "data/stegverse-site-navigation.json";

  async function readJson(path) {
    const res = await fetch(path, { cache: "no-store" });
    if (!res.ok) throw new Error(`Unable to load ${path}: ${res.status}`);
    return res.json();
  }

  function setText(selector, value) {
    document.querySelectorAll(selector).forEach((node) => {
      node.textContent = value == null ? "" : String(value);
    });
  }

  function hydrateState(state) {
    setText("[data-sv-roadmap-status]", state.roadmap_status);
    setText("[data-sv-work-entity]", state.primary_work_entity);
    setText("[data-sv-proof-authority]", state.proof_authority);
    setText("[data-sv-site-role]", state.site_role);
    setText("[data-sv-production-boundary]", state.production_boundary);
    setText("[data-sv-packet-boundary]", state.packet_boundary);
    setText("[data-sv-install-plan-boundary]", state.install_plan_boundary);
    setText("[data-sv-discovery-boundary]", state.discovery_boundary);
    setText("[data-sv-node-boundary]", state.node_boundary);
    setText("[data-sv-finco-boundary]", state.finco_boundary);

    const s31 = state.stage31_summary || {};
    setText("[data-sv-stage31-task]", s31.task_id);
    setText("[data-sv-stage31-case-count]", s31.case_count);
    setText("[data-sv-stage31-assertion-count]", s31.assertion_count);
    setText("[data-sv-stage31-receipt-count]", s31.receipt_count);

    const decisionTarget = document.querySelector("[data-sv-stage31-decisions]");
    if (decisionTarget && s31.decision_counts) {
      decisionTarget.innerHTML = "";
      Object.entries(s31.decision_counts).forEach(([label, value]) => {
        const div = document.createElement("div");
        div.className = "sv-status-row";
        div.innerHTML = `<span>${label}</span><strong>${value}</strong>`;
        decisionTarget.appendChild(div);
      });
    }
  }

  function hydrateNav(nav) {
    document.querySelectorAll("[data-sv-global-nav]").forEach((target) => {
      if (!Array.isArray(nav.items)) return;
      target.innerHTML = "";
      nav.items.forEach((item) => {
        const a = document.createElement("a");
        a.href = item.href;
        a.textContent = item.label;
        target.appendChild(a);
      });
    });
  }

  function injectStatusMount(state) {
    const mount = document.querySelector("[data-sv-status-mount]");
    if (!mount) return;
    mount.innerHTML = `
      <section class="sv-status-panel" aria-label="StegVerse proof status">
        <h2>Current proof status</h2>
        <p><strong>Status:</strong> <span data-sv-roadmap-status></span></p>
        <p><strong>Work entity:</strong> <span data-sv-work-entity></span></p>
        <p><strong>Proof authority:</strong> <span data-sv-proof-authority></span></p>
        <p><strong>Site role:</strong> <span data-sv-site-role></span></p>
        <p><a href="${state.links && state.links.stage_1_to_31 ? state.links.stage_1_to_31 : "formalism-tests-stage-1-to-31.html"}">View Stage 1–31 proof mirror</a></p>
      </section>`;
    hydrateState(state);
  }

  document.addEventListener("DOMContentLoaded", async () => {
    try {
      const [state, nav] = await Promise.all([readJson(STATE_SOURCE), readJson(NAV_SOURCE)]);
      hydrateState(state);
      hydrateNav(nav);
      injectStatusMount(state);
      document.documentElement.setAttribute("data-sv-color-preserving-wiring", "loaded");
    } catch (error) {
      console.error(error);
      document.documentElement.setAttribute("data-sv-color-preserving-wiring", "error");
    }
  });
})();
