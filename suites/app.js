'use strict';
const byId = id => document.getElementById(id);
async function jsonRequest(url, options) {
  const response = await fetch(url, {cache: 'no-store', ...options});
  const data = await response.json();
  if (!response.ok) throw data;
  return data;
}
async function status() {
  try {
    const value = await jsonRequest('api/status');
    byId('status').textContent = Object.entries(value.stages).map(([k, v]) => `${k}: ${v}`).join(' · ');
  } catch (_) { byId('status').textContent = 'Service unavailable. No live stage availability is established.'; }
}
async function specimen() {
  try {
    const value = await jsonRequest('api/specimen');
    // Same-origin, well-formed receipt only. Never render an arbitrary external redirect.
    if (!/^INTAKE-[a-f0-9]{32}$/.test(value.id)) throw new Error('Invalid specimen pointer');
    byId('specimen').href = `api/intakes/${value.id}/bundle`;
    byId('specimen').textContent = 'Download public specimen ↗';
    byId('specimen-state').textContent = `Published specimen ${value.id}. Analysis: api/intakes/${value.id}/analysis. Conformance proof is inside the bundle. This does not establish production acceptance.`;
  } catch (_) { byId('specimen-state').textContent = 'No public specimen is installed on this service yet. Production acceptance remains open.'; }
}
byId('intake').addEventListener('submit', async event => {
  event.preventDefault();
  const form = new FormData(event.target);
  const body = Object.fromEntries(form);
  byId('result').hidden = false;
  byId('download').hidden = true;
  byId('manifest').textContent = '';
  byId('receipt').textContent = '';
  byId('report').textContent = '';
  try {
    body.claims = JSON.parse(form.get('claims'));
    body.public_surfaces = form.get('public_surfaces').split('\n').map(x => x.trim()).filter(Boolean);
    byId('submit').disabled = true;
    byId('progress').textContent = 'Submitting intake…';
    const receipt = await jsonRequest('api/intakes', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
    byId('receipt').textContent = `Your intake receipt: ${receipt.id} · input SHA-256: ${receipt.input_sha256}`;
    byId('result-title').textContent = 'Intake received';
    byId('progress').textContent = 'Locating evidence and checking the canonical template…';
    const result = await jsonRequest(`api/intakes/${receipt.id}/build`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: '{}'});
    byId('result-title').textContent = 'Your specimen is ready';
    byId('progress').textContent = `${result.analysis.located} LOCATED · ${result.analysis.evidence_not_found} EVIDENCE_NOT_FOUND · ${result.conformance.verdict} · connection IN_BUILD`;
    byId('manifest').textContent = `Manifest SHA-256: ${result.manifest_sha256} · Bundle SHA-256: ${result.bundle_sha256}`;
    byId('download').href = `api/intakes/${receipt.id}/bundle`;
    byId('download').textContent = 'Download your suite ↧';
    byId('download').hidden = false;
    byId('report').textContent = JSON.stringify({analysis: result.analysis, connection: result.connection, independent_validation: result.independent_validation}, null, 2);
  } catch (error) {
    byId('progress').textContent = 'This attempt did not complete. Keep any receipt shown above.';
    byId('report').textContent = error instanceof Error ? error.message : JSON.stringify(error, null, 2);
  } finally { byId('submit').disabled = false; status(); }
});
status(); specimen();
setInterval(status, 30000);
