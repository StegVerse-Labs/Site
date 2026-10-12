// Capability panels (Site#1509 WS-PANELS): one reusable renderer for every capability family, deriving each panel
// only from the capability status contract plus the matching KV projection; rows are withheld in every non-row
// state, malformed rows are counted and skipped, producer owners are named, and nothing a panel shows is an
// availability claim or a permission to act.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const caps=read('assets/workspace-capabilities.js'),panelsSrc=read('assets/workspace-panels.js'),search=read('assets/workspace-search.js'),ui=read('assets/workspace.js'),css=read('assets/workspace.css'),page=read('workspace.html'),workflow=read('.github/workflows/workspace-kv-binding-validation.yml');
const bootstrap=JSON.parse(read('data/workspace/bootstrap.json'));
function assert(ok,msg){if(!ok)throw new Error(msg)}
let n=0;const check=(ok,msg)=>{n++;assert(ok,msg)};
const sb={};vm.createContext(sb);vm.runInContext(caps,sb);vm.runInContext(panelsSrc,sb);
const C=sb.StegVerseWorkspaceCapabilities,P=sb.StegVerseWorkspacePanels;
const descs=bootstrap.capability_descriptors;
const NOW=Date.parse('2026-10-11T04:00:00Z');const REV='c'.repeat(64);
const meta=(ref,extra)=>Object.assign({schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:'2026-10-11T03:59:00Z',observed_at_semantics:'KV_PROJECTION_PRODUCTION_TIME',source_revision:REV,provenance_ref:ref+':sha256:'+REV,workspace_type:'PERSONAL',workspace_id:'ws:personal:owner',owner_principal_id:'user:owner',grant_state:'UNKNOWN',revocation_epoch:null,authority_effect:'NONE'},extra||{});
const personal=(extra)=>Object.assign({schema:'stegverse.kv.personal-workspace-projection/v1',workspace_type:'PERSONAL',state:'KV_WORKSPACE_PROJECTED',principals:[{principal_id:'user:alice',principal_type:'HUMAN',display_name:'Alice'}],organizations:[],memberships:[],feed:[{id:'f1',text:'hello',visibility:'PERSONAL'}],assistant:null,credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,authority_effect:'NONE',projection_metadata:meta('kv-workspace-source')},extra||{});
const tasks=(extra)=>Object.assign({schema:'stegverse.kv.workspace-tasks-projection/v1',workspace_type:'PERSONAL',state:'KV_TASKS_PROJECTED',tasks:[{task_id:'t-1',title:'Review aurora release',status:'OPEN',due_at:'2026-10-12T09:00:00Z',action_eligible:false},{bogus:true}],commitments:[{commitment_id:'c-1',statement:'Send Alice the draft',status:'ACTIVE',action_eligible:false}],timeline:[],credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,action_authority:'NONE',projection_metadata:meta('kv-workspace-tasks-source'),authority_effect:'NONE'},extra||{});
// Read-only CryptoBot portfolio projection as the consumer contract (crypto-bot#23) describes it: no trade authority,
// provider observation time distinct from projection time, fields the provider could not supply named as unavailable.
const crypto=(extra)=>Object.assign({schema:'stegverse.kv.cryptobot-portfolio-projection/v1',workspace_type:'PERSONAL',state:'KV_PORTFOLIO_PROJECTED',trade_authority_granted:false,provider_operation_authorized:false,credential_material_present:false,workspace_grants_authority:false,authority_effect:'NONE',
  source:{authority:'crypto-bot read-only portfolio snapshot',provider:'coinbase'},
  portfolio:{provider:'coinbase',source_observed_at:'2026-10-11T03:50:00Z',total_value_usd:1234.5,drawdown_percent:null,unavailable_fields:{drawdown_percent:'PROVIDER_FIELD_ABSENT'},
    positions:[{asset:'BTC',product_id:'BTC-USD',quantity:0.01,value_usd:1000,price_usd:100000},{asset:'ETH',quantity:0.05},{asset:'',quantity:1},{quantity:'x'}]},
  projection_metadata:meta('kv-cryptobot-portfolio-source')},extra||{});
const build=(projs,wt,descriptors)=>{const d=descriptors||descs;return P.build({descriptors:d,statuses:C.evaluateAll(d,projs,wt||'PERSONAL',NOW),projections:projs,workspace_type:wt||'PERSONAL'});};
const byCap=(b)=>Object.fromEntries(b.panels.map(p=>[p.capability,p]));

// 1. Schema and non-assertion: one panel per shipped descriptor, every panel non-authorizing, inputs untouched.
const inputs=[personal(),tasks(),crypto()];const frozen=JSON.stringify(inputs);
const full=build(inputs);
check(full.schema==='stegverse.workspace.capability-panel/v1'&&P.schema===full.schema&&full.disposition==='ALLOW'&&full.predicate==='PANELS_DERIVED_FROM_CAPABILITY_STATUS','panel bundle schema/disposition: '+JSON.stringify(full).slice(0,200));
check(full.panels.length===descs.length&&full.panels.every((p,i)=>p.capability===descs[i].capability),'one panel per descriptor in descriptor order');
check(full.panels.every(p=>p.schema===full.schema&&p.action_eligible===false&&p.authority_effect==='NONE'&&p.context.workspace_type==='PERSONAL'&&typeof p.provenance==='object'&&typeof p.provenance.replay_status==='string'),'every panel is informational only and carries provenance');
check(JSON.stringify(inputs)===frozen,'panels must not mutate projections');
check(full.action_eligible===false&&full.authority_effect==='NONE'&&Object.isFrozen(P),'bundle non-authorizing; contract frozen');
check(JSON.stringify(full).indexOf('"available":true')<0&&!/"admitted"|"approved"/.test(JSON.stringify(full)),'panels never emit availability/admission claims');

// 2. CryptoBot adapter: valid positions become rows, malformed positions are counted and skipped, unavailable fields named.
const cb=byCap(full).CRYPTOBOT_PORTFOLIO;
check(cb.state==='OBSERVED'&&cb.rows_withheld===false&&cb.rows.length===2&&cb.malformed_rows===2,'cryptobot rows/malformed: '+JSON.stringify(cb));
check(cb.rows[0].label==='BTC'&&/product BTC-USD · qty 0\.01 · usd 1000 · price 100000/.test(cb.rows[0].detail)&&cb.rows[1].label==='ETH'&&/value UNAVAILABLE/.test(cb.rows[1].detail),'position rows carry only producer-supplied fields: '+JSON.stringify(cb.rows));
check(cb.notes.includes('total usd 1234.5')&&cb.notes.includes('drawdown UNAVAILABLE')&&cb.notes.includes('provider coinbase')&&cb.notes.some(x=>x.startsWith('provider observation 2026-10-11T03:50:00Z'))&&cb.notes.includes('drawdown_percent: PROVIDER_FIELD_ABSENT')&&cb.notes.some(x=>x.startsWith('source authority '))&&cb.notes.includes('trade_authority_granted: false · provider_operation_authorized: false'),'cryptobot notes: '+JSON.stringify(cb.notes));
check(cb.provenance.provenance_ref==='kv-cryptobot-portfolio-source:sha256:'+REV&&cb.provenance.observed_at==='2026-10-11T03:59:00Z'&&cb.provenance.age_seconds===60&&cb.provenance.replay_status==='REPLAY_STATUS_UNKNOWN','cryptobot provenance from the status contract: '+JSON.stringify(cb.provenance));
// A projection that claims trade authority is MALFORMED and renders nothing.
for(const forged of [{trade_authority_granted:true},{trade_authority_granted:undefined},{trade_authority_granted:'false'}]){const f=byCap(build([personal(),tasks(),crypto(forged)])).CRYPTOBOT_PORTFOLIO;check(f.state==='MALFORMED'&&f.predicate==='PROJECTION_TRADE_AUTHORITY_INVALID'&&f.rows_withheld===true&&f.rows.length===0,'trade authority claim must fail closed: '+JSON.stringify(forged));}
const badPf=byCap(build([personal(),tasks(),crypto({portfolio:[]})])).CRYPTOBOT_PORTFOLIO;check(badPf.state==='MALFORMED'&&badPf.rows_withheld===true,'non-object portfolio fails closed: '+badPf.predicate);
const emptyPf=byCap(build([personal(),tasks(),crypto({portfolio:{positions:[]}})])).CRYPTOBOT_PORTFOLIO;check(emptyPf.state==='OBSERVED'&&emptyPf.rows.length===0&&emptyPf.malformed_rows===0&&emptyPf.notes.includes('drawdown UNAVAILABLE'),'empty portfolio renders no rows and no guessed values');
// Producer bounds re-checked by the consumer (crypto-bot#23 projection contract): a projection that did not come through
// the producer cannot render a label that displays as something else (bidi override, zero-width, control) or an
// impossible figure. Portfolio-level violations withhold the whole panel; position-level ones are counted and skipped.
const pfWith=(extra,src)=>byCap(build([personal(),tasks(),crypto(Object.assign({portfolio:Object.assign({},crypto().portfolio,extra)},src?{source:src}:{}))])).CRYPTOBOT_PORTFOLIO;
for(const [extra,predicate] of [[{drawdown_percent:-1},'PORTFOLIO_DRAWDOWN_INVALID'],[{drawdown_percent:101},'PORTFOLIO_DRAWDOWN_INVALID'],[{drawdown_percent:'5'},'PORTFOLIO_DRAWDOWN_INVALID'],
  [{total_value_usd:-1},'PORTFOLIO_TOTAL_INVALID'],[{total_value_usd:'1'},'PORTFOLIO_TOTAL_INVALID'],
  [{provider:'coin‮base'},'PORTFOLIO_PROVIDER_INVALID'],[{provider:'x'.repeat(65)},'PORTFOLIO_PROVIDER_INVALID'],[{provider:' '},'PORTFOLIO_PROVIDER_INVALID'],[{provider:7},'PORTFOLIO_PROVIDER_INVALID'],
  [{source_observed_at:'2026​-10-11'},'PORTFOLIO_OBSERVED_AT_INVALID'],[{unavailable_fields:{'drawdown\u0000':'ABSENT'}},'PORTFOLIO_UNAVAILABLE_FIELDS_INVALID'],[{unavailable_fields:{drawdown_percent:'A\nB'}},'PORTFOLIO_UNAVAILABLE_FIELDS_INVALID']]){
  const f=pfWith(extra);check(f.state==='MALFORMED'&&f.predicate===predicate&&f.rows_withheld===true&&f.rows.length===0&&f.notes.length===0,'portfolio bound must fail closed: '+JSON.stringify(extra)+' -> '+f.predicate);}
for(const authority of ['crypto\u202Ebot','x'.repeat(129),' ',42]){const f=pfWith({}, {authority,provider:'coinbase'});check(f.state==='MALFORMED'&&f.predicate==='PORTFOLIO_SOURCE_AUTHORITY_INVALID'&&f.notes.length===0,'source authority must be displayable: '+JSON.stringify(authority)+' -> '+f.predicate);}
const badId=pfWith({}, {authority:'crypto-bot',provider:'coinbase',snapshot_id:'snap⁦shot'});check(badId.state==='MALFORMED'&&badId.predicate==='PORTFOLIO_SNAPSHOT_ID_INVALID','hidden snapshot identity fails closed: '+badId.predicate);
check(pfWith({drawdown_percent:0}).state==='OBSERVED'&&pfWith({drawdown_percent:100}).notes.includes('drawdown 100%')&&pfWith({drawdown_percent:null}).notes.includes('drawdown UNAVAILABLE'),'in-range and absent drawdown still render');
const rowsCase=pfWith({positions:[{asset:'BTC',quantity:1},{asset:'E‮TH',quantity:1},{asset:'​',quantity:1},{asset:'A'.repeat(65),quantity:1},{asset:'SOL',quantity:-1},{asset:'ADA',quantity:1,value_usd:-5},{asset:'DOT',quantity:1,price_usd:Infinity},{asset:'XRP',quantity:1,product_id:'XRP\u0007-USD'}]});
check(rowsCase.state==='OBSERVED'&&rowsCase.rows.length===1&&rowsCase.rows[0].label==='BTC'&&rowsCase.malformed_rows===7,'positions outside producer bounds are counted and skipped: '+JSON.stringify(rowsCase.rows)+' malformed='+rowsCase.malformed_rows);

// 3. Tasks/commitments adapters and families rendered elsewhere.
const tp=byCap(full);
check(tp.TASKS.rows.length===1&&tp.TASKS.malformed_rows===1&&tp.TASKS.rows[0].label==='Review aurora release'&&/OPEN · due 2026-10-12T09:00:00Z/.test(tp.TASKS.rows[0].detail)&&tp.TASKS.rendered_in==='Tasks & commitments card','tasks adapter: '+JSON.stringify(tp.TASKS));
check(tp.COMMITMENTS.rows.length===1&&tp.COMMITMENTS.rows[0].label==='Send Alice the draft'&&tp.COMMITMENTS.rows[0].detail==='ACTIVE','commitments adapter: '+JSON.stringify(tp.COMMITMENTS.rows));
check(tp.FEED.state==='OBSERVED'&&tp.FEED.rows.length===0&&tp.FEED.notes.includes('1 row(s) rendered in the Feed card')&&tp.CONTACTS.notes.includes('1 row(s) rendered in the Friends & Contacts card'),'families with their own card are counted, not duplicated: '+JSON.stringify(tp.FEED.notes));

// 4. Non-row states withhold rows and name the producer owner; #3012 is cited as read-only, never acted on.
// Every descriptor without a KV projection contract must name its producer owner (guards the one-line-binding pattern).
for(const d of descs){if(d.allowed_projection_schemas.length===0){const p=byCap(build([],d.workspace_types[0])) [d.capability];check(p.state==='UNAVAILABLE'&&p.predicate==='NO_KV_PROJECTION_CONTRACT'&&typeof p.producer_owner==='string'&&p.producer_owner.length>0,'contract-less descriptor must name a producer owner: '+d.capability);}}
for(const cap of ['VOIP','SPREADSHEETS','PRESENTATIONS'])check(byCap(build([])) [cap]&&byCap(build([]))[cap].state==='UNAVAILABLE'&&byCap(build([]))[cap].rows_withheld===true,'scope family declared and withheld: '+cap);
for(const cap of ['CALENDAR','EMAIL','MESSAGING','DOCUMENTS','SOCIAL','ORG_WORKSPACE','GITHUB_GOVERNANCE']){const p=tp[cap];check(p.state==='UNAVAILABLE'&&p.rows_withheld===true&&p.rows.length===0&&typeof p.producer_owner==='string'&&p.producer_owner.length>0,'unbacked family must withhold rows and name a producer: '+cap);}
check(/\.github#3012/.test(tp.GITHUB_GOVERNANCE.producer_owner)&&/read-only/.test(tp.GITHUB_GOVERNANCE.producer_owner),'governance producer owner cites #3012 as read-only');
check(/Org-KV/.test(tp.ORG_WORKSPACE.producer_owner)&&/not Personal KV/.test(tp.ORG_WORKSPACE.producer_owner),'org workspace producer named as organizational runtime');
const none=build([]);check(none.disposition==='ALLOW'&&none.panels.every(p=>p.rows_withheld===true&&p.rows.length===0&&(p.state==='NOT_OBSERVED'||p.state==='UNAVAILABLE')),'no projections -> every panel withholds rows');
const revoked=byCap(build([personal(),tasks(),crypto({projection_metadata:meta('kv-cryptobot-portfolio-source',{grant_state:'REVOKED'})})])).CRYPTOBOT_PORTFOLIO;
check(revoked.state==='REVOKED'&&revoked.rows_withheld===true&&revoked.rows.length===0&&revoked.predicate==='PROJECTION_GRANT_REVOKED','revoked grant withholds rows: '+JSON.stringify(revoked));
const stale=byCap(build([personal(),tasks(),crypto({projection_metadata:meta('kv-cryptobot-portfolio-source',{observed_at:'2026-10-11T02:00:00Z'})})])).CRYPTOBOT_PORTFOLIO;
check(stale.state==='STALE'&&stale.predicate==='PROJECTION_OLDER_THAN_MAX_AGE'&&stale.rows_withheld===false&&stale.rows.length===2&&stale.provenance.age_seconds===7200,'stale rows stay visible but labelled STALE: '+JSON.stringify(stale.provenance));
const unknown=byCap(build([personal(),tasks(),crypto({projection_metadata:meta('kv-cryptobot-portfolio-source',{observed_at:undefined})})])).CRYPTOBOT_PORTFOLIO;
check(unknown.state==='FRESHNESS_UNKNOWN'&&unknown.rows_withheld===false&&unknown.rows.length===2&&unknown.provenance.observed_at===null,'freshness unknown is labelled, not hidden');
// Two projections claiming the same schema fail closed at the status layer and the panel withholds rows.
const dup=byCap(build([personal(),tasks(),crypto(),crypto()])).CRYPTOBOT_PORTFOLIO;check(dup.rows_withheld===true&&dup.rows.length===0&&C.withholdsRows({state:dup.state}),'ambiguous projection source withholds rows: '+dup.state+'/'+dup.predicate);
// Missing descriptors/statuses fail closed.
const closed=P.build({descriptors:null,statuses:null,projections:inputs,workspace_type:'PERSONAL'});check(closed.disposition==='FAIL_CLOSED'&&closed.predicate==='CAPABILITY_DESCRIPTORS_UNAVAILABLE'&&closed.panels.length===0,'absent descriptors fail closed');
const short=P.build({descriptors:descs,statuses:[],projections:inputs,workspace_type:'PERSONAL'});check(short.panels.every(p=>p.state==='NOT_OBSERVED'&&p.predicate==='CAPABILITY_STATUS_ABSENT'&&p.rows_withheld===true),'missing status entries withhold rows');

// 5. Context separation: personal projections never populate panels in an organizational context, and a projection
// whose workspace_type disagrees with the active context is a CONTEXT_MISMATCH even if its status permitted rows.
const org=build(inputs,'ORG');check(org.panels.every(p=>p.rows_withheld===true&&p.rows.length===0&&p.context.workspace_type==='ORG'),'personal rows leak into ORG context: '+JSON.stringify(org.panels.filter(p=>!p.rows_withheld).map(p=>p.capability)));
const forgedStatus=C.evaluateAll(descs,inputs,'PERSONAL',NOW);const mis=P.build({descriptors:descs,statuses:forgedStatus,projections:[personal(),tasks(),crypto({workspace_type:'ORG'})],workspace_type:'PERSONAL'});
const misCb=byCap(mis).CRYPTOBOT_PORTFOLIO;check(misCb.state==='CONTEXT_MISMATCH'&&misCb.predicate==='PROJECTION_WORKSPACE_TYPE_MISMATCH'&&misCb.rows_withheld===true,'workspace_type disagreement withholds rows: '+JSON.stringify(misCb));
const gone=P.build({descriptors:descs,statuses:forgedStatus,projections:[personal(),tasks()],workspace_type:'PERSONAL'});check(byCap(gone).CRYPTOBOT_PORTFOLIO.predicate==='PROJECTION_SOURCE_NOT_FOUND'&&byCap(gone).CRYPTOBOT_PORTFOLIO.rows_withheld===true,'status without a matching projection withholds rows');

// 6. Source scope: the panel contract reads projections only; no I/O, storage, registration or authority words.
check(!/fetch\(|XMLHttpRequest|localStorage|sessionStorage|indexedDB|registerDevice|navigator\./.test(panelsSrc),'panels contract must not perform I/O or registration');
check(!/disposition:"ALLOW"[^}]*rows:/.test(panelsSrc)&&(panelsSrc.match(/"ALLOW"/g)||[]).length===1,'ALLOW appears only as the bundle disposition');
check(/action_eligible:false/.test(panelsSrc)&&/authority_effect:"NONE"/.test(panelsSrc),'panels declare action_eligible false and authority NONE');

// 7. Page integration: script order, responsive row layout, workflow coverage, bridge seam.
check(page.indexOf('<script src="assets/workspace-search.js"></script>')<page.indexOf('<script src="assets/workspace-panels.js"></script>')&&page.indexOf('<script src="assets/workspace-panels.js"></script>')<page.indexOf('<script src="assets/workspace.js"></script>'),'panels script loads after search and before the page script');
check(/\.panel-rows\{display:grid;gap:6px;margin:8px 0;min-width:0\}\.panel-row\{[^}]*min-width:0[^}]*overflow-wrap:anywhere[^}]*\}/.test(css),'panel rows must shrink and wrap on phone widths');
check(workflow.includes('assets/workspace-panels.js')&&workflow.includes('tests/workspace-panels.test.cjs')&&workflow.includes('node --check assets/workspace-panels.js')&&workflow.includes('node tests/workspace-panels.test.cjs'),'workflow validates and runs the panels contract');
check(ui.includes('typeof bridge.loadPersonalProjections!=="function"')&&ui.includes('state.extraProjections=[]')&&ui.includes('.concat(state.extraProjections)'),'extra projections only through the bridge seam; absent -> none');
check(ui.includes('PANEL_CONTRACT_UNAVAILABLE'),'page names the fallback when the panel contract is not loaded');

// 8. UI harness: the capabilities card renders the panels from projections delivered by bridge.loadPersonalProjections.
const ids=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities','searchResults','tasks'];
function harness(opts){const els={};ids.forEach(i=>els[i]={id:i,innerHTML:'',textContent:'',className:'',value:'',dataset:{},attrs:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},classList:{add(){},remove(){}},listeners:{},addEventListener(t,f){this.listeners[t]=f},scrollIntoView(){}});
  const docListeners={};const bridge=Object.assign({loadPersonalWorkspace:()=>Promise.resolve(live(personal())),loadPersonalTasks:()=>Promise.resolve(live(tasks())),lastNodeBinding:()=>null},opts.bridge||{});
  const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener:(t,f)=>{docListeners[t]=f}},console,fetch:()=>Promise.resolve({json:()=>Promise.resolve(bootstrap)}),window:{StegVerseWorkspaceKVBridge:bridge}};
  vm.createContext(ctx);vm.runInContext(caps,ctx);vm.runInContext(search,ctx);ctx.window.StegVerseWorkspaceCapabilities=ctx.StegVerseWorkspaceCapabilities;ctx.window.StegVerseWorkspaceSearch=ctx.StegVerseWorkspaceSearch;
  if(opts.panels!==false){vm.runInContext(panelsSrc,ctx);ctx.window.StegVerseWorkspacePanels=ctx.StegVerseWorkspacePanels;}
  vm.runInContext(ui,ctx);return {els,switchTo:v=>els.workspaceSwitch.listeners.change({target:{value:v}})};}
// The page evaluates freshness against the real clock, so harness projections are stamped relative to now.
const live=(p)=>{p.projection_metadata.observed_at=new Date(Date.now()-60000).toISOString().replace(/\.\d{3}Z$/,'Z');return p;};
(async()=>{
  const wait=()=>new Promise(r=>setTimeout(r,10));
  let h=harness({bridge:{loadPersonalProjections:()=>Promise.resolve([live(crypto())])}});await wait();
  let html=h.els.capabilities.innerHTML;
  check(html.includes('CryptoBot portfolio (read-only)')&&html.includes('<div class="panel-rows">')&&html.includes('<strong>BTC</strong>')&&html.includes('value UNAVAILABLE')&&html.includes('2 malformed row(s) skipped (MALFORMED_ROW_SKIPPED)')&&html.includes('drawdown UNAVAILABLE')&&html.includes('provenance kv-cryptobot-portfolio-source:sha256:'+REV)&&html.includes('action_eligible: false'),'capabilities card renders the cryptobot panel: '+html.slice(0,600));
  check(html.includes('Producer: StegVerse-Labs/.github#3012'),'governance panel names its producer');
  check(html.includes('Review aurora release')&&html.includes('Send Alice the draft')&&html.includes('row(s) rendered in the Feed card'),'tasks/commitments rows and rendered-elsewhere notes present');
  // Panels expose no action controls. The only buttons allowed are the explain-on-request "Why?" buttons
  // (data-explain-capability), which open the non-authoritative explanation card and carry no action attributes.
  check(!/data-action|data-task-action/.test(html)&&(html.match(/<button\b[^>]*>/g)||[]).length>0&&(html.match(/<button\b[^>]*>/g)||[]).every(b=>/^<button type="button" class="why" data-explain-capability="[A-Z_]+" aria-label="Why\?">$/.test(b)),'panels expose no action controls (only explain-on-request Why? buttons)');
  h.switchTo('ORG');html=h.els.capabilities.innerHTML;
  check(!html.includes('<strong>BTC</strong>')&&!html.includes('Review aurora release')&&!html.includes('<div class="panel-rows">'),'ORG context renders no personal rows: '+html.slice(0,400));
  // Forged trade authority renders no rows, only the predicate.
  h=harness({bridge:{loadPersonalProjections:()=>Promise.resolve([live(crypto({trade_authority_granted:true}))])}});await wait();html=h.els.capabilities.innerHTML;
  check(html.includes('PROJECTION_TRADE_AUTHORITY_INVALID')&&html.includes('MALFORMED')&&!html.includes('<strong>BTC</strong>'),'forged trade authority fails closed in the card: '+html.slice(0,400));
  // Seam absent, rejecting or returning garbage -> NOT_OBSERVED, never a guessed row.
  for(const bridge of [{},{loadPersonalProjections:()=>Promise.reject(new Error('no'))},{loadPersonalProjections:()=>Promise.resolve('junk')},{loadPersonalProjections:()=>Promise.resolve([null,'x',{schema:'other/v1'}])}]){h=harness({bridge});await wait();html=h.els.capabilities.innerHTML;check(html.includes('CryptoBot portfolio (read-only)')&&html.includes('NOT_OBSERVED')&&!html.includes('<strong>BTC</strong>'),'absent/invalid projections delivery must stay NOT_OBSERVED: '+Object.keys(bridge));}
  // Panel contract not loaded -> status-only fallback that names the predicate and renders no rows.
  h=harness({panels:false,bridge:{loadPersonalProjections:()=>Promise.resolve([live(crypto())])}});await wait();html=h.els.capabilities.innerHTML;
  check(html.includes('PANEL_CONTRACT_UNAVAILABLE')&&html.includes('CryptoBot portfolio (read-only)')&&html.includes('OBSERVED')&&!html.includes('<div class="panel-rows">')&&!html.includes('BTC'),'missing panel contract falls back to status only: '+html.slice(0,400));
  console.log('WORKSPACE_PANELS_PASS assertions='+n);
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
