/* Existing Workspace presentation only; the KV owner supplies any admitted delivery. */
(function(){
  'use strict';
  const box=document.querySelector('#ecosystemReview');
  const switcher=document.querySelector('#workspaceSwitch');
  const C=window.StegVerseWorkspaceEcosystemReview;
  if(!box||!switcher||!C)return;
  let epoch=0,delivery=null,view=null,selected='',evidence='ALL',work='ALL',output='',outputKind='',loading=false;
  const safe=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const active=()=>switcher.value==='developer';
  const option=(v,label,current)=>'<option value="'+safe(v)+'"'+(v===current?' selected':'')+'>'+safe(label)+'</option>';
  const select=(name,label,values,current)=>'<label>'+label+'<select data-review-select="'+name+'">'+values.map(([v,l])=>option(v,l,current)).join('')+'</select></label>';
  const boundary='<p class="muted">Review only. Verification and completion labels report filed support. This page does not verify receipts, bind owners, admit tasks, create claims, execute work, or write records. Replay status remains unknown.</p>';
  function current(){
    if(delivery)view=C.evaluate(delivery.projection,delivery.context);
    return view;
  }
  function render(){
    if(!active()){box.innerHTML='<p class="muted">Open Developer Workspace to review Ecosystem KV coordination. Personal KV data is never substituted.</p>';return;}
    current();
    let html='<p>SDK review and owner-binding coordination from the Ecosystem KV.</p><div class="review-toolbar"><button type="button" data-review-action="refresh"'+(loading?' disabled':'')+'>'+(loading?'Reading projection…':'Refresh review')+'</button><span class="muted">stegverse@gmail.com · scoped KV delivery</span></div>';
    if(!view||view.state==='WITHHELD'){
      const d=view||C.refusal('ECOSYSTEM_REVIEW_PROJECTION_NOT_OBSERVED');
      html+='<div class="review-notice" role="status"><strong>Review data unavailable</strong><p>'+safe(d.failure_code)+'</p><dl>'+['required_evidence_or_repair','retry_entrypoint','owning_existing_goal','next_attempt'].map(k=>'<dt>'+safe(k.replace(/_/g,' '))+'</dt><dd>'+safe(d[k])+'</dd>').join('')+'</dl></div>'+boundary;
      box.innerHTML=html;return;
    }
    html+='<div class="review-notice'+(view.state==='STALE'?' warn':'')+'"><strong>'+(view.state==='STALE'?'Stale source view':'Filed source view')+'</strong><p>Observed '+safe(view.observed_at)+' · '+safe(view.provenance_ref)+'</p><p>Queue: '+safe(view.queue.state)+' · read complete: '+safe(view.queue.read_complete)+' · observed '+safe(view.queue.observed_at)+'</p></div>';
    if(view.queue.error)html+='<details><summary>Filed error disposition</summary><dl>'+Object.entries(view.queue.error).map(([k,v])=>'<dt>'+safe(k.replace(/_/g,' '))+'</dt><dd>'+safe(v)+'</dd>').join('')+'</dl></details>';
    if(!view.reviews.length){box.innerHTML=html+'<p>No review records are included in this projection. This is not evidence that the ecosystem has no work.</p>'+boundary;return;}
    if(!view.reviews.some(r=>r.goal.task_id===selected))selected=view.reviews[0].goal.task_id;
    const r=view.reviews.find(r=>r.goal.task_id===selected);
    html+='<div class="review-filters">'+select('goal','Goal',view.reviews.map(r=>[r.goal.task_id,r.goal.task_id]),selected)+select('evidence','Evidence',[['ALL','All filed states'],['VERIFIED','Filed VERIFIED'],['UNRESOLVED','Reported, unknown or conflicting']],evidence)+select('work','Work',[['ALL','All work'],['COMPLETED','Filed completed'],['STILL_REQUIRED','Still required'],['NOT_APPLICABLE','Not applicable'],['UNKNOWN','Completion unknown']],work)+'</div>';
    html+='<p><strong>'+safe(r.goal.task_id)+'</strong><br>Recorded state: '+safe(r.goal.state)+' · COSV '+safe(r.goal.cosv)+'<br>Handoff: '+safe(r.goal.handoff_ref)+'<br>Registry source: '+safe(r.goal.source_ref)+' @ '+safe(r.goal.source_revision)+'</p>';
    const rows=C.selectFacts(r,evidence,work);
    html+='<div class="review-facts">'+(rows.length?rows.map(f=>'<article class="review-fact"><h3>'+safe(f.category.replace(/_/g,' '))+'</h3><p>'+safe(f.statement)+'</p><p class="muted">Filed '+safe(f.evidence_state)+' · '+safe(f.work_state)+'</p><details><summary>Supporting records ('+f.evidence_refs.length+')</summary>'+f.evidence_refs.map(id=>{const e=r.evidence.find(e=>e.evidence_id===id);return '<p>'+safe(e.source_ref)+'<br>'+safe(e.digest)+'<br>Filed by '+safe(e.filed_by)+(e.verified_by?'; verifier '+safe(e.verified_by)+'; '+safe(e.verification_ref):'; no independent verification filed')+'</p>';}).join('')+'</details></article>').join(''):'<p>No facts match these filters.</p>')+'</div>';
    html+='<details><summary>Original inputs and version-specific prior checks</summary>'+r.inputs.map(i=>'<p>'+safe(i.input_id)+' · '+safe(i.source_ref)+'<br>Revision '+safe(i.source_revision)+' · '+safe(i.digest)+'</p>').join('')+r.check_groups.map(g=>'<p>'+safe(g.checks[0].predicate)+' · '+safe(g.repeat_review)+' · '+safe(g.state)+'<br>'+safe(g.duplicate_count)+' duplicate record(s); '+g.checks.map(c=>safe(c.result_ref)).join(' · ')+'</p>').join('')+'<p class="muted">Same-version matches prevent duplicate suggestions only. They do not establish receipt authenticity or replay protection. Changed input, goal or rule revisions require a new review.</p></details>';
    html+='<div class="review-next"><h3>Continue next session</h3><p>'+safe(r.continuity.next_step)+'</p><p class="muted">Required owner: '+safe(r.continuity.required_owner)+'<br>'+safe(r.continuity.source_ref)+'</p></div><div class="review-toolbar">'+[['coordination_update','Coordination update'],['issue_comment','Issue comment'],['evidence_gaps','Evidence gaps'],['next_session','Next-session summary']].map(([k,l])=>'<button type="button" data-review-draft="'+k+'">'+l+'</button>').join('')+'</div>';
    if(output)html+='<label class="review-output-label">Unsubmitted draft<textarea id="ecosystemReviewDraft" readonly rows="12">'+safe(output)+'</textarea></label><button type="button" data-review-action="copy">Copy draft</button><span id="ecosystemReviewCopyStatus" role="status" aria-live="polite"></span>';
    box.innerHTML=html+boundary;
  }
  function invalidate(){epoch++;delivery=null;view=null;output='';outputKind='';selected='';evidence='ALL';work='ALL';loading=false;render();}
  async function refresh(){
    if(!active())return;
    const token=++epoch;delivery=null;output='';outputKind='';selected='';loading=true;
    view=C.refusal('ECOSYSTEM_REVIEW_LOADING');render();
    const bridge=window.StegVerseWorkspaceKVBridge;
    if(!bridge||typeof bridge.loadEcosystemCoordinationReview!=='function'){loading=false;view=C.refusal('ECOSYSTEM_REVIEW_OWNER_BRIDGE_NOT_BOUND');render();return;}
    try{
      const result=await bridge.loadEcosystemCoordinationReview({workspace_type:'DEVELOPER',kv_scope:'ECOSYSTEM'});
      if(token!==epoch||!active())return;
      delivery=result&&{projection:result.projection,context:result.context};
      view=delivery?C.evaluate(delivery.projection,delivery.context):C.refusal('ECOSYSTEM_REVIEW_DELIVERY_INVALID');
      if(view.state==='WITHHELD')delivery=null;
    }catch(error){
      if(token!==epoch||!active())return;
      // Do not render arbitrary exception text: it could contain provider payload or credentials.
      view=C.refusal('ECOSYSTEM_REVIEW_READ_FAILED');delivery=null;
    }
    if(token!==epoch||!active())return;
    loading=false;render();
  }
  box.addEventListener('change',event=>{
    const t=event.target,key=t&&t.getAttribute&&t.getAttribute('data-review-select');
    if(!active()||!key)return;
    if(key==='goal')selected=t.value;if(key==='evidence')evidence=t.value;if(key==='work')work=t.value;
    output='';outputKind='';render();
  });
  box.addEventListener('click',event=>{
    const t=event.target.closest&&event.target.closest('[data-review-action], [data-review-draft]');if(!t||!active())return;
    const action=t.getAttribute('data-review-action');
    if(action==='refresh'){refresh();return;}
    const kind=t.getAttribute('data-review-draft');
    if(kind){const all=C.drafts(current(),selected);if(all&&Object.prototype.hasOwnProperty.call(all,kind)){output=all[kind];outputKind=kind;render();}return;}
    if(action==='copy'){
      const draft=document.querySelector('#ecosystemReviewDraft');if(!draft||!current()||view.state==='WITHHELD')return;
      const latest=C.drafts(view,selected);if(!latest||!outputKind)return;output=latest[outputKind];draft.value=output;
      const copyEpoch=epoch;
      const note=text=>{if(copyEpoch!==epoch||!active())return;const n=document.querySelector('#ecosystemReviewCopyStatus');if(n)n.textContent=text;};
      if(typeof navigator!=='undefined'&&navigator.clipboard&&typeof navigator.clipboard.writeText==='function')navigator.clipboard.writeText(draft.value).then(()=>note('Copied.'),()=>{draft.focus();draft.select();note('Select the draft and copy it.');});
      else{draft.focus();draft.select();note('Select the draft and copy it.');}
    }
  });
  switcher.addEventListener('change',invalidate);
  document.addEventListener('stegverse:ecosystem-review-invalidated',invalidate);
  render();
})();
