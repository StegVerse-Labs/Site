const PRIMARY = Object.freeze({
  version: 'v1.1',
  protocolVersion: 'HIL-PROTOCOL-v1.1',
  promptVersion: 'HIL-PROMPT-v1.1',
  primarySha256: 'a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462',
  promptSha256: 'cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c'
});

const MAX_BYTES = 10 * 1024 * 1024;

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

async function ensureSchema(env) {
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

function readiness() {
  return json({
    schema_version: 'HIL-RECEIVER-READINESS-v1',
    state: 'READY',
    primary_version: PRIMARY.version,
    primary_sha256: PRIMARY.primarySha256,
    protocol_version: PRIMARY.protocolVersion,
    prompt_version: PRIMARY.promptVersion,
    prompt_sha256: PRIMARY.promptSha256,
    provenance_manifest_required: true,
    provenance_manifest_schema: 'HIL-RESPONSE-PROVENANCE-v1.1',
    participant_metadata_required: false,
    maximum_response_bytes: MAX_BYTES,
    custody_backend: 'cloudflare-r2',
    registry_backend: 'cloudflare-d1'
  });
}

async function findExisting(env, responseHash) {
  return env.HIL_REGISTRY.prepare(
    'SELECT receipt_json FROM hil_submissions WHERE response_sha256 = ?1 LIMIT 1'
  ).bind(responseHash).first();
}

async function acceptSubmission(request, env) {
  await ensureSchema(env);

  const contentType = request.headers.get('content-type') || '';
  if (!contentType.toLowerCase().startsWith('multipart/form-data')) {
    return json({ detail: 'multipart_form_data_required' }, 415);
  }

  const form = await request.formData();
  const pdf = form.get('response_pdf');
  const provenancePart = form.get('provenance_manifest');

  if (!(pdf instanceof File) || !(provenancePart instanceof File)) {
    return json({ detail: 'response_pdf_and_provenance_manifest_required' }, 400);
  }
  if (pdf.size === 0 || pdf.size > MAX_BYTES) {
    return json({ detail: 'response_pdf_size_invalid' }, 413);
  }
  if (!pdf.name.toLowerCase().endsWith('.pdf')) {
    return json({ detail: 'response_pdf_extension_invalid' }, 400);
  }

  const pdfBuffer = await pdf.arrayBuffer();
  const signature = new TextDecoder('ascii').decode(new Uint8Array(pdfBuffer).slice(0, 5));
  if (signature !== '%PDF-') return json({ detail: 'response_pdf_signature_invalid' }, 400);

  const responseHash = await sha256Hex(pdfBuffer);
  let provenance;
  try {
    provenance = JSON.parse(await provenancePart.text());
  } catch {
    return json({ detail: 'provenance_manifest_invalid_json' }, 400);
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
    return json({ detail: 'primary_prompt_response_chain_invalid' }, 422);
  }

  const existing = await findExisting(env, responseHash);
  if (existing?.receipt_json) return json(JSON.parse(existing.receipt_json), 200);

  const submissionId = id('HIL-SUBMISSION');
  const receiptId = id('HIL-RECEIPT');
  const createdAt = new Date().toISOString();
  const objectKey = `hil/v1.1/${createdAt.slice(0, 10)}/${submissionId}/response.pdf`;

  await env.HIL_SUBMISSIONS.put(objectKey, pdfBuffer, {
    httpMetadata: { contentType: 'application/pdf' },
    customMetadata: {
      submission_id: submissionId,
      response_sha256: responseHash,
      primary_sha256: PRIMARY.primarySha256,
      prompt_sha256: PRIMARY.promptSha256
    }
  });

  const unsignedReceipt = {
    schema_version: 'HIL-RECEIVER-RECEIPT-v2',
    receipt_id: receiptId,
    submission_id: submissionId,
    received_at: createdAt,
    submitted_file_sha256: responseHash,
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
      responseHash,
      objectKey,
      pdf.name,
      pdf.type || 'application/pdf',
      pdf.size,
      String(form.get('participant_identifier') || 'not_provided'),
      String(form.get('publication_consent') || 'not_provided'),
      provenance.model || null,
      provenance.provider || null,
      JSON.stringify(provenance),
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
      if (request.method === 'GET' && url.pathname === '/api/hil/readiness') return readiness();
      if (request.method === 'POST' && url.pathname === '/api/hil/submissions') return acceptSubmission(request, env);
      if (request.method === 'GET' && /^\/api\/hil\/submissions\/[^/]+$/.test(url.pathname)) {
        return submissionStatus(url, env);
      }
      if (url.pathname.startsWith('/api/hil/')) return json({ detail: 'not_found' }, 404);
      return env.ASSETS.fetch(request);
    } catch (error) {
      console.error('HIL receiver failure', error);
      return json({ detail: 'receiver_internal_error' }, 500);
    }
  }
};
