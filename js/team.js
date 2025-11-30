async function loadCFPData() {
  try {
    const res = await fetch('data/cfp_data.json', { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to load CFP data');
    return await res.json();
  } catch (err) {
    console.error(err);
    return null;
  }
}

function getTeamIdFromQuery() {
  const params = new URLSearchParams(window.location.search);
  return params.get('team');
}

function renderTeam(teamId, data) {
  const team = data.teams && data.teams[teamId];
  const titleEl = document.getElementById('team-title');
  const metaEl = document.getElementById('team-meta');
  const bestEl = document.getElementById('best-case');
  const likelyEl = document.getElementById('likely-case');
  const worstEl = document.getElementById('worst-case');
  const footerEl = document.getElementById('team-footer');

  if (!team) {
    if (titleEl) titleEl.textContent = 'Team not found';
    if (metaEl) metaEl.textContent = 'No data for this team yet.';
    return;
  }

  if (titleEl) {
    titleEl.textContent = `${team.displayName} • Road to the National Championship`;
  }
  if (metaEl) {
    const seed = team.seed ? `CFP seed: #${team.seed}. ` : '';
    const record = team.record ? `Record: ${team.record}.` : '';
    metaEl.textContent = `${seed}${record}`;
  }
  if (bestEl) bestEl.textContent = team.bestCase || '';
  if (likelyEl) likelyEl.textContent = team.likelyCase || '';
  if (worstEl) worstEl.textContent = team.worstCase || '';

  if (footerEl && data.meta) {
    footerEl.textContent = `StegVerse CFP tracker • ${data.meta.sport?.toUpperCase()} ${data.meta.season}`;
  }
}

(async function initTeam() {
  const data = await loadCFPData();
  if (!data) return;
  const teamId = getTeamIdFromQuery();
  renderTeam(teamId, data);
})();
