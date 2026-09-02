(function(root){
"use strict";
if(!root||root.StegVerseKVPersonalInfoFileFallback)return;
function requireValue(ok,msg){if(!ok)throw new Error("FAIL_CLOSED: "+msg);}
function sha256Hex(bytes){return crypto.subtle.digest("SHA-256",bytes).then(d=>Array.from(new Uint8Array(d),x=>x.toString(16).padStart(2,"0")).join(""));}
function validateProfile(profile){
  var api=root.StegVerseMyKVPersonalInfo;
  requireValue(api&&typeof api.validateProfile==="function","Personal Information validator unavailable");
  var errors=api.validateProfile(profile);
  requireValue(Array.isArray(errors)&&errors.length===0,"Profile validation failed"+(errors&&errors.length?": "+errors.join("; "):""));
  api.assertNoForbiddenKeys(profile);
  return profile;
}
function chooseFile(){
  return new Promise(function(resolve,reject){
    var input=document.createElement("input");
    input.type="file";input.accept="*/*";input.style.display="none";
    input.addEventListener("change",function(){
      var file=input.files&&input.files[0];input.remove();
      if(!file){reject(new Error("No profile file selected"));return;}
      file.text().then(function(text){
        var profile;
        try{profile=JSON.parse(text);}catch(e){throw new Error("Selected profile is not valid JSON");}
        resolve({profile:validateProfile(profile),file_name:file.name,source:"OWNER_SELECTED_FILE"});
      }).catch(reject);
    },{once:true});
    document.body.appendChild(input);input.click();
  });
}
function newDraft(){
  var api=root.StegVerseMyKVPersonalInfo;
  requireValue(api&&typeof api.newProfile==="function","Personal Information model unavailable");
  return {profile:validateProfile(api.newProfile()),file_name:"Personal_Contact_Profile.json",source:"OWNER_CREATED_DRAFT"};
}
function saveProfile(profile){
  validateProfile(profile);
  var text=JSON.stringify(profile,null,2)+"\n",bytes=new TextEncoder().encode(text);
  return sha256Hex(bytes).then(function(hash){
    var file=new File([text],"Personal_Contact_Profile.json",{type:"application/json"});
    if(navigator.share&&navigator.canShare&&navigator.canShare({files:[file]})){
      return navigator.share({files:[file],title:"Personal_Contact_Profile.json",text:"Save this file into KnowledgeVault/_Entities/Self/, replacing the prior Personal_Contact_Profile.json if one exists."}).then(function(){
        return {state:"OWNER_FILE_EXPORT_REQUESTED",sha256:"sha256:"+hash,canonical_destination:"_Entities/Self/Personal_Contact_Profile.json",kv_sync_observed:false,authority_effect:"NONE"};
      });
    }
    var url=URL.createObjectURL(file),a=document.createElement("a");a.href=url;a.download=file.name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
    return {state:"OWNER_FILE_DOWNLOAD_STARTED",sha256:"sha256:"+hash,canonical_destination:"_Entities/Self/Personal_Contact_Profile.json",kv_sync_observed:false,authority_effect:"NONE"};
  });
}
root.StegVerseKVPersonalInfoFileFallback=Object.freeze({
  bridge_kind:"OWNER_MEDIATED_PERSONAL_PROFILE_FILE_FALLBACK",
  openExistingProfile:chooseFile,
  createNewProfileDraft:newDraft,
  saveProfile:saveProfile,
  authority_effect:"NONE"
});
}(typeof globalThis!=="undefined"?globalThis:this));
