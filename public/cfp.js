// cfp.js
//
// Front-end logic for NCAAF CFP Live Tracker with:
// - CFP Top 12 + lock status
// - Spot details (non-locked seeds)
// - National polls (CFP / AP / Coaches)
// - Conference standings (selectable)
// - Source markers [1], [2], ... linking to a bottom-of-page list
//
// Expected JSON from CFP_DATA_URL:
//
// {
//   "last_updated": "...",
//   "sources": [
//     { "id": "1", "label": "CFP Rankings", "url": "https://..." },
//     { "id": "2", "label": "AP Top 25", "url": "https://..." },
//     { "id": "3", "label": "USA Today Coaches Poll", "url": "https://..." },
//     { "id": "4", "label": "Conference standings data provider", "url": "https://..." }
//   ],
//   "cfp_source_id": "1",    // which source id applies to CFP Top 12
//   "conf_source_id": "4",   // which source id applies to conference standings
//   "rankings": [ ... CFP Top 12 ... ],
//   "games": [ ... ],
//   "polls": [
//     {
//       "name": "CFP Rankings",
//       "short_name": "CFP",
//       "source_id": "1",
//       "teams": [
//         { "rank": 1, "team": "Ohio State", "record": "12-0", "conference": "Big Ten" },
//         ...
//       ]
//     },
//     {
//       "name": "AP Top 25",
//       "short_name": "AP",
//       "source_id": "2",
//       "teams": [ ... ]
//     },
//     {
//       "name": "Coaches Poll",
//       "short_name": "Coaches",
//       "source_id": "3",
//       "teams": [ ... ]
//     }
//   ],
//   "conferences": [
//     {
//       "id": "big12",
//       "name": "Big 12",
//       "source_id": "4",
//       "teams": [
//         {
//           "team": "Texas Tech",
//           "overall": "11-1",
//           "conference_record": "8-1",
//           "pf": 420,
//           "pa": 260
//         },
//         ...
//       ]
//     },
//     ...
//   ]
// }

const CFP_DATA_URL =
  window.CFP_DATA_URL || "/cfp-data.json";

const elRankings = document.getElementById("cfp-rankings");
const elGames = document.getElementById("cfp-games");
const elLastUpdated = document.getElementById("cfp-last-updated");
const elStatus = document.getElementById("cfp-status");
const elRefreshBtn = document.getElementById("cfp-refresh-btn");
const elSpotDetails = document.getElementById("cfp-spot-details");
const elPolls = document.getElementById("cfp-polls");
const elConfSelect = document.getElementById("cfp-conf-select");
const elConfStandings = document.getElementById("cfp-conf-standings");
const elSources = document.getElementById("cfp-sources");
const elTop12SourceMarker = document.getElementById("cfp-top12-source-marker");
const elConfSourceMarker = document.getElementById("cfp-conf-source-marker");

let sourcesIndex = {}; // id -> source object
let conferences = [];   // from JSON, for conference standings

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

function sourceMarker(sourceId) {
  if (!sourceId) return "";
  const s = sourcesIndex[sourceId];
  const label = s ? s.id : sourceId;
  return `<sup><a href="#cfp-source-${label}" style="color:#ffcc66; text-decoration:none;">[${label}]</a></sup>`;
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

function renderRankings(rankings, cfpSourceId) {
  if (!Array.isArray(rankings) || rankings.length === 0) {
    elRankings.innerHTML = "<p>No rankings available.</p>";
  } else {
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

  if (elTop12SourceMarker) {
    elTop12SourceMarker.innerHTML = sourceMarker(cfpSourceId);
  }
}

function renderSpotDetails(rankings) {
  if (!elSpotDetails) return;

  if (!Array.isArray(rankings) || rankings.length === 0) {
    elSpotDetails.innerHTML = "<p>No data yet.</p>";
    return;
  }

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

function renderPolls(polls) {
  if (!elPolls) return;

  if (!Array.isArray(polls) || polls.length === 0) {
    elPolls.innerHTML = "<p>No poll data available.</p>";
    return;
  }

  const cards = polls
    .map((poll) => {
      const name = poll.name || poll.short_name || "Poll";
      const short = poll.short_name || "";
      const sourceId = poll.source_id;
      const teams = Array.isArray(poll.teams) ? poll.teams : [];
      const marker = sourceMarker(sourceId);

      const rows = teams
        .map((t) => {
          const rank = t.rank ?? "?";
          const team = t.team ?? t.name ?? "Unknown";
          const record = t.record ?? "";
          const conf = t.conference ?? t.conf ?? "";
          return `
            <tr>
              <td>${rank}</td>
              <td>${team}</td>
              <td>${record}</td>
              <td>${conf}</td>
            </tr>
          `;
        })
        .join("");

      return `
        <div class="cfp-poll-card">
          <div class="cfp-poll-header">
            <div class="cfp-poll-title">${name}${marker}</div>
            ${
              short
                ? `<div class="cfp-poll-source">${short}</div>`
                : ""
            }
          </div>
          <table class="cfp-poll-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Team</th>
                <th>Record</th>
                <th>Conf</th>
              </tr>
            </thead>
            <tbody>
              ${rows}
            </tbody>
          </table>
        </div>
      `;
    })
    .join("");

  elPolls.innerHTML = cards;
}

function renderConferences(confs, confSourceId) {
  conferences = Array.isArray(confs) ? confs : [];

  if (!elConfSelect || !elConfStandings) return;

  if (conferences.length === 0) {
    elConfSelect.innerHTML = `<option value="">No conference data</option>`;
    elConfStandings.innerHTML =
      "<p>No conference standings data available.</p>";
    elConfSourceMarker.innerHTML = "";
    return;
  }

  elConfSelect.innerHTML = conferences
    .map(
      (c, idx) =>
        `<option value="${c.id || idx}">${c.name || c.id || "Conference"}</option>`
    )
    .join("");

  // Set marker for conferences (same for all; they share conf_source_id)
  if (elConfSourceMarker) {
    elConfSourceMarker.innerHTML = sourceMarker(confSourceId);
  }

  // Render first conference by default
  renderConferenceStandings(conferences[0]);

  elConfSelect.onchange = () => {
    const value = elConfSelect.value;
    const conf =
      conferences.find((c) => (c.id || "").toString() === value) ||
      conferences[0];
    renderConferenceStandings(conf);
  };
}

function renderConferenceStandings(conf) {
  if (!conf || !elConfStandings) return;

  const teams = Array.isArray(conf.teams) ? conf.teams : [];
  if (teams.length === 0) {
    elConfStandings.innerHTML = "<p>No teams found for this conference.</p>";
    return;
  }

  const rows = teams
    .map((t) => {
      const team = t.team ?? t.name ?? "Team";
      const overall = t.overall ?? t.overall_record ?? "";
      const confRec = t.conference_record ?? t.conf_record ?? "";
      const pf = t.pf ?? t.points_for ?? "";
      const pa = t.pa ?? t.points_against ?? "";
      return `
        <tr>
          <td>${team}</td>
          <td>${overall}</td>
          <td>${confRec}</td>
          <td>${pf}</td>
          <td>${pa}</td>
        </tr>
      `;
    })
    .join("");

  elConfStandings.innerHTML = `
    <table class="cfp-conf-table">
      <thead>
        <tr>
          <th>Team</th>
          <th>Overall</th>
          <th>Conf</th>
          <th>PF</th>
          <th>PA</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

function renderSources(sources) {
  if (!elSources) return;

  if (!Array.isArray(sources) || sources.length === 0) {
    elSources.innerHTML = "<p>No sources defined.</p>";
    return;
  }

  const items = sources
    .map((s) => {
      const id = s.id || "?";
      const label = s.label || "Source";
      const url = s.url || "";
      const link = url
        ? `<a href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>`
        : label;
      return `<li id="cfp-source-${id}">[${id}] ${link}</li>`;
    })
    .join("");

  elSources.innerHTML = `<ul class="cfp-sources-list">${items}</ul>`;
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

    // Build sources index
    const sources = Array.isArray(data.sources) ? data.sources : [];
    sourcesIndex = {};
    for (const s of sources) {
      if (s && s.id) {
        sourcesIndex[String(s.id)] = s;
      }
    }

    renderSources(sources);

    const rankings = data.rankings || [];
    const games = data.games || [];
    const polls = data.polls || [];
    const confs = data.conferences || [];
    const cfpSourceId = data.cfp_source_id || null;
    const confSourceId = data.conf_source_id || null;

    renderRankings(rankings, cfpSourceId);
    renderSpotDetails(rankings);
    renderGames(games);
    renderPolls(polls);
    renderConferences(confs, confSourceId);

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
