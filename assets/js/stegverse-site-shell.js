// StegVerse Site Shell
// Reads shared state and navigation from data/*.json.
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

  function renderNav(nav) {
    const targets = document.querySelectorAll("[data-sv-global-nav]");
    if (!targets.length || !nav || !Array.isArray(nav.items)) return;

    targets.forEach((target) => {
      target.innerHTML = "";
      nav.items.forEach((item) => {
        const a = document.createElement("a");
        a.href = item.href;
        a.textContent = item.label;
        a.setAttribute("data-sv-nav-group", item.group || "general");
        target.appendChild(a);
      });
    });
  }

  function renderDecisionCounts(summary) {
    const target = document.querySelector("[data-sv-stage31-decisions]");
    if (!target || !summary || !summary.decision_counts) return;
    target.innerHTML = "";
    Object.entries(summary.decision_counts).forEach(([label, count]) => {
      const row = document.createElement("div");
      row.className = "sv-decision-row";
      row.innerHTML = `<span>${label}</span><strong>${count}</strong>`;
      target.appendChild(row);
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

    const summary = state.stage31_summary || {};
    setText("[data-sv-stage31-task]", summary.task_id);
    setText("[data-sv-stage31-case-count]", summary.case_count);
    setText("[data-sv-stage31-assertion-count]", summary.assertion_count);
    setText("[data-sv-stage31-receipt-count]", summary.receipt_count);
    renderDecisionCounts(summary);
  }

  document.addEventListener("DOMContentLoaded", async () => {
    try {
      const [state, nav] = await Promise.all([readJson(STATE_SOURCE), readJson(NAV_SOURCE)]);
      hydrateState(state);
      renderNav(nav);
      document.querySelectorAll("[data-sv-loading]").forEach((node) => node.hidden = true);
      document.querySelectorAll("[data-sv-ready]").forEach((node) => node.hidden = false);
      document.documentElement.setAttribute("data-sv-shell-loaded", "true");
    } catch (err) {
      console.error(err);
      document.querySelectorAll("[data-sv-loading]").forEach((node) => {
        node.textContent = "Unable to load StegVerse shared site state.";
      });
    }
  });
})();
