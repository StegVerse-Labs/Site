// HIL submission outcomes as explanation-ready records (StegVerse-Labs/.github#3106 universal explanation contract).
// The upload and retry pages fail with internal codes such as intr_receipt_chain_invalid; this module maps every such
// code to one of a few predicates with a plain-language reason, so the page leads with prose and keeps the code as a
// technical detail. Records carry the predicate only, never the packet, its hashes or participant metadata.
(function(root){
"use strict";
var REASONS=Object.freeze({
 HIL_RECEIVER_UNREACHABLE:"the StegVerse receiver could not be reached or is not accepting submissions right now, so your packet has not been sent",
 HIL_PACKET_REJECTED:"the receiver checked your packet and refused it: the file is not a readable PDF or is larger than the receiver accepts (10 MB), its provenance file is missing or malformed, or its hashes do not match the published Primary and prompt",
 HIL_RECEIPT_NOT_VERIFIED:"an answer came back from the receiver, but its receipt did not pass this page's checks, so the page does not treat your packet as received",
 HIL_LOCAL_PACKET_UNAVAILABLE:"the copy of your packet kept in this browser could not be read back intact, so this page cannot use it",
 HIL_STORED_PACKET_NOT_VERIFIED:"this page could not retrieve the receiver's record and stored copy of your submission and match them to its receipt, so it does not show the submission as verified",
 HIL_PAGE_COMPONENT_UNAVAILABLE:"a part of this page needed to send your packet did not load, so nothing was sent",
 HIL_OUTCOME_UNEXPLAINED:"the page stopped on a condition it has no specific explanation for, so it does not know whether anything was sent"
});
var KEPT="Your packet and its provenance are unchanged; there is no deadline for submitting.";
var DECISIONS=Object.freeze({
 HIL_RECEIVER_UNREACHABLE:{disposition:"FAIL_CLOSED",authority_source:"NONE",next:["Check your connection and try again later; the same packet is reused, so retrying cannot create a second submission.",KEPT]},
 HIL_PACKET_REJECTED:{disposition:"DENY",authority_source:"NONE",next:["Submit the unaltered response PDF together with the provenance file produced with it.","Do not edit or re-save the PDF; any change alters its hash and the receiver refuses it again.","If the PDF is larger than 10 MB, contact the study owner rather than compressing or re-saving it."]},
 HIL_RECEIPT_NOT_VERIFIED:{disposition:"FAIL_CLOSED",authority_source:"NONE",next:["Retry; if the receiver already stored your packet it returns the same receipt instead of a new one.",KEPT]},
 HIL_LOCAL_PACKET_UNAVAILABLE:{disposition:"FAIL_CLOSED",authority_source:"NONE",next:["Submit again from your original PDF file and its provenance file."]},
 HIL_STORED_PACKET_NOT_VERIFIED:{disposition:"FAIL_CLOSED",authority_source:"NONE",action:"verify a submitted HIL response packet against the StegVerse receiver",next:["Reload this page later; this check reads the receiver's record and changes nothing.","Keep your original PDF and its provenance file; resubmitting the same packet returns the existing receipt rather than a second submission."]},
 HIL_PAGE_COMPONENT_UNAVAILABLE:{disposition:"FAIL_CLOSED",authority_source:"NONE",next:["Reload the page and submit again.",KEPT]},
 HIL_OUTCOME_UNEXPLAINED:{disposition:"UNKNOWN",authority_source:"NONE",next:["Treat the packet as not received until a receiver receipt is shown.","Retry; a packet the receiver already stored returns its existing receipt."]}
});
var ACTION="submit a HIL response packet to the StegVerse receiver";
// Ordered: the first matching rule wins. Codes come from the pages and the receiver Worker's refusal details.
var RULES=[
 [/^canonical_|_connector_unavailable$|_carrier_unavailable$/,"HIL_PAGE_COMPONENT_UNAVAILABLE"],
 [/^submission_status_unavailable$|^stored_packet_unavailable$|^retrieved_packet_hash_mismatch$|^submission_not_found$|^custody_verification_failed$/,"HIL_STORED_PACKET_NOT_VERIFIED"],
 [/^indexeddb_|^response_storage_|^response_pdf_not_found$|^response_pdf_hash_mismatch$|^stored_|^local_fallback_|^intr_prestage_/,"HIL_LOCAL_PACKET_UNAVAILABLE"],
 [/^response_pdf_|^invalid_pdf_signature$|^provenance_manifest_|^multipart_form_data_required$|^primary_prompt_response_chain_invalid$/,"HIL_PACKET_REJECTED"],
 [/^invalid_ingress_response|^ingress_http_|^durable_receiver_unavailable$|^registry_unavailable$|^receiver_internal_error$|^failed to fetch|^load failed|^networkerror|network/i,"HIL_RECEIVER_UNREACHABLE"],
 [/^ingress_|^intr_|^receipt_not_issued$|^accepted_receipt_invalid$/,"HIL_RECEIPT_NOT_VERIFIED"]
];
function classify(code){
 var c=String(code==null?"":code).trim();
 for(var i=0;i<RULES.length;i++)if(RULES[i][0].test(c))return RULES[i][1];
 return "HIL_OUTCOME_UNEXPLAINED";
}
function explanationRecord(predicate){
 var d=DECISIONS[predicate];
 if(!d)return null;
 return {disposition:d.disposition,predicate:predicate,requested_action:d.action||ACTION,authority_source:d.authority_source,consequence_observation:d.disposition==="UNKNOWN"?"UNKNOWN":"NOT_AUTHENTICALLY_OBSERVED",why:REASONS[predicate],safe_next_steps:d.next.slice()};
}
// Plain-language sentence for a failure code; the code itself is returned separately for the technical detail.
// ``predicate`` lets a surface whose every failure has one meaning (the result page) name it explicitly.
function describe(code,predicate){
 predicate=predicate&&REASONS[predicate]?predicate:classify(code);
 return {predicate:predicate,sentence:"Because "+REASONS[predicate]+".",record:explanationRecord(predicate)};
}
// Renders the optional explanation (prose plus a copy button for the complete JSON) into an empty container element.
// Returns the built artifact, or null when the explanation contract is not loaded on the page.
function renderExplanation(container,code,surfaceId,predicate){
 var explainer=root.StegVerseWorkspaceExplanation,doc=root.document;
 if(!container||!doc)return null;
 container.replaceChildren();
 if(!explainer||typeof explainer.build!=="function"){container.hidden=true;return null;}
 var artifact=explainer.build(describe(code,predicate).record,{repository:"StegVerse-Labs/Site",surface_id:surfaceId});
 if(!artifact||!artifact.prose){container.hidden=true;return null;}
 var details=doc.createElement("details"),summary=doc.createElement("summary"),pre=doc.createElement("pre"),button=doc.createElement("button");
 summary.textContent="What happened, in full";
 pre.className="receipt";pre.textContent=explainer.prose(artifact);
 button.type="button";button.className="sv-btn sv-btn-outline";button.textContent="Copy explanation JSON for your own AI assistant";
 button.addEventListener("click",function(){
  var text=JSON.stringify(artifact,null,2);
  var nav=root.navigator;
  // Without clipboard access the complete JSON is still reachable: it is shown, selectable, in its own block
  // (compatibility requirement 2: accessible copy or export of the complete artifact).
  var showJson=function(){
   if(jsonPre.parentNode)return;
   jsonPre.textContent=text;
   button.textContent="Clipboard unavailable: select the explanation JSON below and copy it";
   details.appendChild(jsonPre);
  };
  if(nav&&nav.clipboard&&typeof nav.clipboard.writeText==="function")nav.clipboard.writeText(text).then(function(){button.textContent="Explanation JSON copied";},showJson);
  else showJson();
 });
 var jsonPre=doc.createElement("pre");jsonPre.className="receipt";jsonPre.setAttribute("aria-label","Explanation JSON");
 details.append(summary,pre,button);
 container.appendChild(details);
 container.hidden=false;
 return artifact;
}
root.StegVerseHilDecisionReasons=Object.freeze({reasons:REASONS,predicates:Object.freeze(Object.keys(REASONS)),classify:classify,explanationRecord:explanationRecord,describe:describe,renderExplanation:renderExplanation});
}(typeof globalThis!=="undefined"?globalThis:this));
