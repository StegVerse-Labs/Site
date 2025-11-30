// ncaaf-2025.js
// Shared logic for NCAAF 2025 CFP views.
// Views: bracket | standings | polls | championship | team

const NCAAF_2025_DATA_URL = "/data/ncaaf-2025.json";

let ncaafData = null;

function $(id) {
  return document.getElementById(id);
}

function formatDate(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  return d.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit"
  });
}

async function loadNcaafData() {
  const res = await fetch(NCAAF_2025_DATA_URL + "?t=" + Date.now(), {
    cache: "no-store"
  });
  if (!res.ok) {
    throw new Error("Failed to load NCAAF data JSON");
  }
  ncaafData = await res.json();
}

function getTop12() {
  return (ncaafData && ncaafData.cfp_top12) || [];
}

function getTeamById(id) {
  if (!ncaafData || !ncaafData.teams) return null;
  return ncaafData.teams[id] || null;
}

function getSinceLastByTeamId(id) {
  if (!ncaafData || !Array.isArray(ncaafData.since_last_release)) return null;
  return ncaafData.since_last_release.find((t) => t.team_id === id) || null;
}

/* ------------- BRACKET VIEW ------------- */

function renderBracketView() {
  const main = $("view-main");
  const secondary = $("view-secondary");
  const sourcesEl = $("view-sources");

  const top12 = getTop12();

  // Build bracket from top12 + bracket.rounds
  const bracket = ncaafData.bracket || { rounds: [] };
  const roundsHtml = (bracket.rounds || [])
    .map((round) => {
      const gamesHtml = (round.games || [])
        .map((g) => {
          const hi = top12.find((t) => t.rank === g.seed_high);
          const lo =
            g.seed_low != null
              ? top12.find((t) => t.rank === g.seed_low)
              : null;

          const hiLabel = hi
            ? `#${hi.rank} ${hi.team}`
            : g.seed_high
            ? `Seed ${g.seed_high}`
            : "";
          const loLabel = lo
            ? `#${lo.rank} ${lo.team}`
            : g.seed_low
            ? `Seed ${g.seed_low}`
            : g.vs_winner_of
            ? `Winner of ${g.vs_winner_of}`
            : "";

          return `
            <tr>
              <td>${g.id}</td>
              <td>${hiLabel}</td>
              <td>vs</td>
              <td>${loLabel}</td>
            </tr>
          `;
        })
        .join("");

      return `
        <section class="card">
          <h3>${round.name}</h3>
          ${round.note ? `<p class="note">${round.note}</p>` : ""}
          <table class="table">
            <thead>
              <tr><th>Game</th><th>Higher Seed</th><th></th><th>Opponent</th></tr>
            </thead>
            <tbody>${gamesHtml}</tbody>
          </table>
        </section>
      `;
    })
    .join("");

  const top12Rows = top12
    .map((t) => {
      const badge = t.locked
        ? '<span class="badge locked">Locked</span>'
        : '<span class="badge inplay">In Play</span>';
      return `
        <tr>
          <td>#${t.rank}</td>
          <td><a href="team.html?team=${t.team_id}">${t.team}</a></td>
          <td>${t.record}</td>
          <td>${t.conference}</td>
          <td>${badge}</td>
        </tr>
      `;
    })
    .join("");

  const sinceRows = ((ncaafData && ncaafData.since_last_release) || [])
    .map((item) => {
      const team = getTeamById(item.team_id);
      const name = team ? team.name : item.team_id;
      return `
        <tr>
          <td>#${item.rank ?? ""}</td>
          <td>${name}</td>
          <td>${item.since_record}</td>
          <td>${item.key_results || item.summary || ""}</td>
          <td>${item.projected_effect || item.impact || ""}</td>
        </tr>
      `;
    })
    .join("");

  main.innerHTML = `
    <section class="card">
      <h2>2025 CFP 12-Team Bracket (Live)</h2>
      <p class="note">
        This bracket is anchored on the latest official CFP Top 12 release
        (${ncaafData.last_cfp_release || ""}). When the CFP committee publishes
        new rankings, this view updates automatically once the data JSON is refreshed.
      </p>
      ${roundsHtml}
    </section>

    <section class="card">
      <h2>Current CFP Top 12</h2>
      <table class="table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Team</th>
            <th>Record</th>
            <th>Conf</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>${top12Rows}</tbody>
      </table>
    </section>
  `;

  secondary.innerHTML = `
    <section class="card">
      <h2>Since Last CFP Ranking</h2>
      <p class="note">
        How each key team has performed since the last CFP release and how that
        performance is likely to affect the next ranking.
      </p>
      <table class="table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Team</th>
            <th>Since</th>
            <th>Key Results</th>
            <th>Projected Impact</th>
          </tr>
        </thead>
        <tbody>${sinceRows}</tbody>
      </table>
    </section>

    <section class="card">
      <h2>Bracket Notes</h2>
      <p>${bracket.description || ""}</p>
    </section>
  `;

  renderSourcesInto(sourcesEl);
}

/* ------------- STANDINGS VIEW ------------- */

function renderStandingsView() {
  const main = $("view-main");
  const secondary = $("view-secondary");
  const sourcesEl = $("view-sources");

  const conferences = (ncaafData.standings && ncaafData.standings.conferences) || [];

  const confHtml = conferences
    .map((conf) => {
      const rows = (conf.teams || [])
        .map(
          (t) => `
        <tr>
          <td><a href="team.html?team=${t.team_id}">${t.team}</a></td>
          <td>${t.overall}</td>
          <td>${t.conf_record}</td>
          <td>${t.pf}</td>
          <td>${t.pa}</td>
        </tr>
      `
        )
        .join("");

      return `
        <section class="card">
          <h2>${conf.name}</h2>
          <table class="table">
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
        </section>
      `;
    })
    .join("");

  main.innerHTML = confHtml;
  secondary.innerHTML = `
    <section class="card">
      <h2>Standings Notes</h2>
      <p class="note">
        Standings are a live snapshot heading into Championship Weekend. Tiebreakers and internal
        conference rules may apply; always consult official conference sites for formal clinching scenarios.
      </p>
    </section>
  `;

  renderSourcesInto(sourcesEl);
}

/* ------------- POLLS VIEW ------------- */

function renderPollsView() {
  const main = $("view-main");
  const secondary = $("view-secondary");
  const sourcesEl = $("view-sources");

  const polls = ncaafData.polls || [];

  const pollCards = polls
    .map((p) => {
      const rows = (p.teams || [])
        .map(
          (t) => `
        <tr>
          <td>${t.rank}</td>
          <td><a href="team.html?team=${t.team_id}">${t.team}</a></td>
          <td>${t.record}</td>
          <td>${t.conference}</td>
        </tr>
      `
        )
        .join("");

      return `
        <section class="card">
          <h2>${p.name}</h2>
          <table class="table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Team</th>
                <th>Record</th>
                <th>Conf</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </section>
      `;
    })
    .join("");

  main.innerHTML = pollCards;
  secondary.innerHTML = `
    <section class="card">
      <h2>Polls vs CFP</h2>
      <p class="note">
        This view lets you compare how teams are perceived across the three major
        national rankings: CFP, AP, and Coaches. Future versions will highlight
        discrepancies, “underrated” and “overrated” teams, and plot movement week by week.
      </p>
    </section>
  `;

  renderSourcesInto(sourcesEl);
}

/* ------------- CHAMPIONSHIP WEEKEND VIEW ------------- */

function renderChampionshipView() {
  const main = $("view-main");
  const secondary = $("view-secondary");
  const sourcesEl = $("view-sources");

  const cw = ncaafData.championship_weekend || { games: [] };

  const rows = (cw.games || [])
    .map((g) => {
      const t1 = getTeamById(g.teams[0]);
      const t2 = getTeamById(g.teams[1]);
      const label1 = t1 ? t1.name : g.teams[0];
      const label2 = t2 ? t2.name : g.teams[1];

      return `
        <tr>
          <td>${g.title}</td>
          <td>${label1} vs ${label2}</td>
          <td>${formatDate(g.koff)}</td>
          <td>${g.location || ""}</td>
          <td>${g.network || ""}</td>
        </tr>
      `;
    })
    .join("");

  main.innerHTML = `
    <section class="card">
      <h2>Championship Weekend – Key Games</h2>
      <p class="note">
        These games shape the final CFP bracket. Click team names on other pages to
        see detailed “road to the title” scenarios.
      </p>
      <table class="table">
        <thead>
          <tr>
            <th>Game</th>
            <th>Matchup</th>
            <th>Kickoff</th>
            <th>Location</th>
            <th>Network</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </section>
  `;

  const impactList = (cw.games || [])
    .map((g) => `<li><strong>${g.title}:</strong> ${g.cfp_impact || ""}</li>`)
    .join("");

  secondary.innerHTML = `
    <section class="card">
      <h2>CFP Impact Notes</h2>
      <ul>${impactList}</ul>
    </section>
  `;

  renderSourcesInto(sourcesEl);
}

/* ------------- TEAM VIEW ------------- */

function renderTeamView() {
  const main = $("view-main");
  const secondary = $("view-secondary");
  const sourcesEl = $("view-sources");

  const params = new URLSearchParams(window.location.search);
  const teamId = params.get("team");
  const team = getTeamById(teamId);

  if (!team) {
    main.innerHTML = `<section class="card"><p>Team not found.</p></section>`;
    secondary.innerHTML = "";
    renderSourcesInto(sourcesEl);
    return;
  }

  const since = getSinceLastByTeamId(teamId) || team.since_last || {};
  const road = team.road_to_title || { best_case: [], worst_case: [], most_likely: [] };

  main.innerHTML = `
    <section class="card">
      <h2>${team.name} – Road to the National Championship</h2>
      <p class="note">
        Conference: ${team.conference || "N/A"} · Current CFP Rank: #${team.current_rank || "—"} · Record: ${team.record || "—"}
      </p>
      <div class="columns">
        <div class="column">
          <h3>Best Case</h3>
          <ul>${(road.best_case || []).map((x) => `<li>${x}</li>`).join("")}</ul>
        </div>
        <div class="column">
          <h3>Most Likely Case</h3>
          <ul>${(road.most_likely || []).map((x) => `<li>${x}</li>`).join("")}</ul>
        </div>
        <div class="column">
          <h3>Nightmare Case</h3>
          <ul>${(road.worst_case || []).map((x) => `<li>${x}</li>`).join("")}</ul>
        </div>
      </div>
    </section>
  `;

  secondary.innerHTML = `
    <section class="card">
      <h2>Since Last CFP Ranking</h2>
      <p><strong>Record:</strong> ${since.since_record || "—"}</p>
      <p><strong>Summary:</strong> ${since.key_results || since.summary || "No summary yet."}</p>
      <p><strong>Projected Impact:</strong> ${since.projected_effect || since.impact || "TBD."}</p>
    </section>
  `;

  renderSourcesInto(sourcesEl);
}

/* ------------- SOURCES FOOTER ------------- */

function renderSourcesInto(el) {
  if (!el || !ncaafData || !Array.isArray(ncaafData.sources)) return;
  const items = ncaafData.sources
    .map(
      (s) =>
        `<li>[${s.id}] <a href="${s.url}" target="_blank" rel="noopener noreferrer">${s.label}</a></li>`
    )
    .join("");
  el.innerHTML = `
    <h3>Data Sources</h3>
    <ul class="source-list">${items}</ul>
  `;
}

/* ------------- INIT ------------- */

async function initNcaafPage() {
  try {
    await loadNcaafData();
  } catch (e) {
    console.error(e);
    const main = $("view-main");
    if (main) {
      main.innerHTML = `<section class="card"><p>Failed to load data.</p></section>`;
    }
    return;
  }

  const body = document.body;
  const view = body.getAttribute("data-view") || "bracket";

  if (view === "bracket") renderBracketView();
  else if (view === "standings") renderStandingsView();
  else if (view === "polls") renderPollsView();
  else if (view === "championship") renderChampionshipView();
  else if (view === "team") renderTeamView();
}

document.addEventListener("DOMContentLoaded", initNcaafPage);
