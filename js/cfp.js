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

function renderBracket(rankings) {
  const el = document.getElementById('bracket-grid');
  if (!el) return;
  el.innerHTML = '';

  rankings.forEach(team => {
    const div = document.createElement('div');
    div.className = 'bracket-slot';

    const movementClass =
      team.movement > 0 ? 'badge-up' :
      team.movement < 0 ? 'badge-down' :
      'badge-neutral';

    div.innerHTML = `
      <div>
        <span class="seed">#${team.seed}</span>
        <span class="team">${team.name}</span>
      </div>
      <span class="meta">
        ${team.record} • ${team.conference} •
        <span class="${movementClass}">
          ${team.movement > 0 ? `▲ ${team.movement}` :
            team.movement < 0 ? `▼ ${Math.abs(team.movement)}` :
            '–'}
        </span>
      </span>
    `;

    div.addEventListener('click', () => {
      if (team.teamId) {
        window.location.href = `team.html?team=${encodeURIComponent(team.teamId)}`;
      }
    });

    el.appendChild(div);
  });
}

function renderTable(rankings) {
  const tbody = document.querySelector('#cfp-table tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  rankings.forEach(team => {
    const tr = document.createElement('tr');
    const movementClass =
      team.movement > 0 ? 'badge-up' :
      team.movement < 0 ? 'badge-down' :
      'badge-neutral';
    const movementText =
      team.movement > 0 ? `▲ ${team.movement}` :
      team.movement < 0 ? `▼ ${Math.abs(team.movement)}` :
      '–';

    tr.innerHTML = `
      <td>${team.seed}</td>
      <td>${team.name}</td>
      <td>${team.record}</td>
      <td>${team.conference}</td>
      <td>${team.movementText || ''}</td>
      <td class="${movementClass}">${team.projection || movementText}</td>
    `;

    tbody.appendChild(tr);
  });
}

function renderSummary(meta, summary) {
  const el = document.getElementById('summary-text');
  if (!el) return;
  const parts = [];
  if (meta && meta.season && meta.sport) {
    parts.push(`${meta.sport.toUpperCase()} ${meta.season} CFP picture.`);
  }
  if (meta && meta.lastRankingDate) {
    parts.push(`Last official CFP ranking date: ${meta.lastRankingDate}.`);
  }
  if (summary && summary.text) {
    parts.push(summary.text);
  }
  el.textContent = parts.join(' ');
}

function renderChampionship(weekend) {
  const grid = document.getElementById('championship-grid');
  if (!grid) return;
  grid.innerHTML = '';

  weekend.forEach(game => {
    const card = document.createElement('article');
    card.className = 'card';
    card.innerHTML = `
      <h2>${game.conference} Championship</h2>
      <p><strong>Matchup:</strong> ${game.matchup}</p>
      <p><strong>Best case:</strong> ${game.bestCase}</p>
      <p><strong>Most likely:</strong> ${game.likelyCase}</p>
      <p><strong>Nightmare:</strong> ${game.worstCase}</p>
    `;
    grid.appendChild(card);
  });
}

(async function init() {
  const data = await loadCFPData();
  if (!data) return;

  if (document.getElementById('bracket-grid')) {
    renderBracket(data.rankings || []);
    renderTable(data.rankings || []);
    renderSummary(data.meta, data.summary);
  }

  if (document.getElementById('championship-grid')) {
    renderChampionship(data.championshipWeekend || []);
  }
})();
