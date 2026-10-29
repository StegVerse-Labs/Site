// Site#1509 lane B (Goal StegVerse-org/.github#164): the existing WORKSPACE_FAMILY_PROJECTIONS consumer carries the lane A
// email-family projection (continuity-vault-kit runtime/email_family_projection.py, stegverse.kv.email-family-projection/v1,
// PR #278); no email-specific query class is added. Fixture: tests/fixtures/email-family-projection-lane-a.json, the
// producer's verbatim output (its source commit and producer sha256 are recorded in the fixture).
// Checks: credential-shaped keys/values are refused (NFKC, confusables, unanchored values); an absent or stale ADMIT
// receipt (cursor head / chain / sequence recomputed as the producer defines them) fails closed; accounts are never mixed;
// duplicates and replays are refused; projection_digest drift is refused; a failure inside the email projection withholds
// only that projection (CryptoBot stays deliverable); every refusal carries the six actionable fields; the panel renders a
// multi-account view with per-mapping provenance. Evidence class: SOURCE + LOCAL_TEST only.
const fs=require('fs');const path=require('path');const vm=require('vm');const nodeCrypto=require('crypto');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const bridgeSrc=read('assets/workspace-kv-bridge.js'),nodeBindingSrc=read('assets/workspace-node-binding.js'),capsSrc=read('assets/workspace-capabilities.js'),panelsSrc=read('assets/workspace-panels.js');
const bootstrap=JSON.parse(read('data/workspace/bootstrap.json'));
const FIX=JSON.parse(read('tests/fixtures/email-family-projection-lane-a.json'));
function assert(ok,msg){if(!ok)throw new Error(msg)}
let n=0;const check=(ok,msg)=>{n++;assert(ok,msg)};
const sha=(s)=>nodeCrypto.createHash('sha256').update(s,'utf8').digest('hex');
const canon=v=>Array.isArray(v)?'['+v.map(canon).join(',')+']':v&&typeof v==='object'?'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canon(v[k])).join(',')+'}':JSON.stringify(v);
const pysha=v=>'sha256:'+sha(canon(v));
const clone=v=>JSON.parse(JSON.stringify(v));
const EMAIL_SCHEMA='stegverse.kv.email-family-projection/v1';
const [MB,MA]=FIX.projection.accounts.map(a=>a.mapping_id); // producer sorts accounts by mapping_id
// Re-seal a mutated projection the way the producer would (chains, cursors, digest), so a test reaches the guard it targets.
function reseal(p,{chains=true,digest=true}={}){if(chains)for(const a of p.accounts){const rows=p.messages.filter(m=>m.mapping_id===a.mapping_id);let h=null;rows.forEach(m=>{h=pysha({previous:h,receipt_id:m.receipt_id});});a.cursor.chain_digest=h;}if(digest){p.projection_digest=pysha({schema:p.schema,workspace_type:p.workspace_type,accounts:p.accounts,messages:p.messages});p.projection_metadata.provenance_ref='kv-email-ingress-admit-receipts:'+p.projection_digest;p.projection_metadata.source_revision=p.projection_digest.slice(7);}return p;}
const email=(mutate)=>{const p=clone(FIX.projection);if(mutate)mutate(p);return p;};
const meta=(extra)=>Object.assign({schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:'2026-10-28T23:40:00Z',observed_at_semantics:'KV_PROJECTION_PRODUCTION_TIME',source_revision:'c'.repeat(64),provenance_ref:'x:sha256:'+'c'.repeat(64),workspace_type:'PERSONAL',workspace_id:null,owner_principal_id:null,grant_state:'UNKNOWN',revocation_epoch:null,authority_effect:'NONE'},extra||{});
const portfolio=(extra)=>Object.assign({schema:'stegverse.kv.cryptobot-portfolio-projection/v1',workspace_type:'PERSONAL',portfolio:{positions:[],total_value_usd:0,drawdown_percent:null,source_observed_at:'2026-10-28T23:39:00Z',provider:'coinbase',unavailable_fields:{}},source:{authority:'StegVerse-Labs/TVC'},credential_material_present:false,provider_operation_authorized:false,trade_authority_granted:false,workspace_grants_authority:false,projection_metadata:meta(),authority_effect:'NONE'},extra||{});
const familyDelivery=(projections,extra)=>Object.assign({schema:'stegverse.kv.workspace-family-projections/v1',state:'KV_FAMILY_PROJECTIONS_PROJECTED',workspace_type:'PERSONAL',projections:projections,projection_schemas:projections.map(p=>p&&p.schema),credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,action_authority:'NONE',projection_metadata:meta(),authority_effect:'NONE'},extra||{});
const NODE='SV-NODE-'+'a'.repeat(24);
const registered={registered:true,state:'REGISTERED',registration:{node_id:NODE,interlock_id:'SV-IL-'+'b'.repeat(24)},receipts:[{}]};
// Same full-path harness as tests/workspace-delivery-seams.test.cjs; fetch is a local stub (no network). The response is
// serialized with JSON.stringify, so a "__proto__" key survives as an own property, as JSON.parse would deliver it.
function harness(serve){const seen={queries:[],targets:[],materializations:[]};const canonical=(v)=>JSON.stringify(v);
  const ctx={crypto:globalThis.crypto,TextEncoder,TextDecoder,setTimeout,
    fetch:(url,init)=>{const lookup=JSON.parse(init.body);const m=seen.materializations.find(x=>x.materialization_id===lookup.materialization_id);const q=m.query;
      const response={schema:'stegverse.device-kv.query-response/v1',state:'QUERY_COMPLETE',record_class:q.record_class,query_request_id:q.request_id,request_grants_authority:false,response_grants_authority:false,authority_effect:'NONE',projection:serve(q)};
      const text=canonical(response);return Promise.resolve({status:200,json:()=>Promise.resolve(JSON.parse(JSON.stringify({schema:'stegverse.device-kv.query-result-delivery/v1',state:'RESULT_AVAILABLE',materialization_id:m.materialization_id,request_hash:m.request_hash,node_id:NODE,authority_effect:'NONE_RESULT_DELIVERY_ONLY',result_lookup_grants_authority:false,response,response_payload_hash:sha(text),response_carrier_signal:text})))});},
    StegVerseGeneratedInTr:{canonical,buildIntent:(k,bytes,op,id)=>Promise.resolve({packet_id:'pkt-'+id,payload_hash:sha(new TextDecoder().decode(bytes))}),buildMaterializationRequest:(k,i,r,b,extra)=>{const q=extra.kv_request;seen.queries.push(q);const m={materialization_id:'mat-'+q.request_id,request_hash:sha(canonical(q)),query:q};seen.materializations.push(m);return Promise.resolve(m);},sha256Bytes:(bytes)=>Promise.resolve(sha(new TextDecoder().decode(bytes)))},
    StegVerseHBInTrCarrier:{buildBinding:()=>Promise.resolve({}),recoverSignal:(signal)=>Promise.resolve(new TextEncoder().encode(signal))},
    StegVerseNodeContinuity:{status:()=>Promise.resolve(registered),registerDevice(){throw new Error('page must not register');},queueIntrMaterializationRequest:()=>Promise.resolve()},
    StegVerseDeviceKVInTrSync:{synchronizeMaterialization:()=>Promise.resolve(),loadTarget:(cls)=>{seen.targets.push(cls);return Promise.resolve({state:'CONFORMING_SOVEREIGN_INTR_INGRESS',result_url:'https://ingress.invalid/intr/device-kv/result'});},getDeliveryReceipt:()=>Promise.resolve({network_delivery_observed:true})}};
  vm.createContext(ctx);vm.runInContext(nodeBindingSrc,ctx);vm.runInContext(bridgeSrc,ctx);return {bridge:ctx.StegVerseWorkspaceKVBridge,seen};}
const SIX=['failure_code','failed_predicate','required_evidence_or_repair','retry_entrypoint','owning_existing_goal','next_attempt'];
function sixFields(d,predicate,name){
  check(d&&d.disposition==='FAIL_CLOSED'&&d.predicate===predicate&&d.failure_code===predicate&&d.failed_predicate===predicate&&d.authority_effect==='NONE','six-field decision for '+name+': '+JSON.stringify(d));
  for(const k of SIX)check(typeof d[k]==='string'&&d[k].trim().length>0,name+' carries '+k);
  check(/loadPersonalProjections/.test(d.retry_entrypoint)&&d.owning_existing_goal==='STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001'&&/nothing waits/.test(d.next_attempt),name+' names the family entrypoint, existing goal and a no-wait next attempt');
}
// Whole-delivery refusal (envelope or non-email member).
async function refuses(delivery,predicate,name,forbidden){
  const h=harness(()=>delivery);const err=await h.bridge.loadPersonalProjections({recovery_result:null}).then(()=>null,e=>e);
  check(err&&err.message==='FAIL_CLOSED: '+predicate,name+': expected '+predicate+', got '+(err&&err.message));
  sixFields(err.decision,predicate,name);
  if(forbidden)check(!JSON.stringify(err.decision).includes(forbidden)&&!err.message.includes(forbidden),name+' never echoes the secret value');
  return err.decision;
}
// Email-member refusal: only the email projection is withheld; CryptoBot is still delivered.
async function withholds(emailProjection,predicate,name,forbidden){
  const h=harness(()=>familyDelivery([portfolio(),emailProjection]));
  const list=await h.bridge.loadPersonalProjections({recovery_result:null}).then(v=>v,e=>{throw new Error(name+': whole delivery refused: '+e.message);});
  check(list.length===1&&list[0].schema==='stegverse.kv.cryptobot-portfolio-projection/v1',name+': only the email projection is withheld: '+JSON.stringify(list.map(p=>p.schema)));
  const r=h.bridge.lastFamilyRefusals();
  check(r.length===1,name+': one refusal recorded: '+JSON.stringify(r));
  sixFields(r[0],predicate,name);
  check(r[0].projection_schema===emailProjection.schema,name+' names the withheld projection schema');
  if(forbidden)check(!JSON.stringify(r[0]).includes(forbidden),name+' never echoes the secret value');
  return r[0];
}
(async()=>{
  // 0. Fixture provenance and producer-defined digests recompute here.
  check(FIX.source.repository==='StegVerse-Labs/continuity-vault-kit'&&FIX.source.pull_request===278&&/^[0-9a-f]{40}$/.test(FIX.source.commit)&&FIX.source.commit==='3da1e4d9e63546a38c5cbeb4cf491acca1e9df68'&&!('transformed_to_contract_update' in FIX.source)&&FIX.source.producer_path==='runtime/email_family_projection.py'&&/^[0-9a-f]{64}$/.test(FIX.source.producer_sha256)&&FIX.source.runtime_evidence===false,'fixture names its producer source');
  check(FIX.projection.schema===EMAIL_SCHEMA&&FIX.projection.accounts.length===2&&FIX.projection.messages.length===5&&reseal(email()).projection_digest===FIX.projection.projection_digest&&JSON.stringify(reseal(email()).accounts)===JSON.stringify(FIX.projection.accounts),'fixture is self-consistent under the producer chain/digest definitions');

  // 1. The existing family class carries the producer output verbatim; no new query class.
  let h=harness(()=>familyDelivery([portfolio(),email()]));
  check(JSON.stringify(h.bridge.record_classes)==='["WORKSPACE_PERSONAL_PROJECTION","WORKSPACE_TASKS_PROJECTION","WORKSPACE_FAMILY_PROJECTIONS","WORKSPACE_CONTINUITY_CHECKPOINT"]','no email-specific record class is added');
  const list=await h.bridge.loadPersonalProjections({recovery_result:null});
  check(Array.isArray(list)&&list.length===2&&list[1].schema===EMAIL_SCHEMA&&list[1].projection_digest===FIX.projection.projection_digest&&h.bridge.lastFamilyRefusals().length===0,'producer output delivered through WORKSPACE_FAMILY_PROJECTIONS unchanged');
  check(h.seen.queries.length===1&&h.seen.queries[0].record_class==='WORKSPACE_FAMILY_PROJECTIONS'&&h.seen.targets.join()==='WORKSPACE_FAMILY_PROJECTIONS','one bounded family query, one target');
  // An account with no admitted rows yet (sequence 0, null head and chain) is valid.
  {const h2=harness(()=>familyDelivery([email(p=>{p.messages=p.messages.filter(m=>m.mapping_id!==MA);const a=p.accounts.find(a=>a.mapping_id===MA);a.cursor={sequence:0,head_receipt_id:null,chain_digest:null,provider_position:null,provider_cursor_ref:null};reseal(p);})]));check((await h2.bridge.loadPersonalProjections({recovery_result:null}))[0].messages.length===3,'account with no admitted rows is valid');}

  // 2. Secrets. Inside the email projection: only it is withheld. Elsewhere: the whole delivery is refused.
  const SECRET='s3cr3tValueNeverShown0123456789';
  const secretKeys=['seed','seed_phrase','wallet_seed','password','passwd','passphrase','pwd','token','access_token','accessToken','accesstoken','refresh_token','refreshToken','refreshtoken','authtoken','id_token','oauth','oauth_token','client_secret','clientsecret','api_key','apiKey','access_key','accessKey','private_key','signing_key','ssh_key','encryption_key','authorization','Authorization','cookie','raw_credential','credentials','jwt','totp_seed','mnemonic','token_count','tokens',
    'ｔｏｋｅｎ','tοken','to​ken','pass­word','sesѕion'];
  for(const key of secretKeys){
    const d=await withholds(email(p=>{p.accounts[0][key]=SECRET;}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','account key '+JSON.stringify(key),SECRET);
    // The repair text is a fixed sentence (it says "credentials stay in SKAP Vault"); only the located part is variable.
    const located=d.required_evidence_or_repair.split('(found at ')[1]||'';
    check(!d.secret_path.includes(key)&&!located.includes(key),'refusal never echoes the credential-named key '+JSON.stringify(key)+': '+d.secret_path);
  }
  await withholds(email(p=>{p.messages[2].headers={Authorization:SECRET};}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','nested message header',SECRET);
  for(const [name,value] of [['mid-string bearer','note: Bearer '+SECRET],['basic auth','x Basic dXNlcjpwYXNzd29yZA=='],['JWT','tok eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U'],['GitHub PAT','ghp_'+'A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8'],['fine-grained PAT','github_pat_'+'11ABCDEFG0123456789_abcdefghijklmnop'],['private key','x -----BEGIN OPENSSH PRIVATE KEY-----'],['fullwidth bearer','Ｂｅａｒｅｒ '+SECRET],['zero-width bearer','Bea​rer '+SECRET]]){
    await withholds(email(p=>{p.messages[0].note=value;}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','secret value: '+name,SECRET);
  }
  for(const bad of ['https://provider.invalid/x?k='+SECRET,SECRET,'skap://']){
    await withholds(email(p=>{p.accounts[1].skap_ref=bad;reseal(p);}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','non-skap reference '+JSON.stringify(bad).slice(0,24),SECRET);
  }
  await withholds(email(p=>{p.accounts[0].credential_material_present=true;}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','nested credential flag set true');
  {const d=await withholds(email(p=>{p.accounts[1].refresh_token=SECRET;}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','secret path');check(d.secret_path==='$.projections[1].accounts[1].[redacted]'&&!JSON.stringify(d).includes('refresh_token'),'refusal names the path with the credential-named key redacted: '+d.secret_path);}
  {const d=await withholds(email(p=>{p.accounts[0]['tοken']=SECRET;}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','confusable key path');check(d.secret_path.endsWith('<non-ASCII key>')&&!d.secret_path.includes('ο'),'a non-ASCII key is named without echoing it: '+d.secret_path);}
  {let deep={};const top=deep;for(let i=0;i<40;i++){deep.next={};deep=deep.next;}await withholds(email(p=>{p.accounts[0].extra=top;}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','nesting beyond the scan bound');}
  // Credential-shaped keys (a token used as a key) are found and never echoed, in any member.
  const GHP='ghp_'+'A'.repeat(36),JWT='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.c2lnbmF0dXJlMTIz';
  for(const k of [GHP,JWT,'Bearer '+SECRET,'github_pat_'+'B'.repeat(30)]){
    const d=await withholds(email(p=>{p.accounts[0].cursor[k]=1;}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','credential-shaped key '+k.slice(0,6)+' in the email projection',k);
    check(/\.(\[redacted\]|<non-ASCII key>)$/.test(d.secret_path),'credential-shaped key path redacted: '+d.secret_path);
    const e=await refuses(familyDelivery([portfolio({portfolio:Object.assign(portfolio().portfolio,{unavailable_fields:{[k]:'x'}})}),email()]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','credential-shaped key '+k.slice(0,6)+' in a non-email member',k);
    check(/\.(\[redacted\]|<non-ASCII key>)$/.test(e.secret_path),'non-email credential-shaped key path redacted: '+e.secret_path);
  }
  {const e=await refuses(familyDelivery([email()],{[GHP]:{nested:true}}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','credential-shaped key on the envelope',GHP);}
  // An ancestor key that is fine stays readable; only the offending segment is redacted.
  {const d=await withholds(email(p=>{p.accounts[0].cursor.extra={api_key:SECRET};}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','nested key path');check(d.secret_path==='$.projections[1].accounts[0].cursor.extra.[redacted]','only the offending segment is redacted: '+d.secret_path);}
  // Outside the email projection the blast radius is the whole delivery (producer-controlled data, not mail content).
  await refuses(familyDelivery([portfolio({source:{authority:'StegVerse-Labs/TVC',api_key:SECRET}}),email()]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','secret in a non-email family projection',SECRET);
  await refuses(familyDelivery([portfolio({source:{authority:'StegVerse-Labs/TVC',credential_ref:'https://provider.invalid/'+SECRET}})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','non-skap credential_ref in a non-email family projection',SECRET);
  check((await harness(()=>familyDelivery([portfolio({source:{authority:'StegVerse-Labs/TVC',credential_ref:'skap://vault/coinbase'}})])).bridge.loadPersonalProjections({recovery_result:null})).length===1,'a skap:// credential_ref is accepted as a reference');
  await refuses(familyDelivery([email()],{refresh_token:SECRET}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','secret on the delivery envelope',SECRET);
  await refuses(familyDelivery([portfolio({portfolio:Object.assign(portfolio().portfolio,{note:'Bearer '+SECRET})})]),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','bearer value in CryptoBot',SECRET);
  // No false positives on ordinary prose or on the producer's own field names.
  {const benign=portfolio({portfolio:Object.assign(portfolio().portfolio,{unavailable_fields:{staking_rewards:'the bearer of good news',fee_components:'Basic information about fees'}})});const l=await harness(()=>familyDelivery([benign,email()])).bridge.loadPersonalProjections({recovery_result:null});check(l.length===2,'ordinary prose containing bearer/basic is not a secret');}
  {const err=await harness(()=>familyDelivery([email(p=>{p.credential_material_present=true;})])).bridge.loadPersonalProjections({recovery_result:null}).then(()=>null,e=>e);check(err&&/projection authority invalid/.test(err.message),'a producer-declared credential flag keeps the existing whole-delivery authority refusal');}

  // 3. Absent or stale ADMIT receipt, bound to the producer's cursor (head_receipt_id, chain_digest, sequence).
  await withholds(email(p=>{p.messages[1].receipt_id=null;reseal(p);}),'EMAIL_PROJECTION_ADMIT_RECEIPT_ABSENT','row without a receipt id');
  await withholds(email(p=>{p.messages[1].receipt_id='kv-email-receipt:'+'Z'.repeat(64);reseal(p);}),'EMAIL_PROJECTION_ADMIT_RECEIPT_ABSENT','row with a malformed receipt id');
  await withholds(email(p=>{p.accounts[0].cursor.head_receipt_id='kv-email-receipt:'+'e'.repeat(64);reseal(p);}),'EMAIL_PROJECTION_ADMIT_RECEIPT_ABSENT','cursor head receipt no row carries');
  await withholds(email(p=>{p.accounts[0].cursor.sequence-=1;reseal(p);}),'EMAIL_PROJECTION_ADMIT_RECEIPT_STALE','cursor sequence behind its rows');
  await withholds(email(p=>{const rows=p.messages.filter(m=>m.mapping_id===MB);p.accounts[0].cursor.head_receipt_id=rows[0].receipt_id;reseal(p);}),'EMAIL_PROJECTION_ADMIT_RECEIPT_STALE','cursor head is an older receipt');
  await withholds(email(p=>{p.accounts[0].cursor.chain_digest='sha256:'+'0'.repeat(64);reseal(p,{chains:false});}),'EMAIL_PROJECTION_ADMIT_RECEIPT_STALE','chain digest does not recompute');
  await withholds(email(p=>{const i=p.messages.findIndex(m=>m.mapping_id===MB&&m.sequence===2);p.messages[i].sequence=5;reseal(p);}),'EMAIL_PROJECTION_ADMIT_RECEIPT_STALE','row sequence out of chain order');
  await withholds(email(p=>{p.accounts[1].cursor={sequence:0,head_receipt_id:null,chain_digest:'sha256:'+'1'.repeat(64),provider_position:null,provider_cursor_ref:null};p.messages=p.messages.filter(m=>m.mapping_id!==MA);reseal(p,{chains:false});}),'EMAIL_PROJECTION_ADMIT_RECEIPT_STALE','empty account with a chain digest');
  // Structured cursor comparison: a string-typed sequence or position is malformed, not coerced.
  await withholds(email(p=>{p.accounts[0].cursor.sequence=String(p.accounts[0].cursor.sequence);reseal(p);}),'EMAIL_PROJECTION_ACCOUNT_INVALID','string cursor sequence');
  await withholds(email(p=>{p.accounts[0].cursor.provider_position='7';reseal(p);}),'EMAIL_PROJECTION_ACCOUNT_INVALID','string provider position');
  await withholds(email(p=>{p.accounts[0].cursor.provider_position=-1;reseal(p);}),'EMAIL_PROJECTION_ACCOUNT_INVALID','negative provider position');
  await withholds(email(p=>{p.accounts[0].cursor=p.accounts[0].cursor.chain_digest;reseal(p,{chains:false});}),'EMAIL_PROJECTION_ACCOUNT_INVALID','raw-string cursor');

  // Contract update (CVK #278 review): prefixed digests only, optional provider_cursor_ref, exact ids, safe integers.
  check(FIX.projection.projection_digest.startsWith('sha256:')&&FIX.projection.accounts.every(a=>a.cursor.chain_digest.startsWith('sha256:')&&'provider_cursor_ref' in a.cursor)&&FIX.projection.accounts.find(a=>a.mapping_id===MA).cursor.provider_cursor_ref==='sha256:'+'a1'.repeat(32)&&FIX.projection.accounts.find(a=>a.mapping_id===MB).cursor.provider_cursor_ref===null,'producer output carries prefixed digests and a carried-forward provider_cursor_ref');
  check(FIX.projection.projection_metadata.provenance_ref==='kv-email-ingress-admit-receipts:'+FIX.projection.projection_digest&&FIX.projection.projection_metadata.source_revision===FIX.projection.projection_digest.slice(7),'producer metadata binds provenance_ref (prefixed) and source_revision (bare hex) to the digest');
  // The second projection advances from the first: each mapping's earlier rows are a prefix, its sequence grows, and both deliver.
  {const F1=FIX.first_projection;check(FIX.projection.accounts.every(a=>{const a1=F1.accounts.find(x=>x.mapping_id===a.mapping_id);const r1=F1.messages.filter(m=>m.mapping_id===a.mapping_id).map(m=>m.receipt_id),r2=FIX.projection.messages.filter(m=>m.mapping_id===a.mapping_id).map(m=>m.receipt_id);return a1&&a.cursor.sequence>a1.cursor.sequence&&r1.every((r,i)=>r2[i]===r)&&a.cursor.provider_position>=a1.cursor.provider_position;}),'second projection extends the first per mapping');
   const l=await harness(()=>familyDelivery([clone(F1)])).bridge.loadPersonalProjections({recovery_result:null});check(l.length===1&&l[0].projection_digest===F1.projection_digest,'first (genesis) projection is accepted verbatim too');}
  for(const [name,mut] of [['extra projection key',p=>{p.extra_field=1;}],['extra account key',p=>{p.accounts[0].display_name='x';}],['extra cursor key',p=>{p.accounts[0].cursor.page=1;}],['extra row key',p=>{p.messages[0].subject='x';}]]){
    await withholds(email(p=>{mut(p);reseal(p);}),'EMAIL_PROJECTION_ACCOUNT_INVALID','exact key set: '+name);
  }
  await withholds(email(p=>{p.projection_metadata.provenance_ref='kv-email-ingress-admit-receipts:sha256:'+'0'.repeat(64);}),'EMAIL_PROJECTION_DIGEST_DRIFT','provenance_ref not bound to the digest');
  await withholds(email(p=>{p.projection_metadata.source_revision=p.projection_digest;}),'EMAIL_PROJECTION_DIGEST_DRIFT','prefixed source_revision');
  await withholds(email(p=>{p.accounts[0].cursor.chain_digest=p.accounts[0].cursor.chain_digest.slice(7);reseal(p,{chains:false});}),'EMAIL_PROJECTION_ACCOUNT_INVALID','bare-hex chain_digest');
  await withholds(email(p=>{p.projection_digest=p.projection_digest.slice(7);}),'EMAIL_PROJECTION_DIGEST_DRIFT','bare-hex projection_digest');
  {const h3=harness(()=>familyDelivery([email(p=>{p.accounts[0].cursor.provider_cursor_ref='sha256:'+'a'.repeat(64);reseal(p);})]));check((await h3.bridge.loadPersonalProjections({recovery_result:null})).length===1,'a sha256 provider_cursor_ref is accepted');}
  await withholds(email(p=>{delete p.accounts[0].cursor.provider_cursor_ref;reseal(p);}),'EMAIL_PROJECTION_ACCOUNT_INVALID','provider_cursor_ref is required (null when absent)');
  await withholds(email(p=>{p.accounts[0].cursor.provider_cursor_ref='opaque-provider-cursor';reseal(p);}),'EMAIL_PROJECTION_ACCOUNT_INVALID','raw provider cursor instead of a sha256 reference');
  await withholds(email(p=>{p.accounts[0].cursor.provider_position=2**53;reseal(p);}),'EMAIL_PROJECTION_ACCOUNT_INVALID','provider_position beyond 2^53 fails closed, never rounded');
  await withholds(email(p=>{p.messages[0].canonical_message_id='m-1';reseal(p);}),'EMAIL_PROJECTION_ACCOUNT_INVALID','canonical_message_id not kv-email-message');
  await withholds(email(p=>{p.messages[0].staged_content_hash='f'.repeat(64);reseal(p);}),'EMAIL_PROJECTION_ACCOUNT_INVALID','staged_content_hash without sha256 prefix');
  await withholds(email(p=>{p.accounts[1].skap_ref='skap://kv/email/ work';reseal(p);}),'WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD','skap_ref with whitespace');
  // 4. Unadmitted rows and payloads.
  await withholds(email(p=>{p.messages[0].trust_state='QUARANTINED';reseal(p);}),'EMAIL_PROJECTION_MESSAGE_UNADMITTED','unadmitted row');
  await withholds(email(p=>{p.messages[0].payload_present=true;reseal(p);}),'EMAIL_PROJECTION_MESSAGE_UNADMITTED','row carrying its payload');

  // 5. Account separation.
  await withholds(email(p=>{p.messages[0].mapping_id='kv-email:'+'d'.repeat(64);reseal(p);}),'EMAIL_PROJECTION_ACCOUNTS_MIXED','row bound to a mapping not in accounts');
  await withholds(email(p=>{p.accounts.push(clone(p.accounts[0]));reseal(p);}),'EMAIL_PROJECTION_ACCOUNTS_MIXED','mapping listed twice');
  await withholds(email(p=>{const a=p.messages.find(m=>m.mapping_id===MA);const b=p.messages.find(m=>m.mapping_id===MB);b.canonical_message_id=a.canonical_message_id;reseal(p);}),'EMAIL_PROJECTION_ACCOUNTS_MIXED','one message under two mappings');
  for(const [name,mut] of [['accounts not a list',p=>{p.accounts={};}],['messages not a list',p=>{p.messages={};}],['mapping_id not kv-email',p=>{p.accounts[0].mapping_id='acct-a';}],['__proto__ mapping_id',p=>{p.accounts[0].mapping_id='__proto__';}],['no provider_id',p=>{delete p.accounts[0].provider_id;}],['no cursor',p=>{delete p.accounts[0].cursor;}],['row without canonical id',p=>{delete p.messages[0].canonical_message_id;}],['row without sequence',p=>{delete p.messages[0].sequence;}]]){
    await withholds(email(mut),'EMAIL_PROJECTION_ACCOUNT_INVALID',name);
  }

  // 6. Replayed / duplicate records, including "__proto__" ids (Map-keyed, never prototype lookups).
  await withholds(email(p=>{const i=p.messages.findIndex(m=>m.mapping_id===MB&&m.sequence===2);p.messages[i].canonical_message_id=p.messages.find(m=>m.mapping_id===MB&&m.sequence===1).canonical_message_id;reseal(p);}),'EMAIL_PROJECTION_RECORD_DUPLICATED','message repeated within one mapping');
  await withholds(email(p=>{const rows=p.messages.filter(m=>m.mapping_id===MB);rows[0].canonical_message_id='__proto__';rows[1].canonical_message_id='__proto__';reseal(p);}),'EMAIL_PROJECTION_ACCOUNT_INVALID','two "__proto__" message ids are refused by the kv-email-message id rule before any lookup');
  await withholds(email(p=>{const rows=p.messages.filter(m=>m.mapping_id===MB);rows[1].receipt_id=rows[0].receipt_id;reseal(p);}),'EMAIL_PROJECTION_RECORD_DUPLICATED','replayed receipt');
  {const err=await harness(()=>familyDelivery([email(),email()])).bridge.loadPersonalProjections({recovery_result:null}).then(()=>null,e=>e);check(err&&/schema ambiguous/.test(err.message),'a second email projection in one delivery is refused as ambiguous');}
  // 7. Digest drift: a field change the chains cannot see.
  await withholds(email(p=>{p.messages[0].staged_content_hash='sha256:'+'f'.repeat(64);}),'EMAIL_PROJECTION_DIGEST_DRIFT','content hash changed after production');
  await withholds(email(p=>{p.accounts[0].provider_id='other-provider';}),'EMAIL_PROJECTION_DIGEST_DRIFT','provider changed after production');
  // Other email-family spellings are held to the same shape; non-email families are not.
  await withholds(email(p=>{p.schema='stegverse.kv.email-account-projection/v1';}),'EMAIL_PROJECTION_DIGEST_DRIFT','other email-family schema spelling is still digest-bound');
  check((await harness(()=>familyDelivery([portfolio()])).bridge.loadPersonalProjections({recovery_result:null}))[0].schema==='stegverse.kv.cryptobot-portfolio-projection/v1','CryptoBot projection unaffected by the email rules');

  // 8. Rendering. Shipped bootstrap: EMAIL has no KV projection contract, so nothing email renders; CryptoBot unaffected.
  const cctx={};cctx.globalThis=cctx;vm.createContext(cctx);vm.runInContext(capsSrc,cctx);vm.runInContext(panelsSrc,cctx);
  const C=cctx.StegVerseWorkspaceCapabilities,P=cctx.StegVerseWorkspacePanels,NOW=Date.parse('2026-10-28T23:45:00Z');
  const shipped=bootstrap.capability_descriptors;const projs=[portfolio(),email()];
  const byCap=(l)=>Object.fromEntries(l.map(x=>[x.capability,x]));
  let st=C.evaluateAll(shipped,projs,'PERSONAL',NOW);let panels=P.build({descriptors:shipped,statuses:st,projections:projs,workspace_type:'PERSONAL'}).panels;
  check(byCap(st).EMAIL.state==='UNAVAILABLE'&&byCap(st).EMAIL.predicate==='NO_KV_PROJECTION_CONTRACT'&&byCap(panels).EMAIL.rows.length===0&&byCap(panels).EMAIL.rows_withheld===true,'shipped EMAIL descriptor stays UNAVAILABLE; no email rows render without a descriptor binding');
  check(byCap(st).CRYPTOBOT_PORTFOLIO.state==='OBSERVED','CryptoBot status unaffected by a delivered email projection');
  // With EMAIL bound to the producer schema (the descriptor owner's later binding), each mapping renders separately.
  const bound=shipped.map(d=>d.capability==='EMAIL'?Object.assign({},d,{allowed_projection_schemas:[EMAIL_SCHEMA],projection_field:'accounts',workspace_types:['PERSONAL'],max_age_seconds:3600}):d);
  check(C.descriptorProblem(bound.find(d=>d.capability==='EMAIL'))===null,'bound EMAIL descriptor is a valid non-asserting descriptor');
  st=C.evaluateAll(bound,projs,'PERSONAL',NOW);panels=P.build({descriptors:bound,statuses:st,projections:projs,workspace_type:'PERSONAL'}).panels;
  const ep=byCap(panels).EMAIL;
  check(ep.state==='OBSERVED'&&ep.rows_withheld===false&&ep.action_eligible===false&&ep.authority_effect==='NONE'&&ep.provenance.provenance_ref===FIX.projection.projection_metadata.provenance_ref&&ep.provenance.replay_status==='REPLAY_STATUS_UNKNOWN','email panel observed, informational only, producer provenance and replay UNKNOWN: '+JSON.stringify(ep.provenance));
  check(ep.rows.length===7&&ep.malformed_rows===0,'two mapping rows plus five message rows: '+ep.rows.length);
  for(const a of FIX.projection.accounts){
    const id=a.mapping_id,rows=ep.rows.filter(r=>r.account_id===id),head=rows[0],count=FIX.projection.messages.filter(m=>m.mapping_id===id).length;
    check(rows.length===count+1&&head.label===id&&head.detail.includes('provider '+a.provider_id)&&head.detail.includes('cursor sequence '+a.cursor.sequence)&&head.detail.includes('head ADMIT receipt '+a.cursor.head_receipt_id)&&head.detail.includes('chain '+a.cursor.chain_digest)&&head.detail.includes('provider position '+a.cursor.provider_position)&&head.detail.includes(count+' message(s)'),'per-mapping provenance row for '+id+': '+JSON.stringify(head));
    check(rows.slice(1).every(r=>r.detail.startsWith('mapping '+id)&&/ADMIT receipt kv-email-receipt:[0-9a-f]{64}/.test(r.detail)&&r.detail.endsWith('payload not present')),'message rows name their own mapping and receipt: '+id);
    const other=FIX.projection.accounts.find(x=>x.mapping_id!==id).mapping_id;
    check(rows.every(r=>!r.detail.includes(other)&&r.label!==other),'rows of '+id+' carry nothing from the other mapping');
  }
  check(!JSON.stringify(ep).includes('skap://'),'skap references are never displayed');
  check(ep.notes.some(x=>/never merged/.test(x))&&ep.notes.some(x=>/SKAP Vault/.test(x)),'panel notes state account separation and SKAP custody');
  // Panel re-checks independently of the bridge.
  const panelFor=(proj)=>byCap(P.build({descriptors:bound,statuses:C.evaluateAll(bound,[proj],'PERSONAL',NOW),projections:[proj],workspace_type:'PERSONAL'}).panels).EMAIL;
  check(panelFor(email(p=>{p.messages[0].mapping_id='kv-email:'+'d'.repeat(64);})).predicate==='EMAIL_ACCOUNTS_MIXED','panel refuses a row naming an unlisted mapping');
  check(panelFor(email(p=>{p.accounts.push(clone(p.accounts[0]));})).predicate==='EMAIL_ACCOUNTS_MIXED','panel refuses a repeated mapping');
  {const p=panelFor(email(p=>{p.accounts[0].mapping_id='__proto__';p.accounts[1].mapping_id='__proto__';p.messages=[];}));check(p.state==='MALFORMED'&&p.predicate==='EMAIL_ACCOUNTS_MIXED'&&p.rows.length===0,'panel refuses two "__proto__" mappings');}
  for(const mut of [p=>{p.accounts={};},p=>{p.messages=null;}]){const p=panelFor(email(mut));check(p.state==='MALFORMED'&&p.predicate==='EMAIL_ACCOUNTS_INVALID'&&p.rows.length===0,'panel refuses non-list accounts/messages');}
  {const p=panelFor(email(p=>{p.accounts[0].provider_id='hid‮den';}));check(p.state==='OBSERVED'&&p.malformed_rows===1+3&&p.rows.length===1+2&&p.rows.every(r=>r.account_id===MA),'panel withholds a mapping with a non-displayable provider and its rows');}
  {const p=panelFor(email(p=>{p.accounts[0].mapping_state='REVOKED';}));const own=p.rows.filter(r=>r.account_id===MB);check(p.state==='OBSERVED'&&own.length===1&&/3 message row\(s\) withheld: mapping is not SESSION_VERIFIED/.test(own[0].detail)&&p.rows.filter(r=>r.account_id===MA).length===3&&p.notes.some(x=>/3 message row\(s\) withheld/.test(x)),'a non-SESSION_VERIFIED mapping keeps its provenance row and withholds its message rows: '+JSON.stringify(own));}
  {const p=panelFor(email(p=>{p.accounts[0].cursor.provider_cursor_ref='sha256:'+'a'.repeat(64);}));check(p.rows[0].detail.includes('provider cursor sha256:'+'a'.repeat(64)),'provider cursor reference shown as provenance');}
  {const p=panelFor(email(p=>{p.accounts[0].cursor.provider_position=2**60;}));check(p.malformed_rows===4&&p.rows.every(r=>r.account_id===MA),'panel never renders an unsafe provider_position');}
  {const p=panelFor(email(p=>{p.messages[0].payload_present=true;}));check(p.malformed_rows===1&&p.rows.length===6,'panel never renders a row that carries a payload');}
  {const p=panelFor(email(p=>{p.projection_metadata.observed_at='2026-10-28T21:45:00Z';}));check(p.state==='STALE'&&p.provenance.age_seconds===7200,'stale email projection labelled STALE');}
  {const p=byCap(P.build({descriptors:bound,statuses:C.evaluateAll(bound,projs,'ORGANIZATIONAL',NOW),projections:projs,workspace_type:'ORGANIZATIONAL'}).panels).EMAIL;check(p.rows.length===0&&p.rows_withheld,'personal email projection never renders in an org context');}
  // 9. Page: a withheld email projection is shown on the EMAIL capability card (code + plain reason + next attempt),
  // never its repair text, secret path or content; CryptoBot still renders; nothing shows in other contexts.
  {const ui=read('assets/workspace.js'),searchSrc=read('assets/workspace-search.js');
   const realReasons=harness(()=>null).bridge.reasons;
   const hb=harness(()=>familyDelivery([portfolio(),email(p=>{p.accounts[0].refresh_token=SECRET;})]));
   const delivered=await hb.bridge.loadPersonalProjections({recovery_result:null});const realRefusals=hb.bridge.lastFamilyRefusals();
   check(realRefusals.length===1&&realRefusals[0].secret_path.endsWith('[redacted]')&&!JSON.stringify(realRefusals[0]).includes(SECRET),'real bridge refusal carries a (redacted) secret path to be kept off the page');
   const personal={schema:'stegverse.kv.personal-workspace-projection/v1',workspace_type:'PERSONAL',state:'KV_WORKSPACE_EMPTY',principals:[],organizations:[],memberships:[],feed:[],assistant:null,credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,authority_effect:'NONE'};
   const ids=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities','searchResults','tasks'];
   const page=(bridgeExtra,opts)=>{opts=opts||{};const els={};ids.forEach(i=>els[i]={id:i,innerHTML:'',textContent:'',className:'',value:'',dataset:{},attrs:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},classList:{add(){},remove(){}},listeners:{},addEventListener(t,f){this.listeners[t]=f},scrollIntoView(){}});
     const live=(p)=>Object.assign({},p,{projection_metadata:Object.assign({},p.projection_metadata,{observed_at:new Date(Date.now()-60000).toISOString().replace(/\.\d{3}Z$/,'Z')})});
     const bridge=Object.assign({reasons:realReasons,loadPersonalWorkspace:()=>Promise.resolve(personal),lastNodeBinding:()=>null,loadPersonalProjections:()=>Promise.resolve(delivered.map(live))},bridgeExtra);
     const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener(){}},console,fetch:()=>Promise.resolve({json:()=>Promise.resolve(bootstrap)}),window:{StegVerseWorkspaceKVBridge:bridge}};
     vm.createContext(ctx);vm.runInContext(capsSrc,ctx);vm.runInContext(searchSrc,ctx);ctx.window.StegVerseWorkspaceCapabilities=ctx.StegVerseWorkspaceCapabilities;ctx.window.StegVerseWorkspaceSearch=ctx.StegVerseWorkspaceSearch;
     if(opts.panels!==false){vm.runInContext(panelsSrc,ctx);ctx.window.StegVerseWorkspacePanels=ctx.StegVerseWorkspacePanels;}
     vm.runInContext(ui,ctx);return {els,switchTo:v=>els.workspaceSwitch.listeners.change({target:{value:v}})};};
   const wait=()=>new Promise(r=>setTimeout(r,15));
   const emailCard=(html)=>{const i=html.indexOf('<strong>Email</strong>');const j=html.indexOf('<div class="item cap">',i+1);return i<0?'':html.slice(i,j<0?undefined:j);};
   for(const panels of [true,false]){
    const pg=page({lastFamilyRefusals:()=>realRefusals},{panels});await wait();const html=pg.els.capabilities.innerHTML,card=emailCard(html);
    check(card.includes('data-family-refusal="WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD"')&&card.includes('Projection withheld · FAIL_CLOSED · WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD')&&card.includes('A delivered projection contains something shaped like a password')&&card.includes('nothing waits'),'EMAIL card shows the withheld projection (panels '+panels+'): '+card.slice(0,500));
    check(!html.includes(SECRET)&&!html.includes('refresh_token')&&!html.includes('[redacted]')&&!html.includes(realRefusals[0].secret_path)&&!html.includes(realRefusals[0].required_evidence_or_repair),'page echoes no secret, key path or repair text (panels '+panels+')');
    check((html.match(/data-family-refusal=/g)||[]).length===1,'refusal shown once, on the EMAIL card only (panels '+panels+')');
    if(panels)check(html.includes('CryptoBot portfolio (read-only)')&&/CryptoBot portfolio \(read-only\)<\/strong> <span class="pill ok">OBSERVED/.test(html),'CryptoBot still renders beside the withheld email projection');
    pg.switchTo('ORG');check(!pg.els.capabilities.innerHTML.includes('data-family-refusal'),'no family refusal outside the personal context (panels '+panels+')');
   }
   // Only catalogued codes and email schemas render; hostile refusal objects are dropped, never echoed.
   const hostile=[{disposition:'FAIL_CLOSED',failure_code:'<img src=x onerror=alert(1)>',projection_schema:EMAIL_SCHEMA},{disposition:'FAIL_CLOSED',failure_code:'EMAIL_PROJECTION_ACCOUNTS_MIXED',projection_schema:'stegverse.kv.cryptobot-portfolio-projection/v1'},{disposition:'ALLOW',failure_code:'EMAIL_PROJECTION_ACCOUNTS_MIXED',projection_schema:EMAIL_SCHEMA},null,'x'];
   {const pg=page({lastFamilyRefusals:()=>hostile});await wait();const html=pg.els.capabilities.innerHTML;check(!html.includes('data-family-refusal')&&!html.includes('onerror'),'malformed or non-email refusal records are dropped');}
   {const pg=page({lastFamilyRefusals:()=>[{disposition:'FAIL_CLOSED',failure_code:'EMAIL_PROJECTION_ACCOUNTS_MIXED',projection_schema:EMAIL_SCHEMA,required_evidence_or_repair:'<script>x</script>'}]});await wait();const card=emailCard(pg.els.capabilities.innerHTML);check(card.includes('data-family-refusal="EMAIL_PROJECTION_ACCOUNTS_MIXED"')&&card.includes('The email projection mixes messages between accounts')&&!card.includes('<script>'),'catalogued email refusal rendered with its plain reason only');}
   {const pg=page({lastFamilyRefusals:()=>{throw new Error('boom');}});await wait();check(!pg.els.capabilities.innerHTML.includes('data-family-refusal')&&/CryptoBot portfolio \(read-only\)<\/strong> <span class="pill ok">OBSERVED/.test(pg.els.capabilities.innerHTML),'a throwing refusal accessor renders nothing and keeps the delivered projections');}
   {const pg=page({});await wait();check(!pg.els.capabilities.innerHTML.includes('data-family-refusal'),'bridge without lastFamilyRefusals renders no refusal');}
  }
  console.log('WORKSPACE_EMAIL_FAMILY_CONSUMER_PASS assertions='+n);
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
