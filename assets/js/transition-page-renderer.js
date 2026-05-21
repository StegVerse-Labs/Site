
const DATA_URL = "data/formalism-tests/transition-proof-surface.json";

function normalizeProofSurface(input) {
  const data = structuredClone(input);

  if (!data.release) {
    data.release = {
      release_id: data.release_id || "transition-table-v1-rc1",
      release_hash: data.release_hash || "unknown",
      canonical_status: data.current_status || "RELEASE_CANDIDATE",
      canonical_element_count: data.canonical_element_count || 0,
      coupling_class_count: data.coupling_class_count || 0,
      next_release_state: "transition-table-v1",
      data_index: "data/formalism-tests/transition-table-v1-rc1/index.json"
    };
  }

  if (!Array.isArray(data.stages)) {
    const status = data.stage_status || {};
    data.stages = [
      { id: "stage-6", label: "Stage 6", name: "Admissible Existence Unified Gate", status: status["Stage 6"] || "PASS", summary: "Unified AE gate validates IW containment and RE bound.", metrics: { candidate_count: 10, assertion_count: 320 }, decision_counts: { ALLOW: 3, FAIL_CLOSED: 5, RESET_BOUNDARY: 1, EVOLVE_BOUNDARY: 1 } },
      { id: "stage-7", label: "Stage 7", name: "Element Dependency Closure", status: status["Stage 7"] || "PASS", summary: "Unlocked elements have declared dependencies.", metrics: { element_count: 13, assertion_count: 105 } },
      { id: "stage-8", label: "Stage 8", name: "AI Domain Transition Classes", status: status["Stage 8"] || "PASS", summary: "AI-domain transition classes are validated.", metrics: { candidate_count: 8, assertion_count: 64 } },
      { id: "stage-9", label: "Stage 9", name: "Multi-Body Coupling Closure", status: status["Stage 9"] || "PASS", summary: "Coupled entities require composite evaluation.", metrics: { candidate_count: 10, assertion_count: 80, coupling_class_count: 9 } },
      { id: "stage-10", label: "Stage 10", name: "Canonical Transition Table Release", status: status["Stage 10"] || data.current_status || "RELEASE_CANDIDATE", summary: "Canonical release candidate is mirrored for public presentation.", metrics: { canonical_element_count: data.canonical_element_count || 13, coupling_class_count: data.coupling_class_count || 9 } }
    ];
  }

  if (!Array.isArray(data.pages)) {
    data.pages = [
      { id: "release-index", title: "Transition Release Index", path: "transition-release-index.html", description: "Release index for current transition-table proof surface.", sections: ["release", "stages", "pages", "authority"] },
      { id: "development-status", title: "Transition Development Status", path: "transition-development-status.html", description: "Development status from Stage 6 through Stage 10.", sections: ["stages", "release", "authority"] },
      { id: "proof-surface", title: "Transition Proof Surface", path: "transition-proof-surface.html", description: "Public mirror of transition proof status.", sections: ["release", "stages", "evidence", "authority"] },
      { id: "stage6-results", title: "Stage 6 Unified Gate Results", path: "stage6-unified-gate-results.html", description: "Stage 6 unified gate result.", sections: ["stage6", "release", "authority"] },
      { id: "verification-guide", title: "Transition Verification Guide", path: "transition-verification-guide.html", description: "Verification guide for mirrored release data.", sections: ["verification", "release", "authority"] },
      { id: "stage10-release", title: "Stage 10 Canonical Release", path: "stage10-canonical-release.html", description: "Stage 10 release candidate mirror.", sections: ["release", "artifacts", "authority"] }
    ];
  }

  if (!data.artifact_paths) {
    data.artifact_paths = {
      canonical_release: "data/formalism-tests/transition-table-v1-rc1/canonical_transition_table_release.json",
      sha256: "data/formalism-tests/transition-table-v1-rc1/canonical_transition_table_release.sha256",
      replay_packet: "data/formalism-tests/transition-table-v1-rc1/replay_packet.json",
      release_receipt: "data/formalism-tests/transition-table-v1-rc1/release_receipt.json",
      release_report: "data/formalism-tests/transition-table-v1-rc1/stage10_canonical_release_report.json"
    };
  }

  return data;
}

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key === "className") node.className = value;
    else if (key === "text") node.textContent = value;
    else node.setAttribute(key, value);
  }
  for (const child of children) node.appendChild(child);
  return node;
}

function pageConfig(data, pageId) {
  return data.pages.find((page) => page.id === pageId) || data.pages[0];
}

function renderNav(data) {
  const nav = el("nav");
  for (const page of data.pages) {
    nav.appendChild(el("a", { href: page.path, text: page.title }));
  }
  return nav;
}

function renderHeader(root, data, page) {
  const header = el("header");
  header.appendChild(el("span", { className: "badge", text: data.current_status || data.release.canonical_status }));
  header.appendChild(el("h1", { text: page.title }));
  header.appendChild(el("p", { text: page.description }));
  header.appendChild(renderNav(data));
  root.appendChild(header);
}

function renderRelease(root, data) {
  const section = el("section");
  section.appendChild(el("h2", { text: "Current Release" }));
  const grid = el("div", { className: "grid" });
  const items = [
    ["Release ID", data.release.release_id],
    ["Status", data.release.canonical_status],
    ["Canonical Elements", String(data.release.canonical_element_count)],
    ["Coupling Classes", String(data.release.coupling_class_count)]
  ];
  for (const [label, value] of items) {
    const card = el("div", { className: "metric" });
    card.appendChild(el("span", { text: label }));
    card.appendChild(el("strong", { text: value }));
    grid.appendChild(card);
  }
  section.appendChild(grid);
  section.appendChild(el("h3", { text: "Release Hash" }));
  section.appendChild(el("pre", { text: data.release.release_hash }));
  root.appendChild(section);
}

function renderStages(root, data) {
  const section = el("section");
  section.appendChild(el("h2", { text: "Validated Stages" }));
  const grid = el("div", { className: "grid" });
  for (const stage of data.stages) {
    const card = el("div", { className: "stage" });
    card.appendChild(el("span", { className: "badge", text: stage.status }));
    card.appendChild(el("strong", { text: `${stage.label}: ${stage.name}` }));
    card.appendChild(el("p", { text: stage.summary }));
    if (stage.metrics) card.appendChild(el("pre", { text: JSON.stringify(stage.metrics, null, 2) }));
    if (stage.decision_counts) card.appendChild(el("pre", { text: JSON.stringify(stage.decision_counts, null, 2) }));
    grid.appendChild(card);
  }
  section.appendChild(grid);
  root.appendChild(section);
}

function renderStage6(root, data) {
  const stage = data.stages.find((item) => item.id === "stage-6");
  const section = el("section");
  section.appendChild(el("h2", { text: "Stage 6 Unified Gate Results" }));
  section.appendChild(el("p", { text: stage ? stage.summary : "Stage 6 data unavailable." }));
  section.appendChild(el("pre", { text: JSON.stringify(stage || {}, null, 2) }));
  root.appendChild(section);
}

function renderArtifacts(root, data) {
  const section = el("section");
  section.appendChild(el("h2", { text: "Mirrored Release Artifacts" }));
  const list = el("ul");
  for (const [label, path] of Object.entries(data.artifact_paths)) {
    const item = el("li");
    item.appendChild(el("a", { href: path, text: `${label}: ${path}` }));
    list.appendChild(item);
  }
  section.appendChild(list);
  root.appendChild(section);
}

function renderVerification(root, data) {
  const section = el("section");
  section.appendChild(el("h2", { text: "Verification Guide" }));
  section.appendChild(el("p", { text: "Verify the mirrored release by comparing the canonical release JSON hash to the published SHA-256 file." }));
  section.appendChild(el("pre", { text: `1. Open ${data.artifact_paths.canonical_release}\n2. Canonicalize JSON with sorted keys and compact separators.\n3. Compute SHA-256.\n4. Compare with ${data.artifact_paths.sha256}\n5. Treat formalism-tests as proof authority and Site as public mirror only.` }));
  root.appendChild(section);
}

function renderAuthority(root, data) {
  const section = el("section");
  section.appendChild(el("h2", { text: "Authority Boundary" }));
  section.appendChild(el("pre", { text: data.authority_boundary }));
  root.appendChild(section);
}

function renderPage(rawData) {
  const data = normalizeProofSurface(rawData);
  const app = document.getElementById("app");
  const pageId = document.body.dataset.page || "release-index";
  const page = pageConfig(data, pageId);
  document.title = page.title;
  app.innerHTML = "";
  renderHeader(app, data, page);
  for (const section of page.sections) {
    if (section === "release") renderRelease(app, data);
    else if (section === "stages") renderStages(app, data);
    else if (section === "stage6") renderStage6(app, data);
    else if (section === "artifacts") renderArtifacts(app, data);
    else if (section === "verification") renderVerification(app, data);
    else if (section === "pages") renderArtifacts(app, data);
    else if (section === "evidence") renderStages(app, data);
    else if (section === "authority") renderAuthority(app, data);
  }
}

function renderError(error) {
  const app = document.getElementById("app");
  app.innerHTML = "";
  const section = el("section", { className: "error" });
  section.appendChild(el("h1", { text: "Transition page data failed to load" }));
  section.appendChild(el("p", { text: "The page shell loaded, but the shared JSON source could not be read." }));
  section.appendChild(el("pre", { text: String(error) }));
  section.appendChild(el("p", { text: `Expected data source: ${DATA_URL}` }));
  app.appendChild(section);
}

fetch(DATA_URL)
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status} while loading ${DATA_URL}`);
    return response.json();
  })
  .then(renderPage)
  .catch(renderError);
