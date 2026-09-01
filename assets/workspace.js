(() => {
  const state={bootstrap:null,mode:"personal",data:{feed:[],contacts:[],organizations:[],memberships:[],assistant:{principal_id:"workspace-assistant",principal_type:"AI_ENTITY",display_name:"Workspace Assistant",roles:["WORKSPACE_ASSISTANT"]}}};
  const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
  const badge=p=>p.principal_type==="AI_ENTITY"?'<span class="badge ai">AI</span>':p.principal_type==="ORGANIZATION"?'<span class="badge org">ORG</span>':"";
  const safe=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
  function loadLocal(){
    for(const key of ["feed","contacts","organizations","memberships"]){
      try{const v=JSON.parse(localStorage.getItem("stegverse.workspace."+key)||"[]");if(Array.isArray(v))state.data[key]=v}catch{}
    }
    try{const a=JSON.parse(localStorage.getItem("stegverse.workspace.assistant")||"null");if(a)state.data.assistant=a}catch{}
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
    $("#assistant").innerHTML='<strong>'+safe(a.display_name)+badge(a)+'</strong><div class="muted">Your primary Workspace assistant. It can help navigate, search, summarize and prepare governed actions; it does not inherit execution authority.</div>';
  }
  function renderFeed(){
    const items=state.data.feed.filter(visibilityAllows);
    $("#feed").innerHTML=items.length?items.map(ev=>'<div class="item"><strong>'+safe(ev.actor_name||ev.actor_id)+badge({principal_type:ev.actor_type})+'</strong><div>'+safe(ev.text||ev.activity||"Activity")+'</div><div class="muted">'+safe(ev.visibility||"PRIVATE")+'</div></div>').join(""):'<div class="empty">No shared feed items are available in this Workspace yet.</div>';
  }
  function renderContacts(filter=""){
    const q=filter.toLowerCase();
    const items=state.data.contacts.filter(p=>!q||[p.display_name,p.principal_type,p.relationship].join(" ").toLowerCase().includes(q));
    $("#contacts").innerHTML=items.length?items.map(p=>'<div class="item"><strong>'+safe(p.display_name)+badge(p)+'</strong><div class="muted">'+safe(p.relationship||"KNOWN")+'</div><div class="actions"><button data-action="message" data-id="'+safe(p.principal_id)+'">Message</button><button data-action="profile" data-id="'+safe(p.principal_id)+'">Profile</button></div></div>').join(""):'<div class="empty">No known contacts match this view.</div>';
  }
  function renderOrganizations(filter=""){
    const q=filter.toLowerCase();
    const items=state.data.organizations.filter(o=>!q||o.display_name.toLowerCase().includes(q));
    $("#organizations").innerHTML=items.length?items.map(o=>'<div class="item"><strong>'+safe(o.display_name)+'<span class="badge org">ORG</span></strong><div class="muted">'+safe(o.relationship||"KNOWN_ORGANIZATION")+'</div></div>').join(""):'<div class="empty">No organizations match this view.</div>';
  }
  function renderMemberships(){
    const items=state.data.memberships;
    $("#memberships").innerHTML=items.length?items.map(m=>'<div class="item"><strong>'+safe(m.organization_name)+'</strong><div>'+safe(m.role||"Member")+(m.department?' · '+safe(m.department):'')+'</div><div class="muted">Membership: '+safe(m.status||"UNKNOWN")+'</div></div>').join(""):'<div class="empty">No organizational memberships are available in this Workspace context.</div>';
  }
  function renderKvGate(){
    const box=$("#kvGate");
    if(state.mode==="personal"){
      box.innerHTML='<strong>Personal KV</strong><div class="muted">Individual sovereign state. Organizational membership does not convert this into Org-KV.</div>';
      return;
    }
    const keys=["employee_identity_matches","machine_identity_matches","active_membership","role_capability_admitted","transition_admitted"];
    const ctx=JSON.parse(sessionStorage.getItem("stegverse.workspace.orgEmpGate")||"{}");
    const admitted=keys.every(k=>ctx[k]===true);
    box.innerHTML='<div class="lock"><strong>Org-Emp-KV '+(admitted?'<span class="ok">ADMITTED</span>':'<span class="warn">LOCKED</span>')+'</strong><div class="muted">Access requires all five predicates:</div>'+keys.map(k=>'<div>'+safe(k)+': '+(ctx[k]===true?'✓':'—')+'</div>').join("")+'<div class="muted">Workspace UI cannot override this gate.</div></div>';
  }
  function setMode(mode){
    state.mode=mode;
    document.body.dataset.workspaceMode=mode;
    $("#contextTitle").textContent=mode==="personal"?"My Workspace":"Organization Workspace";
    renderKvGate();
  }
  function bind(){
    $("#workspaceSwitch").addEventListener("change",e=>setMode(e.target.value));
    $("#search").addEventListener("input",e=>{renderContacts(e.target.value);renderOrganizations(e.target.value)});
    $$(".nav button").forEach(b=>b.addEventListener("click",()=>{$$(".nav button").forEach(x=>x.classList.remove("active"));b.classList.add("active");document.getElementById(b.dataset.target)?.scrollIntoView({behavior:"smooth"})}));
    document.addEventListener("click",e=>{
      const btn=e.target.closest("[data-action]"); if(!btn)return;
      const contact=state.data.contacts.find(x=>x.principal_id===btn.dataset.id); if(!contact)return;
      const action={schema_version:"stegverse.workspace.interaction-request.v1",action:btn.dataset.action.toUpperCase(),target_principal_id:contact.principal_id,target_principal_type:contact.principal_type,interlock_required:true,intr_required:true,authority_effect:"NONE_REQUEST_ONLY"};
      alert(JSON.stringify(action,null,2));
    });
  }
  async function init(){
    try{state.bootstrap=await fetch("data/workspace/bootstrap.json",{cache:"no-store"}).then(r=>r.json())}catch{state.bootstrap={}}
    loadLocal(); renderAssistant(); renderFeed(); renderContacts(); renderOrganizations(); renderMemberships(); renderKvGate(); bind();
  }
  init();
})();