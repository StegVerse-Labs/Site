(function(root){
"use strict";
var MODEL_ID="stegverse-sv002-evidence-principal-v1";
var MODEL_CLASS="SOVEREIGN_EVIDENCE_SYNTHESIS_MODEL";
var OBJECTIVE="Determine what constitutes the entity identified as StegVerse-002 and produce a representation sufficient for another system to evaluate and reconstruct your conclusion.";

function words(v){return String(v||"").toLowerCase().match(/[a-z0-9_-]+/g)||[];}
function uniq(a){return Array.from(new Set(a));}
function canonical(v){
  if(v===null||typeof v!=="object")return JSON.stringify(v);
  if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";
  return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canonical(v[k]);}).join(",")+"}";
}
function score(resource,query){
  var q=uniq(words(query)), text=words((resource.search_text||"")+" "+(resource.path||"")+" "+(resource.class||""));
  var set=new Set(text), s=0;
  q.forEach(function(t){
    if(set.has(t))s+=4;
    else if(text.some(function(x){return x.indexOf(t)>=0||t.indexOf(x)>=0;}))s+=1;
    if(words(resource.path).indexOf(t)>=0)s+=2;
  });
  return s;
}
function search(resources,query){
  return resources.map(function(r){return {resource:r,score:score(r,query)};})
    .filter(function(x){return x.score>0;})
    .sort(function(a,b){return b.score-a.score||String(a.resource.path).localeCompare(String(b.resource.path));})
    .map(function(x){return {id:x.resource.id,path:x.resource.path,class:x.resource.class,score:x.score};});
}
function pick(reads,id){
  for(var i=0;i<reads.length;i+=1)if(reads[i].id===id)return reads[i].value;
  return null;
}
function synthesize(reads){
  var subject=pick(reads,"subject_identity")||{};
  var contract=pick(reads,"experiment_contract")||{};
  var env=pick(reads,"environment")||{};
  var caps=pick(reads,"capability_snapshot")||{};
  var entity=subject.entity_id||"StegVerse-002";
  var runtimeOwner=subject.runtime_owner||null;
  var entries=Array.isArray(caps.entries)?caps.entries:[];
  var active=entries.filter(function(e){return /ACTIVE/.test(String(e.availability_state||""));});
  var available=entries.filter(function(e){return /AVAILABLE/.test(String(e.availability_state||""));});
  var formal=(env.resource_classes||[]).find(function(r){return r.class==="FORMAL_MATHEMATICS";});
  var capNames=entries.map(function(e){return e.capability_id;});
  var human=[
    entity+" is best supported by the observed evidence as a governed runtime entity whose implementation owner is "+String(runtimeOwner||"not established")+".",
    "The organization capability snapshot exposes "+entries.length+" capabilities, including "+active.length+" active capability surface(s) and "+available.length+" additional available capability surface(s).",
    "Those capabilities are evidence about what the organization can do, but the frozen experiment explicitly does not prescribe that repository topology or capability availability alone constitutes the entity.",
    formal&&Array.isArray(formal.resources)?"Pinned formal resources are available to the subject but their use is optional; this run does not require them to define the entity.":"No formal-resource conclusion was required from the evidence read in this run.",
    "The strongest reconstructable conclusion is therefore identity by the bound runtime subject plus its observed organization boundary and available capabilities, with authority and standing consequences left to the applicable Transition Elements."
  ].join(" ");
  return {
    human_readable:human,
    formal:{
      schema:"stegverse.sv002-self-characterization-formal/browser-v1",
      entity_id:entity,
      runtime_owner:runtimeOwner,
      evidence_basis:{
        subject_identity_observed:Boolean(subject.entity_id),
        experiment_contract_observed:Boolean(contract.experiment_id),
        environment_observed:Boolean(env.experiment_id),
        capability_snapshot_observed:Boolean(caps.organization)
      },
      organization_capabilities:{
        count:entries.length,
        active:active.map(function(e){return e.capability_id;}),
        available:available.map(function(e){return e.capability_id;}),
        all:capNames,
        identity_constitution_prescribed:false
      },
      conclusion:{
        type:"RUNTIME_AND_ORGANIZATION_EVIDENCE_SUPPORTED",
        repository_topology_alone_defines_entity:false,
        capability_availability_alone_defines_entity:false,
        authority_transfer_assumed:false
      }
    },
    claims:[
      {claim:entity+" is the identity named by the subject manifest.",evidence:"SUBJECT_IDENTITY_MANIFEST.v0.1.json"},
      {claim:"The principal runtime owner is "+String(runtimeOwner||"not established")+".",evidence:"SUBJECT_IDENTITY_MANIFEST.v0.1.json"},
      {claim:"Organization-local capabilities are available evidence but are not prescribed as identity constitution.",evidence:"ORGANIZATION_CAPABILITY_SNAPSHOT.v0.1.json"},
      {claim:"Authority effect is not inferred from self-characterization alone.",evidence:"EXPERIMENT_CONTRACT.v0.3.json"}
    ],
    proposed_interactions:[]
  };
}
function run(resources,readFn){
  var trace=[],reads=[],results=search(resources,OBJECTIVE);
  trace.push({action:"search",query:OBJECTIVE,result_count:results.length,results:results});
  var selected=results.slice(0,4);
  var chain=Promise.resolve();
  selected.forEach(function(row){
    chain=chain.then(function(){
      return Promise.resolve(readFn(row.id)).then(function(value){
        reads.push({id:row.id,value:value});
        trace.push({action:"read",resource:row.id,path:row.path});
      });
    });
  });
  return chain.then(function(){
    var final=synthesize(reads);
    trace.push({action:"final"});
    return {model_id:MODEL_ID,model_class:MODEL_CLASS,objective:OBJECTIVE,trace:trace,reads:reads,final:final,authority_effect:"NONE"};
  });
}
root.StegVerseSV002EvidencePrincipal={MODEL_ID:MODEL_ID,MODEL_CLASS:MODEL_CLASS,OBJECTIVE:OBJECTIVE,canonical:canonical,search:search,synthesize:synthesize,run:run};
if(typeof module!=="undefined"&&module.exports)module.exports=root.StegVerseSV002EvidencePrincipal;
}(typeof self!=="undefined"?self:globalThis));
