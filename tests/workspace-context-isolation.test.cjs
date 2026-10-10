// Behavioral checks for Workspace context isolation and non-authorizing interaction drafts (Site#1509 W2/W3).
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const ui=fs.readFileSync(path.join(root,'assets/workspace.js'),'utf8');
function assert(ok,msg){if(!ok)throw new Error(msg)}
function el(id){return {id,innerHTML:'',textContent:'',className:'',value:'',dataset:{},classList:{add(){},remove(){}},listeners:{},addEventListener(t,f){this.listeners[t]=f},scrollIntoView(){}}}
function harness(sessionValues){
  const ids=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft'];
  const els={};ids.forEach(i=>els[i]=el(i));
  const docListeners={};let alerts=0;const storageReads=[];
  const projection={schema:'stegverse.kv.personal-workspace-projection/v1',workspace_type:'PERSONAL',state:'KV_WORKSPACE_PROJECTED',
    principals:[{principal_id:'P-1',principal_type:'HUMAN',display_name:'Personal Friend'}],organizations:[{principal_id:'O-1',principal_type:'ORGANIZATION',display_name:'Personal Org'}],
    memberships:[{organization_name:'Personal Org',role:'Member',status:'ACTIVE'}],feed:[{actor_id:'P-1',viewer_id:'P-1',visibility:'PUBLIC',text:'personal feed item'}],
    assistant:{principal_id:'A-1',principal_type:'AI_ENTITY',display_name:'MyKV Assistant',ai_label_required:true,roles:['WORKSPACE_ASSISTANT']}};
  const storage={getItem(k){storageReads.push(k);return sessionValues[k]??null},setItem(){}};
  const document={body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener:(t,f)=>{docListeners[t]=f}};
  const ctx={document,sessionStorage:storage,localStorage:storage,alert:()=>{alerts++},console,
    fetch:()=>Promise.resolve({json:()=>Promise.resolve({})}),
    window:{StegVerseWorkspaceKVBridge:{loadPersonalWorkspace:()=>Promise.resolve(projection)}}};
  vm.runInNewContext(ui,ctx);
  const click=id=>docListeners.click({target:{closest:()=>({dataset:{action:'message',id}})}});
  return {els,click,switchTo:v=>els.workspaceSwitch.listeners.change({target:{value:v}}),alerts:()=>alerts,storageReads};
}
(async()=>{
  const allTrue={'stegverse.workspace.orgEmpGate':JSON.stringify({employee_identity_matches:true,machine_identity_matches:true,active_membership:true,role_capability_admitted:true,transition_admitted:true})};
  const h=harness(allTrue);await new Promise(r=>setTimeout(r,10));
  // Personal context renders the KV projection.
  assert(h.els.contacts.innerHTML.includes('Personal Friend'),'personal projection not rendered');
  assert(h.els.assistant.innerHTML.includes('MyKV Assistant'),'assistant identity not rendered from KV projection');
  // Message action produces a visible FAIL_CLOSED draft, no alert, no effect.
  h.click('P-1');
  assert(h.alerts()===0,'interaction must not use alert');
  assert(h.els.intentDraft.innerHTML.includes('FAIL_CLOSED')&&h.els.intentDraft.innerHTML.includes('WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND'),'draft must show FAIL_CLOSED predicate');
  assert(h.els.intentDraft.innerHTML.includes('&quot;submitted&quot;: false')&&h.els.intentDraft.innerHTML.includes('NONE_REQUEST_ONLY'),'draft must be non-authorizing and unsubmitted');
  assert(!/completed|sent successfully|ALLOW&quot;/i.test(h.els.intentDraft.innerHTML),'draft must not claim completion');
  // Unknown principal produces nothing.
  h.click('NOT-A-CONTACT');
  // Switch to organizational: browser-asserted gate ignored, personal data hidden, draft invalidated.
  h.switchTo('organizational');
  assert(h.els.intentDraft.innerHTML==='','context switch must invalidate pending draft');
  assert(h.els.kvGate.innerHTML.includes('LOCKED')&&!h.els.kvGate.innerHTML.includes('ADMITTED'),'org gate must stay LOCKED despite browser session values');
  assert(h.els.kvGate.innerHTML.includes('ORG_KV_PROJECTION_NOT_OBSERVED'),'org gate must name failing predicate');
  assert(!h.storageReads.some(k=>k.startsWith('stegverse.workspace.')),'Workspace must not read admission from browser storage');
  for(const id of ['contacts','organizations','memberships','feed','assistant'])assert(!h.els[id].innerHTML.includes('Personal'),'personal KV data leaked into org context: '+id);
  assert(!h.els.assistant.innerHTML.includes('MyKV Assistant'),'personal assistant projection leaked into org context');
  // Personal contact action is not available from org context.
  h.click('P-1');
  assert(h.els.intentDraft.innerHTML==='','org context must not act on personal contacts');
  // Returning to personal restores projection.
  h.switchTo('personal');
  assert(h.els.contacts.innerHTML.includes('Personal Friend'),'personal projection not restored');
  console.log('WORKSPACE_CONTEXT_ISOLATION_PASS');
})().catch(e=>{console.error(e);process.exit(1)});
