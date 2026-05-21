
const DATA_URL = "data/formalism-tests/transition-proof-surface.json";

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key === "className") node.className = value;
    else if (key === "text") node.textContent = value;
    else if (key === "html") node.innerHTML = value;
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
  header.appendChild(el("span", { className: "badge", text: data.current_status }));
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
    if (stage.metrics) {
      card.appendChild(el("pre", { text: JSON.stringify(stage.metrics, null, 2) }));
    }
    grid.appendChild(card);
  }
  section.appendChild(grid);
  root.appendChild(section);
}

function renderStage6(root, data) {
  const stage = data.stages.find((item) => item.id === "stage-6");
  const section = el("section");
  section.appendChild(el("h2", { text: "Stage 6 Unified Gate Results" }));
  section.appendChild(el("p", { text: stage.summary }));
  section.appendChild(el("pre", { text: JSON.stringify({ metrics: stage.metrics, decision_counts: stage.decision_counts }, null, 2) }));
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
  section.appendChild(el("pre", { text:
`1. Open ${data.artifact_paths.canonical_release}
2. Canonicalize JSON with sorted keys and compact separators.
3. Compute SHA-256.
4. Compare with ${data.artifact_paths.sha256}
5. Treat formalism-tests as proof authority and Site as public mirror only.` }));
  root.appendChild(section);
}

function renderAuthority(root, data) {
  const section = el("section");
  section.appendChild(el("h2", { text: "Authority Boundary" }));
  section.appendChild(el("pre", { text: data.authority_boundary }));
  section.appendChild(el("p", { className: "small", text: "This page is rendered dynamically from mirrored JSON. It does not create proof authority." }));
  root.appendChild(section);
}

function renderPage(data) {
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
