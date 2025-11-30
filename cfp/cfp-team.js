// cfp-team.js – per-team CFP road view

const CFP_TEAMS_URL = window.CFP_TEAMS_URL || "/data/cfp-teams.json";

const elTitle = document.getElementById("team-title");
const elMeta = document.getElementById("team-meta");
const elSnapshot = document.getElementById("team-snapshot");
const elSinceLast = document.getElementById("team-since-last");
const elBest = document.getElementById("team-best");
const elWorst = document.getElementById("team-worst");
const elLikely = document.getElementById("team-likely");
const elRemaining = document.getElementById("team-remaining");
const elNotes = document.getElementById("team-notes");

// Utility to read ?team=slug
function getTeamIdFromQuery() {
  const qs = new URLSearchParams(window.location.search);
  return qs.get("team");
}

function escapeHTML(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function renderTeam(meta, t) {
  elTitle.textContent = `${t.name} – CFP Road`;
  elMeta.innerHTML = `
    <div><strong>Conference:</strong> ${escapeHTML(t.conference || "")}</div>
    <div><strong>Current CFP Seed:</strong> #${t.current_seed ?? "–"}</div>
    <div><strong>Record:</strong> ${escapeHTML(t.current_record || "")}</div>
    <div><strong>CFP Rank at Last Release:</strong> #${t.cfp_rank_at_last_release ?? "–"}</div>
    ${
      meta && meta.last_cfp_release
        ? `<div><strong>Last CFP Ranking Release:</strong> ${new Date(
            meta.last_cfp_release
          ).toLocaleString()}</div>`
        : ""
    }
  `;

  elSnapshot.innerHTML = `
    <ul>
      <li><strong>Current Seed:</strong> #${t.current_seed ?? "–"}</li>
      <li><strong>Record:</strong> ${escapeHTML(t.current_record || "")}</li>
      <li><strong>Conference:</strong> ${escapeHTML(t.conference || "")}</li>
    </ul>
  `;

  if (t.since_last_release && (t.since_last_release.wins || t.since_last_release.losses)) {
    const g = t.since_last_release.games || [];
    const gamesList = g
      .map(
        (x) => `
      <li>
        <strong>${escapeHTML(x.result || "")}</strong> vs ${escapeHTML(
          x.opponent || ""
        )} (${escapeHTML(x.location || "")})${
          x.note ? ` – ${escapeHTML(x.note)}` : ""
        }
      </li>`
      )
      .join("");

    elSinceLast.innerHTML = `
      <p>Since last CFP release: <strong>${t.since_last_release.wins || 0}–${
      t.since_last_release.losses || 0
    }</strong></p>
      <ul>${gamesList}</ul>
    `;
  } else {
    elSinceLast.textContent = "No games reported since the last CFP release.";
  }

  elBest.innerHTML = `
    <h3>${escapeHTML(t.best_case?.headline || "Best case")}</h3>
    <p>${escapeHTML(t.best_case?.narrative || "")}</p>
  `;

  elWorst.innerHTML = `
    <h3>${escapeHTML(t.worst_case?.headline || "Worst case")}</h3>
    <p>${escapeHTML(t.worst_case?.narrative || "")}</p>
  `;

  elLikely.innerHTML = `
    <h3>${escapeHTML(t.likely_case?.headline || "Most likely case")}</h3>
    <p>${escapeHTML(t.likely_case?.narrative || "")}</p>
  `;

  if (Array.isArray(t.remaining_games) && t.remaining_games.length) {
    elRemaining.innerHTML = `
      <ul>
        ${t.remaining_games
          .map(
            (g) => `
          <li>
            <strong>${escapeHTML(g.round || g.name || "")}</strong> – ${escapeHTML(
              g.name || ""
            )}${
              g.where ? ` • ${escapeHTML(g.where)}` : ""
            }${g.note ? ` – ${escapeHTML(g.note)}` : ""}
          </li>`
          )
          .join("")}
      </ul>
    `;
  } else {
    elRemaining.textContent = "No remaining games listed.";
  }

  if (Array.isArray(t.notes) && t.notes.length) {
    elNotes.innerHTML = `
      <ul>
        ${t.notes.map((n) => `<li>${escapeHTML(n)}</li>`).join("")}
      </ul>
    `;
  } else {
    elNotes.textContent = "No additional notes.";
  }
}

async function loadTeam() {
  const teamId = getTeamIdFromQuery();
  if (!teamId) {
    elMeta.textContent = "No team specified. Use ?team=texas-tech or similar.";
    return;
  }

  try {
    const res = await fetch(CFP_TEAMS_URL + "?t=" + Date.now(), { cache: "no-store" });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();

    const meta = data.meta || {};
    const teams = data.teams || [];
    const t = teams.find((x) => x.id === teamId);

    if (!t) {
      elMeta.textContent = `Team not found for id: ${teamId}`;
      return;
    }

    renderTeam(meta, t);
  } catch (err) {
    console.error("Failed to load team data:", err);
    elMeta.textContent = "Failed to load team data.";
  }
}

loadTeam();
