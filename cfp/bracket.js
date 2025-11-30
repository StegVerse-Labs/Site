// /cfp/bracket.js

const BRACKET_DATA_URL = window.CFP_DATA_URL || "/data/cfp-data.json";

const elStatus = document.getElementById("bracket-status");
const elLastUpdated = document.getElementById("bracket-last-updated");
const elRefresh = document.getElementById("bracket-refresh-btn");
const elBracketGrid = document.getElementById("bracket-grid");
const elRankings = document.getElementById("bracket-rankings");
const elSinceLast = document.getElementById("bracket-since-last");
const elExplanation = document.getElementById("bracket-explanation");
const elConfSelect = document.getElementById("bracket-conf-select");
const elConfStandings = document.getElementById("bracket-conf-standings");

function setStatus(msg, isError = false) {
  if (!elStatus) return;
  elStatus.textContent = msg;
  elStatus.style.color = isError ? "#ff8080" : "#b0ffa8";
}

function formatDateTime(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  return d.toLocaleString();
}

function statusBadge(status) {
  const s = (status || "").toLowerCase();
  if (s === "locked") return '<span class="cfp-badge cfp-badge-locked">Locked</span>';
  if (s === "in_play") return '<span class="cfp-badge cfp-badge-inplay">In Play</span>';
  if (s === "eliminated") return '<span class="cfp-badge cfp-badge-elim">Eliminated</span>';
  return "";
}

/* -------- Bracket Rendering -------- */

function renderBracket(data) {
  const rankings = data.rankings || [];
  const bracket = data.bracket || {};
  const round12 = bracket.round_of_12 || [];
  const quarters = bracket.quarterfinals || [];

  if (!rankings.length) {
    elBracketGrid.innerHTML = "<p>No rankings available to build bracket.</p>";
    return;
  }

  // helper to get team name by seed
  const teamBySeed = {};
  rankings.forEach(r => {
    if (r.seed != null) teamBySeed[r.seed] = r.team;
  });

  const r12Html = round12.map(g => {
    const hi = g.high_seed;
    const lo = g.low_seed;
    return `
      <div class="cfp-game">
        <div class="cfp-game-header">
          <span>#${hi} ${teamBySeed[hi] || "TBD"}</span>
          <span>vs #${lo} ${teamBySeed[lo] || "TBD"}</span>
        </div>
        <div class="cfp-game-meta">
          First Round – ${g.location || ""} ${g.note ? " – " + g.note : ""}
        </div>
      </div>
    `;
  }).join("");

  const qHtml = quarters.map(q => {
    const top = q.top_seed;
    const topTeam = teamBySeed[top] || "TBD";
    return `
      <div class="cfp-game">
        <div class="cfp-game-header">
          <span>#${top} ${topTeam}</span>
          <span>vs Winner of ${q.winner_of.toUpperCase()}</span>
        </div>
        <div class="cfp-game-meta">
          Quarterfinal – ${q.bowl || "Bowl TBD"}
        </div>
      </div>
    `;
  }).join("");

  elBracketGrid.innerHTML = `
    <div>
      <h3>Round of 12</h3>
      <div class="cfp-games-list">
        ${r12Html || "<p>No Round of 12 defined.</p>"}
      </div>
    </div>
    <div style="margin-top:1.5rem;">
      <h3>Quarterfinals</h3>
      <div class="cfp-games-list">
        ${qHtml || "<p>No Quarterfinals defined.</p>"}
      </div>
    </div>
  `;
}

/* -------- Rankings Table -------- */

function renderRankings(rankings) {
  if (!rankings.length) {
    elRankings.innerHTML = "<p>No rankings.</p>";
    return;
  }

  const rows = rankings.map(r => `
    <tr>
      <td class="cfp-seed">#${r.seed}</td>
      <td>${r.team}</td>
      <td>${r.record}</td>
      <td>${r.conference}</td>
      <td>${statusBadge(r.status)}</td>
    </tr>
  `).join("");

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

/* -------- Since Last Release Table -------- */

function renderSinceLast(rankings) {
  if (!rankings.length) {
    elSinceLast.innerHTML = "<p>No data yet.</p>";
    return;
  }

  const rows = rankings.map(r => {
    const s = r.since_last || {};
    const deltaStr = (r.delta > 0 ? "+" + r.delta : (r.delta || 0));
    return `
      <tr>
        <td>#${r.seed}</td>
        <td>${r.team}</td>
        <td>${deltaStr}</td>
        <td>${s.record || ""}</td>
        <td>${s.avg_margin || ""}</td>
        <td>${s.vs_ranked || ""}</td>
      </tr>
    `;
  }).join("");

  elSinceLast.innerHTML = `
    <table class="cfp-rankings-table">
      <thead>
        <tr>
          <th>Seed</th>
          <th>Team</th>
          <th>Δ Rank</th>
          <th>Record Since</th>
          <th>Avg Margin</th>
          <th>Vs Ranked</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

/* -------- Explanation Block -------- */

function renderExplanation(data) {
  const rankings = data.rankings || [];
  const release = data.official_release || {};

  const movedUp = rankings.filter(r => r.delta > 0);
  const movedDown = rankings.filter(r => r.delta < 0);
  const same = rankings.filter(r => (r.delta || 0) === 0);

  const upText = movedUp.length
    ? movedUp.map(r => `#${r.seed} ${r.team} (+${r.delta})`).join(", ")
    : "None";

  const downText = movedDown.length
    ? movedDown.map(r => `#${r.seed} ${r.team} (${r.delta})`).join(", ")
    : "None";

  const sameText = same.length
    ? same.map(r => `#${r.seed} ${r.team}`).join(", ")
    : "None";

  elExplanation.innerHTML = `
    <p>
      This bracket is based on the official CFP Top 12 from
      <strong>Ranking #${release.ranking_number || "?"}</strong>
      released on <strong>${formatDateTime(release.released_at)}</strong>.
    </p>
    <p>
      <strong>Teams moving up:</strong> ${upText}<br/>
      <strong>Teams moving down:</strong> ${downText}<br/>
      <strong>Unchanged:</strong> ${sameText}
    </p>
    <p>
      Performance since the last release (wins, margins, and results vs ranked opponents)
      is summarized in the table on the right. That performance is the basis for projecting
      where each team is likely to land in the <em>next</em> CFP ranking.
    </p>
  `;
}

/* -------- Conference Standings -------- */

function renderConferences(confs) {
  if (!Array.isArray(confs) || !confs.length) {
    elConfSelect.innerHTML = "<option>No data</option>";
    elConfStandings.innerHTML = "<p>No standings data yet.</p
