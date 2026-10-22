/* Deterministic VA rating arithmetic (38 CFR 4.25 and 4.26).
 * Non-adjudicative; no eligibility, service connection, custody or authority effects.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.VaRatingMath = Object.freeze(api);
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function validRating(value) {
    if (!Number.isInteger(value) || value < 0 || value > 100 || value % 10 !== 0)
      throw new RangeError('Ratings must be multiples of 10 from 0 through 100');
    return value;
  }
  function roundWhole(value) { return Math.floor(value + 0.5); }
  function roundTen(value) { return Math.floor((value + 5) / 10) * 10; }
  function combinePair(a, b) {
    if (!Number.isInteger(a) || a < 0 || a > 100 || !Number.isInteger(b) || b < 0 || b > 100)
      throw new RangeError('Combined values must be integers from 0 through 100');
    return roundWhole(a + (100 - a) * b / 100);
  }
  function combine(values) {
    if (!Array.isArray(values)) throw new TypeError('Expected rating array');
    const ratings = values.map(validRating).sort((a, b) => b - a);
    const steps = [];
    let raw = 0;
    for (const rating of ratings) {
      raw = combinePair(raw, rating);
      steps.push({rating, combined:raw});
    }
    return {raw, rounded:Math.min(100, roundTen(raw)), steps};
  }
  function bilateral(bilateralRatings, otherRatings = []) {
    if (!Array.isArray(bilateralRatings) || !Array.isArray(otherRatings))
      throw new TypeError('Expected arrays');
    if (bilateralRatings.length < 2)
      throw new RangeError('At least two independently qualified bilateral ratings required');
    if (bilateralRatings.some(v => validRating(v) === 0))
      throw new RangeError('Qualifying bilateral ratings must be compensable');
    // Eligibility for 38 CFR 4.26 must be established by the caller, not this arithmetic.
    const paired = combine(bilateralRatings).raw;
    const factor = paired / 10;
    const bilateralValue = roundWhole(Math.min(100, paired + factor));
    const components = [bilateralValue, ...otherRatings.map(validRating)].sort((a,b)=>b-a);
    let raw = 0;
    for (const value of components) raw = combinePair(raw, value);
    return {paired, factor, bilateralValue, raw, rounded:Math.min(100, roundTen(raw))};
  }
  function bilateralMostFavorable(bilateralRatings, otherRatings = []) {
    if (!Array.isArray(bilateralRatings) || !Array.isArray(otherRatings))
      throw new TypeError('Expected arrays');
    if (bilateralRatings.length < 2 || bilateralRatings.length > 12)
      throw new RangeError('Provide 2 through 12 caller-confirmed qualifying bilateral ratings');
    const qualified = bilateralRatings.map(validRating);
    if (qualified.some(v => v === 0)) throw new RangeError('Bilateral ratings must be compensable');
    const others = otherRatings.map(validRating);
    const baseline = combine([...qualified, ...others]);
    let best = {raw:baseline.raw, rounded:baseline.rounded, bilateralIndices:[], factorApplied:false};
    // 38 CFR 4.26(d): consider excluding one or more bilateral disabilities when favorable.
    // Candidate grouping is supplied by the caller; this does not determine extremity eligibility.
    for (let mask = 1; mask < (1 << qualified.length); mask++) {
      const selected = [], excluded = [], indices = [];
      for (let i = 0; i < qualified.length; i++) {
        if (mask & (1 << i)) { selected.push(qualified[i]); indices.push(i); }
        else excluded.push(qualified[i]);
      }
      if (selected.length < 2) continue;
      const candidate = bilateral(selected, [...excluded, ...others]);
      if (candidate.rounded > best.rounded ||
          (candidate.rounded === best.rounded && (candidate.raw > best.raw ||
           (candidate.raw === best.raw && !best.factorApplied))))
        best = {...candidate, bilateralIndices:indices, factorApplied:true};
    }
    return best;
  }
  // Eligibility-aware entrypoint. A rating alone cannot establish bilateral eligibility.
  // Require explicit upper/lower extremity side or paired-muscle group metadata.
  function bilateralFromEvidence(disabilities, otherRatings = []) {
    if (!Array.isArray(disabilities) || !Array.isArray(otherRatings))
      throw new TypeError('Expected disability records and other ratings');
    if (disabilities.length < 2 || disabilities.length > 12)
      throw new RangeError('Provide 2 through 12 documented disabilities');
    const records = disabilities.map((record) => {
      if (!record || typeof record !== 'object' || Array.isArray(record))
        throw new TypeError('Each disability requires a structured evidence record');
      const rating = validRating(record.rating);
      if (rating === 0) throw new RangeError('Bilateral disability must be compensable');
      if (!['upper', 'lower', 'paired-muscle'].includes(record.group) ||
          !['left', 'right'].includes(record.side))
        throw new RangeError('Explicit group and side evidence required');
      if (record.group === 'paired-muscle' &&
          (typeof record.pairId !== 'string' || !/^[a-zA-Z0-9_-]{1,64}$/.test(record.pairId)))
        throw new RangeError('Paired skeletal muscle requires matching pairId');
      return {rating, group:record.group, side:record.side, pairId:record.pairId};
    });
    const others = otherRatings.map(validRating);
    const eligible = (selected) => {
      for (const group of ['upper', 'lower', 'paired-muscle']) {
        const matches = selected.filter((r) => r.group === group);
        if (group !== 'paired-muscle') {
          if (matches.some((r) => r.side === 'left') &&
              matches.some((r) => r.side === 'right')) return true;
        } else {
          const ids = new Set(matches.map((r) => r.pairId));
          for (const id of ids) {
            const pair = matches.filter((r) => r.pairId === id);
            if (pair.some((r) => r.side === 'left') &&
                pair.some((r) => r.side === 'right')) return true;
          }
        }
      }
      return false;
    };
    if (!eligible(records)) throw new RangeError('No documented compensable paired extremities');
    const baseline = combine([...records.map((r) => r.rating), ...others]);
    let best = {raw:baseline.raw, rounded:baseline.rounded, bilateralIndices:[], factorApplied:false};
    for (let mask = 1; mask < (1 << records.length); mask++) {
      const selected = [], excluded = [], indices = [];
      for (let i = 0; i < records.length; i++) {
        if (mask & (1 << i)) { selected.push(records[i]); indices.push(i); }
        else excluded.push(records[i].rating);
      }
      if (!eligible(selected)) continue;
      const candidate = bilateral(selected.map((r) => r.rating), [...excluded, ...others]);
      if (candidate.rounded > best.rounded ||
          (candidate.rounded === best.rounded && (candidate.raw > best.raw ||
           (candidate.raw === best.raw && !best.factorApplied))))
        best = {...candidate, bilateralIndices:indices, factorApplied:true};
    }
    return best;
  }
  return Object.freeze({combinePair, combine, bilateral, bilateralMostFavorable, bilateralFromEvidence});
});
