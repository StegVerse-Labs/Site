// Site#1509 lane B (Goal StegVerse-org/.github#164): the existing WORKSPACE_FAMILY_PROJECTIONS consumer carries
// email-family projections; no email-specific query class is added. The consumer refuses any delivery that holds
// credential-shaped material (only skap:// references may appear), fails closed on an absent or stale ADMIT receipt,
// never mixes accounts, refuses a message repeated in one account, and every refusal carries the six actionable fields.
// The panel contract renders a multi-account email view with per-account source and receipt provenance once a
// descriptor binds EMAIL to the email schema; the shipped bootstrap does not bind it yet, so EMAIL stays UNAVAILABLE.
// Evidence class: SOURCE + LOCAL_TEST only. No network, credentials, provider read or runtime claim.
const fs=require('fs');const path=require('path');const vm=require('vm');const nodeCrypto=require('crypto');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const bridgeSrc=read('assets/workspace-kv-bridge.js'),nodeBindingSrc=read('assets/workspace-node-binding.js'),capsSrc=read('assets/workspace-capabilities.js'),panelsSrc=read('assets/workspace-panels.js');
const bootstrap=JSON.parse(read('data/workspace/bootstrap.json'));
function assert(ok,msg){if(!ok)throw new Error(msg)}
let n=0;const check=(ok,msg)=>{n++;assert(ok,msg)};
const sha=(s)=>nodeCrypto.createHash('sha256').update(s,'utf8').digest('hex');
const REV='c'.repeat(64);
const EMAIL_SCHEMA='stegverse.kv.email-projection/v1';
const meta=(extra)=>Object.assign({schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:'2026-10-28T11:59:00Z',observed_at_semantics:'KV_PROJECTION_PRODUCTION_TIME',source_revision:REV,provenance_ref:'kv-email-projection:sha256:'+REV,workspace_type:'PERSONAL',workspace_id:null,owner_principal_id:null,grant_state:'UNKNOWN',revocation_epoch:null,authority_effect:'NONE'},extra||{});
const clone=(v)=>JSON.parse(JSON.stringify(v));
function account(id,extra){const cursor='cursor-'+id+'-7';return Object.assign({account_id:id,source:{provider:'gmail',adapter:'StegAgents src/gmail_readonly_adapter.py',cursor:cursor},credential_ref:'skap://vault/email/'+id,
  admit_receipt:{receipt_ref:'cvk-email-admit:'+id+':7',receipt_digest:'sha256:'+sha('receipt-'+id),cursor:cursor,admitted_at:'2026-10-28T11:58:00Z'},
  messages:[{message_id:'m-1',account_id:id,subject:'Hello from '+id,from:'sender@example.invalid',received_at:'2026-10-28T11:00:00Z'},{message_id:'m-2',account_id:id,subject:'Second for '+id,from:null,received_at:null}]},extra||{});}
const email=(extra)=>Object.assign({schema:EMAIL_SCHEMA,workspace_type:'PERSONAL',accounts:[account('acct-personal'),account('acct-work')],credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,projection_metadata:meta(),authority_effect:'NONE'},extra||{});
const portfolio=(extra)=>Object.assign({schema:'stegverse.kv.cryptobot-portfolio-projection/v1',workspace_type:'PERSONAL',portfolio:{positions:[],total_value_usd:0,drawdown_percent:null,source_observed_at:'2026-10-28T11:58:00Z',provider:'coinbase',unavailable_fields:{}},source:{authority:'StegVerse-Labs/TVC'},credential_material_present:false,provider_operation_authorized:false,trade_authority_granted:false,workspace_grants_authority:false,projection_metadata:meta({provenance_ref:'cryptobot-portfolio-snapshot:sha256:'+REV}),authority_effect:'NONE'},extra||{});
const familyDelivery=(projections,extra)=>Object.assign({schema:'stegverse.kv.workspace-family-projections/v1',state:'KV_FAMILY_PROJECTIONS_PROJECTED',workspace_type:'PERSONAL',projections:projections,projection_schemas:projections.map(p=>p&&p.schema),credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,action_authority:'NONE',projection_metadata:meta(),authority_effect:'NONE'},extra||{});
const NODE='SV-NODE-'+'a'.repeat(24);
const registered={registered:true,state:'REGISTERED',registration:{node_id:NODE,interlock_id:'SV-IL-'+'b'.repeat(24)},receipts:[{}]};
// Same full-path harness as tests/workspace-delivery-seams.test.cjs: stubs serve the projection back through the
// delivery / HB-return shape the bridge verifies. No network: fetch is a local stub.
function harness(serve){const seen={queries:[],targets:[],materializations:[]};const canonical=(v)=>JSON.stringify(v);
  const ctx={crypto:globalThis.crypto,TextEncoder,TextDecoder,setTimeout,
    fetch:(url,init)=>{const lookup=JSON.parse(init.body);const m=seen.materializations.find(x=>x.materialization_id===lookup.materialization_id);const q=m.query;
      const response={schema:'stegverse.device-kv.query-response/v1',state:'QUERY_COMPLETE',record_class:q.record_class,query_request_id:q.request_id,request_grants_authority:false,response_grants_authority:false,authority_effect:'NONE',projection:serve(q)};
      const text=canonical(response);return Promise.resolve({status:200,json:()=>Promise.resolve({schema:'stegverse.device-kv.query-result-delivery/v1',state:'RESULT_AVAILABLE',materialization_id:m.materialization_id,request_hash:m.request_hash,node_id:NODE,authority_effect:'NONE_RESULT_DELIVERY_ONLY',result_lookup_grants_authority:false,response,response_payload_hash:sha(text),response_carrier_signal:text})});},
    StegVerseGeneratedInTr:{canonical,buildIntent:(k,bytes,op,id)=>Promise.resolve({packet_id:'pkt-'+id,payload_hash:sha(new TextDecoder().decode(bytes))}),buildMaterializationRequest:(k,i,r,b,extra)=>{const q=extra.kv_request;seen.queries.push(q);const m={materialization_id:'mat-'+q.request_id,request_hash:sha(canonical(q)),query:q};seen.materializations.push(m);return Promise.resolve(m);},sha256Bytes:(bytes)=>Promise.resolve(sha(new TextDecoder().decode(bytes)))},
    StegVerseHBInTrCarrier:{buildBinding:()=>Promise.resolve({}),recoverSignal:(signal)=>Promise.resolve(new TextEncoder().encode(signal))},
    StegVerseNodeContinuity:{status:()=>Promise.resolve(registered),registerDevice(){throw new Error('page must not register');},queueIntrMaterializationRequest:()=>Promise.resolve()},
    StegVerseDeviceKVInTrSync:{synchronizeMaterialization:()=>Promise.resolve(),loadTarget:(cls)=>{seen.targets.push(cls);return Promise.resolve({state:'CONFORMING_SOVEREIGN_INTR_INGRESS',result_url:'https://ingress.invalid/intr/device-kv/result'});},getDeliveryReceipt:()=>Promise.resolve({network_delivery_observed:true})}};
  vm.createContext(ctx);vm.runInContext(nodeBindingSrc,ctx);vm.runInContext(bridgeSrc,ctx);return {bridge:ctx.StegVerseWorkspaceKVBridge,seen};}
const load=(delivery)=>harness(()=>delivery).bridge.loadPersonalProjections({recovery_result:null});
const SIX=['failure_code','failed_predicate','required_evidence_or_repair','retry_entrypoint','owning_existing_goal','next_attempt'];
async function refuses(delivery,predicate,name,forbiddenText){
  const err=await load(delivery).then(()=>null,e=>e);
  check(err&&err.message==='FAIL_CLOSED: '+predicate,name+': expected '+predicate+', got '+(err&&err.message));
  const d=err.decision;
  check(d&&d.disposition==='FAIL_CLOSED'&&d.predicate===predicate&&d.failure_code===predicate&&d.failed_predicate===predicate&&d.authority_effect==='NONE','six-field decision for '+name+': '+JSON.stringify(d));
  for(const k of SIX)check(typeof d[k]==='string'&&d[k].trim().length>0,name+' carries '+k);
  check(/loadPersonalProjections/.test(d.retry_entrypoint)&&d.owning_existing_goal==='STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001'&&/nothing waits/.test(d.next_attempt),name+' names the family entrypoint, existing goal and a no-wait next attempt');
  if(forbiddenText)check(!JSON.stringify(d).includes(forbiddenText)&&!err.message.includes(forbiddenText),name+' never echoes the secret value');
  return d;
}
(async()=>{
  // 1. The existing family class carries email projections; no new query class.
  let h=harness(()=>familyDelivery([portfolio(),email()]));
  check(JSON.stringify(h.bridge.record_classes)==='["WORKSPACE_PERSONAL_PROJECTION","WORKSPACE_TASKS_PROJECTION","WORKSPACE_FAMILY_PROJECTIONS","WORKSPACE_CONTINUITY_CHECKPOINT"]','no email-specific record class is added');
  const list=await h.bridge.loadPersonalProjections({recovery_result:null});
  check(Array.isArray(list)&&list.length===2&&list[1].schema===EMAIL_SCHEMA&&list[1].accounts.length===2,'email projection delivered through WORKSPACE_FAMILY_PROJECTIONS');
  check(h.seen.queries.length===1&&h.seen.queries[0].record_class==='WORKSPACE_FAMILY_PROJECTIONS'&&JSON.stringify(h.seen.queries[0].requested_scope)==='["projections"]'&&h.seen.targets.join()==='WORKSPACE_FAMILY_PROJECTIONS','one bounded family query, one target');
  check(list[1].accounts.every(a=>/^skap:\/\//.test(a.credential_ref)),'skap:// credential references are accepted as references');
  // A message id may recur across different accounts (separate mailboxes); it is a duplicate only within one account.
  check((await load(familyDelivery([email({accounts:[account('acct-a'),account('acct-b')]})])))[0].accounts[1].messages[0].message_id==='m-1','same message id in two separate accounts is not a duplicate');
  check((await load(familyDelivery([email({accounts:[account('acct-a',{messages:[]})]})])))[0].accounts[0].messages.length===0,'account with no admitted messages is valid');

  // 2. No secrets: credential-shaped keys at any depth, in any family projection, refuse the whole delivery.
  const SECRET='s3cr3t-value-never-shown';
  const secretKeys=['password','passwd','token','access_token','refresh_token','id_token','session_token','oauth','oauth_token','oauthToken','refreshToken','client_secret','api_key','apiKey','private_key','authorization','cookie','raw_credential','credentials','totp_seed'];
  for(const key of secretKeys){
    await refuses(familyDelivery([email({accounts:[account('acct-a',{[key]:SECRET})]})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','account-level '+key,SECRET);
  }
  await refuses(familyDelivery([email({accounts:[account('acct-a',{messages:[{message_id:'m-1',account_id:'acct-a',subject:'x',headers:{Authorization:SECRET}}]})]})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','nested message header',SECRET);
  await refuses(familyDelivery([email({accounts:[account('acct-a',{source:{provider:'gmail',cursor:'cursor-acct-a-7',oauth:{refresh_token:SECRET}}})]})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','oauth block in source',SECRET);
  await refuses(familyDelivery([email({accounts:[account('acct-a',{credential_ref:'https://provider.invalid/token?x='+SECRET})]})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','non-skap credential reference',SECRET);
  await refuses(familyDelivery([email({accounts:[account('acct-a',{credential_ref:SECRET})]})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','raw credential in credential_ref',SECRET);
  await refuses(familyDelivery([email({accounts:[account('acct-a',{credential_material_present:true})]})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','nested credential flag set true');
  await refuses(familyDelivery([email({accounts:[account('acct-a',{messages:[{message_id:'m-1',account_id:'acct-a',subject:'Bearer '+SECRET}]})]})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','bearer token in a value',SECRET);
  await refuses(familyDelivery([email({accounts:[account('acct-a',{messages:[{message_id:'m-1',account_id:'acct-a',subject:'k',snippet:'-----BEGIN RSA PRIVATE KEY-----'+SECRET}]})]})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','private key in a value',SECRET);
  await refuses(familyDelivery([portfolio({source:{authority:'StegVerse-Labs/TVC',api_key:SECRET}})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','secret in a non-email family projection',SECRET);
  await refuses(familyDelivery([email()],{refresh_token:SECRET}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','secret on the delivery envelope',SECRET);
  {const d=await refuses(familyDelivery([email({accounts:[account('acct-a',{refresh_token:SECRET})]})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','secret path');check(d.secret_path==='$.projections[0].accounts[0].refresh_token','refusal names the key path only: '+d.secret_path);}
  {let deep={};const top=deep;for(let i=0;i<40;i++){deep.next={};deep=deep.next;}await refuses(familyDelivery([email({accounts:[account('acct-a',{extra:top})]})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','nesting beyond the scan bound fails closed');}
  // A projection that declares credential material is refused with the six actionable fields.
  await refuses(familyDelivery([email({credential_material_present:true})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','projection declaring credential material');
  {const err=await load(familyDelivery([email()],{credential_material_present:'false'})).then(()=>null,e=>e);check(err&&/delivery authority invalid/.test(err.message),'non-boolean credential flag on the envelope keeps the existing envelope refusal');}

  // 3. Absent or stale ADMIT receipt fails closed.
  const noReceipt=account('acct-a');delete noReceipt.admit_receipt;
  await refuses(familyDelivery([email({accounts:[account('acct-ok'),noReceipt]})]),'EMAIL_PROJECTION_ADMIT_RECEIPT_ABSENT','absent receipt');
  await refuses(familyDelivery([email({accounts:[account('acct-a',{admit_receipt:null})]})]),'EMAIL_PROJECTION_ADMIT_RECEIPT_ABSENT','null receipt');
  for(const [k,v] of [['receipt_ref',''],['receipt_digest','sha256:'+'z'.repeat(64)],['receipt_digest','f'.repeat(64)],['cursor',undefined]]){
    const a=account('acct-a');if(v===undefined)delete a.admit_receipt[k];else a.admit_receipt[k]=v;
    await refuses(familyDelivery([email({accounts:[a]})]),'EMAIL_PROJECTION_ADMIT_RECEIPT_ABSENT','receipt without valid '+k);
  }
  {const a=account('acct-a');a.admit_receipt.cursor='cursor-acct-a-6';await refuses(familyDelivery([email({accounts:[a]})]),'EMAIL_PROJECTION_ADMIT_RECEIPT_STALE','receipt covering an older cursor');}
  {const a=account('acct-a');a.admit_receipt.cursor=account('acct-b').source.cursor;await refuses(familyDelivery([email({accounts:[a,account('acct-b')]})]),'EMAIL_PROJECTION_ADMIT_RECEIPT_STALE','receipt borrowed from another account cursor');}

  // 4. Account separation.
  await refuses(familyDelivery([email({accounts:[account('acct-a',{messages:[{message_id:'m-1',account_id:'acct-b',subject:'x'}]}),account('acct-b')]})]),'EMAIL_PROJECTION_ACCOUNTS_MIXED','message bound to another account');
  await refuses(familyDelivery([email({accounts:[account('acct-a',{messages:[{message_id:'m-1',subject:'x'}]})]})]),'EMAIL_PROJECTION_ACCOUNTS_MIXED','message without an account binding');
  await refuses(familyDelivery([email({accounts:[account('acct-a'),account('acct-a')]})]),'EMAIL_PROJECTION_ACCOUNTS_MIXED','account named twice');
  for(const [name,acc] of [['accounts not a list',null],['account without id',[account('')]],['account without cursor',[account('acct-a',{source:{provider:'gmail'}})]],['account without provider',[account('acct-a',{source:{cursor:'cursor-acct-a-7'}})]],['account without messages list',[account('acct-a',{messages:'none'})]],['message without id',[account('acct-a',{messages:[{account_id:'acct-a',subject:'x'}]})]]]){
    await refuses(familyDelivery([email({accounts:acc})]),'EMAIL_PROJECTION_ACCOUNT_INVALID',name);
  }

  // 5. Replayed / duplicate records: never deduplicated silently.
  await refuses(familyDelivery([email({accounts:[account('acct-a',{messages:[{message_id:'m-1',account_id:'acct-a',subject:'x'},{message_id:'m-1',account_id:'acct-a',subject:'x'}]})]})]),'EMAIL_PROJECTION_RECORD_DUPLICATED','message repeated in one account');
  {const err=await load(familyDelivery([email(),email()])).then(()=>null,e=>e);check(err&&/schema ambiguous/.test(err.message),'a replayed second email projection in one delivery is refused as ambiguous');}
  // Other email-family schema spellings are held to the same rules; non-email families are not.
  await refuses(familyDelivery([email({schema:'stegverse.kv.email-account-projection/v1',accounts:[noReceipt]})]),'EMAIL_PROJECTION_ADMIT_RECEIPT_ABSENT','email-account-projection schema spelling');
  check((await load(familyDelivery([portfolio()])))[0].schema==='stegverse.kv.cryptobot-portfolio-projection/v1','CryptoBot projection unaffected by the email rules');

  // 6. Rendering. Shipped bootstrap: EMAIL has no KV projection contract, so a delivered email projection renders nothing
  // and does not disturb the CryptoBot panel.
  const cctx={};cctx.globalThis=cctx;vm.createContext(cctx);vm.runInContext(capsSrc,cctx);vm.runInContext(panelsSrc,cctx);
  const C=cctx.StegVerseWorkspaceCapabilities,P=cctx.StegVerseWorkspacePanels,NOW=Date.parse('2026-10-28T12:00:00Z');
  const shipped=bootstrap.capability_descriptors;const projs=[portfolio(),email()];
  let st=C.evaluateAll(shipped,projs,'PERSONAL',NOW);let panels=P.build({descriptors:shipped,statuses:st,projections:projs,workspace_type:'PERSONAL'}).panels;
  const byCap=(list)=>Object.fromEntries(list.map(x=>[x.capability,x]));
  check(byCap(st).EMAIL.state==='UNAVAILABLE'&&byCap(st).EMAIL.predicate==='NO_KV_PROJECTION_CONTRACT'&&byCap(panels).EMAIL.rows.length===0&&byCap(panels).EMAIL.rows_withheld===true,'shipped EMAIL descriptor stays UNAVAILABLE; no email rows render without a descriptor binding');
  check(byCap(st).CRYPTOBOT_PORTFOLIO.state==='OBSERVED','CryptoBot status unaffected by a delivered email projection');
  // With EMAIL bound to the email schema (the binding the descriptor owner adds once the CVK schema is ratified),
  // the panel renders each account separately with its own source and receipt provenance.
  const bound=shipped.map(d=>d.capability==='EMAIL'?Object.assign({},d,{allowed_projection_schemas:[EMAIL_SCHEMA],projection_field:'accounts',workspace_types:['PERSONAL'],max_age_seconds:3600}):d);
  check(C.descriptorProblem(bound.find(d=>d.capability==='EMAIL'))===null,'bound EMAIL descriptor is a valid non-asserting descriptor');
  st=C.evaluateAll(bound,projs,'PERSONAL',NOW);panels=P.build({descriptors:bound,statuses:st,projections:projs,workspace_type:'PERSONAL'}).panels;
  const ep=byCap(panels).EMAIL;
  check(ep.state==='OBSERVED'&&ep.rows_withheld===false&&ep.action_eligible===false&&ep.authority_effect==='NONE'&&ep.provenance.provenance_ref==='kv-email-projection:sha256:'+REV&&ep.provenance.replay_status==='REPLAY_STATUS_UNKNOWN','email panel observed, informational only, projection provenance and replay UNKNOWN: '+JSON.stringify(ep.provenance));
  check(ep.rows.length===6&&ep.malformed_rows===0,'two account rows plus two message rows each: '+ep.rows.length);
  for(const id of ['acct-personal','acct-work']){
    const rows=ep.rows.filter(r=>r.account_id===id),head=rows[0],receipt=account(id).admit_receipt;
    check(rows.length===3&&head.label===id&&head.detail.includes('provider gmail')&&head.detail.includes('cursor cursor-'+id+'-7')&&head.detail.includes(receipt.receipt_ref)&&head.detail.includes(receipt.receipt_digest)&&head.detail.includes('2 message(s)'),'per-account provenance row for '+id+': '+JSON.stringify(head));
    check(rows.slice(1).every(r=>r.detail.startsWith('account '+id)),'message rows name their own account: '+id);
    const other=id==='acct-personal'?'acct-work':'acct-personal';
    check(rows.every(r=>!r.detail.includes(other)&&!r.label.includes(other)),'rows of '+id+' carry nothing from '+other);
  }
  check(!JSON.stringify(ep).includes('skap://'),'credential references are never displayed');
  check(ep.notes.some(x=>/never merged/.test(x))&&ep.notes.some(x=>/SKAP Vault/.test(x)),'panel notes state account separation and SKAP custody');
  // Panel re-checks independently of the bridge (a projection that did not come through it).
  const panelFor=(proj)=>byCap(P.build({descriptors:bound,statuses:C.evaluateAll(bound,[proj],'PERSONAL',NOW),projections:[proj],workspace_type:'PERSONAL'}).panels).EMAIL;
  {const p=panelFor(email({accounts:[account('acct-a',{messages:[{message_id:'m-1',account_id:'acct-b',subject:'x'}]}),account('acct-b')]}));check(p.state==='MALFORMED'&&p.predicate==='EMAIL_ACCOUNTS_MIXED'&&p.rows.length===0&&p.rows_withheld,'panel refuses a cross-account message');}
  {const p=panelFor(email({accounts:[account('acct-a'),account('acct-a')]}));check(p.state==='MALFORMED'&&p.predicate==='EMAIL_ACCOUNTS_MIXED'&&p.rows.length===0,'panel refuses a repeated account');}
  {const p=panelFor(email({accounts:{}}));check(p.state==='MALFORMED'&&p.predicate==='EMAIL_ACCOUNTS_INVALID'&&p.rows.length===0,'panel refuses a non-list accounts field');}
  {const p=panelFor(email({accounts:[noReceipt,account('acct-b')]}));check(p.state==='OBSERVED'&&p.malformed_rows===3&&p.rows.every(r=>r.account_id==='acct-b')&&p.rows.length===3,'panel withholds an account without receipt and its messages: '+JSON.stringify(p.rows));}
  {const p=panelFor(email({accounts:[account('acct-a',{messages:[{message_id:'m-1',account_id:'acct-a',subject:'hid‮den'}]})]}));check(p.malformed_rows===1&&p.rows.length===1,'hidden-character subject is counted malformed, not shown');}
  // Stale projection: rows stay visible but labelled STALE (capability contract), never OBSERVED.
  {const proj=email({projection_metadata:meta({observed_at:'2026-10-28T10:00:00Z'})});const p=panelFor(proj);check(p.state==='STALE'&&p.provenance.age_seconds===7200,'stale email projection labelled STALE');}
  // Org context never receives the personal email projection.
  {const p=byCap(P.build({descriptors:bound,statuses:C.evaluateAll(bound,projs,'ORGANIZATIONAL',NOW),projections:projs,workspace_type:'ORGANIZATIONAL'}).panels).EMAIL;check(p.rows.length===0&&p.rows_withheld,'personal email projection never renders in an org context');}
  console.log('WORKSPACE_EMAIL_FAMILY_CONSUMER_PASS assertions='+n);
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
