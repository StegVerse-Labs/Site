(() => {
  const state={bootstrap:null,mode:"personal",projection:null,data:{feed:[],contacts:[],organizations:[],memberships:[],assistant:null}};
  const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
  const badge=p=>p&&p.principal_type==="AI_ENTITY"?'<span class="badge ai">AI</span>':p&&p.principal_type==="ORGANIZATION"?'<span class="badge org">ORG</span>':"";
  const safe=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
  function setRuntime(text,kind){const el=$("#workspaceRuntimeState");el.textContent=text;el.className=kind==="ok"?"ok":kind==="warn"?"warn":"muted";}
  function applyProjection(p){
    state.projection=p;
    const relationships=Array.isArray(p.relationships)?p.relationships:[];
    const relationshipByObject={};relationships.forEach(r=>{if(r.object_principal_id)relationshipByObject[r.object_principal_id]=r.relationship});
    state.data.contacts=(p.principals||[]).filter(x=>x.principal_type!=="ORGANIZATION"&&(!p.assistant||x.principal_id!==p.assistant.principal_id)).map(x=>Object.assign({},x,{relationship:relationshipByObject[x.principal_id]||x.relationship||"KNOWN"}));
    state.data.organizations=(p.organizations||[]).map(x=>Object.assign({},x,{relationship:relationshipByObject[x.principal_id]||x.relationship||"KNOWN_ORGANIZATION"}));
    state.data.memberships=p.memberships||[];
    state.data.feed=p.feed||[];
    state.data.assistant=p.assistant||null;
  }
  function visibilityAllows(ev){
    const v=ev.visibility||"PRIVATE";
    if(["PUBLIC","ECOSYSTEM"].includes(v))return true;
    if(v==="PRIVATE")return ev.actor_id===ev.viewer_id;
    if(v==="FRIENDS")return ev.relationship==="FRIEND";
    if(v==="KNOWN_USERS")return !!ev.relationship;
    if(v==="ORGANIZATION_MEMBERS")return !!ev.shared_membership;
    if(["SPECIFIC_USERS","SPECIFIC_ORGANIZATIONS"].includes(v))return !!ev.in_audience;
    return false;
  }
  function renderAssistant(){
    const a=state.data.assistant;
    $("#assistant").innerHTML=a?'<strong>'+safe(a.display_name)+badge(a)+'</strong><div class="muted">Primary Workspace assistant admitted by Personal KV identity context. Assistant role does not grant execution authority.</div>':'<div class="empty">No Workspace Assistant identity is admitted by the current KV projection.</div>';
  }
  function renderFeed(){const items=state.data.feed.filter(visibilityAllows);$("#feed").innerHTML=items.length?items.map(ev=>'<div class="item"><strong>'+safe(ev.actor_name||ev.actor_id)+badge({principal_type:ev.actor_type})+'</strong><div>'+safe(ev.text||ev.activity||ev.event_type||"Activity")+'</div><div class="muted">'+safe(ev.visibility||"PRIVATE")+'</div></div>').join(""):'<div class="empty">No admitted shared feed items are available.</div>';}
  function renderContacts(filter=""){const q=filter.toLowerCase();const items=state.data.contacts.filter(p=>!q||[p.display_name,p.principal_type,p.relationship].join(" ").toLowerCase().includes(q));$("#contacts").innerHTML=items.length?items.map(p=>'<div class="item"><strong>'+safe(p.display_name)+badge(p)+'</strong><div class="muted">'+safe(p.relationship||"KNOWN")+'</div><div class="actions"><button data-action="message" data-id="'+safe(p.principal_id)+'">Message</button><button data-action="profile" data-id="'+safe(p.principal_id)+'">Profile</button></div></div>').join(""):'<div class="empty">No admitted contacts match this view.</div>';}
  function renderOrganizations(filter=""){const q=filter.toLowerCase();const items=state.data.organizations.filter(o=>!q||o.display_name.toLowerCase().includes(q));$("#organizations").innerHTML=items.length?items.map(o=>'<div class="item"><strong>'+safe(o.display_name)+badge(o)+'</strong><div class="muted">'+safe(o.relationship||"KNOWN_ORGANIZATION")+'</div></div>').join(""):'<div class="empty">No admitted organizations match this view.</div>';}
  function renderMemberships(){const items=state.data.memberships;$("#memberships").innerHTML=items.length?items.map(m=>'<div class="item"><strong>'+safe(m.organization_name||m.organization_id)+'</strong><div>'+safe(m.role||"Member")+(m.department?' · '+safe(m.department):'')+'</div><div class="muted">Membership: '+safe(m.status||"UNKNOWN")+'</div></div>').join(""):'<div class="empty">No admitted organizational memberships are available.</div>';}
  function renderKvGate(){
    const box=$("#kvGate");
    if(state.mode==="personal"){
      const s=state.projection?state.projection.state:"NOT_OBSERVED";
      box.innerHTML='<strong>Personal KV</strong><div class="muted">DEVICE_KV Workspace projection: '+safe(s)+'. Personal KV remains individual sovereign state.</div>';
      return;
    }
    const keys=["employee_identity_matches","machine_identity_matches","active_membership","role_capability_admitted","transition_admitted"];
    const ctx=JSON.parse(sessionStorage.getItem("stegverse.workspace.orgEmpGate")||"{}");const admitted=keys.every(k=>ctx[k]===true);
    box.innerHTML='<div class="lock"><strong>Org-Emp-KV '+(admitted?'<span class="ok">ADMITTED</span>':'<span class="warn">LOCKED</span>')+'</strong><div class="muted">A distinct organizational runtime must establish all five predicates:</div>'+keys.map(k=>'<div>'+safe(k)+': '+(ctx[k]===true?'✓':'—')+'</div>').join("")+'<div class="muted">Personal KV data is never substituted for Org-KV or Org-Emp-KV.</div></div>';
  }
  function renderAll(){renderAssistant();renderFeed();renderContacts($("#search")?.value||"");renderOrganizations($("#search")?.value||"");renderMemberships();renderKvGate();}
  function setMode(mode){state.mode=mode;document.body.dataset.workspaceMode=mode;$("#contextTitle").textContent=mode==="personal"?"My Workspace":"Organization Workspace";if(mode==="organizational")setRuntime("Organizational runtime admission required; Personal KV is not reused.","warn");else setRuntime(state.projection?"Personal KV Workspace projection admitted.":"Personal KV Workspace projection not yet observed.",state.projection?"ok":"warn");renderKvGate();}
  function bind(){
    $("#workspaceSwitch").addEventListener("change",e=>setMode(e.target.value));$("#search").addEventListener("input",e=>{renderContacts(e.target.value);renderOrganizations(e.target.value)});
    $$(".nav button").forEach(b=>b.addEventListener("click",()=>{$$(".nav button").forEach(x=>x.classList.remove("active"));b.classList.add("active");document.getElementById(b.dataset.target)?.scrollIntoView({behavior:"smooth"})}));
    document.addEventListener("click",e=>{const btn=e.target.closest("[data-action]");if(!btn)return;const contact=state.data.contacts.find(x=>x.principal_id===btn.dataset.id);if(!contact)return;const action={schema_version:"stegverse.workspace.interaction-request.v1",action:btn.dataset.action.toUpperCase(),target_principal_id:contact.principal_id,target_principal_type:contact.principal_type,interlock_required:true,intr_required:true,authority_effect:"NONE_REQUEST_ONLY"};alert(JSON.stringify(action,null,2));});
  }
  async function loadPersonalKV(){
    const bridge=window.StegVerseWorkspaceKVBridge;
    if(!bridge||typeof bridge.loadPersonalWorkspace!=="function"){setRuntime("Workspace DEVICE_KV bridge unavailable; no KV data projected.","warn");return;}
    try{const p=await bridge.loadPersonalWorkspace();applyProjection(p);setRuntime(p.state==="KV_WORKSPACE_EMPTY"?"Personal KV connected; Workspace registry is empty.":"Personal KV Workspace projection admitted.","ok");renderAll();}
    catch(error){state.projection=null;setRuntime(error&&error.message?error.message:"Personal KV Workspace projection unavailable.","warn");renderAll();}
  }
  async function init(){try{state.bootstrap=await fetch("data/workspace/bootstrap.json",{cache:"no-store"}).then(r=>r.json())}catch{state.bootstrap={}}renderAll();bind();await loadPersonalKV();}
  init();
})();