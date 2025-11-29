// cfp.js – StegVerse CFP Live Tracker (full production version)

const CFP_DATA_URL = window.CFP_DATA_URL || "/data/cfp-data.json";
const CFP_TICKETS_URL = window.CFP_TICKETS_URL || "/data/cfp-tickets.json";

let ticketsConfig = null;
let sourcesIndex = {};

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

function setStatus(txt, err=false) {
  elStatus.textContent = txt;
  elStatus.style.color = err ? "#ff8080" : "#b0ffa8";
}
function formatDateTime(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  return d.toLocaleString();
}
function sourceMarker(id){
  if (!id) return "";
  const s = sourcesIndex[id];
  if (!s) return "";
  return `<sup><a href="#cfp-source-${id}" style="color:#ffcc66;">[${id}]</a></sup>`;
}

function statusBadge(status){
  const s = (status||"").toLowerCase();
  if (s==="locked") return `<span class="cfp-badge cfp-badge-locked">Locked</span>`;
  if (s==="in_play") return `<span class="cfp-badge cfp-badge-inplay">In Play</span>`;
  if (s==="eliminated") return `<span class="cfp-badge cfp-badge-elim">Eliminated</span>`;
  return "";
}


/* ---------------------------------------------------------
   RENDER: CFP Top 12
--------------------------------------------------------- */
function renderRankings(rankings, sourceId){
  if (!rankings.length){
    elRankings.innerHTML="<p>No rankings.</p>";
    return;
  }

  const rows = rankings.map(r=>`
    <tr>
      <td class="cfp-seed">#${r.seed}</td>
      <td>${r.team}</td>
      <td>${r.record}</td>
      <td>${r.conference}</td>
      <td>${statusBadge(r.status)}<div style="font-size:0.7rem;opacity:0.7;">${r.lock_reason || ""}</div></td>
    </tr>`
  ).join("");

  elRankings.innerHTML = `
    <table class="cfp-rankings-table">
      <thead><tr><th>Seed</th><th>Team</th><th>Record</th><th>Conf</th><th>Status</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
  `;

  elTop12SourceMarker.innerHTML = sourceMarker(sourceId);
}


/* ---------------------------------------------------------
   RENDER: Spot Details (not locked)
--------------------------------------------------------- */
function renderSpotDetails(rankings){
  const items = rankings.filter(r=>r.status!=="locked");
  if (!items.length){
    elSpotDetails.innerHTML="<p>All seeds are locked.</p>";
    return;
  }

  elSpotDetails.innerHTML = items.map(r=>{
    const scenarios = (r.spot_scenarios || []).map(
      s=>`<li><strong>${s.team}:</strong> ${s.path}</li>`
    ).join("");

    return `
      <div class="cfp-spot-card">
        <div class="cfp-spot-card-header">
          <div class="cfp-spot-card-title">Seed #${r.seed}</div>
          <div>${statusBadge(r.status)}</div>
        </div>
        <div><strong>Current:</strong> ${r.team}</div>
        <ul>${scenarios}</ul>
      </div>
    `;
  }).join("");
}


/* ---------------------------------------------------------
   TICKET CONFIG HANDLING
--------------------------------------------------------- */
function getTicketProfile(game){
  if (!ticketsConfig) return null;

  const base = ticketsConfig.defaults || {};
  const confMap = ticketsConfig.conferences || {};
  const teamMap = ticketsConfig.teams || {};

  const conf = game.conference;
  const home = game.home;
  const away = game.away;

  const confOverride = (conf && confMap[conf]) ? confMap[conf] : {};
  const teamOverride = teamMap[home] || teamMap[away] || {};

  const providers =
    teamOverride.providers ||
    confOverride.providers ||
    base.providers || [];

  const patterns = {
    ...(base.patterns||{}),
    ...(confOverride.patterns||{}),
    ...(teamOverride.patterns||{})
  };

  return { providers, patterns };
}

function buildTicketButtons(game){
  if (!ticketsConfig) return "";
  const profile = getTicketProfile(game);
  if (!profile || !profile.providers.length) return "";

  const labels = ticketsConfig.labels || {};
  const query = encodeURIComponent(`${game.away} at ${game.home} tickets`);

  const links = profile.providers.map(key=>{
    const url = profile.patterns[key]?.replace("{QUERY}", query);
    if (!url) return null;
    const label = labels[key] || key;
    return `<a href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>`;
  }).filter(Boolean).join(' • ');

  return `
    <div style="margin-top:0.4rem;font-size:0.8rem;">
      <span>Tickets: </span>${links}
      <span style="margin-left:0.25rem;opacity:0.6;">(partners)</span>
    </div>
  `;
}


/* ---------------------------------------------------------
   RENDER: Games
--------------------------------------------------------- */
function renderGames(games){
  if (!games.length){
    elGames.innerHTML="<p>No games.</p>";
    return;
  }

  elGames.innerHTML = `<ul class="cfp-games-list">` +
    games.map(g=>`
      <li class="cfp-game">
        <div class="cfp-game-header">
          <span>${g.away} @ ${g.home}</span>
          <span>${g.away_score ?? "-"} – ${g.home_score ?? "-"}</span>
        </div>
        <div class="cfp-game-meta">
          ${g.status ? `Status: ${g.status}` : ""}
          ${g.kickoff ? ` | Kickoff: ${formatDateTime(g.kickoff)}` : ""}
          ${g.note ? ` | ${g.note}` : ""}
          ${buildTicketButtons(g)}
        </div>
      </li>
    `).join("") +
  `</ul>`;
}


/* ---------------------------------------------------------
   RENDER: Polls
--------------------------------------------------------- */
function renderPolls(polls){
  if (!polls.length){
    elPolls.innerHTML="<p>No polls available.</p>";
    return;
  }

  elPolls.innerHTML = polls.map(p=>{
    const rows = p.teams.map(t=>`
      <tr>
        <td>${t.rank}</td>
        <td>${t.team}</td>
        <td>${t.record}</td>
        <td>${t.conference}</td>
      </tr>
    `).join("");

    return `
      <div class="cfp-poll-card">
        <div class="cfp-poll-header">
          <div class="cfp-poll-title">${p.name} ${sourceMarker(p.source_id)}</div>
        </div>
        <table class="cfp-poll-table">
          <thead><tr><th>Rank</th><th>Team</th><th>Record</th><th>Conf</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    `;
  }).join("");
}


/* ---------------------------------------------------------
   RENDER: Conferences
--------------------------------------------------------- */
function renderConferences(confs, sourceId){
  if (!confs.length){
    elConfSelect.innerHTML="<option>No data</option>";
    elConfStandings.innerHTML="<p>No standings.</p>";
    return;
  }

  elConfSourceMarker.innerHTML = sourceMarker(sourceId);

  elConfSelect.innerHTML = confs.map(c=>`
    <option value="${c.id}">${c.name}</option>
  `).join("");

  renderConferenceStandings(confs[0]);

  elConfSelect.onchange = () => {
    const id = elConfSelect.value;
    const conf = confs.find(c=>c.id===id);
    renderConferenceStandings(conf);
  };
}

function renderConferenceStandings(conf){
  if (!conf) return;

  const rows = conf.teams.map(t=>`
    <tr>
      <td>${t.team}</td>
      <td>${t.overall}</td>
      <td>${t.conference_record}</td>
      <td>${t.pf}</td>
      <td>${t.pa}</td>
    </tr>
  `).join("");

  elConfStandings.innerHTML = `
    <table class="cfp-conf-table">
      <thead><tr><th>Team</th><th>Overall</th><th>Conf</th><th>PF</th><th>PA</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}


/* ---------------------------------------------------------
   RENDER: Data Sources
--------------------------------------------------------- */
function renderSources(list){
  if (!list.length){
    elSources.innerHTML="<p>No sources.</p>";
    return;
  }

  elSources.innerHTML = `
    <ul class="cfp-sources-list">
      ${list.map(s=>`
        <li id="cfp-source-${s.id}">[${s.id}] 
          <a href="${s.url}" target="_blank">${s.label}</a>
        </li>
      `).join("")}
    </ul>
  `;
}


/* ---------------------------------------------------------
   LOAD EVERYTHING
--------------------------------------------------------- */
async function loadCfpData(){
  setStatus("Refreshing…");

  try {
    const [dataRes, ticketRes] = await Promise.all([
      fetch(CFP_DATA_URL + "?t="+Date.now()),
      fetch(CFP_TICKETS_URL + "?t="+Date.now()).catch(()=>null)
    ]);

    const data = await dataRes.json();
    ticketsConfig = ticketRes && ticketRes.ok ? await ticketRes.json() : null;

    sourcesIndex = {};
    (data.sources||[]).forEach(s=>sourcesIndex[s.id]=s);

    renderSources(data.sources||[]);
    renderRankings(data.rankings||[], data.cfp_source_id);
    renderSpotDetails(data.rankings||[]);
    renderGames(data.games||[]);
    renderPolls(data.polls||[]);
    renderConferences(data.conferences||[], data.conf_source_id);

    elLastUpdated.textContent = "Last updated: " + formatDateTime(data.last_updated);
    setStatus("Updated.");

  } catch (err){
    console.error(err);
    setStatus("Load failed.", true);
  }
}

elRefreshBtn.onclick = loadCfpData;

// Initial load
loadCfpData();
