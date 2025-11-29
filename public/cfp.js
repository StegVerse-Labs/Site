// cfp.js
//
// Front-end logic for NCAAF CFP Live Tracker with lock status & scenarios.
//
// Expected JSON from CFP_DATA_URL:
//
// {
//   "last_updated": "2025-11-29T18:05:00Z",
//   "rankings": [
//     {
//       "seed": 1,
//       "team": "Ohio State",
//       "record": "12-0",
//       "conference": "Big Ten",
//       "status": "locked",           // "locked" | "in_play" | "eliminated"
//       "lock_reason": "Big Ten champ, CFP #1",
//       "spot_scenarios": [
//         {
//           "team": "Ohio State",
//           "path": "Already locked. No remaining path changes this seed."
//         }
//       ]
//     },
//     ...
//   ],
//   "games": [ ... ]
// }

const CFP_DATA_URL =
  window.CFP_DATA_URL ||
  "/cfp-data.json"; // can be overridden with a global var before this script

const elRankings = document.getElementById("cfp-rankings");
const elGames = document.getElementById("cfp-games");
const elLastUpdated = document.getElementById("cfp-last-updated");
const elStatus = document.getElementById("cfp-status");
const elRefreshBtn = document.getElementById("cfp-refresh-btn");
const elSpotDetails = document.getElementById("cfp-spot-details");

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

function statusBadge(status) {
  const s = (status || "").toLowerCase();
  if (s === "locked") {
    return '<span class="cfp-badge cfp-badge-locked">Locked</span>';
  } else if (s === "in_play" || s === "inplay" || s === "in-play") {
    return '<span class="cfp-badge cfp-badge-inplay">In Play</span>';
  } else if (s === "eliminated" || s === "elim") {
    return '<span class="cfp-badge cfp-badge-elim">Eliminated</span>';
  }
  return "";
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
      const status = r.status ?? "";
      const lockReason = r.lock_reason ?? "";
      const badge = statusBadge(status);
      const reasonText = lockReason
        ? `<div style="font-size:0.7rem; opacity:0.8; margin-top:0.1rem;">${lockReason}</div>`
        : "";

      return `
        <tr>
          <td class="cfp-seed">#${seed}</td>
          <td>${team}</td>
          <td>${record}</td>
          <td>${conf}</td>
          <td class="cfp-status-cell">
            ${badge}
            ${reasonText}
          </td>
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
          <th>Status</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

function renderSpotDetails(rankings) {
  if (!elSpotDetails) return;

  if (!Array.isArray(rankings) || rankings.length === 0) {
    elSpotDetails.innerHTML = "<p>No data yet.</p>";
    return;
  }

  // Only show seeds that are NOT fully locked
  const inPlaySeeds = rankings.filter((r) => {
    const status = (r.status || "").toLowerCase();
    return status !== "locked";
  });

  if (inPlaySeeds.length === 0) {
    elSpotDetails.innerHTML =
      "<p>All Top 12 seeds are locked based on the latest CFP rankings.</p>";
    return;
  }

  const cards = inPlaySeeds
    .map((r) => {
      const seed = r.seed ?? r.rank ?? "?";
      const status = r.status ?? "in_play";
      const badge = statusBadge(status);
      const team = r.team ?? r.name ?? "Unknown";
      const scenarios = Array.isArray(r.spot_scenarios)
        ? r.spot_scenarios
        : [];

      const scenarioItems =
        scenarios.length > 0
          ? scenarios
              .map((s) => {
                const t = s.team || "Team";
                const path = s.path || "";
                return `<li><strong>${t}:</strong> ${path}</li>`;
              })
              .join("")
          : "<li>No scenarios defined yet.</li>";

      return `
        <div class="cfp-spot-card">
          <div class="cfp-spot-card-header">
            <div class="cfp-spot-card-title">Seed #${seed}</div>
            <div>${badge}</div>
          </div>
          <div class="cfp-spot-card-body">
            <div><strong>Current occupant:</strong> ${team}</div>
            <ul class="cfp-spot-eligible-list">
              ${scenarioItems}
            </ul>
          </div>
        </div>
      `;
    })
    .join("");

  elSpotDetails.innerHTML = cards;
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
    const rankings = data.rankings || [];
    const games = data.games || [];

    renderRankings(rankings);
    renderSpotDetails(rankings);
    renderGames(games);

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
