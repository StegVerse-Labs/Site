// cfp/bracket.js
// Historical-only bracket table driven by data/cfp-2025.json.
// It must never be represented as current-season CFP state.

async function loadCFPData() {
  try {
    const res = await fetch("../data/cfp-2025.json", { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error("Failed to load historical 2025 CFP data:", err);
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

  const tdSeed = document.createElement("td");
  tdSeed.textContent = team.seed;
  tr.appendChild(tdSeed);

  const tdTeam = document.createElement("td");
  const link = document.createElement("a");
  link.href = `team.html?team=${encodeURIComponent(team.slug)}`;
  link.textContent = team.name;
  link.className = "cfp-team-link";
  tdTeam.appendChild(link);
  tr.appendChild(tdTeam);

  const tdRecord = document.createElement("td");
  tdRecord.textContent = team.record || "—";
  tr.appendChild(tdRecord);

  const tdConf = document.createElement("td");
  tdConf.textContent = team.conference || "—";
  tr.appendChild(tdConf);

  const tdSince = document.createElement("td");
  tdSince.textContent = formatSinceLast(team.sinceLastRanking);
  tr.appendChild(tdSince);

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
    tbody.innerHTML = '<tr><td colspan="6">Unable to load the historical 2025 CFP snapshot.</td></tr>';
    return;
  }

  const observedSeason = Number(data.season || 2025);
  if (observedSeason !== 2025) {
    tbody.innerHTML = '<tr><td colspan="6">Historical bracket refused: expected the explicit 2025 snapshot.</td></tr>';
    if (releaseNote) {
      releaseNote.textContent = "Historical boundary check failed; this page will not relabel another season as 2025.";
    }
    return;
  }

  if (releaseNote) {
    const release = data.cfp_release_date ? ` CFP release ${data.cfp_release_date}.` : "";
    releaseNote.textContent = `Historical 2025 snapshot.${release} This is not current 2026 CFP committee status.`;
  }

  const teams = [...data.teams].sort((a, b) => (a.seed || 999) - (b.seed || 999));
  tbody.innerHTML = "";
  teams.forEach((team) => tbody.appendChild(buildRow(team)));
}

document.addEventListener("DOMContentLoaded", initBracket);
