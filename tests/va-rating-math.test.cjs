const test = require('node:test');
const assert = require('node:assert/strict');
const math = require('../assets/va-claim-guide/va-rating-math.js');
test('whole-person combinations and final tens rounding', () => {
  assert.deepEqual(math.combine([30,50]), {raw:65,rounded:70,steps:[{rating:50,combined:50},{rating:30,combined:65}]});
  assert.equal(math.combine([20,10]).raw,28);
  assert.equal(math.combine([20,10]).rounded,30);
  assert.equal(math.combine([]).rounded,0);
  assert.equal(math.combine([100,50]).rounded,100);
});
test('invalid schedular inputs fail closed', () => {
  for (const value of [-10,101,5,10.5,NaN,'30',null]) assert.throws(()=>math.combine([value]));
  assert.throws(()=>math.combine('30'));
});
test('bilateral arithmetic is applied before other ratings', () => {
  const r=math.bilateral([20,10],[50]);
  assert.deepEqual(r,{paired:28,factor:2.8,bilateralValue:31,raw:66,rounded:70});
  assert.throws(()=>math.bilateral([20]));
});
test('pure calculation does not mutate input', () => {
  const input=Object.freeze([10,50,20]);
  assert.deepEqual(math.combine(input),math.combine(input));
  assert.deepEqual(input,[10,50,20]);
});

test('38 CFR 4.26 regulatory example and most-favorable exception', () => {
  assert.equal(math.bilateral([10,10],[60,20]).rounded,70);
  const r=math.bilateralMostFavorable([10,10],[60,20]);
  assert.equal(r.rounded,70);
  assert.equal(r.factorApplied,true);
  assert.throws(()=>math.bilateralMostFavorable([10,0]));
});

test('eligibility-aware bilateral subsets require actual left/right evidence', () => {
  const left = {rating:10,group:'upper',side:'left'};
  const right = {rating:10,group:'upper',side:'right'};
  const result = math.bilateralFromEvidence([left,right],[60,20]);
  assert.equal(result.rounded,70);
  assert.equal(result.factorApplied,true);
  assert.deepEqual(result.bilateralIndices,[0,1]);
  assert.throws(()=>math.bilateralFromEvidence([left,{rating:20,group:'upper',side:'left'}]));
  assert.throws(()=>math.bilateralFromEvidence([left,{rating:20,group:'lower',side:'right'}]));
  assert.throws(()=>math.bilateralFromEvidence([left,{rating:0,group:'upper',side:'right'}]));
  assert.throws(()=>math.bilateralFromEvidence([left,{rating:10,group:'upper'}]));
});
test('paired skeletal muscles require matching pair identifiers and sides', () => {
  const pair=[
    {rating:20,group:'paired-muscle',side:'left',pairId:'group-A'},
    {rating:10,group:'paired-muscle',side:'right',pairId:'group-A'}
  ];
  assert.equal(math.bilateralFromEvidence(pair).rounded,30);
  assert.throws(()=>math.bilateralFromEvidence([pair[0],{...pair[1],pairId:'group-B'}]));
});
test('official table examples and no premature final tens rounding', () => {
  assert.equal(math.combinePair(10,10),19);
  assert.equal(math.combinePair(60,30),72);
  assert.equal(math.combine([50,30,20]).raw,72);
  assert.equal(math.combine([50,30,20]).rounded,70);
  assert.equal(math.bilateral([10,10],[60,20]).raw,74);
});
