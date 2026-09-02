const assert=require("assert");
const api=require("../assets/my-kv-personal-form-profile.js");

let p=api.newProfile();
assert.equal(p.schema,"stegverse.kv.personal_form_profile/v1");
assert.equal(p.signature.auto_apply,false);
assert.deepEqual(api.validateProfile(p),[]);

p=api.addIdentifier(p,{kind:"TVC_UNIQUE_ID",value:"example-tvc-id",label:"test"});
p=api.addIdentifier(p,{kind:"SSN",value:"000-00-0000",label:"test"});
p=api.setFilingDefaults(p,{organizer_name:"Example Owner",registered_agent_name:"Example Agent",effective_on_filing:true,accounting_year_close_month:12});
p=api.setSignatureRef(p,"skap://signing/personal-primary","Example Owner");
assert.deepEqual(api.validateProfile(p),[]);
assert.equal(p.signature.auto_apply,false);
assert.equal(p.signature.skap_ref,"skap://signing/personal-primary");
assert.throws(()=>api.setSignatureRef(p,"data:image/png;base64,abc","Example Owner"),/SKAP reference invalid/);
assert.throws(()=>api.setSignatureRef(p,"https://example.invalid/signature","Example Owner"),/SKAP reference invalid/);
console.log("MY_KV_PERSONAL_FORM_PROFILE_TESTS_PASS");
