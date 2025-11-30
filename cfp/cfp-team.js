// cfp/team.js
// Generic team detail page: driven by ?team=<slug> and data/cfp-2025.json.

function getQueryParam(name) {
  const url = new URL(window.location.href);
  return url.searchParams.get(name);
}

async function loadCFPData() {
  try {
    const res = await fetch("../data/cfp-2025.json", { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error("Failed to load CFP data:", err);
    return null;
  }
}

function formatDate(str) {
  if (!str) return "TBD";
  try {
    const d = new Date(str);
    if (Number.isNaN(d.getTime())) return str;
    return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
  } catch {
    return str;
  }
}

function renderSchedule(schedule) {
  const empty = document.getElementById("schedule-empty");
  const wrapper = document.getElementById("schedule-table-wrapper");
  const tbody = document.getElementById("schedule-body");

  if (!tbody) return;

  if (!Array.isArray(schedule) || schedule.length === 0) {
    if (empty) empty.style.display = "block";
    if (wrapper) wrapper.style.display = "none";
    return;
  }

  if (empty) empty.style.display = "none";
  if (wrapper) wrapper.style.display = "block";

  tbody.innerHTML = "";

  schedule.forEach((g) => {
    const tr = document.createElement("tr");

    const tdLabel = document.createElement("td");
    tdLabel.textContent = g.label || "";
    tr.appendChild(tdLabel);

    const tdOpp = document.createElement("td");
    tdOpp.textContent = g.opponent || "";
    tr.appendChild(tdOpp);

    const tdLoc = document.createElement("td");
    tdLoc.textContent = g.location || "";
    tr.appendChild(tdLoc);

    const tdDate = document.createElement("td");
    tdDate.textContent = formatDate(g.date);
    tr.appendChild(tdDate);

    const tdResult = document.createElement("td");
    tdResult.textContent = g.result || "TBD";
    tr.appendChild(tdResult);

    const tdNote = document.createElement("td");
    tdNote.textContent = g.note || "";
    tr.appendChild(tdNote);

    tbody.appendChild(tr);
  });
}

function applyTeamColors(team) {
  if (!team || !team.primaryColor) return;
  const root = document.documentElement;
  root.style.setProperty("--team-primary", team.primaryColor);
  if (team.secondaryColor) {
    root.style.setProperty("--team-secondary", team.secondaryColor);
  }
}

function renderTeam(team, season) {
  const title = document.getElementById("team-title");
  const meta = document.getElementById("team-meta");
  const recEl = document.getElementById("team-record");
  const confEl = document.getElementById("team-conference");
  const seedEl = document.getElementById("team-seed");
  const bestEl = document.getElementById("scenario-best");
  const likelyEl = document.getElementById("scenario-likely");
  const worstEl = document.getElementById("scenario-worst");

  applyTeamColors(team);

  if (title) {
    title.textContent = `${team.name} – Road to the ${season} Title`;
  }
  if (meta) {
    meta.textContent = `Current CFP seed #${team.seed} in the ${season} season. Projections are relative to the most recent CFP release.`;
  }
  if (recEl) {
    recEl.textContent = `Record: ${team.record || "—"}`;
  }
  if (confEl) {
    confEl.textContent = `Conference: ${team.conference || "—"}`;
  }
  if (seedEl) {
    seedEl.textContent = `Seed: #${team.seed}`;
  }

  const scenarios = team.scenarios || {};
  if (bestEl) bestEl.textContent = scenarios.bestCase || "No best-case scenario configured yet.";
  if (likelyEl) likelyEl.textContent = scenarios.mostLikely || "No most-likely scenario configured yet.";
  if (worstEl) worstEl.textContent = scenarios.worstCase || "No nightmare scenario configured yet.";

  renderSchedule(team.schedule || []);
}

function renderNotFound(slug, data) {
  const title = document.getElementById("team-title");
  const meta = document.getElementById("team-meta");
  const cards = document.querySelectorAll(".cfp-card");

  if (title) title.textContent = "Team not found in current CFP Top 12";
  if (meta) meta.textContent = slug
    ? `We couldn't find a team for identifier "${slug}".`
    : "No team identifier was provided.";

  const schedCard = cards[2];
  if (schedCard) schedCard.style.display = "none";

  // Optional: show a simple list of valid teams for quick copy/paste.
  const list = document.createElement("ul");
  list.className = "cfp-simple-list";

  if (data && Array.isArray(data.teams)) {
    data.teams
      .slice()
      .sort((a, b) => (a.seed || 999) - (b.seed || 999))
      .forEach((t) => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = `team.html?team=${encodeURIComponent(t.slug)}`;
        a.textContent = `#${t.seed} – ${t.name}`;
        li.appendChild(a);
        list.appendChild(li);
      });
  }

  const main = document.querySelector("main");
  if (main) {
    const wrapper = document.createElement("section");
    wrapper.className = "cfp-card";
    const h2 = document.createElement("h2");
    h2.className = "cfp-section-title";
    h2.textContent = "Available CFP Teams";
    wrapper.appendChild(h2);
    wrapper.appendChild(list);
    main.appendChild(wrapper);
  }
}

async function initTeamPage() {
  const slug = getQueryParam("team");
  const data = await loadCFPData();

  if (!data || !Array.isArray(data.teams)) {
    renderNotFound(slug, data);
    return;
  }

  const season = data.season || "2025";

  const team =
    data.teams.find((t) => String(t.slug) === String(slug)) ||
    data.teams.find((t) => String(t.seed) === String(slug));

  if (!team) {
    renderNotFound(slug, data);
    return;
  }

  renderTeam(team, season);
}

document.addEventListener("DOMContentLoaded", initTeamPage);
