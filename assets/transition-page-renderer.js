(() => {
  const state = window.STEGVERSE_TRANSITION_DISCOVERY_STATE;
  const root = document.querySelector("[data-transition-view]");
  if (!state || !root) return;
  const jsonStateHref = "data/transition-discovery-state-v1.json";

  function injectTransitionDiscoveryStyles() {
    if (document.getElementById("transition-discovery-renderer-style")) return;
    const style = document.createElement("style");
    style.id = "transition-discovery-renderer-style";
    style.textContent = `
      :root{--td-bg:#080b12;--td-panel:rgba(16,24,39,.86);--td-text:#eef4ff;--td-muted:#a9b7cc;--td-line:rgba(255,255,255,.14);--td-green:#43d694;--td-blue:#4da3ff;--td-gold:#ffbe54;--td-red:#ff6464}
      body{background:radial-gradient(circle at top left,rgba(67,214,148,.12),transparent 30rem),var(--td-bg);color:var(--td-text)}
      main{width:min(1180px,calc(100% - 28px));margin:0 auto;padding:18px 0 54px}
      nav,nav div{display:flex;gap:10px;flex-wrap:wrap}nav{justify-content:space-between;margin-bottom:14px}nav a{text-decoration:none;border:1px solid var(--td-line);border-radius:999px;padding:7px 11px;background:rgba(255,255,255,.05);color:var(--td-muted)}nav a:hover{color:var(--td-text);border-color:rgba(67,214,148,.44)}
      section{border:1px solid var(--td-line);border-radius:24px;background:var(--td-panel);padding:clamp(18px,4vw,42px);margin-top:14px;box-shadow:0 18px 60px rgba(0,0,0,.18);overflow:hidden}
      h1{font-size:clamp(2.2rem,7vw,5.6rem);line-height:.92;margin:0;letter-spacing:-.075em;text-transform:uppercase}h2{margin:0 0 10px;color:var(--td-green);text-transform:uppercase;letter-spacing:.12em;font-size:.85rem}h3{font-size:1.1rem;margin:.35rem 0}.kicker{color:var(--td-green);text-transform:uppercase;letter-spacing:.16em;font-size:.76rem;font-weight:900}p{color:var(--td-muted);font-size:1.02rem}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.table-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}.stack{display:grid;gap:12px}.card,.transition-card{border:1px solid var(--td-line);border-radius:18px;padding:16px;background:rgba(0,0,0,.18);min-width:0}.card strong{display:block;font-size:clamp(1.05rem,4vw,1.45rem);overflow-wrap:anywhere;line-height:1.08}.status{display:inline-flex;margin:3px 5px 3px 0;border:1px solid rgba(67,214,148,.35);border-radius:999px;padding:5px 9px;background:rgba(67,214,148,.08);color:var(--td-green);font-size:.78rem;text-transform:uppercase}.status.locked{color:var(--td-red);border-color:rgba(255,100,100,.35);background:rgba(255,100,100,.08)}.status.observed,.status.candidate,.status.frontier{color:var(--td-gold);border-color:rgba(255,190,84,.35);background:rgba(255,190,84,.08)}.transition-head{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}.transition-id{font-size:1.6rem;font-weight:950;letter-spacing:-.04em}.bar{height:8px;border-radius:999px;background:rgba(255,255,255,.08);overflow:hidden}.bar span{display:block;height:100%;background:linear-gradient(90deg,var(--td-green),var(--td-blue))}ul{margin:8px 0 0;padding-left:20px;color:#dbe7f7}li{margin-bottom:7px}details{margin-top:10px;color:#dbe7f7}summary{cursor:pointer;color:var(--td-text);font-weight:800}.machine-link{display:inline-flex;margin-top:10px;border:1px solid rgba(67,214,148,.35);border-radius:999px;padding:8px 12px;background:rgba(67,214,148,.08);color:var(--td-text);font-weight:800;text-decoration:none}@media(max-width:760px){.grid{grid-template-columns:1fr}section{border-radius:18px}}
    `;
    document.head.appendChild(style);
  }

  injectTransitionDiscoveryStyles();

  const h = value => String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
  const list = values => `<ul>${(values || []).map(value => `<li>${h(value)}</li>`).join("") || "<li>None declared.</li>"}</ul>`;
  const pill = value => `<span class="status ${String(value).toLowerCase().replaceAll("_", "-")}">${h(value).replaceAll("_", " ")}</span>`;
  const section = (title, body) => `<section><h2>${h(title)}</h2>${body}</section>`;
  const card = (title, body, kicker = "") => `<div class="card">${kicker ? `<span class="kicker">${h(kicker)}</span>` : ""}<strong>${h(title)}</strong>${body}</div>`;
  const byId = id => state.partitions.find(partition => partition.id === id);

  function machineLink() {
    return `<p><a class="machine-link" href="${jsonStateHref}">Open machine-readable discovery state JSON</a></p>`;
  }

  function hero(title, role, description) {
    return `<section class="hero"><p class="kicker">${h(role)}</p><h1>${h(title)}</h1><p>${h(description || state.research_premise.short_definition)}</p><p>${pill(state.release_state.current_release)} ${pill(state.release_state.current_frontier)} ${pill(state.release_state.table_status)}</p>${machineLink()}</section>`;
  }

  function premise() {
    return section("Research Premise", `<p>${h(state.research_premise.short_definition)}</p><p><strong>Central question:</strong> ${h(state.research_premise.central_question)}</p><p><strong>Working claim:</strong> ${h(state.research_premise.working_claim)}</p><p><strong>Public caution:</strong> ${h(state.research_premise.public_caution)}</p>`);
  }

  function lifecycleLegend() {
    return section("Discovery Lifecycle", `<div class="grid lifecycle-grid">${state.lifecycle.map(item => card(item.id, `<p>${h(item.meaning)}</p>`, "Lifecycle State")).join("")}</div>`);
  }

  function partitionCard(partition) {
    const width = Math.max(0, Math.min(100, Number(partition.evidence_level || 0) * 20));
    return `<article class="transition-card status-${h(partition.status).toLowerCase()}">
      <div class="transition-head"><span class="transition-id">${h(partition.id)}</span>${pill(partition.status)}</div>
      <h3>${h(partition.name)}</h3>
      <p><strong>Confidence:</strong> ${h(partition.confidence)} · <strong>Family:</strong> ${h(partition.family)}</p>
      <p>${h(partition.partition_claim)}</p>
      <p><strong>Distinctness:</strong> ${h(partition.distinctness)}</p>
      <p><strong>Evidence:</strong> ${h((partition.evidence || []).join(", ") || "none declared")}</p>
      <div class="bar"><span style="width:${width}%"></span></div>
      <details><summary>Open questions</summary>${list(partition.open_questions)}</details>
    </article>`;
  }

  function tableView() {
    const sorted = [...state.partitions].sort((a, b) => Number(a.order) - Number(b.order));
    const counts = state.lifecycle.map(item => {
      const count = state.partitions.filter(partition => partition.status === item.id).length;
      return card(item.id, `<p>${count} partition${count === 1 ? "" : "s"}</p>`, "Current Count");
    }).join("");
    return hero("Transition Table", "Map of Discovered Transition Space", "The table visualizes the current discovery state. Blocks illuminate only when a transition partition crosses a declared threshold.") + premise() + section("Current Table State", `<div class="grid">${counts}</div>`) + section("Transition Partitions", `<div class="table-grid">${sorted.map(partitionCard).join("")}</div>`) + lifecycleLegend();
  }

  function milestonesView() {
    return hero("Transition Milestones", "Epistemic Ledger of Threshold Crossings", "Milestones record changes in public discovery state, not ordinary software releases.") + section("Discovery Events", `<div class="stack">${state.milestones.map(m => card(`${m.id} — ${m.title}`, `<p>${h(m.discovery_meaning)}</p><p>${pill(m.status)}</p><p><strong>Affected partitions:</strong> ${h((m.affected_partitions || []).join(", ") || "none")}</p><p><strong>Evidence:</strong> ${h((m.evidence || []).join(", ") || "none declared")}</p><p><strong>Next frontier:</strong> ${h(m.next_frontier || "none")}</p>`, m.date || "Milestone")).join("")}</div>`) + section("Why This Matters", `<p>A milestone means the table learned something: a transition was observed, partitioned, modeled, sandboxed, receipt-backed, promoted, merged, or deprecated.</p>`);
  }

  function developmentView() {
    const f = state.frontier;
    return hero("Transition Development Status", "Current Frontier of the Exploration", "This page shows what is being actively tested, repaired, separated, merged, or deprecated now.") + section(`${f.id} — ${f.title}`, `<p>${h(f.research_question)}</p>${pill(f.status)}<h3>Active work</h3>${list(f.active_work)}<h3>Candidate outcomes</h3>${list(f.candidate_outcomes)}<h3>Unlock condition</h3><p>${h(f.unlock_condition)}</p>`);
  }

  function snapshotView() {
    const snap = state.snapshots[0];
    return hero("Transition Release Snapshot", "Frozen Knowledge Boundary", "A snapshot freezes what the table knew at a release boundary and what it did not claim.") + section(`${snap.id} — ${snap.title}`, `${pill(snap.status)}<div class="grid"><div>${card("This snapshot knows", list(snap.knows), "Known Claims")}</div><div>${card("This snapshot does not claim", list(snap.does_not_claim), "Non-Claims")}</div></div><p><strong>Receipt-backed partitions:</strong> ${h(snap.receipt_backed_partitions.join(", "))}</p><p><strong>Frontier:</strong> ${h(snap.frontier)}</p>`);
  }

  function releaseIndexView() {
    return hero("Transition Release Index", "Index of Public Discovery States", "This index shows the historical sequence of public table states and what each state added to the discovery process.") + section("Release Sequence", `<div class="stack">${state.milestones.map(m => card(`${m.id} — ${m.title}`, `<p>${h(m.discovery_meaning)}</p><p>${pill(m.status)}</p><p><strong>Evidence:</strong> ${h((m.evidence || []).join(", ") || "none declared")}</p>`, "Discovery State")).join("")}</div>`) + section("Public Surfaces", `<ul><li><a href="transition-table.html">Map of discovered transition space</a></li><li><a href="transition-milestones.html">Epistemic ledger</a></li><li><a href="transition-development-status.html">Current frontier</a></li><li><a href="transition-release-snapshot.html">Frozen knowledge boundary</a></li><li><a href="transition-verification-guide.html">Verification procedure</a></li><li><a href="transition-replay-packet.html">Replayable evidence</a></li><li><a href="${jsonStateHref}">Machine-readable discovery state JSON</a></li></ul>`);
  }

  function verificationView() {
    const v = state.verification_expectations;
    const receiptBacked = v.expected_receipt_backed_partitions.map(id => byId(id)).filter(Boolean);
    return hero("Transition Verification Guide", "Reader Procedure for Checking Table Claims", "This guide verifies the discovery claim, not only the website links.") + section("Expected Public State", `<div class="grid">${card("Current release", `<p>${h(v.current_release)}</p>`, "Expectation")}${card("Current frontier", `<p>${h(v.expected_frontier)}</p>`, "Expectation")}${card("Replay verdict", `<p>${h(v.expected_replay_verdict)}</p>`, "Expectation")}${card("Page contract failures", `<p>${h(v.expected_page_contract_failures)}</p>`, "Expectation")}</div>`) + section("Receipt-backed Partition Checks", `<div class="stack">${receiptBacked.map(p => card(`${p.id} — ${p.name}`, `<p>Status must be RECEIPT_BACKED and evidence must reference a public evidence record.</p><p><strong>Evidence:</strong> ${h(p.evidence.join(", "))}</p>`, p.status)).join("")}</div>`) + section("Stale-State Warnings", list(v.stale_state_warnings)) + section("Machine-readable mirror", `<p>The JSON mirror supports validators, ingestion engines, and non-browser consumers.</p>${machineLink()}`);
  }

  function replayView() {
    const packet = state.replay_packets[0];
    return hero("Transition Replay Packet", "Reconstructable Evidence Surface", "Replay packets bridge description and reconstruction for specific transition claims.") + section(`${packet.id} — ${packet.title}`, `${pill(packet.status)}<p><strong>Supports:</strong> ${h(packet.supports.join(", "))}</p><div class="stack">${packet.replay_claims.map(claim => card(`${claim.partition} replay claim`, `<p>${h(claim.claim)}</p><p><strong>Expected result:</strong> ${h(claim.expected_result)}</p><p><strong>Failure condition:</strong> ${h(claim.failure_condition)}</p>`, "Replay Claim")).join("")}</div><h3>Limitations</h3>${list(packet.limitations)}`);
  }

  const views = { table: tableView, milestones: milestonesView, "development-status": developmentView, "release-snapshot": snapshotView, "release-index": releaseIndexView, "verification-guide": verificationView, "replay-packet": replayView };
  const view = root.dataset.transitionView;
  root.innerHTML = (views[view] || tableView)();
})();
