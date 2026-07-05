/* StegVerse AI Entry browser adapter.
 * Mirrors api/ecosystem_chat_backend.py without live provider calls.
 */
(function () {
  'use strict';

  var PROVIDERS = ['ChatGPT', 'Claude', 'Other LLM'];
  var ROUTES = [
    { id: 'restricted_admin', label: 'Restricted administration', authority_required: true, execution_allowed: false, purpose: 'Reject or require separate authority for restricted administrative actions.', words: ['secret', 'token', 'credential', 'shell', 'delete', 'release', 'permission', 'workflow', 'repo write'] },
    { id: 'llm_comparison', label: 'LLM comparison', authority_required: false, execution_allowed: false, purpose: 'Show StegVerse response first and external LLM comparison panes below.', words: ['compare', 'comparison', 'chatgpt', 'claude', 'gemini', 'grok', 'other llm'] },
    { id: 'sdk_access_guidance', label: 'SDK access guidance', authority_required: false, execution_allowed: false, purpose: 'Explain SDK access, onboarding, manifests, receipts, permissions, and next steps.', words: ['sdk', 'api', 'access', 'onboard', 'permission', 'manifest', 'receipt'] },
    { id: 'sdk_intake_candidate', label: 'SDK intake candidate', authority_required: true, execution_allowed: false, purpose: 'Prepare an SDK intake candidate or manifest preview without execution authority.', words: ['submit', 'intake', 'candidate', 'packet', 'request access', 'integration'] },
    { id: 'governance_review', label: 'Governance review', authority_required: false, execution_allowed: false, purpose: 'Classify authority, admissibility, evidence, receipt, and reconstruction posture.', words: ['governance', 'admissibility', 'authority', 'evidence', 'reconstruction', 'replay', 'transition'] },
    { id: 'runtime_status', label: 'Runtime status', authority_required: false, execution_allowed: false, purpose: 'Explain runtime, adapter, micro-node, and capability status.', words: ['runtime', 'adapter', 'micro-node', 'micro node', 'capability', 'goal'] },
    { id: 'documentation_route', label: 'Documentation route', authority_required: false, execution_allowed: false, purpose: 'Route users to public docs, wiki pages, proofs, papers, runbooks, and specifications.', words: ['docs', 'documentation', 'wiki', 'paper', 'spec', 'runbook', 'proof'] },
    { id: 'ecosystem_explanation', label: 'Ecosystem explanation', authority_required: false, execution_allowed: false, purpose: 'Explain StegVerse ecosystem concepts, components, roles, and status.', words: ['ecosystem', 'stegverse', 'concept', 'component', 'role', 'status'] }
  ];

  function classifyRoute(message) {
    var lower = String(message || '').toLowerCase();
    for (var i = 0; i < ROUTES.length; i += 1) {
      for (var j = 0; j < ROUTES[i].words.length; j += 1) {
        if (lower.indexOf(ROUTES[i].words[j]) !== -1) return ROUTES[i];
      }
    }
    return { id: 'chat_answer', label: 'StegVerse answer', authority_required: false, execution_allowed: false, purpose: 'Answer normal user questions as a StegVerse governed response candidate.', words: [] };
  }

  function responseId(message, routeId) {
    var base = routeId + ':' + String(message || '').length + ':' + String(message || '').slice(0, 24);
    var hash = 0;
    for (var i = 0; i < base.length; i += 1) {
      hash = ((hash << 5) - hash) + base.charCodeAt(i);
      hash |= 0;
    }
    return 'preview-' + routeId + '-' + Math.abs(hash).toString(16);
  }

  function comparisonOutputs(text) {
    return PROVIDERS.map(function (provider) {
      return { provider: provider, authority: false, response: text };
    });
  }

  function buildResponse(message) {
    var clean = String(message || '').trim();
    if (!clean) {
      return {
        response_id: 'welcome',
        primary_route: 'chat_answer',
        stegverse_response: 'Welcome to StegVerse AI.\n\nI can help answer questions, explain StegVerse concepts, route ecosystem requests, describe SDK access, compare external LLM responses, and prepare governed transition candidates with clear authority and receipt boundaries.\n\nHow can I help you today?',
        route_guidance: 'Enter a request to classify the route.',
        sdk_guidance: 'SDK and access guidance appears when relevant.',
        comparison_outputs: comparisonOutputs('Comparison output will appear here when external provider adapters are activated.'),
        governance: { governed_candidate: false, authority_issued: false, receipt_id: null, reconstruction_available: false }
      };
    }

    var route = classifyRoute(clean);
    var sdkGuidance = route.id.indexOf('sdk') === 0
      ? 'SDK route selected: explain SDK entry points, permissions, manifests, receipts, and next steps. Do not expose credentials or imply access has been granted.'
      : 'No SDK-specific route was selected. Ask about SDK access, API onboarding, manifests, or intake packets to open this path.';

    return {
      response_id: responseId(clean, route.id),
      primary_route: route.id,
      stegverse_response: 'StegVerse treats this as one entry-point request.\n\nSelected route: ' + route.label + ' (' + route.id + ').\n\nA live backend would preserve the original request, apply governed route handling, check authority requirements, and return bounded output with receipt/reconstruction metadata when available.',
      route_guidance: 'Route preview: ' + route.label + '.\n\n' + route.purpose + '\n\nauthority_required=' + route.authority_required + ' · execution_allowed=' + route.execution_allowed,
      sdk_guidance: sdkGuidance,
      comparison_outputs: comparisonOutputs('Comparison placeholder pending provider adapter activation.'),
      governance: { governed_candidate: true, authority_issued: false, receipt_id: null, reconstruction_available: false }
    };
  }

  window.StegVerseAIEntryAdapter = { classifyRoute: classifyRoute, buildResponse: buildResponse };
}());
