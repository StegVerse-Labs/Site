(() => {
  'use strict';

  const byId = (id) => document.getElementById(id);
  const params = new URLSearchParams(window.location.search);
  const requestedId = params.get('id');

  function appendField(target, label, value) {
    const item = document.createElement('div');
    item.className = 'hil-detail-item';
    const heading = document.createElement('b');
    heading.textContent = label;
    const body = document.createElement('span');
    body.textContent = value == null || value === '' ? 'unknown' : String(value);
    item.append(heading, body);
    target.appendChild(item);
  }

  function line(label, value) {
    const row = document.createElement('div');
    row.textContent = `${label}: ${value == null || value === '' ? 'unknown' : value}`;
    return row;
  }

  function fail(message) {
    const state = byId('response-state');
    state.textContent = message;
    state.style.borderColor = '#512020';
    state.style.background = '#210d0d';
    state.style.color = '#f4b4b4';
  }

  async function load() {
    if (!requestedId) {
      fail('No response ID was supplied. Open this page from the published response index.');
      return;
    }

    try {
      const response = await fetch('data/hil-responses.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`response index unavailable (${response.status})`);
      const index = await response.json();
      if (!Array.isArray(index.responses)) throw new Error('response index has invalid shape');
      const record = index.responses.find((entry) => entry.response_id === requestedId);
      if (!record) {
        fail(`Response ${requestedId} is not present in the public index.`);
        return;
      }

      byId('response-title').textContent = record.response_id;
      byId('response-summary').textContent = `${record.model || 'Unknown model'} · ${record.provider || 'Unknown provider'} · ${record.publication_state || 'unknown state'}`;

      const metadata = byId('response-metadata');
      appendField(metadata, 'Participant', record.participant_display || 'anonymous');
      appendField(metadata, 'Model', record.model);
      appendField(metadata, 'Provider', record.provider);
      appendField(metadata, 'Primary version', record.primary_version);
      appendField(metadata, 'Prompt status', record.prompt_integrity);
      appendField(metadata, 'Received', record.received_at);
      appendField(metadata, 'Published', record.published_at);
      appendField(metadata, 'Publication state', record.publication_state);

      const pdf = byId('response-pdf');
      if (!record.artifact_path) {
        pdf.removeAttribute('href');
        pdf.setAttribute('aria-disabled', 'true');
        pdf.textContent = 'Response PDF unavailable';
      } else {
        pdf.href = record.artifact_path;
      }

      const chain = byId('response-chain');
      chain.append(
        line('primary_document_sha256', record.primary_sha256),
        line('receiver_verified_file_sha256', record.receiver_verified_file_sha256),
        line('receipt_sha256', record.receipt_sha256),
        line('previous_record_sha256', record.previous_record_sha256),
        line('master_record_release', record.master_record_release)
      );

      const state = byId('response-state');
      state.textContent = 'Public projection loaded from the machine-readable response index.';
      state.style.borderColor = 'var(--green-bd)';
      state.style.background = 'var(--green-bg)';
      state.style.color = '#bce9c5';
      byId('response-content').hidden = false;
    } catch (error) {
      fail(`Unable to load response record: ${error.message}`);
    }
  }

  load();
})();
