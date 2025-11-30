// cfp/bracket.js
// Phase 2: bracket table is fully driven by data/cfp-2025.json.

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

function formatSinceLast(delta) {
  if (delta === null || delta === undefined || delta === "") return "—";
  const n = parseInt(delta, 10);
  if (Number.isNaN(n)) return delta;
  if (n === 0) return "—";
  return n > 0 ? `+${n}` : `${n}`;
}

function buildRow(team) {
  const tr = document.createElement("tr");

  // Seed
  const tdSeed = document.createElement("td");
  tdSeed.textContent = team.seed;
  tr.appendChild(tdSeed);

  // Team (clickable -> team page)
  const tdTeam = document.createElement("td");
  const link = document.createElement("a");
  link.href = `team.html?team=${encodeURIComponent(team.slug)}`;
  link.textContent = team.name;
  link.className = "cfp-team-link";
  tdTeam.appendChild(link);
  tr.appendChild(tdTeam);

  // Record
  const tdRecord = document.createElement("td");
  tdRecord.textContent = team.record || "—";
  tr.appendChild(tdRecord);

  // Conference
  const tdConf = document.createElement("td");
  tdConf.textContent = team.conference || "—";
  tr.appendChild(tdConf);

  // Since last ranking
  const tdSince = document.createElement("td");
  tdSince.textContent = formatSinceLast(team.sinceLastRanking);
  tr.appendChild(tdSince);

  // Projection
  const tdProj = document.createElement("td");
  tdProj.textContent = team.projection || "—";
  tr.appendChild(tdProj);

  return tr;
}

async function initBracket() {
  const tbody = document.getElementById("cfp-table-body");
  const releaseNote = document.getElementById("cfp-release-note");

  if (!tbody) return;

  const data = await loadCFPData();
  if (!data || !Array.isArray(data.teams)) {
    tbody.innerHTML =
      '<tr><td colspan="6">Unable to load CFP data. Please try again later.</td></tr>';
    return;
  }

  // Update release note text if we have a release date.
  if (releaseNote && data.cfp_release_date) {
    releaseNote.textContent =
      `Rankings below are synced to the CFP release on ${data.cfp_release_date}. ` +
      `Movement and projections are relative to that release.`;
  }

  const teams = [...data.teams].sort((a, b) => (a.seed || 999) - (b.seed || 999));

  tbody.innerHTML = "";
  teams.forEach((team) => {
    tbody.appendChild(buildRow(team));
  });
}

document.addEventListener("DOMContentLoaded", initBracket);
