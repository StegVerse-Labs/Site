(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const hashText = async (text) => {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return [...new Uint8Array(digest)].map(v => v.toString(16).padStart(2, '0')).join('');
  };
  const parseCsv = (text) => {
    const rows = text.trim().split(/\r?\n/).map(line => line.split(',').map(v => v.trim()));
    if (rows.length < 2) throw new Error('CSV requires a header and at least one data row.');
    const headers = rows.shift();
    return rows.map(row => Object.fromEntries(headers.map((header, index) => [header, row[index] ?? ''])));
  };
  const scalar = (value) => {
    const text = String(value ?? '').trim();
    if (!text) return null;
    if (/^-?\d+(\.\d+)?$/.test(text)) return Number(text);
    if (/^(true|false)$/i.test(text)) return text.toLowerCase() === 'true';
    return text;
  };
  const buildObservations = (records, evidenceClass) => {
    const output = [];
    records.forEach((record, row) => Object.entries(record).forEach(([field, raw]) => {
      const value = scalar(raw);
      if (value !== null) output.push({field, value, unit:null, evidence_class:evidenceClass, confidence:'MEDIUM', source_path:`records[${row}].${field}`});
    }));
    if (!output.length) throw new Error('No non-empty observations were found.');
    return output;
  };
  const detectConflicts = (items, authorityClass) => {
    const seen = new Map(), found = [];
    items.forEach(item => {
      if (seen.has(item.field) && JSON.stringify(seen.get(item.field)) !== JSON.stringify(item.value)) {
        found.push({field:item.field, existing_value:seen.get(item.field), incoming_value:item.value,
          existing_authority_class:authorityClass, incoming_authority_class:authorityClass,
          resolution_state:'QUALIFIED_REVIEW_REQUIRED'});
      } else seen.set(item.field, item.value);
    });
    return found;
  };
  async function importFile() {
    const file = $('evidenceFile')?.files?.[0];
    if (!file) return $('importStatus').textContent = 'Choose a JSON or CSV file.';
    try {
      const text = await file.text();
      let records;
      if (file.name.toLowerCase().endsWith('.csv')) records = parseCsv(text);
      else {
        const parsed = JSON.parse(text);
        records = Array.isArray(parsed) ? parsed : Array.isArray(parsed.records) ? parsed.records : [parsed];
        if (!records.every(item => item && typeof item === 'object' && !Array.isArray(item))) throw new Error('JSON must contain object records.');
      }
      const authorityClass = $('importAuthorityClass').value;
      const packet = {
        packet_id:`EVP-LOCAL-${Date.now()}`,
        created_at:new Date().toISOString(),
        source:{system:$('importSourceSystem').value.trim() || 'AUTHORIZED_EXPORT', record_id:$('importSourceRecord').value.trim() || file.name,
          owner_role:$('importOwnerRole').value, authority_class:authorityClass,
          transport:file.name.toLowerCase().endsWith('.csv') ? 'CSV' : 'JSON', source_uri:null, observed_at:null, original_sha256:await hashText(text)},
        asset:{candidate_id:$('candidateId').value.trim() || 'UNASSIGNED', unit_number:$('unitNumber').value.trim() || null,
          reporting_mark:null, donor_lineage:$('donorLineage').value},
        observations:buildObservations(records, $('importEvidenceClass').value), conflicts:[],
        custody_state:'BROWSER_LOCAL_UNCUSTODIED', execution_authority:false,
        history:[{timestamp:new Date().toISOString(), actor:'gp10-evidence-import.js', action:'Parsed authorized browser-local export without source mutation'}]
      };
      packet.conflicts = detectConflicts(packet.observations, authorityClass);
      localStorage.setItem('gp10.workspace.import.latest', JSON.stringify(packet));
      $('importPreview').textContent = JSON.stringify(packet, null, 2);
      const reference = `external-evidence:${packet.packet_id}:${packet.source.original_sha256}`;
      if (!$('evidenceRefs').value.includes(reference)) $('evidenceRefs').value = [$('evidenceRefs').value.trim(), reference].filter(Boolean).join('\n');
      $('importStatus').textContent = `Imported ${packet.observations.length} observations; ${packet.conflicts.length} conflict(s). Source authority retained; no execution authority.`;
    } catch (error) { $('importStatus').textContent = `FAIL-CLOSED: ${error.message}`; }
  }
  $('importEvidence')?.addEventListener('click', importFile);
  const latest = localStorage.getItem('gp10.workspace.import.latest');
  if (latest && $('importPreview')) $('importPreview').textContent = latest;
})();
