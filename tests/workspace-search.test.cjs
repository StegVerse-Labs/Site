// Universal search contract (Site#1509 WS-SEARCH): search covers only the KV projections supplied for the active
// context, through the capability contract; provenance on every hit; stale labelled; ambiguous source fails closed;
// cross-context projections never searched; no index or storage; hits grant nothing.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const src=fs.readFileSync(path.join(root,'assets/workspace-search.js'),'utf8');
const caps=fs.readFileSync(path.join(root,'assets/workspace-capabilities.js'),'utf8');
const ui=fs.readFileSync(path.join(root,'assets/workspace.js'),'utf8');
const page=fs.readFileSync(path.join(root,'workspace.html'),'utf8');
const bootstrap=JSON.parse(fs.readFileSync(path.join(root,'data/workspace/bootstrap.json'),'utf8'));
const descs=bootstrap.capability_descriptors;
function assert(ok,msg){if(!ok)throw new Error(msg)}
assert(page.indexOf('assets/workspace-capabilities.js')<page.indexOf('assets/workspace-search.js')&&page.indexOf('assets/workspace-search.js')<page.indexOf('assets/workspace.js'),'search contract loads after capabilities and before the page');
assert(/<div id="searchResults" role="status" aria-live="polite"><\/div>/.test(page),'search results live region');
assert(!/localStorage|sessionStorage|indexedDB|caches\.|fetch\(|XMLHttpRequest|WebSocket/.test(src),'search must not index, store or fetch');
assert(/var SEARCHABLE=\["OBSERVED","STALE","FRESHNESS_UNKNOWN"\]/.test(src)&&src.includes('SEARCHABLE.indexOf(s.state)<0')&&src.includes('source.workspace_type!==wt'),'searchable states are an explicit allow-list and the source must declare the active context');
const sandbox={};vm.createContext(sandbox);vm.runInContext(caps,sandbox);vm.runInContext(src,sandbox);
const S=sandbox.StegVerseWorkspaceSearch;
assert(S.schema==='stegverse.workspace.search/v1'&&S.index==='NONE_EPHEMERAL_QUERY_ONLY'&&S.authority_effect==='NONE','module identity');

const NOW=Date.parse('2026-10-10T12:00:00Z');const REV='a'.repeat(64);
const meta=(extra)=>Object.assign({schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:'2026-10-10T11:59:00Z',source_revision:REV,provenance_ref:'kv-workspace-source:sha256:'+REV,workspace_type:'PERSONAL',workspace_id:'ws:personal:owner',owner_principal_id:'user:owner',grant_state:'UNKNOWN',authority_effect:'NONE'},extra||{});
const personal=(extra)=>Object.assign({schema:'stegverse.kv.personal-workspace-projection/v1',workspace_type:'PERSONAL',state:'KV_WORKSPACE_PROJECTED',
  principals:[{principal_id:'user:owner',principal_type:'HUMAN',display_name:'Owner'},{principal_id:'ai:friend',principal_type:'AI_ENTITY',display_name:'Auri Friend',roles:['COLLABORATOR']},{principal_id:'user:alice',principal_type:'HUMAN',display_name:'Alice Example'}],
  organizations:[{principal_id:'org:aurora',principal_type:'ORGANIZATION',display_name:'Aurora Labs'}],
  memberships:[{organization_id:'org:aurora',organization_name:'Aurora Labs',role:'Engineer',department:'Platform',status:'ACTIVE'}],
  feed:[{event_id:'ev-1',actor_id:'user:alice',actor_name:'Alice Example',viewer_id:'user:owner',visibility:'PUBLIC',text:'Alice shipped the aurora release'},{event_id:'ev-2',actor_id:'user:bob',actor_name:'Bob',viewer_id:'user:owner',visibility:'PRIVATE',text:'aurora private note'}],
  assistant:{principal_id:'auri:primary',principal_type:'AI_ENTITY',display_name:'Auri',roles:['WORKSPACE_ASSISTANT'],ai_label_required:true},
  credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,projection_metadata:meta(),authority_effect:'NONE'},extra||{});
const cryptobot=(extra)=>Object.assign({schema:'stegverse.kv.cryptobot-portfolio-projection/v1',workspace_type:'PERSONAL',portfolio:{positions:[{product_id:'ETH-USD',asset:'ETH',quantity:0.5,value_usd:1000},{product_id:'ATOM-USD',asset:'ATOM',quantity:12,value_usd:90}],total_value_usd:1090},
  credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,trade_authority_granted:false,projection_metadata:meta({observed_at:'2026-10-10T11:58:30Z'}),authority_effect:'NONE'},extra||{});
const visible=ev=>['PUBLIC','ECOSYSTEM'].includes(ev.visibility||'PRIVATE')||(ev.visibility==='PRIVATE'&&ev.actor_id===ev.viewer_id);
const run=(query,projections,wt,extra)=>S.search(Object.assign({query,workspace_type:wt||'PERSONAL',descriptors:descs,projections,now_ms:NOW,visibility:visible},extra||{}));

// Multi-projection filtering: one query spans personal rows and the CryptoBot projection, each hit carrying its own provenance.
let r=run('aurora',[personal(),cryptobot()]);
assert(r.disposition==='ALLOW'&&r.predicate==='SEARCH_COMPLETED'&&r.index==='NONE_EMPHEMERAL_QUERY_ONLY'.replace('EMPHEMERAL','EPHEMERAL')&&r.action_eligible===false&&r.authority_effect==='NONE','search completes');
let kinds=r.hits.map(h=>h.kind+':'+h.id);
assert(kinds.includes('organization:org:aurora')&&kinds.includes('membership:org:aurora')&&kinds.includes('feed:ev-1'),'personal rows found: '+kinds.join(','));
assert(!kinds.includes('feed:ev-2')&&r.visibility_withheld===1,'private feed item of another actor withheld by visibility');
for(const h of r.hits){assert(h.action_eligible===false&&h.context.workspace_type==='PERSONAL'&&h.provenance.projection_schema==='stegverse.kv.personal-workspace-projection/v1'&&h.provenance.freshness_state==='OBSERVED'&&h.provenance.provenance_ref==='kv-workspace-source:sha256:'+REV&&h.provenance.source_revision===REV&&h.provenance.replay_status==='REPLAY_STATUS_UNKNOWN','hit provenance: '+JSON.stringify(h));}
r=run('eth',[personal(),cryptobot()]);
assert(r.hits.length===1&&r.hits[0].kind==='portfolio'&&r.hits[0].id==='ETH-USD'&&r.hits[0].capability==='CRYPTOBOT_PORTFOLIO'&&r.hits[0].provenance.projection_schema==='stegverse.kv.cryptobot-portfolio-projection/v1'&&r.hits[0].provenance.observed_at==='2026-10-10T11:58:30Z','portfolio hit carries its own projection provenance: '+JSON.stringify(r.hits));
r=run('auri',[personal()]);
kinds=r.hits.map(h=>h.kind+':'+h.id);
assert(kinds[0]==='assistant:auri:primary'&&kinds.includes('principal:ai:friend'),'assistant first, then principals: '+kinds.join(','));
assert(r.hits[0].detail.includes('no invocation route'),'assistant hit never implies invocation');
assert(run('alice example',[personal()]).hits.map(h=>h.id).join(',')==='user:alice,ev-1','all query tokens must match');
assert(run('nomatch-zzz',[personal()]).hits.length===0&&run('nomatch-zzz',[personal()]).predicate==='SEARCH_COMPLETED','no hits is still a completed search');
assert(run('',[personal()]).predicate==='QUERY_EMPTY'&&run('   ',[personal()]).hits.length===0,'empty query searches nothing');
// Capabilities without a projection are reported as excluded, not silently absent.
const ex=run('aurora',[personal()]).excluded;
assert(ex.some(e=>e.capability==='CRYPTOBOT_PORTFOLIO'&&e.state==='NOT_OBSERVED')&&ex.some(e=>e.capability==='CALENDAR'),'withheld capabilities are listed: '+JSON.stringify(ex.map(e=>e.capability+':'+e.state)));

// Cross-context denial: a personal projection is never searched in the organizational context, and vice versa.
r=run('aurora',[personal(),cryptobot()],'ORGANIZATIONAL');
assert(r.disposition==='ALLOW'&&r.hits.length===0,'personal rows must not surface in org context: '+JSON.stringify(r.hits));
assert(r.excluded.every(e=>['CONTEXT_MISMATCH','UNAVAILABLE','NOT_OBSERVED','MALFORMED'].includes(e.state)),'org context excludes personal-only sources: '+JSON.stringify(r.excluded));
assert(r.excluded.some(e=>e.state==='CONTEXT_MISMATCH'||e.predicate==='CAPABILITY_NOT_DEFINED_FOR_CONTEXT'),'context mismatch recorded');
r=run('aurora',[personal({workspace_type:'ORGANIZATIONAL'})],'PERSONAL');
assert(r.hits.length===0&&r.excluded.some(e=>e.state==='CONTEXT_MISMATCH'),'org-typed projection never searched in personal context');
assert(run('aurora',[personal()],'OTHER').disposition==='FAIL_CLOSED'&&run('aurora',[personal()],'OTHER').predicate==='WORKSPACE_CONTEXT_INVALID','unknown context fails closed');

// Source ambiguity: two projections for one capability fail the whole search closed.
r=run('aurora',[personal(),personal({principals:[{principal_id:'user:x',principal_type:'HUMAN',display_name:'Aurora Impostor'}]})]);
assert(r.disposition==='FAIL_CLOSED'&&r.predicate==='PROJECTION_SOURCE_AMBIGUOUS'&&r.hits.length===0&&r.ambiguous.includes('CONTACTS'),'ambiguous sources must fail closed: '+r.predicate+' '+JSON.stringify(r.ambiguous));

// Stale and freshness-unknown projections still search but every hit is labelled; revoked or malformed never search.
r=run('aurora',[personal({projection_metadata:meta({observed_at:'2026-10-01T00:00:00Z'})})]);
assert(r.hits.length>0&&r.hits.every(h=>h.provenance.freshness_state==='STALE'&&h.provenance.freshness_predicate==='PROJECTION_OLDER_THAN_MAX_AGE'),'stale hits labelled');
r=run('aurora',[personal({projection_metadata:undefined})]);
assert(r.hits.length>0&&r.hits.every(h=>h.provenance.freshness_state==='FRESHNESS_UNKNOWN'&&h.provenance.observed_at===null),'freshness-unknown hits labelled');
assert(run('aurora',[personal({projection_metadata:meta({grant_state:'REVOKED'})})]).hits.length===0,'revoked projection never searched');
assert(run('aurora',[personal({authority_effect:'ALLOW'})]).hits.length===0,'authority-asserting projection never searched');
assert(run('aurora',[]).hits.length===0&&run('aurora',[]).excluded.every(e=>['NOT_OBSERVED','UNAVAILABLE'].includes(e.state)),'no projections, no hits');
assert(S.search({query:'a',workspace_type:'PERSONAL',projections:[personal()]}).predicate==='CAPABILITY_DESCRIPTORS_UNAVAILABLE','missing descriptors fail closed');
// No index: deterministic and input-only.
const a=JSON.stringify(run('aurora',[personal(),cryptobot()])),b=JSON.stringify(run('aurora',[JSON.parse(JSON.stringify(personal())),JSON.parse(JSON.stringify(cryptobot()))]));
assert(a===b,'deterministic over equal inputs');
const big=personal({principals:Array.from({length:80},(_,i)=>({principal_id:'p'+i,principal_type:'HUMAN',display_name:'Aurora '+i}))});
r=run('aurora',[big]);assert(r.truncated===true&&r.hits.length===S.max_hits,'hit cap');

// Page: results render in the Search card with provenance, cross-context switch empties them, no fetch or storage.
assert(ui.includes('renderSearch(e.target.value)')&&ui.includes('visibility:visibilityAllows'),'page wires the search input and feed visibility');
const ids=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities','searchResults'];
function harness(proj){const els={};ids.forEach(i=>els[i]={id:i,innerHTML:'',textContent:'',className:'',value:'',dataset:{},attrs:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},classList:{add(){},remove(){}},listeners:{},addEventListener(t,f){this.listeners[t]=f},scrollIntoView(){}});
  const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener(){}},console,fetch:()=>Promise.resolve({json:()=>Promise.resolve(bootstrap)}),window:{StegVerseWorkspaceKVBridge:{loadPersonalWorkspace:()=>Promise.resolve(proj),lastNodeBinding:()=>null}}};
  vm.createContext(ctx);vm.runInContext(caps,ctx);vm.runInContext(src,ctx);ctx.window.StegVerseWorkspaceCapabilities=ctx.StegVerseWorkspaceCapabilities;ctx.window.StegVerseWorkspaceSearch=ctx.StegVerseWorkspaceSearch;vm.runInContext(ui,ctx);
  return {els,type:v=>{els.search.value=v;els.search.listeners.input({target:{value:v}})},switchTo:v=>els.workspaceSwitch.listeners.change({target:{value:v}})};}
(async()=>{
  const liveMeta=()=>meta({observed_at:new Date(Date.now()-60000).toISOString().replace(/\.\d{3}Z$/,'Z')});
  const h=harness(personal({projection_metadata:liveMeta()}));await new Promise(r=>setTimeout(r,10));
  assert(h.els.searchResults.innerHTML.includes('Type to search the admitted PERSONAL projections')&&h.els.searchResults.innerHTML.includes('nothing is indexed or stored'),'empty-query state: '+h.els.searchResults.innerHTML);
  h.type('aurora');let html=h.els.searchResults.innerHTML;
  assert(html.includes('Aurora Labs')&&html.includes('ORGANIZATIONS · OBSERVED')&&html.includes('provenance kv-workspace-source:sha256:')&&html.includes('context PERSONAL')&&html.includes('replay REPLAY_STATUS_UNKNOWN'),'hits with provenance: '+html);
  assert(html.includes('1 feed item(s) withheld by visibility')&&!html.includes('aurora private note'),'visibility withheld reported, private row absent');
  assert(html.includes('Not searched (')&&html.includes('CRYPTOBOT_PORTFOLIO NOT_OBSERVED'),'withheld capabilities listed');
  assert(html.includes('action_eligible: false')&&!/ALLOW<|admitted|completed successfully/i.test(html),'informational only');
  assert(h.els.contacts.innerHTML.includes('No admitted contacts match')||!h.els.contacts.innerHTML.includes('Alice'),'existing contact filter still applies');
  h.switchTo('organizational');html=h.els.searchResults.innerHTML;
  assert(!html.includes('Aurora Labs')&&!html.includes('Alice')&&html.includes('No admitted ORGANIZATIONAL projection row matches'),'org context must not surface personal hits: '+html);
  h.switchTo('personal');assert(h.els.searchResults.innerHTML.includes('Aurora Labs'),'personal hits restored');
  console.log('WORKSPACE_SEARCH_PASS');
})().catch(e=>{console.error(e);process.exit(1)});
