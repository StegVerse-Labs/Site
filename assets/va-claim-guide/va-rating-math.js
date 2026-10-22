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
    // Eligibility for 38 CFR 4.26 must be established by the caller, not this arithmetic.
    const paired = combine(bilateralRatings).raw;
    const factor = paired / 10;
    const bilateralValue = roundWhole(Math.min(100, paired + factor));
    const components = [bilateralValue, ...otherRatings.map(validRating)].sort((a,b)=>b-a);
    let raw = 0;
    for (const value of components) raw = combinePair(raw, value);
    return {paired, factor, bilateralValue, raw, rounded:Math.min(100, roundTen(raw))};
  }
  return Object.freeze({combinePair, combine, bilateral});
});
