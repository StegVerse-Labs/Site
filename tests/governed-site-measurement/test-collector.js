const assert = require('assert');
const collector = require('../../api/governed-measurement.js');

const base = { event:'guide_opened', page:'va-disability-claim-guide', policy_version:'1.0.0', content_recorded:false };
assert.deepStrictEqual(collector.validate(base), []);
assert.deepStrictEqual(collector.projection(base), { schema:'stegverse.governed-site-measurement.aggregate-input.v1', event:'guide_opened', page:'va-disability-claim-guide', policy_version:'1.0.0', dimensions:{} });

const valid = [
  {...base,event:'quick_question_selected',choice:'blue_button'},
  {...base,event:'phase_reached',phase:6},
  {...base,event:'official_source_opened',destination_class:'official_va_source'},
  {...base,event:'client_error',error_class:'collector_unavailable'}
];
for (const item of valid) assert.deepStrictEqual(collector.validate(item), []);

const rejected = [
  {...base,question:'What is my rating?'},
  {...base,session_id:'abc'},
  {...base,diagnosis:'PTSD'},
  {...base,content_recorded:true},
  {...base,event:'unknown'},
  {...base,event:'phase_reached',phase:7},
  {...base,event:'quick_question_selected',choice:'free_text'},
  {...base,event:'official_source_opened',destination_class:'advertiser'},
  {...base,extra:'unexpected'}
];
for (const item of rejected) assert.ok(collector.validate(item).length > 0, JSON.stringify(item));

const projected = collector.projection({...base,event:'phase_reached',phase:2});
assert.strictEqual(projected.dimensions.phase,2);
assert.ok(!JSON.stringify(projected).includes('session'));
console.log('GOVERNED_MEASUREMENT_COLLECTOR_TESTS=PASS');
