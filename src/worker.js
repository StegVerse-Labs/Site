const PRIMARY = Object.freeze({
  version: 'v1.1',
  protocolVersion: 'HIL-PROTOCOL-v1.1',
  promptVersion: 'HIL-PROMPT-v1.1',
  primarySha256: 'a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462',
  promptSha256: 'cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c'
});

const MAX_BYTES = 10 * 1024 * 1024;
const CHUNK_BYTES = 192 * 1024;
const OBSERVABILITY_SCHEMA = 'HIL-TRANSITION-OBSERVABILITY-v1';
const CUSTODY_BACKEND = 'portable-sqlite-chunks-v1';

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

function bytesToBase64(bytes) {
  let binary = '';
  const stride = 0x8000;
  for (let offset = 0; offset < bytes.length; offset += stride) {
    binary += String.fromCharCode(...bytes.subarray(offset, offset + stride));
  }
  return btoa(binary);
}

function base64ToBytes(value) {
  const binary = atob(value);
  const bytes = new Uint8Array(binary.length);
  for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index);
  return bytes;
}

function splitBuffer(buffer) {
  const bytes = new Uint8Array(buffer);
  const chunks = [];
  for (let offset = 0; offset < bytes.length; offset += CHUNK_BYTES) {
    chunks.push(bytesToBase64(bytes.subarray(offset, offset + CHUNK_BYTES)));
  }
  return chunks;
}

async function ensureSchema(env) {
  if (!env.HIL_REGISTRY) throw new Error('HIL_REGISTRY binding unavailable');

  await env.HIL_REGISTRY.batch([
    env.HIL_REGISTRY.prepare(`
      CREATE TABLE IF NOT EXISTS hil_submissions (
        submission_id TEXT PRIMARY KEY,
        receipt_id TEXT NOT NULL,
        response_sha256 TEXT NOT NULL UNIQUE,
        object_key TEXT NOT NULL,
        original_filename TEXT NOT NULL,
        content_type TEXT NOT NULL,
        size_bytes INTEGER NOT NULL,
        chunk_count INTEGER NOT NULL DEFAULT 0,
        custody_backend TEXT NOT NULL DEFAULT '${CUSTODY_BACKEND}',
        participant_identifier TEXT,
        publication_consent TEXT,
        model TEXT,
        provider TEXT,
        provenance_json TEXT NOT NULL,
        receipt_json TEXT NOT NULL,
        state TEXT NOT NULL,
        created_at TEXT NOT NULL
      )
    `),
    env.HIL_REGISTRY.prepare(`
      CREATE TABLE IF NOT EXISTS hil_submission_chunks (
        submission_id TEXT NOT NULL,
        chunk_index INTEGER NOT NULL,
        chunk_base64 TEXT NOT NULL,
        chunk_sha256 TEXT NOT NULL,
        size_bytes INTEGER NOT NULL,
        PRIMARY KEY (submission_id, chunk_index)
      )
    `),
    env.HIL_REGISTRY.prepare('CREATE INDEX IF NOT EXISTS idx_hil_chunks_submission ON hil_submission_chunks(submission_id, chunk_index)')
  ]);

  const columns = await env.HIL_REGISTRY.prepare('PRAGMA table_info(hil_submissions)').all();
  const names = new Set((columns.results || []).map((column) => column.name));
  if (!names.has('chunk_count')) {
    await env.HIL_REGISTRY.prepare('ALTER TABLE hil_submissions ADD COLUMN chunk_count INTEGER NOT NULL DEFAULT 0').run();
  }
  if (!names.has('custody_backend')) {
    await env.HIL_REGISTRY.prepare(`ALTER TABLE hil_submissions ADD COLUMN custody_backend TEXT NOT NULL DEFAULT '${CUSTODY_BACKEND}'`).run();
  }
}

async function probeBindings(env) {
  const probes = {
    deployment: { state: 'PASS', detail: 'worker_executing' },
    routing: { state: 'PASS', detail: 'hil_api_route_reached' },
    protocol: { state: 'PASS', detail: 'primary_and_prompt_loaded' },
    assets_binding: {
      state: env.ASSETS ? 'PASS' : 'UNAVAILABLE',
      detail: env.ASSETS ? 'binding_present' : 'binding_missing'
    },
    registry_binding: {
      state: env.HIL_REGISTRY ? 'PRESENT' : 'UNAVAILABLE',
      detail: env.HIL_REGISTRY ? 'binding_present_probe_pending' : 'binding_missing'
    },
    custody_backend: {
      state: env.HIL_REGISTRY ? 'PRESENT' : 'UNAVAILABLE',
      detail: env.HIL_REGISTRY ? 'portable_sqlite_chunk_store_probe_pending' : 'registry_binding_missing'
    }
  };

  if (env.HIL_REGISTRY) {
    try {
      await env.HIL_REGISTRY.prepare('SELECT 1 AS probe').first();
      await ensureSchema(env);
      await env.HIL_REGISTRY.prepare('SELECT COUNT(*) AS count FROM hil_submission_chunks').first();
      probes.registry_binding = { state: 'PASS', detail: 'd1_query_succeeded' };
      probes.custody_backend = { state: 'PASS', detail: 'portable_sqlite_chunk_store_ready' };
    } catch (error) {
      const detail = String(error?.message || error);
      probes.registry_binding = { state: 'FAIL', detail };
      probes.custody_backend = { state: 'FAIL', detail };
    }
  }

  const fullReceiverReady =
    probes.registry_binding.state === 'PASS' &&
    probes.custody_backend.state === 'PASS';

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
      exact_byte_retrieval: fullReceiverReady,
      submission_status: probes.registry_binding.state === 'PASS'
    },
    continuation_paths: fullReceiverReady
      ? ['portable_sqlite_chunk_submission']
      : ['noncustodial_validation', 'attach_or_repair_registry']
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
    custody_backend: observations.probes.custody_backend.state === 'PASS' ? CUSTODY_BACKEND : 'unavailable',
    registry_backend: observations.probes.registry_binding.state === 'PASS' ? 'sqlite-compatible-registry' : 'unavailable',
    observations
  }, observations.full_receiver_ready ? 200 : 207);
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

async function persistExactBytes(env, submissionId, pdfBuffer) {
  const chunks = splitBuffer(pdfBuffer);
  const statements = [];
  for (let index = 0; index < chunks.length; index += 1) {
    const chunkBytes = base64ToBytes(chunks[index]);
    statements.push(
      env.HIL_REGISTRY.prepare(`
        INSERT INTO hil_submission_chunks (
          submission_id, chunk_index, chunk_base64, chunk_sha256, size_bytes
        ) VALUES (?1, ?2, ?3, ?4, ?5)
      `).bind(
        submissionId,
        index,
        chunks[index],
        await sha256Hex(chunkBytes.buffer),
        chunkBytes.byteLength
      )
    );
  }
  if (statements.length) await env.HIL_REGISTRY.batch(statements);
  return chunks.length;
}

async function deleteSubmission(env, submissionId) {
  await env.HIL_REGISTRY.batch([
    env.HIL_REGISTRY.prepare('DELETE FROM hil_submission_chunks WHERE submission_id = ?1').bind(submissionId),
    env.HIL_REGISTRY.prepare('DELETE FROM hil_submissions WHERE submission_id = ?1').bind(submissionId)
  ]);
}

async function reconstructBytes(env, submissionId) {
  const result = await env.HIL_REGISTRY.prepare(`
    SELECT chunk_index, chunk_base64, chunk_sha256, size_bytes
    FROM hil_submission_chunks
    WHERE submission_id = ?1
    ORDER BY chunk_index ASC
  `).bind(submissionId).all();

  const rows = result.results || [];
  if (!rows.length) throw new Error('submission_chunks_missing');

  const chunks = [];
  let totalBytes = 0;
  for (const row of rows) {
    const bytes = base64ToBytes(row.chunk_base64);
    if (bytes.byteLength !== Number(row.size_bytes)) throw new Error('submission_chunk_size_mismatch');
    if (await sha256Hex(bytes.buffer) !== row.chunk_sha256) throw new Error('submission_chunk_hash_mismatch');
    chunks.push(bytes);
    totalBytes += bytes.byteLength;
  }

  const joined = new Uint8Array(totalBytes);
  let offset = 0;
  for (const chunk of chunks) {
    joined.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return joined;
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

  const unsignedReceipt = {
    schema_version: 'HIL-RECEIVER-RECEIPT-v2',
    receipt_id: receiptId,
    submission_id: submissionId,
    received_at: createdAt,
    submitted_file_sha256: parsed.responseHash,
    primary_sha256: PRIMARY.primarySha256,
    prompt_sha256: PRIMARY.promptSha256,
    chain_validation_state: 'PRIMARY_PROMPT_RESPONSE_CHAIN_VERIFIED',
    custody_state: 'EXACT_BYTES_PERSISTED',
    custody_backend: CUSTODY_BACKEND,
    registry_state: 'RECORDED',
    review_state: 'PENDING',
    publication_state: 'NOT_AUTHORIZED',
    object_reference: objectKey
  };
  const receipt = {
    ...unsignedReceipt,
    receipt_sha256: await sha256Hex(canonicalJson(unsignedReceipt))
  };

  try {
    const chunkCount = await persistExactBytes(env, submissionId, parsed.pdfBuffer);
    await env.HIL_REGISTRY.prepare(`
      INSERT INTO hil_submissions (
        submission_id, receipt_id, response_sha256, object_key,
        original_filename, content_type, size_bytes, chunk_count, custody_backend,
        participant_identifier, publication_consent, model, provider,
        provenance_json, receipt_json, state, created_at
      ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16, ?17)
    `).bind(
      submissionId,
      receiptId,
      parsed.responseHash,
      objectKey,
      parsed.pdf.name,
      parsed.pdf.type || 'application/pdf',
      parsed.pdf.size,
      chunkCount,
      CUSTODY_BACKEND,
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
    await deleteSubmission(env, submissionId);
    throw error;
  }

  const reconstructed = await reconstructBytes(env, submissionId);
  if (reconstructed.byteLength !== parsed.pdf.size || await sha256Hex(reconstructed.buffer) !== parsed.responseHash) {
    await deleteSubmission(env, submissionId);
    throw new Error('post_persistence_exact_byte_verification_failed');
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
    SELECT submission_id, response_sha256, size_bytes, chunk_count, custody_backend, state, created_at, receipt_json
    FROM hil_submissions WHERE submission_id = ?1 LIMIT 1
  `).bind(submissionId).first();
  if (!record) return json({ detail: 'submission_not_found' }, 404);
  return json({
    submission_id: record.submission_id,
    submitted_file_sha256: record.response_sha256,
    size_bytes: record.size_bytes,
    chunk_count: record.chunk_count,
    custody_backend: record.custody_backend,
    state: record.state,
    created_at: record.created_at,
    receipt: JSON.parse(record.receipt_json)
  });
}

async function submissionContent(url, env) {
  if (!env.HIL_REGISTRY) return json({ detail: 'registry_unavailable' }, 503);
  await ensureSchema(env);
  const parts = url.pathname.split('/');
  const submissionId = decodeURIComponent(parts[4] || '');
  const record = await env.HIL_REGISTRY.prepare(`
    SELECT original_filename, content_type, size_bytes, response_sha256
    FROM hil_submissions WHERE submission_id = ?1 LIMIT 1
  `).bind(submissionId).first();
  if (!record) return json({ detail: 'submission_not_found' }, 404);

  const bytes = await reconstructBytes(env, submissionId);
  const hash = await sha256Hex(bytes.buffer);
  if (bytes.byteLength !== Number(record.size_bytes) || hash !== record.response_sha256) {
    return json({ detail: 'custody_verification_failed' }, 500);
  }

  return new Response(bytes, {
    status: 200,
    headers: {
      'content-type': record.content_type || 'application/pdf',
      'content-length': String(bytes.byteLength),
      'content-disposition': `attachment; filename="${String(record.original_filename || 'response.pdf').replace(/["\r\n]/g, '_')}"`,
      'x-content-sha256': hash,
      'cache-control': 'no-store'
    }
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
      if (request.method === 'GET' && /^\/api\/hil\/submissions\/[^/]+\/content$/.test(url.pathname)) {
        return submissionContent(url, env);
      }
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