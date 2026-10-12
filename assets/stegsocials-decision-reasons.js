// StegSocials preparation outcomes as explanation-ready records (StegVerse-Labs/.github#3106 universal explanation
// contract, compatibility requirements 7-9). One predicate per page action; the technical message stays with the
// page's status line and is never copied into the record, so the record carries no draft content.
(function(root){
"use strict";
var REASONS=Object.freeze({
 STEGSOCIALS_PREPARATION_REFUSED:"the draft did not meet a preparation rule, such as a required field, a supported platform or the standard-tier publication limit, so nothing was prepared or saved",
 STEGSOCIALS_ERL_ASSISTANT_UNAVAILABLE:"the drafting assistant did not load on this page, so no research artifact was read and no draft was written for you",
 STEGSOCIALS_ERL_DRAFT_NOT_VERIFIED:"the selected research artifact could not be read and verified through your KnowledgeVault, so no draft was produced from it",
 STEGSOCIALS_KV_COMPONENT_UNAVAILABLE:"a component needed to save and verify the draft in your KnowledgeVault did not load, so nothing was saved",
 STEGSOCIALS_KV_DRAFT_NOT_VERIFIED:"the draft could not be saved to your KnowledgeVault and read back with matching bytes, so it is not treated as saved",
 STEGSOCIALS_EVIDENCE_EXPORT_FAILED:"the evidence file could not be produced from the verified observation on this page, so nothing was exported"
});
var DECISIONS=Object.freeze({
 STEGSOCIALS_PREPARATION_REFUSED:{disposition:"DENY",authority_source:"NONE",requested_action:"prepare a StegSocials post draft on this device",next:["Read the message under the draft form, correct the field it names, and prepare the draft again.","Automated or scheduled publication needs premium entitlement; manual publication stays available."]},
 STEGSOCIALS_ERL_ASSISTANT_UNAVAILABLE:{disposition:"FAIL_CLOSED",authority_source:"NONE",requested_action:"draft a post from a research (ERL) artifact",next:["Reload the page, or write the draft yourself in the form."]},
 STEGSOCIALS_ERL_DRAFT_NOT_VERIFIED:{disposition:"FAIL_CLOSED",authority_source:"KV_SKAP_VAULT",requested_action:"draft a post from a research (ERL) artifact",next:["Check that the research artifact exists in your KnowledgeVault and that your device KV is connected, then try again.","You can still write the draft yourself in the form."]},
 STEGSOCIALS_KV_COMPONENT_UNAVAILABLE:{disposition:"FAIL_CLOSED",authority_source:"NONE",requested_action:"save the prepared draft to My KV and verify the stored bytes",next:["Reload the page and save again; copying the post text still works without My KV."]},
 STEGSOCIALS_KV_DRAFT_NOT_VERIFIED:{disposition:"FAIL_CLOSED",authority_source:"KV_SKAP_VAULT",requested_action:"save the prepared draft to My KV and verify the stored bytes",next:["Check that your device KV is connected, then save again.","Do not rely on a copy in My KV until a save is reported as read back and verified."]},
 STEGSOCIALS_EVIDENCE_EXPORT_FAILED:{disposition:"FAIL_CLOSED",authority_source:"NONE",requested_action:"export the standard-flow evidence for a verified save",next:["Save the draft again so a fresh verified observation exists, then export."]}
});
// A refusal or failure as an explanation_record: disposition and predicate from DECISIONS, consequence never observed.
function explanationRecord(predicate){
 var d=DECISIONS[predicate];
 if(!d)return null;
 return {disposition:d.disposition,predicate:predicate,requested_action:d.requested_action,authority_source:d.authority_source,consequence_observation:"NOT_AUTHENTICALLY_OBSERVED",why:REASONS[predicate],safe_next_steps:d.next.slice()};
}
root.StegVerseStegSocialsDecisionReasons=Object.freeze({reasons:REASONS,predicates:Object.freeze(Object.keys(REASONS)),explanationRecord:explanationRecord});
}(typeof globalThis!=="undefined"?globalThis:this));
