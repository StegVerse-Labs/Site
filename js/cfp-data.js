// js/cfp-data.js

/**
 * Load CFP data JSON for the 2025 NCAAF season.
 * Returns a parsed object or throws on hard failure.
 */
export async function loadCfpData() {
  const url = '/data/cfp-2025.json';

  try {
    const res = await fetch(url, {
      cache: 'no-store' // ensure the latest rankings load after edits
    });

    if (!res.ok) {
      throw new Error(`Failed to load CFP data (${res.status})`);
    }

    const data = await res.json();

    if (!data || !Array.isArray(data.teams)) {
      throw new Error('CFP data missing "teams" array');
    }

    return data;
  } catch (err) {
    console.error('Error loading CFP data:', err);
    throw err;
  }
}

/**
 * Find a team by its ID (e.g. 'ttu', 'uga').
 */
export function getTeamById(data, id) {
  if (!data || !Array.isArray(data.teams)) return null;
  const safeId = String(id || '').trim().toLowerCase();
  return data.teams.find((t) => String(t.id).toLowerCase() === safeId) || null;
}

/**
 * Return teams sorted by currentRank (1–12).
 */
export function listTeamsByRank(data) {
  if (!data || !Array.isArray(data.teams)) return [];
  return [...data.teams].sort((a, b) => (a.currentRank || 999) - (b.currentRank || 999));
}
