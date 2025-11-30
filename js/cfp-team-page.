// js/cfp-team-page.js

import { loadCfpData, getTeamById, listTeamsByRank } from './cfp-data.js';

function getTeamIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get('team') || '';
}

function renderError(message, teams) {
  const root = document.getElementById('team-root');
  if (!root) return;

  root.innerHTML = `
    <section class="cfp-card cfp-card-error">
      <h1>Team not found</h1>
      <p>${message}</p>
      ${teams && teams.length
        ? `
        <h2>Available CFP teams</h2>
        <ul class="cfp-team-list">
          ${teams
            .map(
              (t) => `
            <li>
              <a href="/team.html?team=${encodeURIComponent(t.id)}">
                #${t.currentRank ?? '?'} &mdash; ${t.name} (${t.shortName || t.id})
              </a>
            </li>
          `
            )
            .join('')}
        </ul>`
        : ''}
      <p class="cfp-nav-link">
        <a href="/">Back to CFP Bracket</a>
      </p>
    </section>
  `;
}

function renderSchedule(schedule) {
  if (!schedule || !schedule.length) {
    return `
      <p class="cfp-faded">
        No detailed schedule loaded yet. Add games to <code>remainingSchedule</code> in
        <code>data/cfp-2025.json</code>.
      </p>
    `;
  }

  return `
    <table class="cfp-table cfp-schedule-table">
      <thead>
        <tr>
          <th>Week</th>
          <th>Opponent</th>
          <th>Loc</th>
          <th>Date</th>
          <th>Conf</th>
          <th>Status</th>
          <th>Result</th>
        </tr>
      </thead>
      <tbody>
        ${schedule
          .map((g) => {
            const confFlag = g.isConference ? 'Yes' : 'No';
            const status = g.status || 'upcoming';
            const result = g.result
              ? `${g.result} ${g.score || ''}`.trim()
              : '';
            const loc =
              g.location === 'home'
                ? 'H'
                : g.location === 'away'
                ? 'A'
                : g.location === 'neutral'
                ? 'N'
                : '';

            return `
              <tr class="cfp-schedule-row cfp-schedule-${status}">
                <td>${g.week ?? ''}</td>
                <td>${g.opponent || ''}</td>
                <td>${loc}</td>
                <td>${g.date || ''}</td>
                <td>${confFlag}</td>
                <td>${status}</td>
                <td>${result}</td>
              </tr>
            `;
          })
          .join('')}
      </tbody>
    </table>
  `;
}

function renderList(list, emptyMessage) {
  if (!list || !list.length) {
    return `<p class="cfp-faded">${emptyMessage}</p>`;
  }

  return `
    <ul class="cfp-bullet-list">
      ${list.map((item) => `<li>${item}</li>`).join('')}
    </ul>
  `;
}

function renderPaths(team) {
  const paths = team.paths || {};

  function block(key, label) {
    const p = paths[key] || {};
    const record = p.record ? `<div class="cfp-path-record">${p.record}</div>` : '';
    const seed = p.seed ? `<div class="cfp-path-seed">Projected seed: ${p.seed}</div>` : '';
    const summary = p.summary || 'No summary written yet.';

    return `
      <article class="cfp-path-card">
        <h3>${label}</h3>
        ${record}
        ${seed}
        <p>${summary}</p>
      </article>
    `;
  }

  return `
    <section class="cfp-section cfp-paths">
      <h2>Road to the National Championship</h2>
      <div class="cfp-path-grid">
        ${block('bestCase', 'Best Case')}
        ${block('mostLikely', 'Most Likely')}
        ${block('worstCase', 'Nightmare Case')}
      </div>
    </section>
  `;
}

function renderTeamPage(data, team) {
  const root = document.getElementById('team-root');
  if (!root) return;

  const teamsByRank = listTeamsByRank(data);

  const movement =
    team.sinceLastRanking === 0
      ? 'No movement since last ranking.'
      : team.sinceLastRanking > 0
      ? `Moved up ${team.sinceLastRanking} spots since last ranking.`
      : `Dropped ${Math.abs(team.sinceLastRanking)} spots since last ranking.`;

  const projection = team.projection || {};
  const projLine = projection.movementText || 'Projection notes not set yet.';

  root.innerHTML = `
    <header class="cfp-header cfp-header-sub">
      <div class="cfp-brand">
        <a href="/" class="cfp-logo-link">STEGVERSE • CFP</a>
      </div>
      <nav class="cfp-nav">
        <a href="/">Bracket</a>
        <a href="/championship.html">Championship Weekend</a>
        <a href="/providers.html">Rankings Providers</a>
      </nav>
    </header>

    <main class="cfp-main cfp-main-team">
      <section class="cfp-section cfp-team-hero">
        <p class="cfp-pill">CFP ${data.season} • Team Roadmap</p>
        <h1>
          #${team.currentRank ?? '?'} &mdash; ${team.name}
        </h1>
        <p class="cfp-team-subtitle">
          ${team.headline || 'Custom headline goes here.'}
        </p>
        <p class="cfp-body">
          ${team.summary || 'Use the summary field in the data file to describe this team\'s 2025 story arc.'}
        </p>
        <dl class="cfp-team-meta">
          <div>
            <dt>Conference</dt>
            <dd>${team.conference || '—'}</dd>
          </div>
          <div>
            <dt>Record</dt>
            <dd>${team.record || '0-0'} (${team.confRecord || '0-0'} conf)</dd>
          </div>
          <div>
            <dt>Seed</dt>
            <dd>${team.seed ?? team.currentRank ?? '—'}</dd>
          </div>
          <div>
            <dt>Movement</dt>
            <dd>${movement}</dd>
          </div>
        </dl>
        <p class="cfp-body">
          <strong>Projection:</strong> ${projLine}
        </p>
      </section>

      ${renderPaths(team)}

      <section class="cfp-section cfp-schedule-section">
        <h2>Remaining Schedule (Impact on CFP Résumé)</h2>
        ${renderSchedule(team.remainingSchedule)}
      </section>

      <section class="cfp-section cfp-notes-grid">
        <article>
          <h2>Notable Wins</h2>
          ${renderList(team.notableWins, 'Add notable wins for this team in the data file.')}
        </article>
        <article>
          <h2>Risk Factors</h2>
          ${renderList(team.riskFactors, 'List major concerns, injuries, or matchup issues here.')}
        </article>
      </section>

      <section class="cfp-section cfp-other-teams">
        <h2>Other CFP Teams</h2>
        <p class="cfp-faded">Tap another team to jump to their roadmap.</p>
        <div class="cfp-tag-list">
          ${teamsByRank
            .map((t) => {
              const isCurrent = t.id === team.id;
              return `
                <a
                  class="cfp-tag ${isCurrent ? 'cfp-tag-active' : ''}"
                  href="/team.html?team=${encodeURIComponent(t.id)}"
                >
                  #${t.currentRank ?? '?'} ${t.shortName || t.name}
                </a>
              `;
            })
            .join('')}
        </div>
      </section>
    </main>
  `;
}

async function initTeamPage() {
  const teamId = getTeamIdFromUrl();

  let data;
  try {
    data = await loadCfpData();
  } catch (err) {
    renderError(
      'Could not load CFP data. Check that /data/cfp-2025.json exists and is valid JSON.',
      []
    );
    return;
  }

  const teamsByRank = listTeamsByRank(data);
  if (!teamId) {
    renderError(
      'No team selected. Use ?team=<id> in the URL, for example: /team.html?team=ttu',
      teamsByRank
    );
    return;
  }

  const team = getTeamById(data, teamId);
  if (!team) {
    renderError(
      `No team with ID "${teamId}" was found in cfp-2025.json.`,
      teamsByRank
    );
    return;
  }

  renderTeamPage(data, team);
}

document.addEventListener('DOMContentLoaded', () => {
  initTeamPage().catch((err) => {
    console.error('Unexpected error rendering team page:', err);
    renderError('Unexpected error rendering team page.', []);
  });
});
