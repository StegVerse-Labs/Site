// StegVerse CFP / NCAAF current-season public projection.

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

const elConfSelect = document.getElementById("cfp-conf-select");
const elConfStandings = document.getElementById("cfp-conf-standings");
const elSources = document.getElementById("cfp-sources");
const elTop12SourceMarker = document.getElementById("cfp-top12-source-marker");
const elConfSourceMarker = document.getElementById("cfp-conf-source-marker");

function setStatus(text, error = false) {
  if (!elStatus) return;
  elStatus.textContent = text;
  elStatus.style.color = error ? "#ff8080" : "#b0ffa8";
}

function formatDateTime(iso) {
  if (!iso) return "unknown";
  const date = new Date(iso);
  return Number.isNaN(date.getTime()) ? String(iso) : date.toLocaleString();
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function sourceMarker(id) {
  if (!id || !sourcesIndex[id]) return "";
  return `<sup><a href="#cfp-source-${escapeHtml(id)}" style="color:#ffcc66;">[${escapeHtml(id)}]</a></sup>`;
}

function statusBadge(status) {
  const normalized = String(status || "").toLowerCase();
  if (normalized === "locked") return '<span class="cfp-badge cfp-badge-locked">Locked</span>';
  if (normalized === "in_play") return '<span class="cfp-badge cfp-badge-inplay">In Play</span>';
  if (normalized === "eliminated") return '<span class="cfp-badge cfp-badge-elim">Eliminated</span>';
  return "";
}

function rankingEmptyMessage(data) {
  if (data.phase === "PRE_CFP_RANKINGS") {
    return `No current ${escapeHtml(data.season)} CFP committee rankings have been published or observed yet. AP/other polls below remain separate and are not CFP rankings.`;
  }
  const state = data.availability?.cfp_rankings || data.freshness?.rankings_state;
  if (state && state !== "PUBLISHED_CURRENT_SEASON") {
    return `Current CFP rankings unavailable: ${escapeHtml(state)}.`;
  }
  return "No current CFP rankings available.";
}

function renderRankings(rankings, sourceId, data) {
  if (!Array.isArray(rankings) || !rankings.length) {
    elRankings.innerHTML = `<p>${rankingEmptyMessage(data)}</p>`;
    if (elTop12SourceMarker) elTop12SourceMarker.innerHTML = sourceMarker(sourceId);
    return;
  }

  const rankCell = (value) => (Number.isInteger(value) ? `#${value}` : "—");
  const recordCell = (r) => (r.conference_record ? `${r.record} (${r.conference_record})` : `${r.record || ""}`);
  const nextCell = (r) => {
    if (!r.next_opponent) return "—";
    const where = r.next_home ? "vs" : "at";
    let when = "";
    if (r.next_date) {
      const d = new Date(r.next_date);
      if (!Number.isNaN(d.getTime())) {
        when = d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", timeZone: "UTC" });
      }
    }
    return `${escapeHtml(where)} ${escapeHtml(r.next_opponent)}<div style="font-size:0.7rem;opacity:0.7;">${escapeHtml(when)}</div>`;
  };
  const rows = rankings.map((r) => `
    <tr>
      <td class="cfp-seed">#${escapeHtml(r.seed)}</td>
      <td>${escapeHtml(rankCell(r.ap_rank))}</td>
      <td>${escapeHtml(rankCell(r.coaches_rank))}</td>
      <td>${escapeHtml(rankCell(r.sv_rank))}</td>
      <td>${escapeHtml(r.team)}</td>
      <td>${escapeHtml(recordCell(r))}</td>
      <td>${escapeHtml(r.conference)}</td>
      <td>${statusBadge(r.status)}<div style="font-size:0.7rem;opacity:0.7;">${escapeHtml(r.lock_reason || "")}</div></td>
      <td>${nextCell(r)}</td>
    </tr>`).join("");

  elRankings.innerHTML = `
    <table class="cfp-rankings-table">
      <thead><tr><th>CFP</th><th>AP</th><th>Coaches Poll</th><th>SV</th><th>Team</th><th>Record</th><th>Conf</th><th>Status</th><th>Next</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>`;
  if (elTop12SourceMarker) elTop12SourceMarker.innerHTML = sourceMarker(sourceId);
}

function renderSpotDetails(rankings, data) {
  if (data.phase === "PRE_CFP_RANKINGS") {
    elSpotDetails.innerHTML = "<p>Playoff spot scenarios are withheld until current-season CFP committee rankings are observed.</p>";
    return;
  }
  const rows = rankings || [];
  const items = rows.filter((r) => r.status !== "locked");
  const unknowns = items.map((r) => {
    const scenarios = (r.spot_scenarios || []).map((s) => `<li><strong>${escapeHtml(s.team)}:</strong> ${escapeHtml(s.path)}</li>`).join("");
    return `<div class="cfp-spot-card">
      <div class="cfp-spot-card-header"><div class="cfp-spot-card-title">Rank #${escapeHtml(r.seed)}</div><div>${statusBadge(r.status)}</div></div>
      <div><strong>Current:</strong> ${escapeHtml(r.team)}</div><ul>${scenarios}</ul>
    </div>`;
  }).join("");
  const field = rows
    .filter((r) => { const s = Number(r.seed); return Number.isInteger(s) && s >= 1 && s <= 12; })
    .slice().sort((a, b) => Number(a.seed) - Number(b.seed));
  if (field.length === 12) {
    elSpotDetails.innerHTML = renderBracket(field) +
      `<h3 style="margin:1rem 0 0.5rem;">Still open — the unknowns</h3>` +
      (items.length ? unknowns : "<p>No unknowns remain — every projected spot is locked.</p>");
    return;
  }
  if (!items.length) {
    elSpotDetails.innerHTML = "<p>No current spot-scenario data available.</p>";
    return;
  }
  elSpotDetails.innerHTML = unknowns;
}

function renderBracket(field) {
  const bySeed = {};
  field.forEach((r) => { bySeed[Number(r.seed)] = r; });
  const name = (seed) => (bySeed[seed] ? escapeHtml(bySeed[seed].team) : "TBD");
  const slot = (seed) => {
    const r = bySeed[seed];
    if (!r) return `#${seed} TBD`;
    const badge = statusBadge(r.status);
    return `#${seed} ${escapeHtml(r.team)}${badge ? " " + badge : ""}`;
  };
  const byes = [1, 2, 3, 4].map((s) => `<li>${slot(s)} — first-round bye</li>`).join("");
  const firstRound = [[5, 12], [6, 11], [7, 10], [8, 9]]
    .map(([a, b]) => `<li>${slot(a)} vs ${slot(b)} <span style="opacity:0.7;">(at the #${a} seed)</span></li>`).join("");
  const quarters = [[1, "8/9"], [4, "5/12"], [2, "7/10"], [3, "6/11"]]
    .map(([s, w]) => `<li>#${s} ${name(s)} vs the winner of #${w}</li>`).join("");
  return `<div class="cfp-spot-card">
    <div class="cfp-spot-card-header"><div class="cfp-spot-card-title">Projected Playoff Bracket</div></div>
    <p style="margin:0.3rem 0;">The bracket as the current table projects it — seeds and pairings, not a prediction of who wins each game. A spot marked In Play is a projected holder whose berth is not yet secured; everything that can still change is listed under the bracket.</p>
    <div style="margin-top:0.5rem;"><strong>First-round byes</strong><ul>${byes}</ul></div>
    <div style="margin-top:0.5rem;"><strong>First round (on campus)</strong><ul>${firstRound}</ul></div>
    <div style="margin-top:0.5rem;"><strong>Quarterfinals</strong><ul>${quarters}</ul></div>
    <div style="margin-top:0.5rem;"><strong>Semifinals</strong><ul><li>The #1 quarterfinal winner vs the #4 quarterfinal winner</li><li>The #2 quarterfinal winner vs the #3 quarterfinal winner</li></ul></div>
    <div style="margin-top:0.5rem;"><strong>Championship</strong><ul><li>The two semifinal winners</li></ul></div>
  </div>`;
}

function getTicketProfile(game) {
  if (!ticketsConfig) return null;
  const base = ticketsConfig.defaults || {};
  const confOverride = (game.conference && ticketsConfig.conferences?.[game.conference]) || {};
  const teamOverride = ticketsConfig.teams?.[game.home] || ticketsConfig.teams?.[game.away] || {};
  return {
    providers: teamOverride.providers || confOverride.providers || base.providers || [],
    patterns: {...(base.patterns || {}), ...(confOverride.patterns || {}), ...(teamOverride.patterns || {})},
  };
}

function buildTicketButtons(game) {
  const profile = getTicketProfile(game);
  if (!profile?.providers?.length) return "";
  const labels = ticketsConfig.labels || {};
  const query = encodeURIComponent(`${game.away} at ${game.home} tickets`);
  const links = profile.providers.map((key) => {
    const pattern = profile.patterns[key];
    if (!pattern) return null;
    const url = pattern.replace("{QUERY}", query);
    return `<a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(labels[key] || key)}</a>`;
  }).filter(Boolean).join(" • ");
  return links ? `<div style="margin-top:0.4rem;font-size:0.8rem;"><span>Tickets: </span>${links}<span style="margin-left:0.25rem;opacity:0.6;">(partners)</span></div>` : "";
}

function renderGames(games, availability) {
  if (!Array.isArray(games) || !games.length) {
    const state = availability?.games || "NO_CURRENT_EVENTS_OBSERVED";
    elGames.innerHTML = `<p>No current games to display (${escapeHtml(state)}).</p>`;
    return;
  }
  elGames.innerHTML = `<ul class="cfp-games-list">${games.map((g) => `
    <li class="cfp-game">
      <div class="cfp-game-header"><span>${escapeHtml(g.away)} @ ${escapeHtml(g.home)}</span><span>${g.away_score ?? "-"} – ${g.home_score ?? "-"}</span></div>
      <div class="cfp-game-meta">
        ${g.status ? `Status: ${escapeHtml(g.status)}` : ""}
        ${g.kickoff ? ` | Kickoff: ${escapeHtml(formatDateTime(g.kickoff))}` : ""}
        ${g.note ? ` | ${escapeHtml(g.note)}` : ""}
        ${buildTicketButtons(g)}
      </div>
    </li>`).join("")}</ul>`;
}

function renderConferenceStandings(conf) {
  if (!conf) return;
  const rows = (conf.teams || []).map((team) => `<tr><td>${escapeHtml(team.team)}</td><td>${escapeHtml(team.overall)}</td><td>${escapeHtml(team.conference_record)}</td><td>${escapeHtml(team.pf)}</td><td>${escapeHtml(team.pa)}</td></tr>`).join("");
  elConfStandings.innerHTML = `<table class="cfp-conf-table"><thead><tr><th>Team</th><th>Overall</th><th>Conf</th><th>PF</th><th>PA</th></tr></thead><tbody>${rows}</tbody></table>`;
}

function renderConferences(conferences, sourceId, availability) {
  if (!Array.isArray(conferences) || !conferences.length) {
    elConfSelect.innerHTML = "<option>No current data</option>";
    elConfStandings.innerHTML = `<p>Conference standings unavailable (${escapeHtml(availability?.conference_standings || "NOT_AVAILABLE")}).</p>`;
    return;
  }
  if (elConfSourceMarker) elConfSourceMarker.innerHTML = sourceMarker(sourceId);
  elConfSelect.innerHTML = conferences.map((conf) => `<option value="${escapeHtml(conf.id)}">${escapeHtml(conf.name)}</option>`).join("");
  renderConferenceStandings(conferences[0]);
  elConfSelect.onchange = () => renderConferenceStandings(conferences.find((conf) => conf.id === elConfSelect.value));
}

function renderSources(sources) {
  if (!Array.isArray(sources) || !sources.length) {
    elSources.innerHTML = "<p>No sources declared.</p>";
    return;
  }
  elSources.innerHTML = `<ul class="cfp-sources-list">${sources.map((source) => `<li id="cfp-source-${escapeHtml(source.id)}">[${escapeHtml(source.id)}] <a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.label)}</a> — ${escapeHtml(source.status || "UNKNOWN")}</li>`).join("")}</ul>`;
}

async function loadCfpData() {
  setStatus("Refreshing…");
  try {
    const [dataRes, ticketRes] = await Promise.all([
      fetch(`${CFP_DATA_URL}?t=${Date.now()}`),
      fetch(`${CFP_TICKETS_URL}?t=${Date.now()}`).catch(() => null),
    ]);
    if (!dataRes.ok) throw new Error(`CFP data HTTP ${dataRes.status}`);
    const data = await dataRes.json();
    ticketsConfig = ticketRes && ticketRes.ok ? await ticketRes.json() : null;

    sourcesIndex = {};
    (data.sources || []).forEach((source) => { sourcesIndex[source.id] = source; });

    renderSources(data.sources || []);
    renderRankings(data.rankings || [], data.cfp_source_id, data);
    renderSpotDetails(data.rankings || [], data);
    renderGames(data.games || [], data.availability || {});
    renderConferences(data.conferences || [], data.conf_source_id, data.availability || {});

    elLastUpdated.textContent = `Season ${data.season || "?"} • ${data.phase || "UNKNOWN"} • Projection generated: ${formatDateTime(data.last_updated)}`;
    const sourceErrors = Object.keys(data.freshness?.source_errors || {});
    setStatus(sourceErrors.length ? `Updated with ${sourceErrors.length} source warning(s).` : "Updated.", false);
  } catch (error) {
    console.error(error);
    setStatus("Current-season data load failed; stale rankings are not substituted.", true);
  }
}

if (elRefreshBtn) elRefreshBtn.onclick = loadCfpData;
loadCfpData();
