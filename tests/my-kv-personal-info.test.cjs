const assert = require("assert");
const api = require("../assets/my-kv-personal-info.js");
const fs = require("fs");
const path = require("path");

(async function () {
  let profile = api.newProfile();
  profile = api.setIdentity(profile, { display_name: "Example Owner", legal_name: "Example Owner", date_of_birth: "2000-01-01" });
  profile = api.addPhone(profile, { number: "+1 555 555 0100", label: "mobile", primary: true });
  profile = api.addPostalAddress(profile, { label: "home", line1: "123 Example St", line2: "", city: "Example City", region: "EX", postal_code: "00000", country_code: "US", primary: true });
  assert.equal(profile.display_name, "Example Owner");
  assert.equal(profile.phone_numbers.length, 1);
  assert.equal(profile.postal_addresses.length, 1);
  assert.deepEqual(api.validateProfile(profile), []);
  profile = api.addEmail(profile, { address: "One@Example.com", label: "personal", primary: true });
  profile = api.addEmail(profile, { address: "two@example.com", label: "work", primary: false });

  assert.equal(profile.email_addresses.length, 2);
  assert.equal(profile.email_addresses[0].address, "one@example.com");
  assert.equal(profile.email_addresses.filter((entry) => entry.primary).length, 1);
  assert.deepEqual(api.validateProfile(profile), []);

  assert.throws(
    () => api.addEmail(profile, { address: "ONE@example.com", label: "duplicate" }),
    /already exists/
  );

  profile = api.setPrimary(profile, "two@example.com");
  assert.equal(profile.email_addresses.find((entry) => entry.address === "two@example.com").primary, true);
  assert.equal(profile.email_addresses.find((entry) => entry.address === "one@example.com").primary, false);

  const beforeFailure = JSON.stringify(profile);
  await assert.rejects(
    () => api.connectEmail(profile, "one@example.com", null),
    /FAIL_CLOSED: canonical KV email mapping bridge unavailable/
  );
  assert.equal(JSON.stringify(profile), beforeFailure);

  const mappingId = "kv-email:" + "a".repeat(64);
  const bridge = {
    mapEmail(request) {
      assert.equal(request.requested_capability, "email-continuity");
      assert.equal(request.credential_destination, "SKAP_VAULT");
      assert.equal(request.authority_effect, "NONE");
      assert.equal(Object.prototype.hasOwnProperty.call(request, "password"), false);
      return {
        email_address: request.address,
        mapping_id: mappingId,
        mapping_state: "MAPPED_CREDENTIAL_REQUIRED",
        provider_id: "synthetic-provider",
        authority_effect: "NONE"
      };
    }
  };

  profile = await api.connectEmail(profile, "one@example.com", bridge);
  const mapped = profile.email_addresses.find((entry) => entry.address === "one@example.com");
  assert.equal(mapped.mapping_id, mappingId);
  assert.equal(mapped.connection_state, "MAPPED_CREDENTIAL_REQUIRED");
  assert.equal(mapped.email_continuity_enabled, true);

  const guidance = api.connectionGuidance(mapped);
  assert.equal(guidance.action, "COMPLETE_SKAP_CREDENTIAL_SETUP");
  assert.match(guidance.message, /SKAP Vault/);

  assert.throws(
    () => api.assertNoForbiddenKeys({ refresh_token: "synthetic" }),
    /Secret-bearing field prohibited/
  );
  assert.throws(
    () => api.applyMapping(profile, "two@example.com", {
      email_address: "two@example.com",
      mapping_id: "kv-email:" + "b".repeat(64),
      mapping_state: "SESSION_VERIFIED"
    }),
    /Initial Site mapping may only enter MAPPED_CREDENTIAL_REQUIRED/
  );

  const draftResult = await api.persistProfile(profile, null);
  assert.equal(draftResult.persisted, false);
  assert.equal(draftResult.state, "DRAFT_ONLY");

  const persisted = await api.persistProfile(profile, {
    saveProfile(savedProfile) {
      assert.deepEqual(api.validateProfile(savedProfile), []);
      return { persisted: true };
    }
  });
  assert.equal(persisted.persisted, true);
  assert.equal(persisted.state, "KV_PERSISTED");

  const page = fs.readFileSync(path.join(__dirname, "..", "my-kv.html"), "utf8");
  assert.match(page, /SKIPPED — OPTIONAL/);
  assert.match(page, /result==="COMPLETED"\|\|result==="VERIFIED"/);
  assert.match(page, /card\.classList\.toggle\("skipped",result==="SKIPPED_OPTIONAL"\)/);
  assert.doesNotMatch(page, /var done=receipt&&\["COMPLETED","VERIFIED","SKIPPED_OPTIONAL"\]/);
  assert.match(page, /of 5 progressed/);
  assert.match(page, /_Entities\/Self\/Personal_Contact_Profile\.json/);

  const fileFallback = fs.readFileSync(path.join(__dirname, "..", "assets", "my-kv-personal-profile-file-fallback.js"), "utf8");
  assert.match(fileFallback, /input\.accept="\*\/\*"/);

  assert.match(page, /my-kv-personal-profile-file-fallback\.js\?v=20260902-ios-picker-r4/);

  const profileBridge = fs.readFileSync(path.join(__dirname, "..", "assets", "my-kv-personal-profile-write-bridge.js"), "utf8");
  for (const marker of ["response_transported_on_hb_derived_carrier","exact_response_packet_recovered","hb.recoverSignal","response_carrier_signal","response_payload_hash","response_receipt_hash","NONE_CARRIER_ONLY","hb_observation"]) {
    assert.ok(profileBridge.includes(marker), "missing Personal Profile HB runtime marker: " + marker);
  }

  const deviceSync = fs.readFileSync(path.join(__dirname, "..", "stegos-node", "device-kv-intr-sync.js"), "utf8");
  assert.ok(deviceSync.includes('body&&body.reason?": "+body.reason:""'), "DEVICE_KV denial reason must surface to runtime UI");

  console.log("MY_KV_PERSONAL_INFORMATION_TESTS_PASS");
}()).catch((error) => {
  console.error(error);
  process.exit(1);
});
