// StegVerse Site State Loader
// Single public-mirror source: data/stegverse-site-state.json
(function () {
  const DEFAULT_SOURCE = "data/stegverse-site-state.json";

  function text(value, fallback) {
    return value === undefined || value === null ? fallback : String(value);
  }

  function setText(selector, value) {
    document.querySelectorAll(selector).forEach((node) => {
      node.textContent = value;
    });
  }

  function renderStages(target, stages) {
    if (!target || !Array.isArray(stages)) return;
    target.innerHTML = "";
    stages.forEach((stage) => {
      const item = document.createElement("div");
      item.className = "sv-stage-card";
      const task = stage.task_id ? `<span class="sv-small">${stage.task_id}</span>` : "";
      item.innerHTML = `<strong>Stage ${stage.stage} — ${stage.name}</strong><span>${stage.status}</span>${task}`;
      target.appendChild(item);
    });
  }

  function renderNav(target, nav) {
    if (!target || !Array.isArray(nav)) return;
    target.innerHTML = "";
    nav.forEach((entry) => {
      const link = document.createElement("a");
      link.href = entry.href;
      link.textContent = entry.label;
      target.appendChild(link);
    });
  }

  function renderDecisionCounts(target, counts) {
    if (!target || !counts) return;
    target.innerHTML = "";
    Object.entries(counts).forEach(([key, value]) => {
      const row = document.createElement("div");
      row.className = "sv-decision-row";
      row.innerHTML = `<span>${key}</span><strong>${value}</strong>`;
      target.appendChild(row);
    });
  }

  async function loadStegVerseSiteState() {
    const configured = document.querySelector("[data-sv-source]");
    const source = configured ? configured.getAttribute("data-sv-source") : DEFAULT_SOURCE;
    const response = await fetch(source, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Unable to load ${source}: ${response.status}`);
    }
    return response.json();
  }

  function hydrate(state) {
    document.documentElement.setAttribute("data-sv-state-loaded", "true");

    setText("[data-sv-roadmap-status]", text(state.roadmap_status, "Unknown"));
    setText("[data-sv-work-entity]", text(state.primary_work_entity, "Unknown"));
    setText("[data-sv-proof-authority]", text(state.proof_authority, "Unknown"));
    setText("[data-sv-site-role]", text(state.site_role, "public_mirror_only"));
    setText("[data-sv-production-boundary]", text(state.production_boundary, ""));
    setText("[data-sv-packet-boundary]", text(state.packet_boundary, ""));
    setText("[data-sv-install-plan-boundary]", text(state.install_plan_boundary, ""));
    setText("[data-sv-discovery-boundary]", text(state.discovery_boundary, ""));
    setText("[data-sv-node-boundary]", text(state.node_boundary, ""));
    setText("[data-sv-finco-boundary]", text(state.finco_boundary, ""));

    const summary = state.stage31_summary || {};
    setText("[data-sv-stage31-task]", text(summary.task_id, ""));
    setText("[data-sv-stage31-case-count]", text(summary.case_count, ""));
    setText("[data-sv-stage31-assertion-count]", text(summary.assertion_count, ""));
    setText("[data-sv-stage31-receipt-count]", text(summary.receipt_count, ""));

    renderStages(document.querySelector("[data-sv-stages]"), state.stages);
    renderNav(document.querySelector("[data-sv-nav]"), state.navigation);
    renderDecisionCounts(document.querySelector("[data-sv-stage31-decisions]"), summary.decision_counts);

    document.querySelectorAll("[data-sv-loading]").forEach((node) => {
      node.hidden = true;
    });
    document.querySelectorAll("[data-sv-ready]").forEach((node) => {
      node.hidden = false;
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    loadStegVerseSiteState()
      .then(hydrate)
      .catch((error) => {
        console.error(error);
        document.querySelectorAll("[data-sv-loading]").forEach((node) => {
          node.textContent = "Unable to load StegVerse site state.";
        });
      });
  });
})();
