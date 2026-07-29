const PRIMARY = Object.freeze({
  version: 'v1.1',
  protocolVersion: 'HIL-PROTOCOL-v1.1',
  promptVersion: 'HIL-PROMPT-v1.1',
  primarySha256: 'a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462',
  promptSha256: 'cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c'
});

const MAX_BYTES = 10 * 1024 * 1024;
const OBSERVABILITY_SCHEMA = 'HIL-TRANSITION-OBSERVABILITY-v1';

function json(body, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store',
      ...extraHeaders
    }
  });
}

function canonicalJson(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(',')}}`;
}

async function sha256Hex(value) {
  const bytes = value instanceof ArrayBuffer
    ? value
    : new TextEncoder().encode(value).buffer;
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
}

function id(prefix) {
  return `${prefix}-${crypto.randomUUID()}`;
}

function bindingPresence(env) {
  return {
    assets: Boolean(env.ASSETS),
    registry: Boolean(env.HIL_REGISTRY),
    custody: Boolean(env.HIL_SUBMISSIONS)
  };
}

async function probeBindings(env) {
  const present = bindingPresence(env);
  const probes = {
    deployment: { state: 'PASS', detail: 'worker_executing' },
    routing: { state: 'PASS', detail: 'hil_api_route_reached' },
    protocol: { state: 'PASS', detail: 'primary_and_prompt_loaded' },
    assets_binding: {
      state: present.assets ? 'PASS' : 'UNAVAILABLE',
      detail: present.assets ? 'binding_present' : 'binding_missing'
    },
    registry_binding: {
      state: present.registry ? 'PRESENT' : 'UNAVAILABLE',
      detail: present.registry ? 'binding_present_probe_pending' : 'binding_missing'
    },
    custody_binding: {
      state: present.custody ? 'PRESENT' : 'UNAVAILABLE',
      detail: present.custody ? 'binding_present_probe_pending' : 'binding_missing'
    }
  };

  if (present.registry) {
    try {
      await env.HIL_REGISTRY.prepare('SELECT 1 AS probe').first();
      probes.registry_binding = { state: 'PASS', detail: 'd1_query_succeeded' };
    } catch (error) {
      probes.registry_binding = { state: 'FAIL', detail: String(error?.message || error) };
    }
  }

  if (present.custody) {
    try {
      await env.HIL_SUBMISSIONS.list({ limit: 1 });
      probes.custody_binding = { state: 'PASS', detail: 'r2_list_succeeded' };
    } catch (error) {
      probes.custody_binding = { state: 'FAIL', detail: String(error?.message || error) };
    }
  }

  const fullReceiverReady =
    probes.registry_binding.state === 'PASS' &&
    probes.custody_binding.state === 'PASS';

  return {
    schema_version: OBSERVABILITY_SCHEMA,
    observed_at: new Date().toISOString(),
    receiver_mode: fullReceiverReady ? 'FULL_CUSTODY' : 'DIAGNOSTIC',
    full_receiver_ready: fullReceiverReady,
    probes,
    supported_operations: {
      readiness: true,
      transition_probes: true,
      noncustodial_validation: true,
      durable_submission: fullReceiverReady,
      submission_status: probes.registry_binding.state === 'PASS'
    },
    continuation_paths: fullReceiverReady
      ? ['durable_cloudflare_submission']
      : ['noncustodial_validation', 'attach_existing_d1', 'activate_or_replace_r2', 'github_backed_custody']
  };
}

async function readiness(env) {
  const observations = await probeBindings(env);
  return json({
    schema_version: 'HIL-RECEIVER-READINESS-v2',
    state: observations.full_receiver_ready ? 'READY' : 'DEGRADED',
    receiver_mode: observations.receiver_mode,
    primary_version: PRIMARY.version,
    primary_sha256: PRIMARY.primarySha256,
    protocol_version: PRIMARY.protocolVersion,
    prompt_version: PRIMARY.promptVersion,
    prompt_sha256: PRIMARY.promptSha256,
    provenance_manifest_required: true,
    provenance_manifest_schema: 'HIL-RESPONSE-PROVENANCE-v1.1',
    participant_metadata_required: false,
    maximum_response_bytes: MAX_BYTES,
    custody_backend: observations.probes.custody_binding.state === 'PASS' ? 'cloudflare-r2' : 'unavailable',
    registry_backend: observations.probes.registry_binding.state === 'PASS' ? 'cloudflare-d1' : 'unavailable',
    observations
  }, observations.full_receiver_ready ? 200 : 207);
}

async function ensureSchema(env) {
  if (!env.HIL_REGISTRY) throw new Error('HIL_REGISTRY binding unavailable');
  await env.HIL_REGISTRY.prepare(`
    CREATE TABLE IF NOT EXISTS hil_submissions (
      submission_id TEXT PRIMARY KEY,
      receipt_id TEXT NOT NULL,
      response_sha256 TEXT NOT NULL UNIQUE,
      object_key TEXT NOT NULL,
      original_filename TEXT NOT NULL,
      content_type TEXT NOT NULL,
      size_bytes INTEGER NOT NULL,
      participant_identifier TEXT,
      publication_consent TEXT,
      model TEXT,
      provider TEXT,
      provenance_json TEXT NOT NULL,
      receipt_json TEXT NOT NULL,
      state TEXT NOT NULL,
      created_at TEXT NOT NULL
    )
  `).run();
}

async function parseAndValidateSubmission(request) {
  const contentType = request.headers.get('content-type') || '';
  if (!contentType.toLowerCase().startsWith('multipart/form-data')) {
    return { error: json({ detail: 'multipart_form_data_required' }, 415) };
  }

  const form = await request.formData();
  const pdf = form.get('response_pdf');
  const provenancePart = form.get('provenance_manifest');

  if (!(pdf instanceof File) || !(provenancePart instanceof File)) {
    return { error: json({ detail: 'response_pdf_and_provenance_manifest_required' }, 400) };
  }
  if (pdf.size === 0 || pdf.size > MAX_BYTES) {
    return { error: json({ detail: 'response_pdf_size_invalid' }, 413) };
  }
  if (!pdf.name.toLowerCase().endsWith('.pdf')) {
    return { error: json({ detail: 'response_pdf_extension_invalid' }, 400) };
  }

  const pdfBuffer = await pdf.arrayBuffer();
  const signature = new TextDecoder('ascii').decode(new Uint8Array(pdfBuffer).slice(0, 5));
  if (signature !== '%PDF-') return { error: json({ detail: 'response_pdf_signature_invalid' }, 400) };

  const responseHash = await sha256Hex(pdfBuffer);
  let provenance;
  try {
    provenance = JSON.parse(await provenancePart.text());
  } catch {
    return { error: json({ detail: 'provenance_manifest_invalid_json' }, 400) };
  }

  const declaredPrimary = String(form.get('primary_sha256') || '');
  const declaredPrompt = String(form.get('prompt_sha256') || '');
  if (
    provenance.schema_version !== 'HIL-RESPONSE-PROVENANCE-v1.1' ||
    provenance.primary_sha256 !== PRIMARY.primarySha256 ||
    provenance.prompt_sha256 !== PRIMARY.promptSha256 ||
    provenance.response_sha256 !== responseHash ||
    declaredPrimary !== PRIMARY.primarySha256 ||
    declaredPrompt !== PRIMARY.promptSha256
  ) {
    return { error: json({ detail: 'primary_prompt_response_chain_invalid' }, 422) };
  }

  return { form, pdf, pdfBuffer, responseHash, provenance };
}

async function validateSubmission(request, env) {
  const parsed = await parseAndValidateSubmission(request);
  if (parsed.error) return parsed.error;

  const observedAt = new Date().toISOString();
  const unsignedReceipt = {
    schema_version: 'HIL-DIAGNOSTIC-VALIDATION-RECEIPT-v1',
    validation_id: id('HIL-VALIDATION'),
    validated_at: observedAt,
    submitted_file_sha256: parsed.responseHash,
    primary_sha256: PRIMARY.primarySha256,
    prompt_sha256: PRIMARY.promptSha256,
    chain_validation_state: 'PRIMARY_PROMPT_RESPONSE_CHAIN_VERIFIED',
    custody_state: 'NOT_PERSISTED_DIAGNOSTIC',
    registry_state: 'NOT_RECORDED_DIAGNOSTIC',
    review_state: 'NOT_STARTED',
    publication_state: 'NOT_AUTHORIZED',
    diagnostic_only: true
  };

  return json({
    ...unsignedReceipt,
    receipt_sha256: await sha256Hex(canonicalJson(unsignedReceipt)),
    observations: await probeBindings(env)
  }, 200);
}

async function findExisting(env, responseHash) {
  return env.HIL_REGISTRY.prepare(
    'SELECT receipt_json FROM hil_submissions WHERE response_sha256 = ?1 LIMIT 1'
  ).bind(responseHash).first();
}

async function acceptSubmission(request, env) {
  const observations = await probeBindings(env);
  if (!observations.full_receiver_ready) {
    return json({
      detail: 'durable_receiver_unavailable',
      diagnostic_endpoint: '/api/hil/submissions/validate',
      observations
    }, 503);
  }

  await ensureSchema(env);
  const parsed = await parseAndValidateSubmission(request);
  if (parsed.error) return parsed.error;

  const existing = await findExisting(env, parsed.responseHash);
  if (existing?.receipt_json) return json(JSON.parse(existing.receipt_json), 200);

  const submissionId = id('HIL-SUBMISSION');
  const receiptId = id('HIL-RECEIPT');
  const createdAt = new Date().toISOString();
  const objectKey = `hil/v1.1/${createdAt.slice(0, 10)}/${submissionId}/response.pdf`;

  await env.HIL_SUBMISSIONS.put(objectKey, parsed.pdfBuffer, {
    httpMetadata: { contentType: 'application/pdf' },
    customMetadata: {
      submission_id: submissionId,
      response_sha256: parsed.responseHash,
      primary_sha256: PRIMARY.primarySha256,
      prompt_sha256: PRIMARY.promptSha256
    }
  });

  const unsignedReceipt = {
    schema_version: 'HIL-RECEIVER-RECEIPT-v2',
    receipt_id: receiptId,
    submission_id: submissionId,
    received_at: createdAt,
    submitted_file_sha256: parsed.responseHash,
    primary_sha256: PRIMARY.primarySha256,
    prompt_sha256: PRIMARY.promptSha256,
    chain_validation_state: 'PRIMARY_PROMPT_RESPONSE_CHAIN_VERIFIED',
    custody_state: 'RECEIVED_R2',
    registry_state: 'RECORDED_D1',
    review_state: 'PENDING',
    publication_state: 'NOT_AUTHORIZED',
    object_reference: objectKey
  };
  const receipt = {
    ...unsignedReceipt,
    receipt_sha256: await sha256Hex(canonicalJson(unsignedReceipt))
  };

  try {
    await env.HIL_REGISTRY.prepare(`
      INSERT INTO hil_submissions (
        submission_id, receipt_id, response_sha256, object_key,
        original_filename, content_type, size_bytes,
        participant_identifier, publication_consent, model, provider,
        provenance_json, receipt_json, state, created_at
      ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15)
    `).bind(
      submissionId,
      receiptId,
      parsed.responseHash,
      objectKey,
      parsed.pdf.name,
      parsed.pdf.type || 'application/pdf',
      parsed.pdf.size,
      String(parsed.form.get('participant_identifier') || 'not_provided'),
      String(parsed.form.get('publication_consent') || 'not_provided'),
      parsed.provenance.model || null,
      parsed.provenance.provider || null,
      JSON.stringify(parsed.provenance),
      JSON.stringify(receipt),
      'ACCEPTED',
      createdAt
    ).run();
  } catch (error) {
    await env.HIL_SUBMISSIONS.delete(objectKey);
    throw error;
  }

  return json(receipt, 201);
}

async function submissionStatus(url, env) {
  if (!env.HIL_REGISTRY) {
    return json({ detail: 'registry_unavailable', observations: await probeBindings(env) }, 503);
  }
  await ensureSchema(env);
  const submissionId = decodeURIComponent(url.pathname.split('/').pop() || '');
  const record = await env.HIL_REGISTRY.prepare(`
    SELECT submission_id, response_sha256, state, created_at, receipt_json
    FROM hil_submissions WHERE submission_id = ?1 LIMIT 1
  `).bind(submissionId).first();
  if (!record) return json({ detail: 'submission_not_found' }, 404);
  return json({
    submission_id: record.submission_id,
    submitted_file_sha256: record.response_sha256,
    state: record.state,
    created_at: record.created_at,
    receipt: JSON.parse(record.receipt_json)
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    try {
      if (request.method === 'GET' && url.pathname === '/api/hil/readiness') return readiness(env);
      if (request.method === 'GET' && url.pathname === '/api/hil/probes') return json(await probeBindings(env));
      if (request.method === 'POST' && url.pathname === '/api/hil/submissions/validate') return validateSubmission(request, env);
      if (request.method === 'POST' && url.pathname === '/api/hil/submissions') return acceptSubmission(request, env);
      if (request.method === 'GET' && /^\/api\/hil\/submissions\/[^/]+$/.test(url.pathname)) {
        return submissionStatus(url, env);
      }
      if (url.pathname.startsWith('/api/hil/')) return json({ detail: 'not_found' }, 404);
      if (!env.ASSETS) return json({ detail: 'assets_binding_unavailable' }, 503);
      return env.ASSETS.fetch(request);
    } catch (error) {
      console.error('HIL receiver failure', error);
      return json({
        detail: 'receiver_internal_error',
        error_class: error?.name || 'Error',
        observations: await probeBindings(env)
      }, 500);
    }
  }
};