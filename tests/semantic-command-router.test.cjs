const assert = require('assert');
const fs = require('fs');
const vm = require('vm');

const source = fs.readFileSync('assets/semantic-command-router.js', 'utf8');
global.window = {};
vm.runInThisContext(source, { filename: 'semantic-command-router.js' });

const api = window.StegVerseSemanticCommands;
assert(api, 'semantic command API was not installed');

const va = api.resolve('/disability', 'VA_CLAIMS_CHAT');
assert.equal(va.recognized, true);
assert.equal(va.command, 'disability');
assert.equal(va.commit_intent, false);
assert.equal(va.authority_effect, false);
assert.equal(va.activation_effect, false);
assert(va.topics.includes('Service connection'));
assert(va.topics.includes('I do not know which topic applies'));

const ecosystem = api.resolve('/disability', 'ECOSYSTEM_CHAT');
assert.equal(ecosystem.recognized, true);
assert(ecosystem.topics.includes('VA disability claims'));
assert(ecosystem.topics.includes('I do not know which route applies'));

const argument = api.resolve('/disability knee pain', 'VA_CLAIMS_CHAT');
assert.equal(argument.argument, 'knee pain');
assert.equal(argument.commit_intent, false);
assert(api.renderText(argument).includes('I will not treat that as a committed intent'));

const unknown = api.resolve('/not-a-command', 'ECOSYSTEM_CHAT');
assert.equal(unknown.recognized, false);
assert(unknown.available.includes('disability'));
assert(api.renderText(unknown).includes('Available shortcuts'));

for (const command of ['/help', '/evidence', '/timeline', '/compare', '/explain', '/visualize']) {
  const result = api.resolve(command, 'ECOSYSTEM_CHAT');
  assert.equal(result.recognized, true, `${command} should resolve`);
  assert.equal(result.commit_intent, false);
  assert.equal(result.authority_effect, false);
  assert.equal(result.activation_effect, false);
}

assert.equal(api.parse('ordinary language'), null);
console.log('SEMANTIC_COMMAND_ROUTER_NODE_TEST=PASS');
