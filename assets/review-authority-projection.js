(function () {
  'use strict';

  const AUTHORITY_FIELDS = [
    'claim_authority',
    'publication_authority',
    'attribution_authority',
    'public_association_authority'
  ];

  function assertEnvelope(envelope) {
    if (!envelope || typeof envelope !== 'object') throw new Error('envelope required');
    ['artifact_id', 'artifact_version', 'visibility_state', 'process_state'].forEach((field) => {
      if (typeof envelope[field] !== 'string' || !envelope[field].trim()) {
        throw new Error(`${field} required`);
      }
    });
    AUTHORITY_FIELDS.forEach((field) => {
      if (typeof envelope[field] !== 'boolean') throw new Error(`${field} must be boolean`);
    });
    if (envelope.authority_source === 'VISIBILITY') {
      throw new Error('visibility cannot be an authority source');
    }
    if (envelope.process_state === 'REVIEW_ONLY') {
      if (AUTHORITY_FIELDS.some((field) => envelope[field])) {
        throw new Error('review-only authority escalation');
      }
      ['endorsement', 'compatibility', 'interoperability'].forEach((field) => {
        if (envelope[field] !== 'NONE') throw new Error('review-only external claim escalation');
      });
    }
    return Object.freeze({ ...envelope });
  }

  function renderAuthorityProjection(root, input) {
    const envelope = assertEnvelope(input);
    root.replaceChildren();

    const heading = document.createElement('h2');
    heading.textContent = 'Visibility and authority';
    root.appendChild(heading);

    const summary = document.createElement('dl');
    summary.className = 'authority-summary';
    const fields = [
      ['Visibility state', envelope.visibility_state],
      ['Process state', envelope.process_state],
      ['Claim authority', String(envelope.claim_authority)],
      ['Publication authority', String(envelope.publication_authority)],
      ['Attribution authority', String(envelope.attribution_authority)],
      ['Public-association authority', String(envelope.public_association_authority)],
      ['Endorsement', envelope.endorsement],
      ['Compatibility', envelope.compatibility],
      ['Interoperability', envelope.interoperability]
    ];
    fields.forEach(([label, value]) => {
      const dt = document.createElement('dt');
      dt.textContent = label;
      const dd = document.createElement('dd');
      dd.textContent = value;
      summary.append(dt, dd);
    });
    root.appendChild(summary);

    const boundary = document.createElement('p');
    boundary.className = 'authority-boundary';
    boundary.textContent = 'Public visibility does not grant publication, attribution, endorsement, compatibility, interoperability, or public-association authority.';
    root.appendChild(boundary);

    const raw = document.createElement('pre');
    raw.className = 'authority-raw';
    raw.textContent = JSON.stringify(envelope, null, 2);
    root.appendChild(raw);
    return envelope;
  }

  window.StegVerseReviewAuthorityProjection = Object.freeze({
    assertEnvelope,
    renderAuthorityProjection
  });
}());
