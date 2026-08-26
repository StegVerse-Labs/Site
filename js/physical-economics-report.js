(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.PhysicalEconomicsReport = api;
})(typeof window !== "undefined" ? window : globalThis, function () {
  "use strict";

  const PERTINENCE_MATRIX_VERSION = "physical-economics-report-pertinence.v0.1";
  const ACCEPTED_BACKEND_STATE = "GENERATED_NOT_PUBLICLY_ACTIVATED";
  const VERIFIED_STATE = "VERIFIABLE";
  const CLAIM_CLASSES = Object.freeze([
    "PRICE_CHANGE",
    "PHYSICAL_PURCHASING_POWER",
    "ESSENTIAL_AFFORDABILITY",
    "UNMET_ESSENTIAL_NEED",
    "SUBSTITUTION_OR_QUALITY_COMPRESSION",
    "PRODUCER_COST_PRESSURE",
    "PRODUCER_MARGIN_STATE",
    "COST_MARGIN_TRANSMISSION",
    "DISTRIBUTIONAL_BURDEN",
    "REGIONAL_BURDEN",
    "HOUSEHOLD_RESILIENCE",
    "ARREARS_DEFERRED_OBLIGATION",
    "CAPACITY_INVENTORY_CONSTRAINT",
    "TAX_FEE_REGULATORY_FLOW",
    "TRANSFER_OFFSET_EFFECT",
    "ECONOMIC_CONDITION_STATE_VECTOR"
  ]);

  const FINDING_CLASSES = new Set([
    "OBSERVED",
    "RECONSTRUCTED",
    "COMPARATOR_ONLY",
    "PROXY",
    "PARTIAL",
    "UNRESOLVED",
    "NOT_COMPARABLE"
  ]);

  function fail(code, message, details) {
    const error = new Error(message);
    error.code = code;
    if (details !== undefined) error.details = details;
    throw error;
  }

  function asTrimmed(value) {
    return typeof value === "string" ? value.trim() : "";
  }

  function requiredText(value, field) {
    const result = asTrimmed(value);
    if (!result) fail("INVALID_REQUEST", `${field} is required`);
    return result;
  }

  function optionalText(value) {
    const result = asTrimmed(value);
    return result || null;
  }

  function dedupe(values) {
    return Array.from(new Set(values));
  }

  function safeDate(value, field) {
    if (!value) return null;
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) fail("INVALID_REQUEST", `${field} must be YYYY-MM-DD`);
    return value;
  }

  function safeDateTime(value, field) {
    const text = requiredText(value, field);
    if (Number.isNaN(Date.parse(text))) fail("INVALID_REQUEST", `${field} must be an ISO date-time`);
    return new Date(text).toISOString();
  }

  function makeRequestId(now, randomSource) {
    const stamp = now.toISOString().replace(/[-:.TZ]/g, "").slice(0, 14);
    const raw = Math.floor((randomSource ? randomSource() : Math.random()) * 0xffffffff)
      .toString(16)
      .padStart(8, "0");
    return `PE-RPT-${stamp}-${raw}`;
  }

  function normalizeClaimClasses(values) {
    const selected = dedupe((values || []).map(asTrimmed).filter(Boolean));
    if (!selected.length) fail("INVALID_REQUEST", "At least one claim class is required");
    const invalid = selected.filter((item) => !CLAIM_CLASSES.includes(item));
    if (invalid.length) fail("INVALID_REQUEST", `Unsupported claim class: ${invalid.join(", ")}`);
    return selected;
  }

  function buildRequest(input, options) {
    const now = options && options.now ? new Date(options.now) : new Date();
    const randomSource = options && options.randomSource;
    const claimClasses = normalizeClaimClasses(input.claim_classes);
    const requestedAsOf = input.requested_as_of_time
      ? safeDateTime(input.requested_as_of_time, "requested_as_of_time")
      : now.toISOString();

    const startDate = safeDate(input.requested_start_date, "requested_start_date");
    const endDate = safeDate(input.requested_end_date, "requested_end_date");
    if (startDate && endDate && startDate > endDate) {
      fail("INVALID_REQUEST", "requested_start_date cannot be after requested_end_date");
    }

    const essentialClass = asTrimmed(input.essential_or_discretionary_class) || "UNRESOLVED";
    if (!["ESSENTIAL", "DISCRETIONARY", "MIXED", "UNRESOLVED"].includes(essentialClass)) {
      fail("INVALID_REQUEST", "Invalid essential_or_discretionary_class");
    }

    const request = {
      report_request_id: asTrimmed(input.report_request_id) || makeRequestId(now, randomSource),
      question: requiredText(input.question, "question"),
      requested_as_of_time: requestedAsOf,
      scope: {
        subject: requiredText(input.subject, "subject"),
        economic_domain: requiredText(input.economic_domain, "economic_domain"),
        geography: requiredText(input.geography, "geography"),
        population_scope: requiredText(input.population_scope, "population_scope"),
        essential_or_discretionary_class: essentialClass,
        unit_definition: optionalText(input.unit_definition),
        requested_start_date: startDate,
        requested_end_date: endDate
      },
      claim_classes: claimClasses,
      pertinence_policy: {
        mode: "DETERMINISTIC_CLAIM_CLASS_MAPPING",
        required_attribute_sets_version: PERTINENCE_MATRIX_VERSION,
        allow_optional_context_attributes: Boolean(input.allow_optional_context_attributes),
        user_requested_attributes: dedupe((input.user_requested_attributes || []).map(asTrimmed).filter(Boolean)),
        excluded_attributes: []
      },
      vintage_policy: asTrimmed(input.vintage_policy) || "CURRENT_VINTAGE",
      output_preferences: {
        include_state_vector: input.include_state_vector !== false,
        include_data_coverage_matrix: input.include_data_coverage_matrix !== false,
        include_prospective_evidence_gates: input.include_prospective_evidence_gates !== false,
        include_source_receipts: input.include_source_receipts !== false,
        include_uncertainty_surface: input.include_uncertainty_surface !== false
      }
    };

    if (![
      "CURRENT_VINTAGE",
      "AS_KNOWN_AT_REQUESTED_TIME",
      "BOTH_CURRENT_AND_HISTORICAL_VINTAGE"
    ].includes(request.vintage_policy)) {
      fail("INVALID_REQUEST", "Invalid vintage_policy");
    }

    return request;
  }

  function isObject(value) {
    return Boolean(value) && typeof value === "object" && !Array.isArray(value);
  }

  function requireObject(value, field) {
    if (!isObject(value)) fail("INVALID_RESPONSE", `${field} must be an object`);
    return value;
  }

  function requireArray(value, field) {
    if (!Array.isArray(value)) fail("INVALID_RESPONSE", `${field} must be an array`);
    return value;
  }

  function validateReportDocument(document) {
    requireObject(document, "report_document");
    requiredText(document.report_id, "report_document.report_id");
    requiredText(document.question, "report_document.question");
    requireArray(document.claim_classes, "report_document.claim_classes");
    requireObject(document.scope, "report_document.scope");
    const boundary = requireObject(document.boundary, "report_document.boundary");
    requiredText(boundary.completeness_state, "report_document.boundary.completeness_state");
    requiredText(boundary.statement, "report_document.boundary.statement");
    requireArray(document.coverage_matrix, "report_document.coverage_matrix");
    requireArray(document.uncertainty_surface, "report_document.uncertainty_surface");
    const findings = requireArray(document.findings, "report_document.findings");
    requireArray(document.opaque_elements, "report_document.opaque_elements");
    requireArray(document.prospective_evidence_gates, "report_document.prospective_evidence_gates");
    requireObject(document.receipts, "report_document.receipts");
    requiredText(document.renderer_version, "report_document.renderer_version");

    findings.forEach((finding, index) => {
      requireObject(finding, `report_document.findings[${index}]`);
      if (!FINDING_CLASSES.has(finding.finding_class)) {
        fail("INVALID_RESPONSE", `Unrecognized finding posture: ${finding.finding_class}`);
      }
      requiredText(finding.statement, `report_document.findings[${index}].statement`);
      requiredText(finding.claim_class, `report_document.findings[${index}].claim_class`);
      requireArray(finding.source_receipt_ids, `report_document.findings[${index}].source_receipt_ids`);
    });

    return document;
  }

  function validateVerificationReceipt(receipt, reportId) {
    requireObject(receipt, "verification_receipt");
    requiredText(receipt.verification_receipt_id, "verification_receipt.verification_receipt_id");
    if (receipt.report_id !== reportId) fail("INVALID_RESPONSE", "Verification receipt report_id mismatch");
    if (receipt.verification_state !== VERIFIED_STATE) {
      fail("UNVERIFIED_REPORT", `Verification state is ${receipt.verification_state || "missing"}`);
    }
    [
      "report_request_hash",
      "evidence_snapshot_id",
      "evidence_snapshot_hash",
      "boundary_manifest_id",
      "boundary_manifest_hash",
      "pertinence_matrix_version",
      "contract_version",
      "renderer_version",
      "report_content_hash"
    ].forEach((field) => requiredText(receipt[field], `verification_receipt.${field}`));
    requireArray(receipt.source_receipt_ids, "verification_receipt.source_receipt_ids");
    return receipt;
  }

  function validateBackendResponse(payload) {
    requireObject(payload, "response");
    if (payload.state !== ACCEPTED_BACKEND_STATE) {
      fail("BACKEND_STATE_NOT_ADMISSIBLE", `Backend state is ${payload.state || "missing"}`);
    }
    const document = validateReportDocument(payload.report_document);
    const receipt = validateVerificationReceipt(payload.verification_receipt, document.report_id);
    if (receipt.renderer_version !== document.renderer_version) {
      fail("INVALID_RESPONSE", "Renderer version mismatch between report and verification receipt");
    }
    return {
      state: payload.state,
      report_document: document,
      verification_receipt: receipt,
      report_markdown: typeof payload.report_markdown === "string" ? payload.report_markdown : null
    };
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function renderCoverageRow(row) {
    return `<tr><td><code>${escapeHtml(row.attribute_id)}</code></td><td>${row.required ? "Required" : "Context"}</td><td>${escapeHtml(row.earliest_admissible_date || "—")}</td><td>${escapeHtml(row.latest_observed_date || "—")}</td><td>${escapeHtml(row.latest_complete_date || "—")}</td><td>${escapeHtml(row.current_period_state || "—")}</td><td>${escapeHtml(row.comparability || "—")}</td><td>${escapeHtml(row.missingness_posture || "—")}</td></tr>`;
  }

  function renderFinding(finding) {
    const receipts = (finding.source_receipt_ids || []).map((item) => `<code>${escapeHtml(item)}</code>`).join(", ") || "None";
    const notes = [finding.uncertainty_note, finding.boundary_note].filter(Boolean).map((item) => `<p class="finding-note">${escapeHtml(item)}</p>`).join("");
    return `<article class="finding finding-${escapeHtml(finding.finding_class.toLowerCase())}"><div class="finding-head"><span class="posture">${escapeHtml(finding.finding_class)}</span><span>${escapeHtml(finding.claim_class)}</span></div><p>${escapeHtml(finding.statement)}</p><div class="receipt-line">Evidence receipts: ${receipts}</div>${notes}</article>`;
  }

  function renderUncertainty(item) {
    const posture = item.uncertainty_posture == null
      ? "No source-native uncertainty object supplied"
      : typeof item.uncertainty_posture === "string"
        ? item.uncertainty_posture
        : JSON.stringify(item.uncertainty_posture);
    return `<li><code>${escapeHtml(item.attribute_id)}</code> — ${escapeHtml(posture)}${item.aggregate_propagation_state ? ` · aggregate: ${escapeHtml(item.aggregate_propagation_state)}` : ""}</li>`;
  }

  function renderReportToHtml(response) {
    const validated = validateBackendResponse(response);
    const document = validated.report_document;
    const receipt = validated.verification_receipt;
    const findings = document.findings.length
      ? document.findings.map(renderFinding).join("")
      : `<div class="empty-state">No governed findings were supplied for this report. The UI will not invent any.</div>`;
    const opaque = document.opaque_elements.length
      ? `<ul>${document.opaque_elements.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`
      : `<p class="muted">No opaque elements were declared.</p>`;
    const gates = document.prospective_evidence_gates.length
      ? `<ul>${document.prospective_evidence_gates.map((gate) => `<li><code>${escapeHtml(gate.gate_id)}</code> · ${escapeHtml(gate.attribute_or_source)} · <strong>${escapeHtml(gate.state)}</strong>${gate.expected_or_known_date ? ` · ${escapeHtml(gate.expected_or_known_date)}` : ""}${gate.notes ? ` — ${escapeHtml(gate.notes)}` : ""}</li>`).join("")}</ul>`
      : `<p class="muted">No prospective evidence gates were declared.</p>`;

    return `<section id="report-boundary" class="card boundary-card"><div class="eyebrow">Evidence-derived boundary</div><h2>Report boundary</h2><div class="status-pill">${escapeHtml(document.boundary.completeness_state)}</div><p class="boundary-statement">${escapeHtml(document.boundary.statement)}</p><dl class="boundary-dates"><div><dt>Earliest common comparable</dt><dd>${escapeHtml(document.boundary.earliest_common_comparable_date || "Not established")}</dd></div><div><dt>Latest common complete</dt><dd>${escapeHtml(document.boundary.latest_common_complete_date || "Not established")}</dd></div></dl></section>
<section class="card"><div class="eyebrow">Coverage</div><h2>Data coverage matrix</h2><div class="table-wrap"><table><thead><tr><th>Attribute</th><th>Role</th><th>Earliest</th><th>Latest observed</th><th>Latest complete</th><th>Current state</th><th>Comparability</th><th>Missingness</th></tr></thead><tbody>${document.coverage_matrix.map(renderCoverageRow).join("")}</tbody></table></div></section>
<section class="card"><div class="eyebrow">Uncertainty</div><h2>Uncertainty and quality</h2>${document.uncertainty_surface.length ? `<ul>${document.uncertainty_surface.map(renderUncertainty).join("")}</ul>` : `<p class="muted">No uncertainty objects were supplied.</p>`}</section>
<section id="report-findings" class="card"><div class="eyebrow">Governed findings</div><h2>Findings</h2>${findings}</section>
<section class="grid two"><div class="card"><div class="eyebrow">Unresolved</div><h2>Opaque elements</h2>${opaque}</div><div class="card"><div class="eyebrow">Prospective</div><h2>Evidence gates</h2>${gates}</div></section>
<section class="card verification-card"><div class="eyebrow">Portable verification</div><h2>Verification receipt</h2><div class="status-pill verified">${escapeHtml(receipt.verification_state)}</div><dl class="receipt-grid"><div><dt>Report</dt><dd><code>${escapeHtml(document.report_id)}</code></dd></div><div><dt>Receipt</dt><dd><code>${escapeHtml(receipt.verification_receipt_id)}</code></dd></div><div><dt>Snapshot</dt><dd><code>${escapeHtml(receipt.evidence_snapshot_id)}</code></dd></div><div><dt>Snapshot hash</dt><dd><code>${escapeHtml(receipt.evidence_snapshot_hash)}</code></dd></div><div><dt>Boundary</dt><dd><code>${escapeHtml(receipt.boundary_manifest_id)}</code></dd></div><div><dt>Boundary hash</dt><dd><code>${escapeHtml(receipt.boundary_manifest_hash)}</code></dd></div><div><dt>Report content hash</dt><dd><code>${escapeHtml(receipt.report_content_hash)}</code></dd></div><div><dt>Renderer</dt><dd><code>${escapeHtml(receipt.renderer_version)}</code></dd></div></dl></section>`;
  }

  function resolveEndpoint(documentRef, explicitEndpoint) {
    if (explicitEndpoint) return asTrimmed(explicitEndpoint);
    if (!documentRef) return "";
    const meta = documentRef.querySelector('meta[name="physical-economics-report-endpoint"]');
    return meta ? asTrimmed(meta.getAttribute("content")) : "";
  }

  async function submitReportRequest(request, options) {
    const opts = options || {};
    const fetchImpl = opts.fetchImpl || (typeof fetch === "function" ? fetch.bind(globalThis) : null);
    const endpoint = asTrimmed(opts.endpoint);
    if (!endpoint) fail("BACKEND_NOT_CONFIGURED", "Physical Economics report backend is not configured");
    if (!fetchImpl) fail("BACKEND_UNAVAILABLE", "No fetch implementation is available");

    let response;
    try {
      response = await fetchImpl(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(request),
        credentials: "omit",
        cache: "no-store",
        redirect: "error"
      });
    } catch (error) {
      fail("BACKEND_UNAVAILABLE", "Physical Economics report backend could not be reached", error && error.message);
    }

    if (!response || !response.ok) {
      fail("BACKEND_REJECTED", `Physical Economics report backend returned HTTP ${response ? response.status : "unknown"}`);
    }

    let payload;
    try {
      payload = await response.json();
    } catch (error) {
      fail("INVALID_RESPONSE", "Physical Economics report backend did not return valid JSON");
    }
    return validateBackendResponse(payload);
  }

  function formToInput(form) {
    const data = new FormData(form);
    return {
      question: data.get("question"),
      subject: data.get("subject"),
      economic_domain: data.get("economic_domain"),
      geography: data.get("geography"),
      population_scope: data.get("population_scope"),
      essential_or_discretionary_class: data.get("essential_or_discretionary_class"),
      unit_definition: data.get("unit_definition"),
      requested_start_date: data.get("requested_start_date"),
      requested_end_date: data.get("requested_end_date"),
      requested_as_of_time: data.get("requested_as_of_time"),
      vintage_policy: data.get("vintage_policy"),
      claim_classes: data.getAll("claim_classes"),
      allow_optional_context_attributes: data.get("allow_optional_context_attributes") === "on",
      include_state_vector: data.get("include_state_vector") === "on",
      include_data_coverage_matrix: data.get("include_data_coverage_matrix") === "on",
      include_prospective_evidence_gates: data.get("include_prospective_evidence_gates") === "on",
      include_source_receipts: data.get("include_source_receipts") === "on",
      include_uncertainty_surface: data.get("include_uncertainty_surface") === "on"
    };
  }

  function installBrowserUi(documentRef, options) {
    if (!documentRef) return;
    const form = documentRef.getElementById("physical-economics-report-form");
    const result = documentRef.getElementById("physical-economics-report-result");
    const status = documentRef.getElementById("physical-economics-report-status");
    const requestPreview = documentRef.getElementById("physical-economics-request-preview");
    if (!form || !result || !status) return;

    const endpoint = resolveEndpoint(documentRef, options && options.endpoint);
    const endpointState = documentRef.getElementById("physical-economics-backend-state");
    if (endpointState) {
      endpointState.textContent = endpoint
        ? "Configured report backend detected. Verification is still required per response."
        : "Report backend is not configured on this published surface. Requests fail closed until activation evidence exists.";
      endpointState.dataset.state = endpoint ? "configured" : "fail-closed";
    }

    form.addEventListener("submit", async function (event) {
      event.preventDefault();
      result.innerHTML = "";
      status.textContent = "Building bounded request…";
      status.dataset.state = "working";
      try {
        const request = buildRequest(formToInput(form));
        if (requestPreview) requestPreview.textContent = JSON.stringify(request, null, 2);
        status.textContent = "Submitting to governed report backend…";
        const validated = await submitReportRequest(request, { endpoint });
        result.innerHTML = renderReportToHtml(validated);
        status.textContent = "Report generated and portable verification returned VERIFIABLE. Public release authority is not inferred.";
        status.dataset.state = "verified";
      } catch (error) {
        const code = error && error.code ? error.code : "FAIL_CLOSED";
        status.textContent = `${code}: ${error && error.message ? error.message : "Report generation failed closed"}`;
        status.dataset.state = "fail-closed";
        result.innerHTML = `<section class="card fail-card"><div class="eyebrow">Fail closed</div><h2>Report not generated</h2><p>${escapeHtml(status.textContent)}</p><p class="muted">No findings, boundaries, or verification state are inferred from a failed or unavailable backend.</p></section>`;
      }
    });
  }

  return Object.freeze({
    PERTINENCE_MATRIX_VERSION,
    CLAIM_CLASSES,
    ACCEPTED_BACKEND_STATE,
    VERIFIED_STATE,
    buildRequest,
    validateBackendResponse,
    renderReportToHtml,
    submitReportRequest,
    resolveEndpoint,
    installBrowserUi,
    escapeHtml
  });
});
