(function(root){
"use strict";
// MyKV consumer of the universal explanation contract (stegverse.user-facing-explanation/v1, .github#3106).
// It turns a MyKV refusal (an Error carrying the six actionable fields) into the contract's record and renders the
// prose with the complete JSON to copy. Explanatory only: it never grants, submits, retries or records anything, and
// a refusal without its six fields or a non-conforming artifact is withheld, leaving the canonical status to stand.
var SURFACE={repository:"StegVerse-Labs/Site",surface_id:"my-kv"};
var SIX=["failure_code","failed_predicate","required_evidence_or_repair","retry_entrypoint","owning_existing_goal","next_attempt"];
var PREDICATE_RE=/^FAIL_CLOSED: ([A-Z0-9_]+)/;
function safe(v){return String(v==null?"":v).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c];});}
function record(error,requestedAction){
 var a=error&&error.actionable_disposition;
 if(!a||typeof a!=="object"||!SIX.every(function(k){return typeof a[k]==="string"&&a[k].trim();}))return null;
 var m=PREDICATE_RE.exec(error&&error.message?String(error.message):"");
 var r={disposition:"FAIL_CLOSED",predicate:m?m[1]:a.failed_predicate,requested_action:requestedAction,authority_source:"INTERLOCK_INTR",consequence_observation:"NOT_AUTHENTICALLY_OBSERVED",evidence:[]};
 SIX.forEach(function(k){r[k]=a[k];});
 r.why="the result of this Personal KV request was not materialized on this device, so nothing was read or changed";
 return r;
}
function html(error,requestedAction){
 var E=root.StegVerseWorkspaceExplanation;
 if(!E||typeof E.build!=="function"||typeof E.prose!=="function"||typeof E.conforms!=="function")return "";
 var r=record(error,requestedAction);if(!r)return "";
 var a=E.build(r,SURFACE);if(!a||a.predicate==="EXPLANATION_NOT_BUILDABLE")return "";
 var c=E.conforms(a);if(!c||c.ok!==true)return "";
 var out='<div class="explanation-prose">',list=false;
 E.prose(a).split("\n").filter(function(l){return l.length;}).forEach(function(l){
  if(l.indexOf("  - ")===0){if(!list){out+="<ul>";list=true;}out+="<li>"+safe(l.slice(4))+"</li>";return;}
  if(list){out+="</ul>";list=false;}var i=l.indexOf(":");out+="<p><strong>"+safe(l.slice(0,i+1))+"</strong>"+safe(l.slice(i+1))+"</p>";
 });
 if(list)out+="</ul>";
 out+='</div><details class="explanation-json"><summary>Show the complete JSON explanation (copy it into any independent LLM)</summary><pre>'+safe(JSON.stringify(a,null,2))+"</pre></details>";
 out+='<p class="status">Non-authoritative projection (authority_effect NONE, explanation version '+safe(a.explanation_version)+"): the status above remains the only authority.</p>";
 return out;
}
function render(box,error,requestedAction){if(!box)return false;var h=html(error,requestedAction);box.innerHTML=h;box.hidden=!h;return !!h;}
root.StegVerseMyKVOutcomeExplanation=Object.freeze({surface:SURFACE,authority_effect:"NONE",record:record,html:html,render:render});
}(typeof window!=="undefined"?window:globalThis));
