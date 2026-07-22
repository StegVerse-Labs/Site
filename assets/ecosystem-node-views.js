(() => {
  'use strict';

  const EVENT_TYPES = new Set(['message', 'decision', 'execution', 'receipt', 'policy', 'evidence']);
  const stream = [];
  const eventIndex = new Map();
  let activeEventId = null;
  let rawMode = false;

  const chatShell = document.querySelector('#console + .chat-shell');
  const chatPanel = chatShell && chatShell.querySelector('.chat-panel');
  const continuationPanel = chatShell && chatShell.querySelector('.continuation-panel');
  const chatLog = document.getElementById('chatLog');

  if (!chatShell || !chatPanel || !chatLog) return;

  chatShell.classList.add('ecosystem-node-shell');
  chatShell.innerHTML = '';

  const controls = document.createElement('div');
  controls.className = 'node-view-controls';
  controls.innerHTML = `
    <div class="node-view-tabs" role="tablist" aria-label="Ecosystem Node view">
      <button type="button" class="node-view-tab active" data-node-view="conversation" role="tab" aria-selected="true">Conversation</button>
      <button type="button" class="node-view-tab" data-node-view="governed" role="tab" aria-selected="false">Governed record</button>
      <button type="button" class="node-view-tab" data-node-view="split" role="tab" aria-selected="false">Split</button>
    </div>
    <div class="node-view-actions">
      <button type="button" class="sv-btn sv-btn-secondary" id="nodeFormatToggle">Raw JSONL</button>
      <button type="button" class="sv-btn sv-btn-secondary" id="nodeExportJson">Export JSON</button>
      <button type="button" class="sv-btn sv-btn-secondary" id="nodeExportJsonl">Export JSONL</button>
    </div>`;

  const workspace = document.createElement('div');
  workspace.className = 'node-view-workspace conversation';
  workspace.innerHTML = `
    <section class="node-pane conversation-pane" aria-label="Conversation projection"></section>
    <section class="node-pane governed-pane" aria-label="Governed record projection">
      <div class="governed-record-head">
        <div><strong>Canonical governed event stream</strong><span>Formatted inspection and raw output resolve to the same in-memory records.</span></div>
        <span class="node-authority-badge">projection only · authority unchanged</span>
      </div>
      <div id="governedRecordList" class="governed-record-list" aria-live="polite"></div>
      <pre id="governedRecordRaw" class="governed-record-raw" hidden></pre>
    </section>`;

  chatShell.append(controls, workspace);
  workspace.querySelector('.conversation-pane').append(chatPanel);
  if (continuationPanel) workspace.querySelector('.conversation-pane').append(continuationPanel);

  const recordList = document.getElementById('governedRecordList');
  const rawRecord = document.getElementById('governedRecordRaw');

  document.querySelectorAll('[data-node-view]').forEach((button) => {
    button.addEventListener('click', () => setView(button.dataset.nodeView));
  });
  document.getElementById('nodeFormatToggle').addEventListener('click', toggleRecordFormat);
  document.getElementById('nodeExportJson').addEventListener('click', () => exportRecords('json'));
  document.getElementById('nodeExportJsonl').addEventListener('click', () => exportRecords('jsonl'));

  hydrateExistingMessages();

  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => mutation.addedNodes.forEach((node) => {
      if (node.nodeType !== Node.ELEMENT_NODE) return;
      if (node.matches('.chat-message')) ingestMessageElement(node);
      node.querySelectorAll?.('.chat-message').forEach(ingestMessageElement);
    }));
  });
  observer.observe(chatLog, { childList: true, subtree: true });

  function setView(mode) {
    if (!['conversation', 'governed', 'split'].includes(mode)) return;
    workspace.className = `node-view-workspace ${mode}`;
    document.querySelectorAll('[data-node-view]').forEach((button) => {
      const selected = button.dataset.nodeView === mode;
      button.classList.toggle('active', selected);
      button.setAttribute('aria-selected', String(selected));
    });
  }

  function hydrateExistingMessages() {
    chatLog.querySelectorAll('.chat-message').forEach(ingestMessageElement);
  }

  function ingestMessageElement(element) {
    if (element.dataset.eventId) return;
    const label = element.querySelector('.label')?.textContent.trim() || 'Conversation event';
    const body = element.querySelector('.body')?.textContent.trim() || '';
    const receiptLine = element.querySelector('.receipt-block')?.textContent.trim() || '';
    const isUser = element.classList.contains('user');
    const parentEvent = [...stream].reverse().find((event) => event.event_type === 'message');

    const event = createCanonicalEvent({
      parent_event_id: parentEvent?.event_id || null,
      actor: {
        actor_type: isUser ? 'human' : 'agent',
        display_name: label,
        identity_ref: isUser ? 'identity:local-user' : 'identity:stegverse-preview-agent'
      },
      event_type: 'message',
      human_projection: {
        label,
        body,
        visible_in_conversation: true
      },
      governed_projection: {
        classification: isUser ? 'user_input' : 'governed_preview_output',
        local_simulation: true,
        authority: 'none',
        shell_allowed: false,
        receipt_status: receiptLine || 'not-issued'
      },
      policy_refs: ['policy:site-preview-boundary'],
      evidence_refs: [],
      artifact_refs: [],
      continuity_refs: parentEvent ? [parentEvent.event_id] : []
    });

    element.dataset.eventId = event.event_id;
    element.tabIndex = 0;
    element.setAttribute('aria-label', `${label}; correlated event ${event.event_id}`);
    element.addEventListener('click', () => selectEvent(event.event_id, 'conversation'));
    element.addEventListener('focus', () => selectEvent(event.event_id, 'conversation'));
    appendCanonicalEvent(event);

    if (!isUser) {
      appendCanonicalEvent(createCanonicalEvent({
        parent_event_id: event.event_id,
        actor: { actor_type: 'system', display_name: 'Site classifier', identity_ref: 'identity:site-local-classifier' },
        event_type: 'decision',
        human_projection: { summary: receiptLine || 'Local preview classification completed.', visible_in_conversation: false },
        governed_projection: {
          decision: 'PREVIEW_ONLY',
          admissibility: 'NOT_EVALUATED',
          execution_requested: false,
          execution_result: 'NOT_ATTEMPTED',
          confidence: null,
          uncertainty: 'No live provider or authority-issued receipt is represented.'
        },
        policy_refs: ['policy:site-preview-boundary'],
        evidence_refs: [event.event_id],
        artifact_refs: [],
        continuity_refs: [event.event_id]
      }));
    }
  }

  function createCanonicalEvent(partial) {
    const eventId = crypto.randomUUID ? crypto.randomUUID() : fallbackUuid();
    const timestamp = new Date().toISOString();
    const event = {
      event_id: eventId,
      parent_event_id: partial.parent_event_id ?? null,
      timestamp,
      actor: partial.actor || {},
      event_type: EVENT_TYPES.has(partial.event_type) ? partial.event_type : 'evidence',
      human_projection: partial.human_projection || {},
      governed_projection: partial.governed_projection || {},
      policy_refs: partial.policy_refs || [],
      evidence_refs: partial.evidence_refs || [],
      artifact_refs: partial.artifact_refs || [],
      continuity_refs: partial.continuity_refs || [],
      hash: ''
    };
    event.hash = canonicalDigest(event);
    return deepFreeze(event);
  }

  function appendCanonicalEvent(event) {
    if (eventIndex.has(event.event_id)) return;
    stream.push(event);
    eventIndex.set(event.event_id, event);
    renderGovernedRecords();
  }

  function renderGovernedRecords() {
    recordList.innerHTML = '';
    stream.forEach((event) => {
      const article = document.createElement('article');
      article.className = 'governed-event';
      article.dataset.eventId = event.event_id;
      article.tabIndex = 0;
      article.innerHTML = `
        <div class="governed-event-title">
          <strong>${escapeHtml(event.event_type)}</strong>
          <span>${escapeHtml(event.timestamp)}</span>
        </div>
        <dl>
          <div><dt>event_id</dt><dd>${escapeHtml(event.event_id)}</dd></div>
          <div><dt>parent</dt><dd>${escapeHtml(event.parent_event_id || 'null')}</dd></div>
          <div><dt>actor</dt><dd>${escapeHtml(event.actor.display_name || event.actor.actor_type || 'unknown')}</dd></div>
          <div><dt>hash</dt><dd>${escapeHtml(event.hash)}</dd></div>
        </dl>
        <pre>${escapeHtml(JSON.stringify(event.governed_projection, null, 2))}</pre>`;
      article.addEventListener('click', () => selectEvent(event.event_id, 'governed'));
      article.addEventListener('focus', () => selectEvent(event.event_id, 'governed'));
      recordList.append(article);
    });
    rawRecord.textContent = stream.map((event) => JSON.stringify(event)).join('\n');
    if (activeEventId) applySelection(activeEventId);
  }

  function selectEvent(eventId, source) {
    activeEventId = eventId;
    applySelection(eventId);
    if (source === 'governed') {
      const conversationNode = chatLog.querySelector(`[data-event-id="${cssEscape(eventId)}"]`);
      conversationNode?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    } else {
      const recordNode = recordList.querySelector(`[data-event-id="${cssEscape(eventId)}"]`);
      recordNode?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  function applySelection(eventId) {
    document.querySelectorAll('[data-event-id].correlated-active').forEach((node) => node.classList.remove('correlated-active'));
    document.querySelectorAll(`[data-event-id="${cssEscape(eventId)}"]`).forEach((node) => node.classList.add('correlated-active'));
    const direct = eventIndex.get(eventId);
    if (!direct) return;
    stream.filter((event) => event.parent_event_id === eventId || event.evidence_refs.includes(eventId))
      .forEach((event) => recordList.querySelector(`[data-event-id="${cssEscape(event.event_id)}"]`)?.classList.add('correlated-active'));
    if (direct.parent_event_id) {
      document.querySelectorAll(`[data-event-id="${cssEscape(direct.parent_event_id)}"]`).forEach((node) => node.classList.add('correlated-active'));
    }
  }

  function toggleRecordFormat() {
    rawMode = !rawMode;
    recordList.hidden = rawMode;
    rawRecord.hidden = !rawMode;
    document.getElementById('nodeFormatToggle').textContent = rawMode ? 'Formatted records' : 'Raw JSONL';
  }

  function exportRecords(format) {
    const content = format === 'jsonl'
      ? stream.map((event) => JSON.stringify(event)).join('\n') + '\n'
      : JSON.stringify({ schema: 'stegverse.canonical-event-stream.v0.1', events: stream }, null, 2);
    const blob = new Blob([content], { type: format === 'jsonl' ? 'application/x-ndjson' : 'application/json' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = `stegverse-governed-events.${format}`;
    anchor.click();
    URL.revokeObjectURL(url);
  }

  function canonicalDigest(event) {
    const source = JSON.stringify({ ...event, hash: '' });
    let hash = 2166136261;
    for (let i = 0; i < source.length; i += 1) {
      hash ^= source.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }
    return `fnv1a32:${(hash >>> 0).toString(16).padStart(8, '0')}`;
  }

  function fallbackUuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (character) => {
      const random = Math.random() * 16 | 0;
      const value = character === 'x' ? random : (random & 0x3 | 0x8);
      return value.toString(16);
    });
  }

  function deepFreeze(value) {
    Object.values(value).forEach((child) => {
      if (child && typeof child === 'object' && !Object.isFrozen(child)) deepFreeze(child);
    });
    return Object.freeze(value);
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[character]));
  }

  function cssEscape(value) {
    return window.CSS?.escape ? CSS.escape(value) : value.replace(/["\\]/g, '\\$&');
  }

  window.StegVerseCanonicalEventStream = Object.freeze({
    version: '0.1',
    getEvents: () => stream.slice(),
    getEvent: (eventId) => eventIndex.get(eventId) || null,
    selectEvent
  });
})();