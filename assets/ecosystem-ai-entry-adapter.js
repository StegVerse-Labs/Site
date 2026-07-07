/* StegVerse AI Entry browser adapter.
 * Mirrors api/ecosystem_chat_backend.py without live provider calls.
 */
(function () {
  'use strict';

  var PROVIDERS = ['ChatGPT', 'Claude', 'Other LLM'];
  var ACTIVATION_STATUS = {
    current_mode: 'local_ready_live_disabled',
    readiness_state: 'not_ready_fail_closed',
    status_message: 'Governed-live activation is planned but not ready. Provider calls, SDK calls, credential access, real receipts, execution authority, and repo mutation remain disabled.',
    live_calls_enabled: false,
    live_provider_calls_enabled: false,
    live_sdk_calls_enabled: false,
    credential_surface_enabled: false,
    execution_authority_issued: false,
    real_receipt_issued: false,
    repo_mutation_from_chat_enabled: false
  };
  var ROUTE_PRIORITY = {
    restricted_admin: 100,
    activation_request_preview: 95,
    sdk_intake_candidate: 90,
    activation_boundary_review: 85,
    activation_guidance: 82,
    sdk_access_guidance: 80,
    runtime_status: 70,
    llm_comparison: 60,
    governance_review: 50,
    documentation_route: 40,
    ecosystem_explanation: 30,
    chat_answer: 10
  };
  var ROUTES = [
    { id: 'restricted_admin', label: 'Restricted administration', authority_required: true, execution_allowed: false, purpose: 'Reject or require separate authority for restricted administrative actions.', words: ['secret', 'token', 'credential', 'shell', 'delete', 'release', 'permission', 'workflow', 'repo write'] },
    { id: 'activation_request_preview', label: 'Activation request preview', authority_required: true, execution_allowed: false, purpose: 'Prepare a non-executing governed-live backend activation request preview. This does not enable providers, SDK calls, credentials, receipts, authority, or repo mutation.', words: ['request activation', 'activation request', 'enable backend', 'enable provider', 'go live'] },
    { id: 'activation_boundary_review', label: 'Activation boundary review', authority_required: false, execution_allowed: false, purpose: 'Review authority, receipt issuer, provider capture, SDK access, recoverability, and fail-closed execution boundaries before any activation.', words: ['activation boundary', 'receipt issuer', 'authority service', 'recoverability', 'fail closed'] },
    { id: 'activation_guidance', label: 'Activation guidance', authority_required: false, execution_allowed: false, purpose: 'Explain what must exist before governed-live activation can proceed while keeping the current UI local-ready and live-disabled.', words: ['activate', 'activation', 'live', 'provider', 'backend', 'adapter'] },
    { id: 'llm_comparison', label: 'LLM comparison', authority_required: false, execution_allowed: false, purpose: 'Show StegVerse response first and external LLM comparison panes below.', words: ['compare', 'comparison', 'chatgpt', 'claude', 'gemini', 'grok', 'other llm'] },
    { id: 'sdk_access_guidance', label: 'SDK access guidance', authority_required: false, execution_allowed: false, purpose: 'Explain SDK access, onboarding, manifests, receipts, permissions, and next steps.', words: ['sdk', 'api', 'access', 'onboard', 'permission', 'manifest', 'receipt'] },
    { id: 'sdk_intake_candidate', label: 'SDK intake candidate', authority_required: true, execution_allowed: false, purpose: 'Prepare an SDK intake candidate or manifest preview without execution authority.', words: ['submit', 'intake', 'candidate', 'packet', 'request access', 'integration'] },
    { id: 'governance_review', label: 'Governance review', authority_required: false, execution_allowed: false, purpose: 'Classify authority, admissibility, evidence, receipt, and reconstruction posture.', words: ['governance', 'admissibility', 'authority', 'evidence', 'reconstruction', 'replay', 'transition'] },
    { id: 'runtime_status', label: 'Runtime status', authority_required: false, execution_allowed: false, purpose: 'Explain runtime, adapter, micro-node, and capability status.', words: ['runtime', 'adapter', 'micro-node', 'micro node', 'capability', 'goal'] },
    { id: 'documentation_route', label: 'Documentation route', authority_required: false, execution_allowed: false, purpose: 'Route users to public docs, wiki pages, proofs, papers, runbooks, and specifications.', words: ['docs', 'documentation', 'wiki', 'paper', 'spec', 'runbook', 'proof'] },
    { id: 'ecosystem_explanation', label: 'Ecosystem explanation', authority_required: false, execution_allowed: false, purpose: 'Explain StegVerse ecosystem concepts, components, roles, and status.', words: ['ecosystem', 'stegverse', 'concept', 'component', 'role', 'status'] }
  ];

  function routeScore(route, lower) {
    var matches = 0;
    for (var i = 0; i < route.words.length; i += 1) {
      if (lower.indexOf(route.words[i]) !== -1) matches += 1;
    }
    return { matches: matches, priority: ROUTE_PRIORITY[route.id] || 0 };
  }

  function classifyRoute(message) {
    var lower = String(message || '').toLowerCase();
    var bestRoute = null;
    var bestScore = { matches: 0, priority: 0 };
    for (var i = 0; i < ROUTES.length; i += 1) {
      var score = routeScore(ROUTES[i], lower);
      if (score.matches > bestScore.matches || (score.matches === bestScore.matches && score.priority > bestScore.priority)) {
        bestRoute = ROUTES[i];
        bestScore = score;
      }
    }
    return bestRoute || { id: 'chat_answer', label: 'StegVerse answer', authority_required: false, execution_allowed: false, purpose: 'Answer normal user questions as a StegVerse governed response candidate.', words: [] };
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

  function inputHash(message) {
    var base = String(message || '');
    var hash = 0;
    for (var i = 0; i < base.length; i += 1) {
      hash = ((hash << 5) - hash) + base.charCodeAt(i);
      hash |= 0;
    }
    var hex = Math.abs(hash).toString(16);
    return (hex + '0000000000000000000000000000000000000000000000000000000000000000').slice(0, 64);
  }

  function comparisonOutputs(text) {
    return PROVIDERS.map(function (provider) {
      return { provider: provider, authority: false, response: text };
    });
  }

  function activationStatus() {
    return Object.assign({}, ACTIVATION_STATUS);
  }

  function adapterExtension(message, routeId, responseIdValue) {
    return {
      adapter_status: {
        provider_calls: false,
        provider_authority: false,
        test_secret_required: false,
        capture_required_before_activation: true
      },
      preview_marker: {
        preview_only: true,
        capture_enabled: false,
        record_saved: false,
        authority_granted: false,
        input_hash: inputHash(message),
        route_id: routeId,
        response_id: responseIdValue
      },
      endpoint_marker: {
        mode: 'pure_function_preview',
        started: false,
        calls_performed: false,
        side_effects: false
      },
      service_marker: {
        name: 'stegverse-ai-entry-interim-backend',
        wrapper_present: true,
        started_by_import: false,
        calls_enabled: false,
        side_effects_enabled: false
      }
    };
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
        governance: { governed_candidate: false, authority_issued: false, receipt_id: null, reconstruction_available: false },
        activation_status: activationStatus(),
        adapter_extension: adapterExtension('', 'chat_answer', 'welcome')
      };
    }

    var route = classifyRoute(clean);
    var rid = responseId(clean, route.id);
    var sdkGuidance = route.id.indexOf('sdk') === 0
      ? 'SDK route selected: explain SDK entry points, permissions, manifests, receipts, and next steps. Do not expose credentials or imply access has been granted.'
      : 'No SDK-specific route was selected. Ask about SDK access, API onboarding, manifests, or intake packets to open this path.';

    return {
      response_id: rid,
      primary_route: route.id,
      stegverse_response: 'StegVerse treats this as one entry-point request.\n\nSelected route: ' + route.label + ' (' + route.id + ').\n\nA live backend would preserve the original request, apply governed route handling, check authority requirements, and return bounded output with receipt/reconstruction metadata when available.',
      route_guidance: 'Route preview: ' + route.label + '.\n\n' + route.purpose + '\n\nauthority_required=' + route.authority_required + ' · execution_allowed=' + route.execution_allowed,
      sdk_guidance: sdkGuidance,
      comparison_outputs: comparisonOutputs('Comparison placeholder pending provider adapter activation.'),
      governance: { governed_candidate: true, authority_issued: false, receipt_id: null, reconstruction_available: false },
      activation_status: activationStatus(),
      adapter_extension: adapterExtension(clean, route.id, rid)
    };
  }

  window.StegVerseAIEntryAdapter = { classifyRoute: classifyRoute, buildResponse: buildResponse };
}());
