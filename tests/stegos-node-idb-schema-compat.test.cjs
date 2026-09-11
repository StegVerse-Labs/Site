const fs=require('fs');
const vm=require('vm');
const assert=require('assert');
const path=require('path');

const source=fs.readFileSync(path.join(__dirname,'..','assets','stegos-node-idb-schema-compat.js'),'utf8');

function makeContext(initialStores){
  const calls=[];
  class IDBFactory{}
  IDBFactory.prototype.open=function(name,version){
    const listeners={};
    const stores=new Set(initialStores||[]);
    const db={
      objectStoreNames:{contains:(name)=>stores.has(name)},
      createObjectStore:(name,options)=>{assert(!stores.has(name),`duplicate store ${name}`);stores.add(name);return {name,options};}
    };
    const request={
      result:db,
      addEventListener:(kind,fn)=>{(listeners[kind]||(listeners[kind]=[])).push(fn);},
      _fire:(kind)=>{(listeners[kind]||[]).forEach(fn=>fn({target:request}));},
      _stores:stores
    };
    calls.push({name,version,request});
    return request;
  };
  const factory=new IDBFactory();
  const context={IDBFactory,indexedDB:factory,console};
  context.window=context;
  vm.createContext(context);
  vm.runInContext(source,context,{filename:'stegos-node-idb-schema-compat.js'});
  return {context,calls,factory};
}

{
  const {context,calls,factory}=makeContext(['meta','receipts']);
  const req=factory.open('stegos-node-v1',2);
  assert.strictEqual(calls.length,1);
  assert.strictEqual(calls[0].version,3,'malformed v2 must be redirected to canonical v3');
  req._fire('upgradeneeded');
  assert.deepStrictEqual([...req._stores].sort(),['intr_outbox','meta','receipts']);
  assert.strictEqual(context.StegVerseNodeDbSchemaCompatState.deletes_database,false);
  assert.strictEqual(context.StegVerseNodeDbSchemaCompatState.deletes_store,false);
  assert.strictEqual(context.StegVerseNodeDbSchemaCompatState.preserves_existing_rows,true);
}

{
  const {calls,factory}=makeContext(['meta','receipts']);
  const req=factory.open('stegos-node-v1',1);
  assert.strictEqual(calls[0].version,3,'legacy v1 must migrate directly to canonical v3');
  req._fire('upgradeneeded');
  assert.deepStrictEqual([...req._stores].sort(),['intr_outbox','meta','receipts']);
}

{
  const {calls,factory}=makeContext(['meta','receipts','intr_outbox']);
  factory.open('stegos-node-v1',3);
  assert.strictEqual(calls[0].version,3,'current schema reopen must remain idempotent');
}

{
  const {calls,factory}=makeContext([]);
  factory.open('other-db',2);
  assert.deepStrictEqual(calls.map(c=>[c.name,c.version]),[['other-db',2]],'non-Node databases must not be rewritten');
}

const html=fs.readFileSync(path.join(__dirname,'..','my-kv-directory.html'),'utf8');
const compat='assets/stegos-node-idb-schema-compat.js?v=20260911-v3';
const continuity='assets/stegverse-node-continuity.js';
const sync='stegos-node/device-kv-intr-sync.js?v=20260902-device-local-r5';
assert(html.includes(compat),'My KV directory must load Node DB compatibility migration');
assert(html.indexOf(compat)<html.indexOf(continuity),'compat migration must load before Node continuity opens IndexedDB');
assert(html.indexOf(compat)<html.indexOf(sync),'compat migration must load before DEVICE_KV sync opens IndexedDB');

console.log('PASS stegos-node IndexedDB schema compatibility migration');
