const STEGVERSE_ROUTES = [
  { name: 'Site', terms: ['site', 'page', 'html', 'nav', 'navigation', 'mirror', 'public', 'readme', 'papers'] },
  { name: 'repo-standards', terms: ['repo-standards', 'standard', 'standards', 'allowed task', 'manifest', 'maintenance', 'remediation', 'branch cleanup'] },
  { name: 'StegVerse-002', terms: ['sv002', 'stegverse-002', 'core-lite', 'intake', 'deployment', 'm10'] },
  { name: 'formalism-tests', terms: ['formalism', 'test', 'proof', 'admissibility', 'allow', 'deny', 'fail-closed', 'stage'] },
  { name: 'Continuity', terms: ['continuity', 'receipt', 'replay', 'hash', 'chain', 'state'] },
  { name: 'Publisher', terms: ['publisher', 'paper', 'publication', 'mirror-papers'] },
  { name: 'Solver', terms: ['math', 'solve', 'solver', 'equation', 'calculate', 'calculation', 'algebra', 'proof', 'unit conversion', 'derivative', 'integral'] },
  { name: 'Restricted admin', terms: ['delete branch', 'delete branches', 'secret', 'token', 'credential', 'permission', 'workflow', 'force push', 'force-push', 'release', 'deploy key', 'webhook', 'collaborator'] }
];

const TRANSITION_INTENTS = [
  { id: 'explain', label: 'Explain', transition: 'Explain admissibility', destination: 'admissibility-wiki.html', keywords: ['explain', 'define', 'what is', 'meaning', 'admissibility', 'glossary', 'ontology', 'formal definition'], boundary: 'public explanation only' },
  { id: 'demonstrate', label: 'Demonstrate', transition: 'Demonstrate governance', destination: 'demo.html', keywords: ['demo', 'demonstrate', 'show', 'simulate', 'example', 'run example', 'browser demo'], boundary: 'static browser demonstration only' },
  { id: 'compare', label: 'Compare', transition: 'Compare an external framework', destination: 'governance-observatory.html', keywords: ['compare', 'framework', 'external', 'morrison', 'resurrection', 'decisionassure', 'glm', 'evide', 'runtime governance'], boundary: 'comparison posture only' },
  { id: 'research', label: 'Research', transition: 'Read the research', destination: 'Papers.html', keywords: ['paper', 'research', 'publish', 'theorem', 'proof', 'citation', 'scientific', 'peer review'], boundary: 'research reference only' },
  { id: 'build', label: 'Build', transition: 'Prepare build handoff', destination: 'docs/SITE_MIRROR_HANDOFF.md', keywords: ['build', 'continue', 'install', 'patch', 'repo', 'handoff', 'workflow', 'validator'], boundary: 'handoff preview only; no repo mutation from Site' },
  { id: 'replay', label: 'Replay', transition: 'Inspect replay or receipt posture', destination: 'transition-verification-guide.html', keywords: ['replay', 'receipt', 'hash', 'reconstruct', 'reconstruction', 'audit', 'verify', 'verification'], boundary: 'public verification guide only' },
  { id: 'runtime', label: 'Runtime', transition: 'Evaluate runtime governance', destination: 'governance-observatory.html', keywords: ['runtime', 'agent', 'tool', 'allow', 'block', 'deny', 'boundary', 'morrison', 'resurrection'], boundary: 'runtime evaluation preview only' },
  { id: 'formalism', label: 'Formalism', transition: 'Inspect formalisms', destination: 'formalisms/index.html', keywords: ['formalism', 'stcm', 'rtg', 'transition table', 'geometry', 'model', 'math'], boundary: 'formalism mirror only' },
  { id: 'sdk', label: 'SDK', transition: 'Inspect SDK manifest preview', destination: 'ecosystem-chat.html#technical-details', keywords: ['sdk', 'adapter', 'manifest', 'api', 'backend', 'gateway', 'provider', 'client'], boundary: 'SDK preview only; no backend submission' },
  { id: 'implementation', label: 'Implementation', transition: 'Inspect implementation mirrors', destination: 'tt-code-representation.html', keywords: ['implementation', 'code', 'registry', 'handler', 'fixture', 'script', 'package', 'module'], boundary: 'public implementation mirror only' },
  { id: 'solver', label: 'Solver', transition: 'Use math-solver adapter preview', destination: 'math-solver/index.html', keywords: ['solve', 'calculate', 'equation', 'unit', 'math', 'symbolic', 'proof step'], boundary: 'solver preview only; no live solver execution' }
];

const FALLBACK_INTENT = { id: 'explain', label: 'Explain', transition: 'Explain request boundary first', destination: 'ecosystem-chat.html#how-it-works', boundary: 'classification fallback only' };
const CONTINUATION_SUPPORT = [
  { label: 'Boundary', transition: 'Review boundary explanation', destination: '#how-it-works', boundary: 'local page explanation only' },
  { label: 'Telemetry', transition: 'Inspect routing bands', destination: '#interaction-bands', boundary: 'local telemetry preview only' },
  { label: 'Technical', transition: 'Inspect SDK and gateway preview', destination: '#technical-details', boundary: 'technical preview only' }
];

const INTERACTION_BANDS = [
  { key: 'intra', label: 'INTRA', terms: ['site', 'stegverse', 'repo', 'wiki', 'manifest', 'receipt', 'handoff', 'standard', 'transition', 'continuity', 'publisher', 'admissibility'] },
  { key: 'inter', label: 'INTER', terms: ['adapter', 'api', 'provider client', 'partner', 'external system', 'github', 'google', 'slack', 'connector', 'node'] },
  { key: 'research', label: 'RESEARCH', terms: ['search', 'web', 'online', 'latest', 'current', 'news', 'paper', 'source', 'documentation', 'research'] },
  { key: 'provider', label: 'PROVIDER', terms: ['llm', 'model', 'provider', 'token', 'quota', 'cost', 'latency', 'openai', 'claude', 'gemini'] },
  { key: 'solver', label: 'SOLVER', terms: ['math', 'solve', 'solver', 'equation', 'calculate', 'calculation', '+', '-', '*', '/', '=', 'algebra', 'proof', 'unit'] },
  { key: 'receipt', label: 'RECEIPT', terms: ['receipt', 'replay', 'hash', 'reconstruct', 'fingerprint', 'authority', 'admissibility', 'evidence', 'audit'] }
];

const RESTRICTED_PATTERNS = [/\bgh\s+/i,/\bgit\s+push\b/i,/\bgit\s+branch\b/i,/\brm\s+-rf\b/i,/\bcurl\s+/i,/\btoken\b/i,/\bsecret\b/i,/\bcredential\b/i,/\bworkflow\b/i,/\bforce[-\s]?push\b/i,/\bdelete\s+(branch|branches|repo|repository|release|tag|workflow)\b/i];
const STEGVERSE_GATEWAY_PATH = '/api/ecosystem-chat';
const STEGVERSE_LOCAL_MODE = true;

const form = document.getElementById('chatForm');
const input = document.getElementById('messageInput');
const log = document.getElementById('chatLog');
const sdkForm = document.getElementById('sdkEntryForm');
const manifestPreview = document.getElementById('manifestPreview');
const receiptPreview = document.getElementById('receiptPreview');
const sdkStatus = document.getElementById('sdkFormStatus');
const useManifestButton = document.getElementById('useManifestAsConsoleMessage');
const interactionBandMeter = document.getElementById('interactionBandMeter');
const continuationSummary = document.getElementById('continuationSummary');
const continuationGrid = document.getElementById('continuationGrid');

if (interactionBandMeter) renderInteractionBands(calculateInteractionProfile(''));
renderContinuationPanel(FALLBACK_INTENT, 'Unknown');

if (input) {
  input.addEventListener('input', () => {
    const posture = classifyRequestPosture(input.value);
    if (interactionBandMeter) renderInteractionBands(posture.interaction_profile);
    renderContinuationPanel(posture.intent, posture.route);
  });
}

if (form && input && log) {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    appendMessage('User', message, 'user');
    input.value = '';
    const result = await routeEcosystemRequest(message);
    appendMessage('Governed Transition Preview', result.response, 'system', result.receipt_line);
    if (interactionBandMeter) renderInteractionBands(result.interaction_profile);
    renderContinuationPanel(result.intent, result.route);
  });
}

if (sdkForm && manifestPreview && receiptPreview) {
  sdkForm.addEventListener('input', updateGeneratedWindows);
  sdkForm.addEventListener('change', updateGeneratedWindows);
  sdkForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const result = getSubmissionCheck();
    sdkStatus.textContent = result.ok ? 'Submission check passed locally. Payload is ready for a governed SDK entry point; Site still issues no proof receipt and performs no execution.' : `Submission check failed: ${result.errors.join('; ')}`;
  });
  if (useManifestButton) {
    useManifestButton.addEventListener('click', () => {
      if (!input) return;
      const payload = buildSdkPayload();
      input.value = JSON.stringify(payload, null, 2);
      input.focus();
      const posture = classifyRequestPosture(input.value);
      if (interactionBandMeter) renderInteractionBands(posture.interaction_profile);
      renderContinuationPanel(posture.intent, posture.route);
    });
  }
  updateGeneratedWindows();
}

async function routeEcosystemRequest(message) {
  const posture = classifyRequestPosture(message);
  if (posture.restricted) return localRouteResult(message, 'Restricted request detected; local gateway refuses execution and routes to authority review.', posture);
  if (!STEGVERSE_LOCAL_MODE) {
    try { return await sendGatewayRequest(message, posture); }
    catch (error) { return localRouteResult(message, 'Gateway request failed; fail-closed to local classification.', posture); }
  }
  return localRouteResult(message, 'Local simulation mode; no external execution attempted.', posture);
}

async function sendGatewayRequest(message, posture) {
  const response = await fetch(STEGVERSE_GATEWAY_PATH, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message, session_id: getSessionId(), requested_route: posture.route, transition_intent: posture.intent.id, transition_destination: posture.intent.destination, goal: 'user advancement console with governed task boundaries', execution_model: 'allowlisted_task_request_only', raw_shell_allowed: false, authority_required: true, rate_limit_required: true, receipt_required_for_execution: true, interaction_profile: posture.interaction_profile, interaction_bands: INTERACTION_BANDS.map((band) => band.key), math_solver_supported: true }) });
  if (!response.ok) throw new Error(`Gateway returned ${response.status}`);
  const data = await response.json();
  const receiptLine = data.receipt_id ? `receipt_id=${data.receipt_id}` : 'receipt=not-issued';
  const interactionProfile = normalizeInteractionProfile(data.interaction_profile || posture.interaction_profile);
  return { response: data.response || buildLocalResponse(message, data.routed_module || 'Unknown', 'Gateway returned no response body.', posture), receipt_line: `${receiptLine} · routed_module=${data.routed_module || 'Unknown'} · intent=${posture.intent.id} · source=gateway · shell=disabled · bands=${formatInteractionProfile(interactionProfile)}`, interaction_profile: interactionProfile, intent: posture.intent, route: data.routed_module || posture.route };
}

async function localRouteResult(message, status, posture = classifyRequestPosture(message)) {
  const receiptLine = await localReceipt(message, posture);
  return { response: buildLocalResponse(message, posture.route, status, posture), receipt_line: receiptLine, interaction_profile: posture.interaction_profile, intent: posture.intent, route: posture.route };
}

function classifyRequestPosture(message) {
  const route = classifyRoute(message);
  const intent = classifyTransitionIntent(message);
  const restricted = route === 'Restricted admin' || RESTRICTED_PATTERNS.some((pattern) => pattern.test(message));
  const taskStatus = restricted ? 'pending_authority' : 'preview_only';
  const interactionProfile = calculateInteractionProfile(message);
  return { route: restricted ? 'Restricted admin' : route, intent, restricted, raw_shell_allowed: false, authority_required: true, task_status: taskStatus, receipt_required_for_execution: true, interaction_profile: interactionProfile, math_solver_supported: true };
}

function classifyRoute(message) {
  const text = message.toLowerCase();
  const scored = STEGVERSE_ROUTES.map((route) => ({ name: route.name, score: route.terms.reduce((total, term) => total + (text.includes(term) ? 1 : 0), 0) })).sort((a, b) => b.score - a.score);
  return scored[0].score > 0 ? scored[0].name : 'Unknown';
}

function classifyTransitionIntent(message) {
  const text = message.toLowerCase();
  const scored = TRANSITION_INTENTS.map((intent) => ({ intent, score: intent.keywords.reduce((total, keyword) => total + (text.includes(keyword.toLowerCase()) ? 1 : 0), 0) })).sort((a, b) => b.score - a.score);
  return scored[0].score > 0 ? scored[0].intent : FALLBACK_INTENT;
}

function calculateInteractionProfile(message) {
  const text = message.toLowerCase();
  const profile = {};
  INTERACTION_BANDS.forEach((band) => {
    const score = band.terms.reduce((total, term) => total + (text.includes(term.toLowerCase()) ? 1 : 0), 0);
    const operatorSignal = band.key === 'solver' && /\d+\s*[+\-*/=]\s*\d+/.test(message) ? 2 : 0;
    const authoritySignal = band.key === 'receipt' && /\b(allow|deny|defer|quarantine|fail[-_ ]closed)\b/i.test(message) ? 1 : 0;
    profile[band.key] = Math.min(100, Math.max(0, (score + operatorSignal + authoritySignal) * 20));
  });
  return normalizeInteractionProfile(profile);
}

function normalizeInteractionProfile(profile) {
  return INTERACTION_BANDS.reduce((normalized, band) => { const value = Number(profile && profile[band.key]); normalized[band.key] = Number.isFinite(value) ? Math.min(100, Math.max(0, Math.round(value))) : 0; return normalized; }, {});
}

function formatInteractionProfile(profile) {
  const normalized = normalizeInteractionProfile(profile);
  return INTERACTION_BANDS.map((band) => `${band.key}:${normalized[band.key]}`).join(',');
}

function renderInteractionBands(profile) {
  if (!interactionBandMeter) return;
  const normalized = normalizeInteractionProfile(profile);
  interactionBandMeter.innerHTML = '';
  INTERACTION_BANDS.forEach((band) => {
    const row = document.createElement('div'); row.className = 'band-row';
    const label = document.createElement('span'); label.textContent = band.label;
    const track = document.createElement('span'); track.className = 'band-track';
    const fill = document.createElement('span'); fill.className = 'band-fill'; fill.style.setProperty('--value', `${normalized[band.key]}%`); track.appendChild(fill);
    const value = document.createElement('span'); value.textContent = `${normalized[band.key]}%`;
    row.appendChild(label); row.appendChild(track); row.appendChild(value); interactionBandMeter.appendChild(row);
  });
}

function renderContinuationPanel(intent = FALLBACK_INTENT, route = 'Unknown') {
  if (!continuationSummary || !continuationGrid) return;
  continuationSummary.textContent = `Intent: ${intent.label} · Route: ${route} · Boundary: ${intent.boundary}`;
  const items = [intent, ...CONTINUATION_SUPPORT].slice(0, 4);
  continuationGrid.innerHTML = '';
  items.forEach((item) => {
    const card = document.createElement('div'); card.className = 'continuation-item';
    const title = document.createElement('strong'); title.textContent = item.transition;
    const summary = document.createElement('span'); summary.textContent = item.boundary;
    const link = document.createElement('a'); link.className = 'sv-btn sv-btn-secondary'; link.href = item.destination; link.textContent = 'Continue';
    card.appendChild(title); card.appendChild(summary); card.appendChild(link); continuationGrid.appendChild(card);
  });
}

function buildLocalResponse(message, route, status, posture = classifyRequestPosture(message)) {
  const intent = posture.intent || FALLBACK_INTENT;
  const nextAction = posture.restricted ? 'Route to a governed admin task definition, authority check, scope limit, and receipt path before any execution can occur.' : `Offer governed transition: ${intent.transition} -> ${intent.destination}.`;
  return [`Route: ${route}`, `Transition intent: ${intent.label} (${intent.id})`, `Suggested transition: ${intent.transition}`, `Transition destination: ${intent.destination}`, `Transition boundary: ${intent.boundary}`, `Task status: ${posture.task_status}`, `Interaction bands: ${formatInteractionProfile(posture.interaction_profile)}`, 'Authority: none; browser-local classification only.', 'Shell: disabled; raw commands are not executed.', 'Credentials: not accepted; do not paste secrets or tokens.', 'Math solver: preview-supported; live checked solving requires governed backend integration.', `Status: ${status}`, 'Boundary: Site may draft, classify, and display; Site must not issue proof receipts, perform governed commits, or expose administrative execution.', `Next action: ${nextAction}`, '', 'Request preserved:', message].join('\n');
}

function buildManifest() {
  const userRequest = getFieldValue('userRequest').trim();
  const posture = classifyRequestPosture(userRequest);
  return { target_entry_point: getFieldValue('targetEntryPoint'), input_mode: getFieldValue('inputMode'), requested_route: getFieldValue('requestedRoute'), detected_route: posture.route, transition_intent: posture.intent.id, transition_label: posture.intent.label, transition_destination: posture.intent.destination, transition_boundary: posture.intent.boundary, task_status: posture.task_status, raw_shell_allowed: false, authority_required: true, rate_limit_required: true, receipt_required_for_execution: true, restricted_admin_review_required: posture.restricted, interaction_profile: posture.interaction_profile, interaction_bands: INTERACTION_BANDS.map((band) => band.key), math_solver_supported: true, user_request: userRequest, declared_goal: getFieldValue('declaredGoal').trim(), operator_note: getFieldValue('operatorNote').trim(), source_surface: 'StegVerse-Labs/Site/ecosystem-chat.html' };
}

function buildReceiptWindow(manifest) {
  const check = getSubmissionCheck(manifest);
  return { receipt_expectation: getFieldValue('receiptExpectation'), submission_posture: getFieldValue('submissionPosture'), site_receipt_authority: false, site_shell_authority: false, site_credential_authority: false, manifest_correct_at_submission: check.ok, submission_target: 'StegVerse-org/SDK', execution_allowed_from_site: false, authority_required_before_execution: true, receipt_required_for_execution: true, transition_intent: manifest.transition_intent, transition_destination: manifest.transition_destination, interaction_profile: manifest.interaction_profile, interaction_bands: manifest.interaction_bands, math_solver_supported: manifest.math_solver_supported, correctness_errors: check.errors };
}

function buildSdkPayload() { const manifest = buildManifest(); const receipt_window = buildReceiptWindow(manifest); return { fields: readSdkFields(), manifest, receipt_window }; }
function updateGeneratedWindows() { const manifest = buildManifest(); const receiptWindow = buildReceiptWindow(manifest); manifestPreview.textContent = JSON.stringify(manifest, null, 2); receiptPreview.textContent = JSON.stringify(receiptWindow, null, 2); if (interactionBandMeter) renderInteractionBands(manifest.interaction_profile); renderContinuationPanel(classifyTransitionIntent(manifest.user_request), manifest.detected_route); if (sdkStatus) { const check = getSubmissionCheck(manifest); sdkStatus.textContent = check.ok ? 'Generated JSON is locally complete. Final correctness, authority, rate limits, allowed-task status, transition intent, solver use, and interaction-band telemetry are determined at submission time.' : `Generated JSON is incomplete: ${check.errors.join('; ')}`; } }
function getSubmissionCheck(manifest = buildManifest()) { const errors = []; if (!manifest.user_request) errors.push('user_request is required'); if (!manifest.declared_goal) errors.push('declared_goal is required'); if (!manifest.transition_intent) errors.push('transition_intent is required'); if (!manifest.transition_destination) errors.push('transition_destination is required'); if (manifest.target_entry_point !== 'StegVerse-org/SDK') errors.push('target_entry_point must be StegVerse-org/SDK'); if (manifest.input_mode !== 'text_form') errors.push('input_mode must be text_form'); if (manifest.raw_shell_allowed !== false) errors.push('raw_shell_allowed must be false'); if (manifest.authority_required !== true) errors.push('authority_required must be true'); if (manifest.rate_limit_required !== true) errors.push('rate_limit_required must be true'); if (manifest.receipt_required_for_execution !== true) errors.push('receipt_required_for_execution must be true'); if (!Array.isArray(manifest.interaction_bands)) errors.push('interaction_bands must be present'); if (manifest.math_solver_supported !== true) errors.push('math_solver_supported must be true'); return { ok: errors.length === 0, errors }; }
function readSdkFields() { return { target_entry_point: getFieldValue('targetEntryPoint'), input_mode: getFieldValue('inputMode'), requested_route: getFieldValue('requestedRoute'), receipt_expectation: getFieldValue('receiptExpectation'), submission_posture: getFieldValue('submissionPosture'), user_request: getFieldValue('userRequest').trim(), declared_goal: getFieldValue('declaredGoal').trim(), operator_note: getFieldValue('operatorNote').trim() }; }
function getFieldValue(id) { const element = document.getElementById(id); return element ? element.value : ''; }

async function localReceipt(message, posture) {
  const payload = JSON.stringify({ route: posture.route, transition_intent: posture.intent.id, transition_destination: posture.intent.destination, message, mode: 'local-simulation', authority: 'none', shell: 'disabled', raw_shell_allowed: false, task_status: posture.task_status, receipt: 'not-issued', interaction_profile: posture.interaction_profile, interaction_bands: INTERACTION_BANDS.map((band) => band.key), math_solver_supported: true, issued_at: new Date().toISOString() });
  const data = new TextEncoder().encode(payload);
  const digest = await crypto.subtle.digest('SHA-256', data);
  const hash = Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, '0')).join('');
  return `local_receipt_hash=sha256:${hash} · authority=none · shell=disabled · task_status=${posture.task_status} · intent=${posture.intent.id} · receipt=not-issued · bands=${formatInteractionProfile(posture.interaction_profile)}`;
}

function appendMessage(label, body, type, receipt) {
  const wrapper = document.createElement('div'); wrapper.className = `chat-message ${type || ''}`.trim();
  const labelNode = document.createElement('div'); labelNode.className = 'label'; labelNode.textContent = label;
  const bodyNode = document.createElement('div'); bodyNode.className = 'body'; bodyNode.textContent = body;
  wrapper.appendChild(labelNode); wrapper.appendChild(bodyNode);
  if (receipt) { const receiptNode = document.createElement('div'); receiptNode.className = 'receipt-block'; receiptNode.textContent = receipt; wrapper.appendChild(receiptNode); }
  log.appendChild(wrapper); log.scrollTop = log.scrollHeight;
}

function getSessionId() { const key = 'stegverse_ecosystem_chat_session'; const existing = window.sessionStorage.getItem(key); if (existing) return existing; const generated = crypto.randomUUID ? crypto.randomUUID() : `session-${Date.now()}`; window.sessionStorage.setItem(key, generated); return generated; }
