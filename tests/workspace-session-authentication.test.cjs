// Session-authentication contract (Site#1509 W4): the session principal handed to the MyKV assistant binding
// resolver must come from a caller-authentication receipt. KV ownership data, device registration and browser
// state are never authentication, and the contract never reads the projection at all.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const src=fs.readFileSync(path.join(root,'assets/workspace-session-authentication.js'),'utf8');
const ui=fs.readFileSync(path.join(root,'assets/workspace.js'),'utf8');
const page=fs.readFileSync(path.join(root,'workspace.html'),'utf8');
function assert(ok,msg){if(!ok)throw new Error(msg)}
const sandbox={};vm.createContext(sandbox);vm.runInContext(src,sandbox);
const S=sandbox.StegVerseWorkspaceSessionAuthentication;
assert(S.schema==='stegverse.workspace.session-authentication/v1'&&S.authority_effect==='NONE'&&S.receipt_source_class==='CALLER_AUTHENTICATION_RECEIPT','module identity');
assert(S.resolve.length===1,'the contract takes the session only; the projection must never be an input');
assert(!/\.(projection|projection_metadata|owner_principal_id|principals|assistant|registration|node_id)\b|localStorage|sessionStorage|indexedDB|StegVerseNodeContinuity|StegVerseWorkspaceKVBridge/.test(src.split('\n').filter(l=>!l.trim().startsWith('//')).join('\n')),'contract source must not read projection, device or browser identity');
assert(page.indexOf('assets/workspace-session-authentication.js')>=0&&page.indexOf('assets/workspace-session-authentication.js')<page.indexOf('assets/workspace-assistant-binding.js'),'page must load the session contract before the binding resolver');

const receipt=(extra)=>Object.assign({authenticated:true,credential_authority:'TV/TVC',receipt_ref:'tv-tvc:session-receipt:example',principal_id:'user:owner',authority_effect:'NONE'},extra||{});
const session=(extra)=>Object.assign({principal_id:'user:owner',workspace_id:'ws:personal:owner',source_class:'CALLER_AUTHENTICATION_RECEIPT',authentication:receipt()},extra||{});
const ok=S.resolve(session());
assert(ok.disposition==='ALLOW'&&ok.predicate==='CALLER_AUTHENTICATION_RECEIPT_PRESENT','receipt-backed session admitted');
assert(JSON.stringify(ok.session)===JSON.stringify({principal_id:'user:owner',workspace_id:'ws:personal:owner',source_class:'CALLER_AUTHENTICATION_RECEIPT',receipt_ref:'tv-tvc:session-receipt:example',credential_authority:'TV/TVC'}),'admitted session shape');
assert(ok.verification==='CALLER_SUPPLIED_NOT_PAGE_VERIFIED'&&ok.identity_from_projection===false&&ok.action_eligible===false&&ok.authority_effect==='NONE','ALLOW is admission of a declared receipt only; no verification, action or authority is claimed');
assert(S.resolve(session({workspace_id:undefined})).session.workspace_id===null,'absent workspace is null');

const cases=[
  [null,'SESSION_PRINCIPAL_UNAUTHENTICATED'],
  [{},'SESSION_PRINCIPAL_UNAUTHENTICATED'],
  [{principal_id:null,workspace_id:null,source_class:'NO_AUTHENTICATED_SESSION_PRINCIPAL',authentication:null},'SESSION_PRINCIPAL_UNAUTHENTICATED'],
  [{principal_id:'user:owner',source_class:'NO_AUTHENTICATED_SESSION_PRINCIPAL'},'SESSION_PRINCIPAL_UNAUTHENTICATED'],
  // The projection owner is whose data was projected, never who the caller is.
  [{principal_id:'user:owner',source_class:'KV_PROJECTION_OWNER'},'KV_OWNERSHIP_IS_NOT_AUTHENTICATION'],
  [{principal_id:'user:owner',source_class:'KV_PROJECTION_METADATA',authentication:receipt()},'KV_OWNERSHIP_IS_NOT_AUTHENTICATION'],
  [{principal_id:'user:owner',source_class:'KV_PROJECTION_PRINCIPAL'},'KV_OWNERSHIP_IS_NOT_AUTHENTICATION'],
  [{principal_id:'user:owner',source_class:'KV_WORKSPACE_CONTEXT'},'KV_OWNERSHIP_IS_NOT_AUTHENTICATION'],
  [{principal_id:'stegos-node://node-1',source_class:'DEVICE_REGISTRATION'},'DEVICE_REGISTRATION_IS_NOT_AUTHENTICATION'],
  [{principal_id:'node-1',source_class:'STEGOS_NODE_REGISTRATION'},'DEVICE_REGISTRATION_IS_NOT_AUTHENTICATION'],
  [{principal_id:'user:owner',source_class:'BROWSER_STORAGE'},'BROWSER_STATE_IS_NOT_AUTHENTICATION'],
  [{principal_id:'user:owner',source_class:'PAGE_STATE'},'BROWSER_STATE_IS_NOT_AUTHENTICATION'],
  [{principal_id:'user:owner',source_class:'URL_PARAMETER'},'BROWSER_STATE_IS_NOT_AUTHENTICATION'],
  [{principal_id:'user:owner',source_class:'BOOTSTRAP_DATA'},'BROWSER_STATE_IS_NOT_AUTHENTICATION'],
  // A bare principal_id, however it was obtained, is not authentication.
  [{principal_id:'user:owner'},'SESSION_PRINCIPAL_SOURCE_NOT_AUTHENTICATION'],
  [{principal_id:'user:owner',source_class:'TEST_INJECTED'},'SESSION_PRINCIPAL_SOURCE_NOT_AUTHENTICATION'],
  [{principal_id:'',source_class:'CALLER_AUTHENTICATION_RECEIPT',authentication:receipt()},'SESSION_PRINCIPAL_UNAUTHENTICATED'],
  [session({authentication:null}),'SESSION_AUTHENTICATION_RECEIPT_ABSENT'],
  [session({authentication:'receipt'}),'SESSION_AUTHENTICATION_RECEIPT_ABSENT'],
  [session({authentication:receipt({authenticated:false})}),'SESSION_NOT_AUTHENTICATED'],
  [session({authentication:receipt({authenticated:'true'})}),'SESSION_NOT_AUTHENTICATED'],
  [session({authentication:receipt({credential_authority:'GITHUB_TOKEN'})}),'SESSION_CREDENTIAL_AUTHORITY_INVALID'],
  [session({authentication:receipt({receipt_ref:''})}),'SESSION_AUTHENTICATION_RECEIPT_REF_ABSENT'],
  [session({authentication:receipt({principal_id:'user:other'})}),'SESSION_AUTHENTICATION_PRINCIPAL_MISMATCH'],
  [session({authentication:receipt({transaction_authority:true})}),'SESSION_AUTHENTICATION_CLAIMS_AUTHORITY'],
  [session({authentication:receipt({execution_authority:true})}),'SESSION_AUTHENTICATION_CLAIMS_AUTHORITY'],
  [session({authentication:receipt({delegation_authority:true})}),'SESSION_AUTHENTICATION_CLAIMS_AUTHORITY'],
  [session({authentication:receipt({authority_effect:'ALLOW'})}),'SESSION_AUTHENTICATION_CLAIMS_AUTHORITY'],
];
for(const [input,pred] of cases){const d=S.resolve(input);assert(d.disposition==='FAIL_CLOSED'&&d.predicate===pred&&d.session===null&&d.action_eligible===false,pred+' expected, got '+d.disposition+'/'+d.predicate);}
assert(JSON.stringify(S.resolve(session()))===JSON.stringify(S.resolve(JSON.parse(JSON.stringify(session())))),'deterministic');

// Page wiring: the projection never flows into the session contract, and the binding resolver only ever
// receives a principal that the session contract admitted.
assert(ui.includes('session:{principal_id:null,workspace_id:null,source_class:"NO_AUTHENTICATED_SESSION_PRINCIPAL",authentication:null}'),'page must not invent a session principal or receipt');
assert(ui.includes('S.resolve(state.session)')&&!/S\.resolve\([^)]*projection/.test(ui),'session contract receives state.session only');
assert(ui.includes('if(sa.disposition!=="ALLOW"||!sa.session)return bindingRefusal(sa.predicate)')&&ui.includes('principal_id:sa.session.principal_id'),'binding resolver must only receive an admitted session principal');
assert(!/principal_id:state\.session\.principal_id/.test(ui),'page must not hand its raw session principal to the binding resolver');
assert(!/state\.session(\.\w+)?\s*=[^=]/.test(ui)&&ui.split('session:{').length===2,'page must never assign or rebuild the session; the only session literal is the null one');
console.log('WORKSPACE_SESSION_AUTHENTICATION_PASS');
