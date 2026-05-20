const TRANSITION_PROOF_SURFACE_PATH = "data/formalism-tests/transition-proof-surface.json";

async function loadTransitionProofSurface() {
  const response = await fetch(TRANSITION_PROOF_SURFACE_PATH, { cache: "no-store" });
  if (!response.ok) throw new Error("Could not load transition-proof-surface.json");
  return response.json();
}

function transitionBadge(text) {
  const span = document.createElement("span");
  span.className = "badge";
  span.textContent = text;
  return span;
}

function transitionCard(title, body, cls) {
  const div = document.createElement("div");
  div.className = "card";
  div.innerHTML = `<h3>${title}</h3>${body}`;
  if (cls) div.classList.add(cls);
  return div;
}

function renderTransitionBase(data) {
  document.querySelectorAll("[data-transition-claim]").forEach((node) => {
    node.textContent = data.canonical_claim || data.status || "";
  });

  document.querySelectorAll("[data-transition-current]").forEach((node) => {
    node.textContent = `${data.current_stage || ""} — ${data.status || ""}`;
  });

  document.querySelectorAll("[data-transition-next]").forEach((node) => {
    node.textContent = data.next_integration_target || "";
  });

  document.querySelectorAll("[data-transition-authority]").forEach((node) => {
    node.textContent = data.authority_boundary || "";
  });

  document.querySelectorAll("[data-transition-badges]").forEach((node) => {
    node.innerHTML = "";
    [data.current_stage, data.status, data.source_repo].filter(Boolean).forEach((item) => {
      node.appendChild(transitionBadge(item));
    });
  });
}

function renderTransitionStages(data, targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;
  target.innerHTML = "";
  (data.stages || []).forEach((stage) => {
    const statusClass = stage.status === "verified" ? "ok" : "warn";
    target.appendChild(transitionCard(
      `${stage.stage}: ${stage.name}`,
      `<p class="${statusClass}">${stage.status}</p><pre>${stage.proof_claim}</pre><p>${stage.summary}</p>`
    ));
  });
}

function renderTransitionStageList(data, targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;
  target.innerHTML = "";
  (data.stages || []).forEach((stage) => {
    const statusClass = stage.status === "verified" ? "ok" : "warn";
    const li = document.createElement("li");
    li.innerHTML = `<strong>${stage.stage}</strong> — ${stage.name}: <span class="${statusClass}">${stage.status}</span>`;
    target.appendChild(li);
  });
}

function renderTransitionTasks(data, targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;
  target.textContent = (data.verified_tasks || []).join("\n");
}

function renderTransitionArtifacts(data, targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;
  target.innerHTML = "";
  Object.entries(data.source_artifacts || {}).forEach(([stage, artifacts]) => {
    const details = Object.entries(artifacts)
      .map(([key, value]) => `<p><strong>${key}</strong><br><code>${value}</code></p>`)
      .join("");
    target.appendChild(transitionCard(stage, details));
  });
}

function renderTransitionPages(data, targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;
  target.innerHTML = "";
  (data.site_pages || []).forEach((page) => {
    target.appendChild(transitionCard(page, `<p><a href="${page}">Open page</a></p>`));
  });
}

function renderTransitionStage6(data, targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;
  const result = data.stage6_result || {};
  target.innerHTML = "";
  [
    ["Candidates", result.candidate_count],
    ["Assertions", result.assertion_count],
    ["Workflow", result.workflow],
    ["Task", result.task_id],
    ["Status", result.success ? "PASS" : "FAIL"]
  ].forEach(([title, value]) => {
    target.appendChild(transitionCard(title, `<p class="${result.success ? "ok" : "bad"}">${value}</p>`));
  });
}

function renderTransitionDecisionCounts(data, targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;
  target.innerHTML = "";
  Object.entries((data.stage6_result || {}).decision_counts || {}).forEach(([decision, count]) => {
    target.appendChild(transitionCard(decision, `<p class="ok">${count}</p>`));
  });
}

function renderTransitionRaw(data, targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;
  target.textContent = JSON.stringify(data, null, 2);
}

function renderTransitionStatusPage(options) {
  loadTransitionProofSurface()
    .then((data) => {
      renderTransitionBase(data);
      if (options?.stages) renderTransitionStages(data, options.stages);
      if (options?.stageList) renderTransitionStageList(data, options.stageList);
      if (options?.tasks) renderTransitionTasks(data, options.tasks);
      if (options?.artifacts) renderTransitionArtifacts(data, options.artifacts);
      if (options?.pages) renderTransitionPages(data, options.pages);
      if (options?.stage6) renderTransitionStage6(data, options.stage6);
      if (options?.decisions) renderTransitionDecisionCounts(data, options.decisions);
      if (options?.raw) renderTransitionRaw(data, options.raw);
    })
    .catch((error) => {
      document.querySelectorAll("[data-transition-claim]").forEach((node) => {
        node.textContent = error.message;
      });
    });
}
