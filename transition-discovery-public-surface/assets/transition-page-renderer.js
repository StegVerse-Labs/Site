(() => {
  const state = window.STEGVERSE_TRANSITION_DISCOVERY_STATE;
  const root = document.getElementById("transition-page-root");
  if (!state || !root) return;

  const $ = (value) => String(value ?? "").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;");
  const slug = (value) => String(value || "").toLowerCase().replaceAll("_","-");
  const lifecycle = Object.fromEntries(state.discovery_lifecycle.map(item => [item.id, item]));
  const partitions = Object.fromEntries(state.partitions.map(item => [item.id, item]));
  const evidence = Object.fromEntries(state.evidence_records.map(item => [item.id, item]));
  const rank = (status) => lifecycle[status]?.rank ?? 0;
  const statusClass = (status) => {
    if (["RECEIPT_BACKED","PROMOTED","SANDBOXED"].includes(status)) return "status";
    if (["MODELED","PARTITIONED"].includes(status)) return "status blue";
    if (["CANDIDATE","OBSERVED"].includes(status)) return "status gold";
    if (["MERGED","DEPRECATED"].includes(status)) return "status red";
    if (status === "LOCKED") return "status violet";
    return "status";
  };
  const list = (items) => items && items.length ? `<ul>${items.map(item => `<li>${$(item)}</li>`).join("")}</ul>` : "<p class=\"muted\">None declared.</p>";
  const linkList = (ids, collection, pageField) => ids && ids.length ? `<ul>${ids.map(id => {
    const item = collection[id] || {title:id, name:id};
    const label = item.title || item.name || id;
    const href = item[pageField] || "";
    return `<li>${href ? `<a href="${$(href)}">${$(id)} — ${$(label)}</a>` : `<span class="mono">${$(id)}</span> — ${$(label)}`}</li>`;
  }).join("")}</ul>` : "<p class=\"muted\">None declared.</p>";
  const hero = (role) => `
    <section>
      <h2>Research Role</h2>
      <p>${$(role)}</p>
      <div class="grid four">
        <div class="card"><span class="kicker">Current Release</span><strong>${$(state.current.release)}</strong><p>${$(state.milestones.find(m => m.id === state.current.release)?.title || "")}</p></div>
        <div class="card"><span class="kicker">Current Frontier</span><strong>${$(state.current.frontier)}</strong><p>${$(state.frontier.title)}</p></div>
        <div class="card"><span class="kicker">Table State</span><strong>${$(state.current.table_status)}</strong><p>Discovery state is canonical; page copy is a view.</p></div>
        <div class="card"><span class="kicker">Updated</span><strong>${$(state.last_updated)}</strong><p>${$(state.schema_version)}</p></div>
      </div>
    </section>
    <section>
      <h2>Research Premise</h2>
      <p><strong>${$(state.research_premise.short_definition)}</strong></p>
      <p>${$(state.research_premise.central_question)}</p>
      <p>${$(state.research_premise.working_claim)}</p>
      <p class="muted">${$(state.research_premise.public_caution)}</p>
    </section>`;

  const partitionCard = (p) => {
    const width = Math.round((rank(p.status) / 7) * 100);
    const isLocked = p.status === "LOCKED" ? " locked" : "";
    return `<article class="transition-card${isLocked}">
      <div class="id">${$(p.id)}</div>
      <div class="name">${$(p.name)}</div>
      <span class="${statusClass(p.status)}">${$(p.status.replaceAll("_"," "))}</span>
      <span class="status blue">${$(p.confidence)}</span>
      <div class="meta">${$(p.partition_claim)}</div>
      <div class="brightness"><span style="--w:${Math.max(0, Math.min(100, width))}%"></span></div>
      <div class="meta">Evidence: ${p.evidence?.length ? p.evidence.map($).join(", ") : "none public"}</div>
      <details>
        <summary>Open partition record</summary>
        ${partitionDetails(p)}
      </details>
    </article>`;
  };

  const partitionDetails = (p) => `
    <dl>
      <dt>Distinctness</dt><dd>${$(p.distinctness)}</dd>
      <dt>Admissibility boundary</dt><dd>${$(p.admissibility_boundary)}</dd>
      <dt>Authority requirement</dt><dd>${$(p.authority_requirement)}</dd>
      <dt>Reality-touch condition</dt><dd>${$(p.reality_touch_condition)}</dd>
      <dt>Reversibility class</dt><dd>${$(p.reversibility_class)}</dd>
      <dt>Entropy / imprint cost</dt><dd>${$(p.entropy_imprint_cost)}</dd>
      <dt>Observer-reality coupling</dt><dd>${$(p.observer_reality_coupling)}</dd>
      <dt>Receipt requirement</dt><dd>${$(p.receipt_requirement)}</dd>
      <dt>Failure mode</dt><dd>${$(p.failure_mode)}</dd>
      <dt>Open questions</dt><dd>${list(p.open_questions)}</dd>
    </dl>`;

  const renderLifecycle = () => `
    <section>
      <h2>Discovery Lifecycle</h2>
      <div class="grid">
        ${state.discovery_lifecycle.map(item => `<div class="card"><span class="${statusClass(item.id)}">${$(item.id.replaceAll("_"," "))}</span><p><strong>${$(item.public_interpretation)}</strong></p><p>${$(item.meaning)}</p></div>`).join("")}
      </div>
    </section>`;

  const renderTable = () => {
    const counts = state.partitions.reduce((acc, p) => (acc[p.status] = (acc[p.status] || 0) + 1, acc), {});
    root.innerHTML = hero("Map of discovered transition space.") + `
      <section>
        <h2>Discovery State Summary</h2>
        <div class="grid four">
          ${Object.entries(counts).map(([status,count]) => `<div class="card"><span class="${statusClass(status)}">${$(status.replaceAll("_"," "))}</span><strong>${count}</strong><p>${$(lifecycle[status]?.public_interpretation || "")}</p></div>`).join("")}
        </div>
      </section>
      ${renderLifecycle()}
      <section>
        <h2>Transition Partition Map</h2>
        <p>A block illuminates only according to its canonical lifecycle status. Locked space remains visible because the unknown is part of the research surface.</p>
        <div class="table-grid">${state.partitions.map(partitionCard).join("")}</div>
      </section>
      <section>
        <h2>Transition Dimensions</h2>
        <div class="grid">${state.transition_dimensions.map(d => `<div class="card"><span class="kicker">${$(d.label)}</span><p>${$(d.question)}</p></div>`).join("")}</div>
      </section>`;
  };

  const renderMilestones = () => {
    root.innerHTML = hero("Epistemic ledger of discovery threshold crossings.") + `
      <section>
        <h2>Milestone Ledger</h2>
        <div class="timeline">
          ${state.milestones.map(m => `<article class="card">
            <span class="${m.status === "released" ? "status" : "status gold"}">${$(m.status)}</span>
            <h3>${$(m.id)} — ${$(m.title)}</h3>
            <p><strong>Discovery meaning:</strong> ${$(m.discovery_meaning)}</p>
            <p><strong>Affected partitions:</strong> ${m.affected_partitions?.length ? m.affected_partitions.map(id => `${$(id)} ${partitions[id] ? "— " + $(partitions[id].name) : ""}`).join(", ") : "none declared"}</p>
            ${m.threshold_crossed?.length ? `<p><strong>Threshold crossed:</strong></p><ul>${m.threshold_crossed.map(t => `<li>${$(t.partition)}: ${$(t.from)} → ${$(t.to)}</li>`).join("")}</ul>` : ""}
            <p><strong>Evidence:</strong></p>${linkList(m.evidence, evidence, "public_page")}
            <p><strong>Unresolved questions:</strong></p>${list(m.unresolved_questions)}
            ${m.next_frontier ? `<p><strong>Next frontier:</strong> ${$(m.next_frontier)}</p>` : ""}
          </article>`).join("")}
        </div>
      </section>`;
  };

  const renderDevelopmentStatus = () => {
    const candidates = state.partitions.filter(p => ["OBSERVED","CANDIDATE","PARTITIONED","MODELED"].includes(p.status));
    root.innerHTML = hero("Current frontier of the exploration.") + `
      <section>
        <h2>Current Frontier</h2>
        <div class="card">
          <span class="status gold">${$(state.frontier.status)}</span>
          <h3>${$(state.frontier.id)} — ${$(state.frontier.title)}</h3>
          <p><strong>Research question:</strong> ${$(state.frontier.research_question)}</p>
          <p><strong>Unlock condition:</strong> ${$(state.frontier.unlock_condition)}</p>
        </div>
      </section>
      <section><h2>Active Work</h2>${list(state.frontier.active_work)}</section>
      <section><h2>Candidate Outcomes</h2><div class="grid">${state.frontier.candidate_outcomes.map(item => `<div class="card"><strong>${$(item)}</strong></div>`).join("")}</div></section>
      <section><h2>Blockers</h2>${list(state.frontier.blockers)}</section>
      <section><h2>Partitions Under Active Pressure</h2><div class="table-grid">${candidates.map(partitionCard).join("")}</div></section>`;
  };

  const renderReleaseSnapshot = () => {
    const snap = state.snapshots.find(s => s.id === state.current.release) || state.snapshots[0];
    root.innerHTML = hero("Frozen knowledge boundary.") + `
      <section>
        <h2>${$(snap.id)} — ${$(snap.title)}</h2>
        <span class="status">${$(snap.status)}</span>
      </section>
      <section><h2>What This Snapshot Knows</h2>${list(snap.knows)}</section>
      <section class="warning"><h2>What This Snapshot Does Not Claim</h2>${list(snap.does_not_claim)}</section>
      <section>
        <h2>Snapshot Partition Sets</h2>
        <div class="grid four">
          <div class="card"><span class="kicker">Receipt-backed</span><strong>${snap.receipt_backed_partitions.length}</strong>${linkList(snap.receipt_backed_partitions, partitions, "")}</div>
          <div class="card"><span class="kicker">Promoted</span><strong>${snap.promoted_partitions.length}</strong>${linkList(snap.promoted_partitions, partitions, "")}</div>
          <div class="card"><span class="kicker">Candidate</span><strong>${snap.candidate_partitions.length}</strong>${linkList(snap.candidate_partitions, partitions, "")}</div>
          <div class="card"><span class="kicker">Frontier</span><strong>${$(snap.frontier)}</strong><p>${$(state.frontier.title)}</p></div>
        </div>
      </section>`;
  };

  const renderReleaseIndex = () => {
    root.innerHTML = hero("Index of public discovery states.") + `
      <section>
        <h2>Public Discovery State Sequence</h2>
        <div class="timeline">
          ${state.milestones.map(m => `<article class="card">
            <span class="${m.status === "released" ? "status" : "status gold"}">${$(m.status)}</span>
            <h3>${$(m.id)} — ${$(m.title)}</h3>
            <p>${$(m.discovery_meaning)}</p>
            <p><strong>Evidence availability:</strong> ${m.evidence?.length ? "yes" : "none declared"}</p>
            <p><strong>Replay availability:</strong> ${m.evidence?.some(id => evidence[id]?.type === "replay_packet") ? "yes" : "not for this state"}</p>
          </article>`).join("")}
        </div>
      </section>
      <section>
        <h2>Page Roles</h2>
        <div class="grid">
          ${Object.entries(state.page_roles).map(([page, role]) => `<a class="card" href="${$(page)}"><span class="kicker">${$(role)}</span><strong>${$(page)}</strong></a>`).join("")}
        </div>
      </section>`;
  };

  const renderVerificationGuide = () => {
    const v = state.verification_expectations;
    root.innerHTML = hero("Reader procedure for checking table claims.") + `
      <section>
        <h2>Expected Current State</h2>
        <div class="grid four">
          <div class="card"><span class="kicker">Release</span><strong>${$(v.current_release)}</strong></div>
          <div class="card"><span class="kicker">Frontier</span><strong>${$(v.expected_frontier)}</strong></div>
          <div class="card"><span class="kicker">Replay Verdict</span><strong>${$(v.expected_replay_verdict)}</strong></div>
          <div class="card"><span class="kicker">Page Contract Failures</span><strong>${$(v.expected_page_contract_failures)}</strong></div>
        </div>
      </section>
      <section>
        <h2>Expected Receipt-backed Partitions</h2>
        <div class="table-grid">${v.expected_receipt_backed_partitions.map(id => partitionCard(partitions[id])).join("")}</div>
      </section>
      <section><h2>Block Verification Procedure</h2>${list(v.block_verification_procedure)}</section>
      <section class="warning"><h2>Stale-State Warnings</h2>${list(v.stale_state_warnings)}</section>
      <section>
        <h2>Unlock Rules</h2>
        <div class="grid">
          ${state.unlock_rules.map(rule => `<div class="card"><span class="kicker">${$(rule.from)} → ${$(rule.to)}</span><p>${$(rule.meaning)}</p><p><strong>Required:</strong></p>${list(rule.required)}</div>`).join("")}
        </div>
      </section>`;
  };

  const renderReplayPacket = () => {
    root.innerHTML = hero("Reconstructable evidence surface.") + `
      <section>
        <h2>Replay Packets</h2>
        <div class="timeline">
          ${state.replay_packets.map(packet => `<article class="card">
            <span class="status">${$(packet.status)}</span>
            <h3>${$(packet.id)} — ${$(packet.title)}</h3>
            <p><strong>Supports:</strong> ${packet.supports.map(id => `${$(id)} — ${$(partitions[id]?.name || "")}`).join(", ")}</p>
            <h3>Replay Claims</h3>
            <div class="grid">
              ${packet.replay_claims.map(claim => `<div class="card">
                <span class="kicker">${$(claim.partition)}</span>
                <p>${$(claim.claim)}</p>
                <p><strong>Expected:</strong> ${$(claim.expected_result)} · <strong>Actual:</strong> ${$(claim.actual_result)}</p>
                <p><strong>Failure condition:</strong> ${$(claim.failure_condition)}</p>
              </div>`).join("")}
            </div>
            <h3>Limitations</h3>${list(packet.limitations)}
          </article>`).join("")}
        </div>
      </section>
      <section>
        <h2>Evidence Records</h2>
        <div class="grid">
          ${state.evidence_records.map(ev => `<article class="card">
            <span class="${ev.status === "public" ? "status" : "status gold"}">${$(ev.status)}</span>
            <h3>${$(ev.id)} — ${$(ev.title)}</h3>
            <p>${$(ev.evidence_meaning)}</p>
            <p><strong>Supports:</strong> ${ev.supports.map(id => `${$(id)} — ${$(partitions[id]?.name || "")}`).join(", ")}</p>
            <p><strong>Expected verdict:</strong> ${$(ev.expected_verdict)} · <strong>Actual:</strong> ${$(ev.actual_verdict)}</p>
            <p><strong>Limitations:</strong></p>${list(ev.limitations)}
          </article>`).join("")}
        </div>
      </section>`;
  };

  const view = root.dataset.transitionView;
  const renderers = {
    "table": renderTable,
    "milestones": renderMilestones,
    "development-status": renderDevelopmentStatus,
    "release-snapshot": renderReleaseSnapshot,
    "release-index": renderReleaseIndex,
    "verification-guide": renderVerificationGuide,
    "replay-packet": renderReplayPacket
  };
  (renderers[view] || renderTable)();
})();