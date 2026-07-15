(() => {
  'use strict';

  const form = document.getElementById('chatForm');
  const input = document.getElementById('messageInput');
  const log = document.getElementById('chatLog');
  const continuationSummary = document.getElementById('continuationSummary');
  const continuationGrid = document.getElementById('continuationGrid');
  if (!form || !input || !log) return;

  const CONVERSATIONAL_PATTERNS = [
    /^(?:hi|hello|hey|hiya|howdy)[.!?\s]*$/i,
    /^good\s+(?:morning|afternoon|evening)[.!?\s]*$/i,
    /^(?:greetings|welcome)[.!?\s]*$/i,
    /^(?:thanks|thank\s+you|much\s+appreciated)[.!?\s]*$/i,
    /^(?:goodbye|bye|see\s+you|talk\s+later)[.!?\s]*$/i,
    /^(?:how\s+are\s+you|who\s+are\s+you|what\s+can\s+you\s+do)[.!?\s]*$/i
  ];

  function isConversationalOnly(message) {
    const normalized = String(message || '').trim();
    return normalized.length > 0 && normalized.length <= 80 && CONVERSATIONAL_PATTERNS.some((pattern) => pattern.test(normalized));
  }

  function responseFor(message) {
    const normalized = message.trim().toLowerCase();
    if (/^good\s+morning/.test(normalized)) return 'Good morning! How can I help you explore or work with the StegVerse ecosystem today?';
    if (/^good\s+afternoon/.test(normalized)) return 'Good afternoon! How can I help you explore or work with the StegVerse ecosystem today?';
    if (/^good\s+evening/.test(normalized)) return 'Good evening! How can I help you explore or work with the StegVerse ecosystem today?';
    if (/^(thanks|thank\s+you|much\s+appreciated)/.test(normalized)) return 'You’re welcome. What would you like to work on next?';
    if (/^(goodbye|bye|see\s+you|talk\s+later)/.test(normalized)) return 'Goodbye. Your local preview session remains non-authorizing and no execution was requested.';
    if (/^how\s+are\s+you/.test(normalized)) return 'I’m ready to help. You can ask a general question or request a governed ecosystem task.';
    if (/^who\s+are\s+you/.test(normalized)) return 'I’m the StegVerse Ecosystem Chat preview. I can respond conversationally and classify governed ecosystem requests without granting execution authority.';
    if (/^what\s+can\s+you\s+do/.test(normalized)) return 'You can ask a general question, summarize Site state, classify a transition, inspect a handoff, or preview a solver request. Execution and proof authority remain disabled here.';
    return 'Hello! How can I help you explore or work with the StegVerse ecosystem today?';
  }

  function appendMessage(label, body, type, statusLine) {
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
    if (statusLine) {
      const statusNode = document.createElement('div');
      statusNode.className = 'receipt-block';
      statusNode.textContent = statusLine;
      wrapper.appendChild(statusNode);
    }
    log.appendChild(wrapper);
    log.scrollTop = log.scrollHeight;
  }

  function renderConversationContinuation() {
    if (!continuationSummary || !continuationGrid) return;
    continuationSummary.textContent = 'Conversation acknowledged · no transition or execution requested.';
    continuationGrid.innerHTML = '';
    const card = document.createElement('div');
    card.className = 'continuation-item';
    const title = document.createElement('strong');
    title.textContent = 'Ask an ecosystem question';
    const summary = document.createElement('span');
    summary.textContent = 'Continue naturally, or request classification, research, a solver preview, or a governed handoff.';
    const link = document.createElement('a');
    link.className = 'sv-btn sv-btn-secondary';
    link.href = '#console';
    link.textContent = 'Continue chatting';
    card.appendChild(title);
    card.appendChild(summary);
    card.appendChild(link);
    continuationGrid.appendChild(card);
  }

  form.addEventListener('submit', (event) => {
    const message = input.value.trim();
    if (!isConversationalOnly(message)) return;

    event.preventDefault();
    event.stopImmediatePropagation();
    appendMessage('User', message, 'user');
    appendMessage(
      'StegVerse Ecosystem Chat',
      responseFor(message),
      'system',
      'mode=local-simulation · authority=none · execution=not-requested · receipt=not-issued'
    );
    input.value = '';
    renderConversationContinuation();
  }, true);
})();
