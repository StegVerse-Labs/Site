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
