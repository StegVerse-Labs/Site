// cfp.js
//
// Front-end logic for NCAAF CFP Live Tracker
//
// It expects a JSON endpoint at CFP_DATA_URL that returns:
//
// {
//   "last_updated": "2025-11-29T18:05:00Z",
//   "rankings": [
//     { "seed": 1, "team": "Ohio State", "record": "12-0", "conference": "Big Ten" },
//     ...
//   ],
//   "games": [
//     {
//       "id": "ttu-byu-2025-big12",
//       "home": "Texas Tech",
//       "away": "BYU",
//       "home_score": 45,
//       "away_score": 17,
//       "status": "Final",
//       "note": "Big 12 Championship Game"
//     },
//     ...
//   ]
// }

const CFP_DATA_URL =
  window.CFP_DATA_URL ||
  "/cfp-data.json"; // you can override this with a global var if needed

const elRankings = document.getElementById("cfp-rankings");
const elGames = document.getElementById("cfp-games");
const elLastUpdated = document.getElementById("cfp-last-updated");
const elStatus = document.getElementById("cfp-status");
const elRefreshBtn = document.getElementById("cfp-refresh-btn");

function setStatus(message, isError = false) {
  if (!elStatus) return;
  elStatus.textContent = message || "";
  elStatus.style.color = isError ? "#ff8080" : "#b0ffa8";
}

function formatDateTime(iso) {
  if (!iso) return "—";
  try {
    const d = new Date(iso);
    return d.toLocaleString(undefined, {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit",
    });
  } catch {
    return iso;
  }
}

function renderRankings(rankings) {
  if (!Array.isArray(rankings) || rankings.length === 0) {
    elRankings.innerHTML = "<p>No rankings available.</p>";
    return;
  }

  const rows = rankings
    .map((r) => {
      const seed = r.seed ?? r.rank ?? "?";
      const team = r.team ?? r.name ?? "Unknown";
      const record = r.record ?? "";
      const conf = r.conference ?? r.conf ?? "";
      return `
        <tr>
          <td class="cfp-seed">#${seed}</td>
          <td>${team}</td>
          <td>${record}</td>
          <td>${conf}</td>
        </tr>
      `;
    })
    .join("");

  elRankings.innerHTML = `
    <table class="cfp-rankings-table">
      <thead>
        <tr>
          <th>Seed</th>
          <th>Team</th>
          <th>Record</th>
          <th>Conf</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

function renderGames(games) {
  if (!Array.isArray(games) || games.length === 0) {
    elGames.innerHTML = "<p>No tracked games yet.</p>";
    return;
  }

  const items = games
    .map((g) => {
      const home = g.home || "Home";
      const away = g.away || "Away";
      const hs = g.home_score ?? "-";
      const as = g.away_score ?? "-";
      const status = g.status ?? "";
      const note = g.note ?? "";
      const kickoff = g.kickoff ? formatDateTime(g.kickoff) : "";

      return `
        <li class="cfp-game">
          <div class="cfp-game-header">
            <span>${away} @ ${home}</span>
            <span>${as} – ${hs}</span>
          </div>
          <div class="cfp-game-meta">
            ${status ? `<span>Status: ${status}</span>` : ""}
            ${
              kickoff
                ? `<span style="margin-left:0.5rem;">Kickoff: ${kickoff}</span>`
                : ""
            }
            ${note ? `<span style="margin-left:0.5rem;">${note}</span>` : ""}
          </div>
        </li>
      `;
    })
    .join("");

  elGames.innerHTML = `<ul class="cfp-games-list">${items}</ul>`;
}

async function loadCfpData() {
  setStatus("Refreshing…");
  try {
    const res = await fetch(CFP_DATA_URL + "?_t=" + Date.now(), {
      cache: "no-store",
    });
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    const data = await res.json();
    renderRankings(data.rankings || []);
    renderGames(data.games || []);
    if (elLastUpdated) {
      elLastUpdated.textContent =
        "Last updated: " + formatDateTime(data.last_updated);
    }
    setStatus("Updated.", false);
  } catch (err) {
    console.error("Failed to load CFP data:", err);
    setStatus("Failed to load live data.", true);
  }
}

if (elRefreshBtn) {
  elRefreshBtn.addEventListener("click", () => {
    loadCfpData();
  });
}

// Initial load
loadCfpData();
