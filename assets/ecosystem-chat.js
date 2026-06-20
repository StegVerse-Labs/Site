const STEGVERSE_ROUTES = [
  { name: 'Site', terms: ['site', 'page', 'html', 'nav', 'navigation', 'mirror', 'public', 'readme', 'papers'] },
  { name: 'StegVerse-002', terms: ['sv002', 'stegverse-002', 'core-lite', 'intake', 'deployment', 'm10'] },
  { name: 'formalism-tests', terms: ['formalism', 'test', 'proof', 'admissibility', 'allow', 'deny', 'fail-closed', 'stage'] },
  { name: 'Continuity', terms: ['continuity', 'receipt', 'replay', 'hash', 'chain', 'state'] },
  { name: 'Publisher', terms: ['publisher', 'paper', 'manifest', 'publication', 'mirror-papers'] }
];

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

if (form && input && log) {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) return;

    appendMessage('User', message, 'user');
    input.value = '';

    const result = await routeEcosystemRequest(message);
    appendMessage('Console Route', result.response, 'system', result.receipt_line);
  });
}

if (sdkForm && manifestPreview && receiptPreview) {
  sdkForm.addEventListener('input', updateGeneratedWindows);
  sdkForm.addEventListener('change', updateGeneratedWindows);
  sdkForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const result = getSubmissionCheck();
    sdkStatus.textContent = result.ok
      ? 'Submission check passed locally. Payload is ready for a governed SDK entry point; Site still issues no proof receipt.'
      : `Submission check failed: ${result.errors.join('; ')}`;
  });

  if (useManifestButton) {
    useManifestButton.addEventListener('click', () => {
      if (!input) return;
      const payload = buildSdkPayload();
      input.value = JSON.stringify(payload, null, 2);
      input.focus();
    });
  }

  updateGeneratedWindows();
}

async function routeEcosystemRequest(message) {
  if (!STEGVERSE_LOCAL_MODE) {
    try {
      return await sendGatewayRequest(message);
    } catch (error) {
      return localRouteResult(message, 'Gateway request failed; fail-closed to local classification.');
    }
  }

  return localRouteResult(message, 'Local simulation mode; no external execution attempted.');
}

async function sendGatewayRequest(message) {
  const response = await fetch(STEGVERSE_GATEWAY_PATH, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      session_id: getSessionId(),
      repo: 'StegVerse-Labs/Site',
      goal: 'text-only ecosystem command console'
    })
  });

  if (!response.ok) {
    throw new Error(`Gateway returned ${response.status}`);
  }

  const data = await response.json();
  const receiptLine = data.receipt_id
    ? `receipt_id=${data.receipt_id}`
    : 'receipt=not-issued';

  return {
    response: data.response || buildLocalResponse(message, data.routed_module || 'Unknown', 'Gateway returned no response body.'),
    receipt_line: `${receiptLine} · routed_module=${data.routed_module || 'Unknown'} · source=gateway`
  };
}

async function localRouteResult(message, status) {
  const route = classifyRoute(message);
  const receiptLine = await localReceipt(message, route);

  return {
    response: buildLocalResponse(message, route, status),
    receipt_line: receiptLine
  };
}

function classifyRoute(message) {
  const text = message.toLowerCase();
  const scored = STEGVERSE_ROUTES.map((route) => ({
    name: route.name,
    score: route.terms.reduce((total, term) => total + (text.includes(term) ? 1 : 0), 0)
  })).sort((a, b) => b.score - a.score);

  return scored[0].score > 0 ? scored[0].name : 'Unknown';
}

function buildLocalResponse(message, route, status) {
  const nextAction = route === 'Unknown'
    ? 'Define a new ecosystem route or restate the request with repo/module context.'
    : `Send this request to the ${route} handler once the governed backend gateway is connected.`;

  return [
    `Route: ${route}`,
    'Authority: none; browser-local classification only.',
    `Status: ${status}`,
    'Boundary: Site may draft, classify, and display; Site must not issue proof receipts or perform governed commits.',
    `Next action: ${nextAction}`,
    '',
    'Request preserved:',
    message
  ].join('\n');
}

function buildManifest() {
  return {
    target_entry_point: getFieldValue('targetEntryPoint'),
    input_mode: getFieldValue('inputMode'),
    requested_route: getFieldValue('requestedRoute'),
    user_request: getFieldValue('userRequest').trim(),
    declared_goal: getFieldValue('declaredGoal').trim(),
    operator_note: getFieldValue('operatorNote').trim(),
    source_surface: 'StegVerse-Labs/Site/ecosystem-chat.html'
  };
}

function buildReceiptWindow(manifest) {
  const check = getSubmissionCheck(manifest);
  return {
    receipt_expectation: getFieldValue('receiptExpectation'),
    submission_posture: getFieldValue('submissionPosture'),
    site_receipt_authority: false,
    manifest_correct_at_submission: check.ok,
    submission_target: 'StegVerse-org/SDK',
    correctness_errors: check.errors
  };
}

function buildSdkPayload() {
  const manifest = buildManifest();
  const receipt_window = buildReceiptWindow(manifest);
  return {
    fields: readSdkFields(),
    manifest,
    receipt_window
  };
}

function updateGeneratedWindows() {
  const manifest = buildManifest();
  const receiptWindow = buildReceiptWindow(manifest);
  manifestPreview.textContent = JSON.stringify(manifest, null, 2);
  receiptPreview.textContent = JSON.stringify(receiptWindow, null, 2);

  if (sdkStatus) {
    const check = getSubmissionCheck(manifest);
    sdkStatus.textContent = check.ok
      ? 'Generated JSON is locally complete. Final correctness is determined at submission time.'
      : `Generated JSON is incomplete: ${check.errors.join('; ')}`;
  }
}

function getSubmissionCheck(manifest = buildManifest()) {
  const errors = [];
  if (!manifest.user_request) errors.push('user_request is required');
  if (!manifest.declared_goal) errors.push('declared_goal is required');
  if (manifest.target_entry_point !== 'StegVerse-org/SDK') errors.push('target_entry_point must be StegVerse-org/SDK');
  if (manifest.input_mode !== 'text_form') errors.push('input_mode must be text_form');

  return { ok: errors.length === 0, errors };
}

function readSdkFields() {
  return {
    target_entry_point: getFieldValue('targetEntryPoint'),
    input_mode: getFieldValue('inputMode'),
    requested_route: getFieldValue('requestedRoute'),
    receipt_expectation: getFieldValue('receiptExpectation'),
    submission_posture: getFieldValue('submissionPosture'),
    user_request: getFieldValue('userRequest').trim(),
    declared_goal: getFieldValue('declaredGoal').trim(),
    operator_note: getFieldValue('operatorNote').trim()
  };
}

function getFieldValue(id) {
  const element = document.getElementById(id);
  return element ? element.value : '';
}

async function localReceipt(message, route) {
  const payload = JSON.stringify({
    route,
    message,
    mode: 'local-simulation',
    authority: 'none',
    issued_at: new Date().toISOString()
  });
  const data = new TextEncoder().encode(payload);
  const digest = await crypto.subtle.digest('SHA-256', data);
  const hash = Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, '0')).join('');
  return `local_receipt_hash=sha256:${hash} · authority=none · receipt=not-issued`;
}

function appendMessage(label, body, type, receipt) {
  const wrapper = document.createElement('div');
  wrapper.className = `chat-message ${type || ''}`.trim();

  const labelNode = document.createElement('div');
  labelNode.className = 'label';
  labelNode.textContent = label;

  const bodyNode = document.createElement('div');
  bodyNode.className = 'body';
  bodyNode.textContent = body;

  wrapper.appendChild(labelNode);
  wrapper.appendChild(bodyNode);

  if (receipt) {
    const receiptNode = document.createElement('div');
    receiptNode.className = 'receipt-block';
    receiptNode.textContent = receipt;
    wrapper.appendChild(receiptNode);
  }

  log.appendChild(wrapper);
  log.scrollTop = log.scrollHeight;
}

function getSessionId() {
  const key = 'stegverse_ecosystem_chat_session';
  const existing = window.sessionStorage.getItem(key);
  if (existing) return existing;

  const generated = crypto.randomUUID ? crypto.randomUUID() : `session-${Date.now()}`;
  window.sessionStorage.setItem(key, generated);
  return generated;
}
